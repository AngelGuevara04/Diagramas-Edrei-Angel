import { jsToPythonLiteral, normalizeConfig } from "./utils.js";

export function createRuntimeApi({
  dom,
  state,
  constants,
  setStatus,
  configFormApi,
  previewApi
}) {
  let lastAutoImageSyncSignature = "";
  let lastReviewCatalogSignature = "";
  let bingSearchRunning = false;
  let bingSearchStopRequested = false;
  let activeBingJobId = "";
  const providerLabels = {
    openverse: "Openverse + Wikimedia", puente: "Puente Local (DuckDuckGo)",
    bing: "Bing",
    ddg: "DuckDuckGo"
  };
  let sessionImageEntries = [];
  const reviewState = {
    active: false,
    entries: [],
    pendingItems: [],
    selectedPendingId: "",
    index: 0,
    currentImage: null,
    currentDisplayWidth: 0,
    currentDisplayHeight: 0,
    isDragging: false,
    selectionCanceled: false,
    dragStart: null,
    dragCurrent: null,
    previewTimeoutId: null,
    undoStack: [],
    suggestionProvider: "openverse",
    suggestionQueryLabel: "",
    suggestionItems: [],
    suggestionLoading: false,
    pendingResolvedIds: new Set(),
    keyboardBound: false,
    pasteBound: false
  };

  function getSelectedImageProvider() {
    const raw = String(dom.imageProvider?.value || "openverse").trim().toLowerCase();
    if (raw in providerLabels) return raw;
    return "openverse";
  }

  function getProviderLabel(provider) {
    return providerLabels[String(provider || "").trim().toLowerCase()] || "Proveedor";
  }

  function getRuntimeProjectPrefix() {
    const pathName = String(window.location?.pathname || "");
    if (pathName.includes("/Mapa%20mental/")) return "/Mapa%20mental";
    if (pathName.includes("/Mapa mental/")) return "/Mapa mental";
    return "";
  }

  function buildCandidateImageUrls(webPath) {
    const cleanPath = String(webPath || "").trim();
    if (!cleanPath) return [];
    const prefix = getRuntimeProjectPrefix();
    const urls = [];
    if (
      cleanPath.startsWith("/") &&
      !cleanPath.startsWith("/Mapa%20mental/") &&
      !cleanPath.startsWith("/Mapa mental/")
    ) {
      urls.push(`/Mapa%20mental${cleanPath}`);
      urls.push(`/Mapa mental${cleanPath}`);
    }
    if (
      prefix &&
      cleanPath.startsWith("/") &&
      !cleanPath.startsWith("/Mapa%20mental/") &&
      !cleanPath.startsWith("/Mapa mental/")
    ) {
      urls.push(`${prefix}${cleanPath}`);
    }
    urls.push(cleanPath);
    const deduped = [];
    const seen = new Set();
    for (const url of urls) {
      if (!seen.has(url)) {
        seen.add(url);
        deduped.push(url);
      }
    }
    return deduped;
  }

  function buildCandidateImageUrlsWithCacheBust(webPath) {
    const urls = buildCandidateImageUrls(webPath);
    const stamp = `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
    return urls.map((url) => {
      const sep = url.includes("?") ? "&" : "?";
      return `${url}${sep}cb=${stamp}`;
    });
  }

  function bindImageWithFallback(imgElement, webPath) {
    if (!imgElement) return;
    const candidates = buildCandidateImageUrlsWithCacheBust(webPath);
    if (!candidates.length) {
      imgElement.removeAttribute("src");
      return;
    }
    let idx = 0;
    const tryNext = () => {
      if (idx >= candidates.length) {
        imgElement.onerror = null;
        return;
      }
      imgElement.src = candidates[idx];
      idx += 1;
    };
    imgElement.onerror = tryNext;
    tryNext();
  }

  function normalizeSessionImageEntry(imageInfo, fallbackImageDir) {
    const fileName = String(imageInfo?.file_name || "").trim();
    const webPath = String(imageInfo?.web_path || "").trim();
    if (!fileName || !webPath) return null;
    const safeName = fileName.replaceAll("\\", "/").split("/").filter(Boolean).pop();
    if (!safeName) return null;
    return {
      key: `${String(fallbackImageDir || "").trim()}::${safeName}`,
      label: String(imageInfo?.label || safeName).trim() || safeName,
      file_name: safeName,
      web_path: webPath,
      image_dir: String(fallbackImageDir || "").trim()
    };
  }

  function setSessionImageEntries(images, imageDir) {
    const targetDir = String(imageDir || "").trim();
    const normalized = [];
    const seen = new Set();
    for (const imageInfo of Array.isArray(images) ? images : []) {
      const entry = normalizeSessionImageEntry(imageInfo, targetDir);
      if (!entry) continue;
      if (seen.has(entry.key)) continue;
      seen.add(entry.key);
      normalized.push(entry);
    }
    sessionImageEntries = normalized;
  }

  function normalizePendingId(label) {
    return String(label || "").trim().toLowerCase();
  }

  function buildPendingItemsFromPayload(payload) {
    const out = [];
    const seen = new Set();
    const imageDir = String(payload?.image_dir || state.currentConfig?.IMAGE_DIR || constants.DEFAULT_CONFIG.IMAGE_DIR || "");
    const pushLabel = (rawLabel, source = "missing") => {
      const label = String(rawLabel || "").trim();
      if (!label) return;
      const id = normalizePendingId(label);
      if (!id || seen.has(id)) return;
      seen.add(id);
      out.push({ id, label, source, image_dir: imageDir });
    };

    for (const row of Array.isArray(payload?.missing_labels) ? payload.missing_labels : []) {
      pushLabel(row?.label, "missing");
    }
    for (const row of Array.isArray(payload?.failures) ? payload.failures : []) {
      pushLabel(row?.label, "failed");
    }
    out.sort((a, b) => a.label.localeCompare(b.label, "es", { sensitivity: "base" }));
    return out;
  }

  function getSelectedPendingItem() {
    const selectedId = String(reviewState.selectedPendingId || "");
    if (!selectedId) return null;
    return reviewState.pendingItems.find((item) => item.id === selectedId) || null;
  }

  function renderPendingList() {
    const container = dom.imageReviewPendingList;
    if (!container) return;
    container.innerHTML = "";
    const items = Array.isArray(reviewState.pendingItems) ? reviewState.pendingItems : [];

    if (!items.length) {
      const empty = document.createElement("div");
      empty.className = "small";
      empty.textContent = "No hay pendientes.";
      container.appendChild(empty);
      if (dom.imageReviewPendingMeta) dom.imageReviewPendingMeta.textContent = "0 pendientes.";
      return;
    }

    if (!getSelectedPendingItem()) {
      reviewState.selectedPendingId = items[0].id;
    }

    for (const item of items) {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "image-pending-item";
      if (item.id === reviewState.selectedPendingId) {
        button.classList.add("is-selected");
      }
      if (reviewState.pendingResolvedIds.has(item.id)) {
        button.classList.add("is-resolved");
      }
      button.textContent = item.label;
      button.title = "Clic para abrir Google Imagenes con este titulo.";
      button.addEventListener("click", () => {
        reviewState.selectedPendingId = item.id;
        renderPendingList();
        openGoogleImagesForPendingItem(item);
      });
      container.appendChild(button);
    }

    if (dom.imageReviewPendingMeta) {
      const failedCount = items.filter((item) => item.source === "failed").length;
      dom.imageReviewPendingMeta.textContent =
        failedCount > 0
          ? `${items.length} pendientes (${failedCount} con intento fallido).`
          : `${items.length} pendientes.`;
    }
  }

  function setPendingItems(items) {
    reviewState.pendingItems = Array.isArray(items) ? items : [];
    reviewState.pendingResolvedIds = new Set();
    if (!getSelectedPendingItem()) {
      reviewState.selectedPendingId = reviewState.pendingItems[0]?.id || "";
    }
    renderPendingList();
  }

  function removePendingLabel(label) {
    const id = normalizePendingId(label);
    if (!id) return;
    const next = reviewState.pendingItems.filter((item) => item.id !== id);
    reviewState.pendingItems = next;
    if (reviewState.selectedPendingId === id) {
      reviewState.selectedPendingId = next[0]?.id || "";
    }
    renderPendingList();
  }

  function markPendingLabelResolved(label) {
    const id = normalizePendingId(label);
    if (!id) return;
    reviewState.pendingResolvedIds.add(id);
    renderPendingList();
  }

  function addPendingLabel(label, imageDir = null) {
    const text = String(label || "").trim();
    if (!text) return;
    const id = normalizePendingId(text);
    if (!id) return;
    if (reviewState.pendingItems.some((item) => item.id === id)) return;
    const dir = String(imageDir || state.currentConfig?.IMAGE_DIR || constants.DEFAULT_CONFIG.IMAGE_DIR || "");
    reviewState.pendingItems.push({ id, label: text, source: "missing", image_dir: dir });
    reviewState.pendingItems.sort((a, b) => a.label.localeCompare(b.label, "es", { sensitivity: "base" }));
    if (!reviewState.selectedPendingId) {
      reviewState.selectedPendingId = id;
    }
    renderPendingList();
  }

  function openGoogleImagesForPendingItem(item) {
    if (!item) return;
    const suffix = String(dom.imageReviewPendingSuffix?.value || "").trim();
    const query = `${item.label} ${suffix}`.trim();
    const url = `https://www.google.com/search?tbm=isch&q=${encodeURIComponent(query)}`;
    window.open(url, "_blank", "noopener,noreferrer");
  }

  function imageReviewSearchReplaceCurrent() {
    if (!isImageReviewOpen() || !reviewState.active || !reviewState.entries.length) {
      setStatus("No hay imagen actual para buscar reemplazo.", "error");
      return;
    }
    const entry = reviewState.entries[reviewState.index];
    if (!entry || entry.deleted) {
      setStatus("La imagen actual no esta disponible para buscar reemplazo.", "error");
      return;
    }
    const baseLabel = String(entry.label || entry.file_name || "").replace(/\.[a-z0-9]+$/i, "").trim();
    if (!baseLabel) {
      setStatus("No se encontro titulo para buscar reemplazo.", "error");
      return;
    }
    openGoogleImagesForPendingItem({ label: baseLabel });
  }

  function pickImageBlobFromClipboardEvent(event) {
    const items = Array.from(event?.clipboardData?.items || []);
    for (const item of items) {
      if (item.kind === "file" && String(item.type || "").startsWith("image/")) {
        return item.getAsFile();
      }
    }
    return null;
  }

  const reviewCtx = dom.imageReviewCanvas?.getContext("2d") || null;
  const pendingCtx = dom.imagePendingCanvas?.getContext("2d") || null;

  function isImageReviewOpen() {
    return Boolean(dom.imageReviewModal && !dom.imageReviewModal.classList.contains("hidden"));
  }

  function isImagePendingOpen() {
    return Boolean(dom.imagePendingModal && !dom.imagePendingModal.classList.contains("hidden"));
  }

  function clearImageReviewTimeout() {
    if (reviewState.previewTimeoutId) {
      clearTimeout(reviewState.previewTimeoutId);
      reviewState.previewTimeoutId = null;
    }
  }

  function renderImageReviewEmpty(message) {
    if (!dom.imageReviewCanvas || !reviewCtx) return;
    dom.imageReviewCanvas.width = 960;
    dom.imageReviewCanvas.height = 620;
    reviewCtx.fillStyle = "#0f172a";
    reviewCtx.fillRect(0, 0, dom.imageReviewCanvas.width, dom.imageReviewCanvas.height);
    reviewCtx.fillStyle = "#dbeafe";
    reviewCtx.font = "22px 'Trebuchet MS', sans-serif";
    reviewCtx.textAlign = "center";
    reviewCtx.textBaseline = "middle";
    reviewCtx.fillText(String(message || "Sin imagenes"), dom.imageReviewCanvas.width / 2, dom.imageReviewCanvas.height / 2);
    if (dom.imageReviewFilename) dom.imageReviewFilename.textContent = "";
    if (dom.imageReviewCounter) dom.imageReviewCounter.textContent = "Sin imagenes en sesion.";
    reviewState.currentImage = null;
  }

  function renderImagePendingEmpty(message) {
    if (!dom.imagePendingCanvas || !pendingCtx) return;
    dom.imagePendingCanvas.width = 960;
    dom.imagePendingCanvas.height = 620;
    pendingCtx.fillStyle = "#0f172a";
    pendingCtx.fillRect(0, 0, dom.imagePendingCanvas.width, dom.imagePendingCanvas.height);
    pendingCtx.fillStyle = "#dbeafe";
    pendingCtx.font = "22px 'Trebuchet MS', sans-serif";
    pendingCtx.textAlign = "center";
    pendingCtx.textBaseline = "middle";
    pendingCtx.fillText(String(message || "Sin imagen pendiente"), dom.imagePendingCanvas.width / 2, dom.imagePendingCanvas.height / 2);
  }

  async function renderImagePendingPreviewFromBlob(blob) {
    if (!blob || !pendingCtx || !dom.imagePendingCanvas) return;
    const img = await loadImageFromBlob(blob);
    const maxW = 960;
    const maxH = 620;
    const naturalW = Math.max(1, Number(img?.naturalWidth) || 1);
    const naturalH = Math.max(1, Number(img?.naturalHeight) || 1);
    const scale = Math.min(maxW / naturalW, maxH / naturalH, 1);
    const displayW = Math.max(1, Math.round(naturalW * scale));
    const displayH = Math.max(1, Math.round(naturalH * scale));

    dom.imagePendingCanvas.width = maxW;
    dom.imagePendingCanvas.height = maxH;
    pendingCtx.fillStyle = "#0f172a";
    pendingCtx.fillRect(0, 0, maxW, maxH);
    const x = Math.round((maxW - displayW) / 2);
    const y = Math.round((maxH - displayH) / 2);
    pendingCtx.drawImage(img, x, y, displayW, displayH);
  }

  function loadImageFromBlob(blob) {
    return new Promise((resolve, reject) => {
      const url = URL.createObjectURL(blob);
      const img = new Image();
      img.onload = () => {
        URL.revokeObjectURL(url);
        resolve(img);
      };
      img.onerror = (error) => {
        URL.revokeObjectURL(url);
        reject(error);
      };
      img.src = url;
    });
  }

  function drawImageReview(img, selectionRect = null) {
    if (!dom.imageReviewCanvas || !reviewCtx) return;
    const maxW = 1120;
    const maxH = 760;
    const naturalW = Math.max(1, Number(img?.naturalWidth) || 1);
    const naturalH = Math.max(1, Number(img?.naturalHeight) || 1);
    const scale = Math.min(maxW / naturalW, maxH / naturalH, 1);
    const displayW = Math.max(1, Math.round(naturalW * scale));
    const displayH = Math.max(1, Math.round(naturalH * scale));

    dom.imageReviewCanvas.width = displayW;
    dom.imageReviewCanvas.height = displayH;
    reviewCtx.clearRect(0, 0, displayW, displayH);
    reviewCtx.drawImage(img, 0, 0, displayW, displayH);
    reviewState.currentDisplayWidth = displayW;
    reviewState.currentDisplayHeight = displayH;

    if (selectionRect) {
      reviewCtx.save();
      reviewCtx.strokeStyle = "#ffeb3b";
      reviewCtx.lineWidth = 2;
      reviewCtx.setLineDash([6, 4]);
      reviewCtx.strokeRect(selectionRect.x, selectionRect.y, selectionRect.w, selectionRect.h);
      reviewCtx.restore();
    }
  }

  function findReviewNextIndex(direction = 1) {
    const total = reviewState.entries.length;
    if (!total) return null;
    let idx = reviewState.index;
    for (let i = 0; i < total; i += 1) {
      idx = (idx + direction + total) % total;
      if (!reviewState.entries[idx]?.deleted) return idx;
    }
    return null;
  }

  async function fetchImageBlobFromEntry(entry) {
    const urls = buildCandidateImageUrls(entry?.web_path || "");
    for (const url of urls) {
      let response = null;
      try {
        response = await fetch(url, { cache: "no-store" });
      } catch (_) {
        response = null;
      }
      if (!response || !response.ok) continue;
      return await response.blob();
    }
    throw new Error("No se pudo abrir la imagen actual desde el servidor.");
  }

  async function fetchImageBlobFromWebPath(webPath) {
    const urls = buildCandidateImageUrls(webPath || "");
    for (const url of urls) {
      let response = null;
      try {
        response = await fetch(url, { cache: "no-store" });
      } catch (_) {
        response = null;
      }
      if (!response || !response.ok) continue;
      return await response.blob();
    }
    throw new Error("No se pudo abrir la imagen candidata desde el servidor.");
  }

  function blobToDataUrl(blob) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(String(reader.result || ""));
      reader.onerror = () => reject(new Error("No se pudo convertir la imagen a base64."));
      reader.readAsDataURL(blob);
    });
  }

  function fileStemFromLabel(label) {
    let text = String(label || "").trim();
    if (!text) text = "nodo";
    text = text.replace(/[\\/:*?"<>|]+/g, "-");
    text = text.replace(/\s+/g, " ").trim().replace(/[. ]+$/g, "");
    return text || "nodo";
  }

  function extFromBlobType(typeText) {
    const type = String(typeText || "").toLowerCase();
    if (type.includes("image/png")) return ".png";
    if (type.includes("image/jpeg") || type.includes("image/jpg")) return ".jpg";
    if (type.includes("image/webp")) return ".webp";
    return "";
  }

  async function savePendingImageBlob(blob, pendingItem) {
    if (!blob) throw new Error("No se detecto imagen en portapapeles.");
    if (!pendingItem) throw new Error("Selecciona una imagen pendiente primero.");

    const ext = extFromBlobType(blob.type) || ".png";
    if (![".png", ".jpg", ".webp"].includes(ext)) {
      throw new Error("Formato de imagen no soportado. Usa PNG, JPG o WEBP.");
    }
    const imageDir = String(pendingItem.image_dir || state.currentConfig?.IMAGE_DIR || constants.DEFAULT_CONFIG.IMAGE_DIR || "");
    const fileName = `${fileStemFromLabel(pendingItem.label)}${ext}`;
    const entry = {
      key: `${imageDir}::${fileName}`,
      label: pendingItem.label,
      file_name: fileName,
      web_path: "",
      image_dir: imageDir
    };

    await writeImageFileToServer(entry, blob);
    await syncReviewEntryIntoPyodide(entry);

    const existingIdx = sessionImageEntries.findIndex((item) => item.key === entry.key);
    if (existingIdx >= 0) {
      sessionImageEntries[existingIdx] = { ...sessionImageEntries[existingIdx], ...entry };
    } else {
      sessionImageEntries.push(entry);
    }

    const reviewIdx = reviewState.entries.findIndex((item) => item.key === entry.key);
    if (reviewIdx >= 0) {
      reviewState.entries[reviewIdx] = { ...reviewState.entries[reviewIdx], ...entry, deleted: false };
      reviewState.index = reviewIdx;
    } else {
      reviewState.entries.push({ ...entry, deleted: false });
      reviewState.index = reviewState.entries.length - 1;
    }

    markPendingLabelResolved(pendingItem.label);
    await renderImagePendingPreviewFromBlob(blob);
    await refreshPreviewAfterReviewChange();
    await showCurrentImageReview();
    setStatus(`Imagen pegada y guardada para: ${pendingItem.label}`, "ok");
  }

  async function readImageBlobFromClipboard() {
    if (navigator.clipboard?.read) {
      const clipboardItems = await navigator.clipboard.read();
      for (const clipItem of clipboardItems) {
        const imageType = clipItem.types.find((type) => String(type).startsWith("image/"));
        if (!imageType) continue;
        return await clipItem.getType(imageType);
      }
      return null;
    }
    return null;
  }

  async function saveCurrentReviewImageBlob(blob) {
    if (!blob) throw new Error("No se detecto imagen en portapapeles.");
    if (!isImageReviewOpen() || !reviewState.active) return;
    if (!reviewState.entries.length) {
      throw new Error("No hay imagen actual para reemplazar.");
    }
    const entry = reviewState.entries[reviewState.index];
    if (!entry || entry.deleted) {
      throw new Error("La imagen actual no esta disponible para reemplazo.");
    }

    const backupBlob = await fetchImageBlobFromEntry(entry);
    reviewState.undoStack.push({
      type: "crop",
      index: reviewState.index,
      entryKey: entry.key,
      previousBlob: backupBlob
    });

    await writeImageFileToServer(entry, blob);
    await syncReviewEntryIntoPyodide(entry);
    await refreshPreviewAfterReviewChange();
    await showCurrentImageReview();
    setStatus(`Imagen reemplazada: ${entry.file_name}`, "ok");
  }

  function getActiveReviewEntry() {
    if (!reviewState.entries.length) return null;
    const idx = Math.min(Math.max(0, Number(reviewState.index) || 0), reviewState.entries.length - 1);
    const entry = reviewState.entries[idx];
    if (!entry || entry.deleted) return null;
    return entry;
  }

  function renderSuggestionGrid() {
    const container = dom.imageSuggestionGrid;
    if (!container) return;
    container.innerHTML = "";
    const list = Array.isArray(reviewState.suggestionItems) ? reviewState.suggestionItems : [];
    if (!list.length) {
      const empty = document.createElement("div");
      empty.className = "small";
      empty.textContent = reviewState.suggestionLoading ? "Buscando opciones..." : "Sin resultados para esta imagen.";
      container.appendChild(empty);
      return;
    }

    for (const item of list) {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "image-suggestion-item";
      const img = document.createElement("img");
      bindImageWithFallback(img, String(item.web_path || ""));
      img.alt = String(item.file_name || "sugerencia");
      img.loading = "lazy";
      const cap = document.createElement("span");
      cap.textContent = String(item.file_name || "imagen");
      button.appendChild(img);
      button.appendChild(cap);
      button.addEventListener("click", async () => {
        const current = getActiveReviewEntry();
        if (!current) {
          setStatus("No hay imagen activa para reemplazar.", "error");
          return;
        }
        try {
          const blob = await fetchImageBlobFromWebPath(String(item.web_path || ""));
          await saveCurrentReviewImageBlob(blob);
          setStatus(`Reemplazo aplicado con ${getProviderLabel(reviewState.suggestionProvider)}.`, "ok");
        } catch (error) {
          setStatus(`No se pudo aplicar sugerencia: ${error.message}`, "error");
        }
      });
      container.appendChild(button);
    }
  }

  async function loadSuggestionCandidates(provider, options = {}) {
    if (!isImageReviewOpen() || !reviewState.active) return;
    const entry = getActiveReviewEntry();
    if (!entry) {
      reviewState.suggestionItems = [];
      renderSuggestionGrid();
      return;
    }

    const useProvider = String(provider || reviewState.suggestionProvider || "openverse").trim().toLowerCase();
    reviewState.suggestionProvider = useProvider;
    reviewState.suggestionLoading = true;
    reviewState.suggestionItems = [];
    renderSuggestionGrid();
    if (dom.imageSuggestionMeta) {
      dom.imageSuggestionMeta.textContent = `Buscando en ${getProviderLabel(useProvider)}...`;
    }

    const suffix = String(dom.imageReviewPendingSuffix?.value || dom.bingSuffix?.value || "").trim();
    const forceRefresh = Boolean(options?.forceRefresh);
    try {
      const response = await fetch("/api/images/review/candidates", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          label: entry.label || entry.file_name,
          provider: useProvider,
          image_dir: entry.image_dir || state.currentConfig?.IMAGE_DIR || constants.DEFAULT_CONFIG.IMAGE_DIR,
          suffix,
          max_results: 8,
          force_refresh: forceRefresh
        })
      });
      let payload = {};
      try {
        payload = await response.json();
      } catch (_) {
        payload = {};
      }
      if (!response.ok || payload.ok === false) {
        throw new Error(payload.error || `Error HTTP ${response.status}`);
      }
      reviewState.suggestionQueryLabel = String(payload.label || "");
      reviewState.suggestionItems = Array.isArray(payload.files) ? payload.files : [];
      if (dom.imageSuggestionMeta) {
        dom.imageSuggestionMeta.textContent = `${getProviderLabel(useProvider)}: ${reviewState.suggestionItems.length} opciÃ³n(es) para "${reviewState.suggestionQueryLabel}".`;
      }
    } catch (error) {
      reviewState.suggestionItems = [];
      if (dom.imageSuggestionMeta) {
        dom.imageSuggestionMeta.textContent = `No se pudieron cargar sugerencias: ${error.message}`;
      }
      setStatus(`Sugerencias no disponibles: ${error.message}`, "error");
    } finally {
      reviewState.suggestionLoading = false;
      renderSuggestionGrid();
    }
  }

  async function imageReviewPasteFromClipboard() {
    if (!isImagePendingOpen() || !reviewState.active) return;
    const pendingItem = getSelectedPendingItem();
    if (!pendingItem) {
      setStatus("Selecciona un pendiente para pegar la imagen.", "error");
      return;
    }
    try {
      const blob = await readImageBlobFromClipboard();
      if (!blob) {
        setStatus("El portapapeles no contiene una imagen.", "error");
        return;
      }
      await savePendingImageBlob(blob, pendingItem);
    } catch (_) {
      setStatus("Usa Ctrl+V dentro de Imagenes pendientes para pegar imagen.", "error");
    }
  }

  async function imageReviewReplaceCurrentFromClipboard() {
    if (!isImageReviewOpen() || !reviewState.active) return;
    try {
      const blob = await readImageBlobFromClipboard();
      if (!blob) {
        setStatus("El portapapeles no contiene una imagen.", "error");
        return;
      }
      await saveCurrentReviewImageBlob(blob);
    } catch (_) {
      setStatus("No se pudo leer imagen del portapapeles. Usa el boton de reemplazar tras copiar imagen.", "error");
    }
  }

  async function writeImageFileToServer(entry, blob) {
    const dataUrl = await blobToDataUrl(blob);
    const response = await fetch("/api/images/review/write", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        image_dir: entry.image_dir,
        file_name: entry.file_name,
        image_base64: dataUrl
      })
    });
    let payload = {};
    try {
      payload = await response.json();
    } catch (_) {
      payload = {};
    }
    if (!response.ok || payload.ok === false) {
      throw new Error(payload.error || `Error HTTP ${response.status}`);
    }
    if (payload.web_path) {
      entry.web_path = String(payload.web_path);
    }
  }

  async function deleteImageFileFromServer(entry) {
    const response = await fetch("/api/images/review/delete", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        image_dir: entry.image_dir,
        file_name: entry.file_name
      })
    });
    let payload = {};
    try {
      payload = await response.json();
    } catch (_) {
      payload = {};
    }
    if (!response.ok || payload.ok === false) {
      throw new Error(payload.error || `Error HTTP ${response.status}`);
    }
  }

  function removeEntryFromPyodideFs(entry) {
    if (!state.pyReady || !state.pyodide?.FS) return;
    try {
      const targetDir = normalizeRelativePath(entry.image_dir || constants.DEFAULT_CONFIG.IMAGE_DIR);
      state.pyodide.FS.unlink(`${targetDir}/${entry.file_name}`);
    } catch (_) {
      // Si no existe en FS runtime, se ignora.
    }
  }

  async function syncReviewEntryIntoPyodide(entry) {
    if (!state.pyReady) return;
    await syncImagesToPyodideFs([entry], entry.image_dir);
  }

  async function refreshSessionImagesForReview(options = {}) {
    const force = Boolean(options?.force);
    const onStep = typeof options?.onStep === "function" ? options.onStep : null;
    if (onStep) onStep({ current: 1, total: 4, text: "Preparando configuracion..." });
    await applyConfigFromEditor(false);
    const signature = getCurrentImageSyncSignature();
    if (!force && sessionImageEntries.length > 0 && lastReviewCatalogSignature === signature) {
      if (onStep) onStep({ current: 4, total: 4, text: "Lista de imagenes en cache de sesion." });
      return;
    }

    if (onStep) onStep({ current: 2, total: 4, text: "Leyendo etiquetas del mapa..." });
    const payload = await requestSessionImageCatalog({
      downloadMissing: false,
      forceRefresh: false,
      maxLabels: null,
      silent: false,
      skipApplyConfig: true
    });
    if (onStep) onStep({ current: 3, total: 4, text: "Consolidando imagenes de sesion..." });
    setSessionImageEntries(payload?.images || [], payload?.image_dir || state.currentConfig?.IMAGE_DIR);
    setPendingItems(buildPendingItemsFromPayload(payload));
    lastReviewCatalogSignature = signature;
    if (onStep) onStep({ current: 4, total: 4, text: "Revisor listo." });
  }

  function updateImageReviewCounter() {
    if (!dom.imageReviewCounter) return;
    const total = reviewState.entries.length;
    if (!total) {
      dom.imageReviewCounter.textContent = "Sin imagenes en sesion.";
      return;
    }
    dom.imageReviewCounter.textContent = `Imagen ${reviewState.index + 1} de ${total}`;
  }

  async function showCurrentImageReview() {
    if (!isImageReviewOpen()) return;
    if (!reviewState.entries.length) {
      renderImageReviewEmpty("No hay imagenes de la sesion para revisar.");
      return;
    }

    if (reviewState.index < 0) reviewState.index = 0;
    if (reviewState.index >= reviewState.entries.length) reviewState.index = reviewState.entries.length - 1;
    if (reviewState.entries[reviewState.index]?.deleted) {
      const next = findReviewNextIndex(1);
      if (next === null) {
        renderImageReviewEmpty("Todas las imagenes en sesion estan marcadas como borradas.");
        return;
      }
      reviewState.index = next;
    }

    const entry = reviewState.entries[reviewState.index];
    try {
      const blob = await fetchImageBlobFromEntry(entry);
      const img = await loadImageFromBlob(blob);
      reviewState.currentImage = img;
      drawImageReview(img);
      if (dom.imageReviewFilename) dom.imageReviewFilename.textContent = entry.file_name;
      updateImageReviewCounter();
      await loadSuggestionCandidates(reviewState.suggestionProvider);
    } catch (error) {
      renderImageReviewEmpty(`No se pudo cargar ${entry.file_name}.`);
      if (dom.imageReviewHint) {
        dom.imageReviewHint.textContent = `Error: ${error.message}`;
      }
    }
  }

  async function imageReviewNext() {
    const next = findReviewNextIndex(1);
    if (next === null) {
      renderImageReviewEmpty("No quedan imagenes activas en esta sesion.");
      return;
    }
    reviewState.index = next;
    await showCurrentImageReview();
  }

  async function imageReviewPrev() {
    const prev = findReviewNextIndex(-1);
    if (prev === null) {
      renderImageReviewEmpty("No quedan imagenes activas en esta sesion.");
      return;
    }
    reviewState.index = prev;
    await showCurrentImageReview();
  }

  async function refreshPreviewAfterReviewChange() {
    try {
      await generatePreview({ silent: true, preserveViewport: true, skipImageSync: true });
    } catch (_) {
      // no-op; el estado principal ya mostrara errores si aplica.
    }
  }

  async function imageReviewDeleteCurrent() {
    if (!isImageReviewOpen() || !reviewState.entries.length) return;
    const entry = reviewState.entries[reviewState.index];
    if (!entry || entry.deleted) {
      await imageReviewNext();
      return;
    }

    try {
      const backupBlob = await fetchImageBlobFromEntry(entry);
      reviewState.undoStack.push({
        type: "delete",
        index: reviewState.index,
        entryKey: entry.key,
        previousBlob: backupBlob
      });

      await deleteImageFileFromServer(entry);
      removeEntryFromPyodideFs(entry);
      entry.deleted = true;
      addPendingLabel(entry.label, entry.image_dir);
      await refreshPreviewAfterReviewChange();
      await imageReviewNext();
      setStatus(`Imagen borrada: ${entry.file_name}`, "ok");
    } catch (error) {
      setStatus(`No se pudo borrar imagen: ${error.message}`, "error");
    }
  }

  async function scheduleReviewNext() {
    clearImageReviewTimeout();
    reviewState.previewTimeoutId = setTimeout(() => {
      imageReviewNext().catch(() => {});
    }, 500);
  }

  async function imageReviewCropBottom() {
    if (!isImageReviewOpen() || !reviewState.entries.length) return;
    const entry = reviewState.entries[reviewState.index];
    if (!entry || entry.deleted) return;

    try {
      const fileBlob = await fetchImageBlobFromEntry(entry);
      const backupBlob = fileBlob.slice(0, fileBlob.size, fileBlob.type || "image/png");
      const img = await loadImageFromBlob(fileBlob);
      const naturalW = Math.max(1, Number(img.naturalWidth) || 1);
      const naturalH = Math.max(1, Number(img.naturalHeight) || 1);
      const newH = Math.max(1, Math.round(naturalH * 0.9));

      const tmpCanvas = document.createElement("canvas");
      tmpCanvas.width = naturalW;
      tmpCanvas.height = newH;
      const tctx = tmpCanvas.getContext("2d");
      if (!tctx) throw new Error("No se pudo crear contexto para recorte.");
      tctx.drawImage(img, 0, 0);

      const croppedBlob = await new Promise((resolve) => tmpCanvas.toBlob(resolve, fileBlob.type || "image/png"));
      if (!croppedBlob) throw new Error("No se pudo generar imagen recortada.");

      reviewState.undoStack.push({
        type: "crop",
        index: reviewState.index,
        entryKey: entry.key,
        previousBlob: backupBlob
      });

      await writeImageFileToServer(entry, croppedBlob);
      await syncReviewEntryIntoPyodide(entry);
      await refreshPreviewAfterReviewChange();

      const previewImg = await loadImageFromBlob(croppedBlob);
      reviewState.currentImage = previewImg;
      drawImageReview(previewImg);
      setStatus(`Recorte aplicado: ${entry.file_name}`, "ok");
      await scheduleReviewNext();
    } catch (error) {
      setStatus(`No se pudo recortar imagen: ${error.message}`, "error");
    }
  }

  async function applyManualReviewCrop(selection) {
    const entry = reviewState.entries[reviewState.index];
    if (!entry || entry.deleted || !reviewState.currentImage || !dom.imageReviewCanvas) return;

    const fileBlob = await fetchImageBlobFromEntry(entry);
    const backupBlob = fileBlob.slice(0, fileBlob.size, fileBlob.type || "image/png");
    const img = reviewState.currentImage;
    const naturalW = Math.max(1, Number(img.naturalWidth) || 1);
    const naturalH = Math.max(1, Number(img.naturalHeight) || 1);
    const displayW = reviewState.currentDisplayWidth || dom.imageReviewCanvas.width;
    const displayH = reviewState.currentDisplayHeight || dom.imageReviewCanvas.height;

    if (!displayW || !displayH) throw new Error("No se pudo calcular escala de recorte.");

    const scaleX = naturalW / displayW;
    const scaleY = naturalH / displayH;
    const sx = Math.max(0, selection.x * scaleX);
    const sy = Math.max(0, selection.y * scaleY);
    const sw = Math.max(1, selection.w * scaleX);
    const sh = Math.max(1, selection.h * scaleY);

    const cropW = Math.max(1, Math.round(sw));
    const cropH = Math.max(1, Math.round(sh));
    const tmpCanvas = document.createElement("canvas");
    tmpCanvas.width = cropW;
    tmpCanvas.height = cropH;
    const tctx = tmpCanvas.getContext("2d");
    if (!tctx) throw new Error("No se pudo crear contexto para recorte.");
    tctx.drawImage(img, sx, sy, sw, sh, 0, 0, cropW, cropH);

    const croppedBlob = await new Promise((resolve) => tmpCanvas.toBlob(resolve, fileBlob.type || "image/png"));
    if (!croppedBlob) throw new Error("No se pudo generar imagen recortada.");

    reviewState.undoStack.push({
      type: "crop",
      index: reviewState.index,
      entryKey: entry.key,
      previousBlob: backupBlob
    });

    await writeImageFileToServer(entry, croppedBlob);
    await syncReviewEntryIntoPyodide(entry);
    await refreshPreviewAfterReviewChange();
    const previewImg = await loadImageFromBlob(croppedBlob);
    reviewState.currentImage = previewImg;
    drawImageReview(previewImg);
    setStatus(`Recorte libre aplicado: ${entry.file_name}`, "ok");
    await scheduleReviewNext();
  }

  async function undoImageReviewAction() {
    if (!isImageReviewOpen() || !reviewState.undoStack.length) return;
    const op = reviewState.undoStack.pop();
    const entry = reviewState.entries.find((item) => item.key === op?.entryKey);
    if (!entry) return;

    try {
      await writeImageFileToServer(entry, op.previousBlob);
      entry.deleted = false;
      removePendingLabel(entry.label);
      await syncReviewEntryIntoPyodide(entry);
      reviewState.index = Math.max(0, Number(op.index) || 0);
      await refreshPreviewAfterReviewChange();
      await showCurrentImageReview();
      setStatus(`Deshacer aplicado sobre ${entry.file_name}.`, "ok");
    } catch (error) {
      setStatus(`No se pudo deshacer: ${error.message}`, "error");
    }
  }

  function cancelImageReviewSelection() {
    reviewState.selectionCanceled = true;
    reviewState.isDragging = false;
    reviewState.dragStart = null;
    reviewState.dragCurrent = null;
    if (reviewState.currentImage) {
      drawImageReview(reviewState.currentImage);
    }
  }

  async function handleImageReviewKeyboard(event) {
    if (!reviewState.active || !isImageReviewOpen()) return;
    const targetTag = String(event.target?.tagName || "").toLowerCase();
    if (targetTag === "input" || targetTag === "textarea" || targetTag === "select") return;

    const pendingOpen = isImagePendingOpen();
    const key = String(event.key || "").toLowerCase();
    if (key === "v" && event.ctrlKey && !event.shiftKey && !pendingOpen) {
      event.preventDefault();
      await imageReviewReplaceCurrentFromClipboard();
      return;
    }
    if (key === "s") {
      event.preventDefault();
      await imageReviewNext();
    } else if (key === "d") {
      event.preventDefault();
      await imageReviewDeleteCurrent();
    } else if (key === "x") {
      event.preventDefault();
      await imageReviewCropBottom();
    } else if (key === "m") {
      event.preventDefault();
      if (reviewState.isDragging) cancelImageReviewSelection();
    } else if (event.key === "ArrowLeft") {
      event.preventDefault();
      await imageReviewPrev();
    } else if (key === "z") {
      event.preventDefault();
      await undoImageReviewAction();
    }
  }

  function bindImageReviewCanvasEvents() {
    if (!dom.imageReviewCanvas || !reviewCtx || reviewState.keyboardBound) return;
    reviewState.keyboardBound = true;

    dom.imageReviewCanvas.addEventListener("mousedown", (event) => {
      if (!reviewState.active || !reviewState.currentImage) return;
      const rect = dom.imageReviewCanvas.getBoundingClientRect();
      reviewState.dragStart = {
        x: event.clientX - rect.left,
        y: event.clientY - rect.top
      };
      reviewState.dragCurrent = { ...reviewState.dragStart };
      reviewState.isDragging = true;
      reviewState.selectionCanceled = false;
    });

    dom.imageReviewCanvas.addEventListener("mousemove", (event) => {
      if (!reviewState.active || !reviewState.isDragging || reviewState.selectionCanceled || !reviewState.currentImage) return;
      const rect = dom.imageReviewCanvas.getBoundingClientRect();
      const x = event.clientX - rect.left;
      const y = event.clientY - rect.top;
      const x1 = reviewState.dragStart?.x ?? x;
      const y1 = reviewState.dragStart?.y ?? y;
      const selection = {
        x: Math.min(x1, x),
        y: Math.min(y1, y),
        w: Math.abs(x - x1),
        h: Math.abs(y - y1)
      };
      reviewState.dragCurrent = selection;
      drawImageReview(reviewState.currentImage, selection);
    });

    dom.imageReviewCanvas.addEventListener("mouseup", async () => {
      if (!reviewState.active || !reviewState.isDragging) return;
      reviewState.isDragging = false;
      if (reviewState.selectionCanceled) return;
      const selection = reviewState.dragCurrent;
      reviewState.dragStart = null;
      reviewState.dragCurrent = null;
      if (!selection || selection.w < 5 || selection.h < 5) {
        if (reviewState.currentImage) drawImageReview(reviewState.currentImage);
        return;
      }
      try {
        await applyManualReviewCrop(selection);
      } catch (error) {
        setStatus(`No se pudo aplicar recorte libre: ${error.message}`, "error");
      }
    });

    document.addEventListener("keydown", (event) => {
      handleImageReviewKeyboard(event).catch(() => {});
    });

    if (!reviewState.pasteBound) {
      reviewState.pasteBound = true;
      document.addEventListener("paste", (event) => {
        if (!reviewState.active) return;
        const pendingOpen = isImagePendingOpen();
        const reviewOpen = isImageReviewOpen();
        if (!pendingOpen && !reviewOpen) return;
        const targetTag = String(event.target?.tagName || "").toLowerCase();
        if (targetTag === "input" || targetTag === "textarea") return;
        const imageBlob = pickImageBlobFromClipboardEvent(event);
        if (!imageBlob) return;
        event.preventDefault();
        let actionPromise = null;
        if (pendingOpen) {
          const pendingItem = getSelectedPendingItem();
          actionPromise = pendingItem
            ? savePendingImageBlob(imageBlob, pendingItem)
            : Promise.reject(new Error("Selecciona un pendiente para pegar imagen."));
        } else {
          actionPromise = saveCurrentReviewImageBlob(imageBlob);
        }
        actionPromise.catch((error) => {
          setStatus(`No se pudo pegar imagen: ${error.message}`, "error");
        });
      });
    }
  }

  function normalizeReviewIndex(index, total) {
    const parsed = Number(index);
    if (!Number.isInteger(parsed) || total <= 0) return 0;
    return Math.min(Math.max(parsed, 0), total - 1);
  }

  async function openImageReviewModal(options = {}) {
    const skipRefresh = Boolean(options?.skipRefresh);
    const initialIndex = normalizeReviewIndex(options?.initialIndex, Math.max(1, sessionImageEntries.length));
    const initialEntries = Array.isArray(options?.entries) ? options.entries : null;
    let progressOpened = false;
    const reportStep = ({ current = 0, total = 1, text = "" } = {}) => {
      if (!progressOpened) {
        progressOpened = openImageSyncModal(total || 1);
      }
      if (progressOpened) {
        updateImageSyncModalProgress({ current, total, label: "" });
        if (dom.imageSyncText) {
          dom.imageSyncText.textContent = String(text || "Preparando revisor de imagenes...");
        }
      }
    };
    try {
      bindImageReviewCanvasEvents();
      if (dom.imageReviewHint) {
        dom.imageReviewHint.textContent = "Sincronizando imagenes de esta sesion...";
      }
      if (!skipRefresh) {
        reportStep({ current: 0, total: 4, text: "Preparando revisor de imagenes..." });
        await refreshSessionImagesForReview({ onStep: reportStep });
      }
      const sourceEntries = initialEntries || sessionImageEntries || [];
      reviewState.entries = sourceEntries.map((entry) => ({ ...entry, deleted: false }));
      reviewState.index = normalizeReviewIndex(initialIndex, reviewState.entries.length);
      reviewState.undoStack = [];
      reviewState.suggestionItems = [];
      reviewState.suggestionLoading = false;
      reviewState.active = true;
      dom.imageReviewModal?.classList.remove("hidden");
      renderPendingList();
      renderSuggestionGrid();
      if (dom.imageReviewHint) {
        dom.imageReviewHint.textContent = "Solo se muestran imagenes detectadas en el mapa de esta sesion.";
      }
      await showCurrentImageReview();
    } catch (error) {
      setStatus(`No se pudo abrir revisor de imagenes: ${error.message}`, "error");
    } finally {
      if (progressOpened) {
        closeImageSyncModal();
      }
    }
  }

  function renderImageReviewGallery(entries) {
    const container = dom.imageReviewGalleryList;
    if (!container) return;
    container.innerHTML = "";
    const list = Array.isArray(entries) ? entries : [];
    if (!list.length) {
      const empty = document.createElement("div");
      empty.className = "small";
      empty.textContent = "No hay imagenes disponibles en esta sesion.";
      container.appendChild(empty);
      return;
    }

    list.forEach((entry, index) => {
      const item = document.createElement("button");
      item.type = "button";
      item.className = "image-gallery-item";
      const img = document.createElement("img");
      img.loading = "lazy";
      bindImageWithFallback(img, entry.web_path || "");
      img.alt = entry.label || entry.file_name || `imagen-${index + 1}`;
      const title = document.createElement("div");
      title.className = "image-gallery-title";
      title.textContent = entry.file_name || entry.label || `Imagen ${index + 1}`;
      item.appendChild(img);
      item.appendChild(title);
      item.addEventListener("click", async () => {
        closeImageReviewGalleryModal();
        await openImageReviewModal({
          skipRefresh: true,
          initialIndex: index,
          entries: list
        });
      });
      container.appendChild(item);
    });
  }

  async function refreshCurrentImageReview() {
    if (!isImageReviewOpen() || !reviewState.active) return;
    if (!reviewState.entries.length) {
      renderImageReviewEmpty("No hay imagenes de la sesion para revisar.");
      return;
    }
    try {
      await showCurrentImageReview();
      setStatus("Imagen actual refrescada.", "ok");
    } catch (error) {
      setStatus(`No se pudo refrescar la imagen actual: ${error.message}`, "error");
    }
  }

  function openImagePendingModal() {
    if (!reviewState.active) return;
    dom.imagePendingModal?.classList.remove("hidden");
    renderImagePendingEmpty("Sin imagen seleccionada");
    renderPendingList();
  }

  function closeImagePendingModal() {
    if (reviewState.pendingResolvedIds.size > 0) {
      reviewState.pendingItems = reviewState.pendingItems.filter(
        (item) => !reviewState.pendingResolvedIds.has(item.id)
      );
      reviewState.pendingResolvedIds = new Set();
      if (!getSelectedPendingItem()) {
        reviewState.selectedPendingId = reviewState.pendingItems[0]?.id || "";
      }
      renderPendingList();
    }
    dom.imagePendingModal?.classList.add("hidden");
  }

  function imageReviewSearchReplacePending() {
    const pendingItem = getSelectedPendingItem();
    if (!pendingItem) {
      setStatus("Selecciona una imagen pendiente.", "error");
      return;
    }
    openGoogleImagesForPendingItem(pendingItem);
  }

  async function loadOpenverseSuggestions() {
    await loadSuggestionCandidates("openverse", { forceRefresh: true });
  }

  async function loadBingSuggestions() {
    await loadSuggestionCandidates("bing", { forceRefresh: true });
  }

  async function loadDdgSuggestions() {
    await loadSuggestionCandidates("ddg", { forceRefresh: true });
  }

  async function refreshImageReviewGallery() {
    let progressOpened = false;
    const reportStep = ({ current = 0, total = 1, text = "" } = {}) => {
      if (!progressOpened) {
        progressOpened = openImageSyncModal(total || 1);
      }
      if (progressOpened) {
        updateImageSyncModalProgress({ current, total, label: "" });
        if (dom.imageSyncText) {
          dom.imageSyncText.textContent = String(text || "Refrescando galeria de imagenes...");
        }
      }
    };

    try {
      reportStep({ current: 0, total: 4, text: "Refrescando imagenes de sesion..." });
      await refreshSessionImagesForReview({ force: true, onStep: reportStep });
      const entries = (sessionImageEntries || []).map((entry) => ({ ...entry, deleted: false }));
      renderImageReviewGallery(entries);
      setStatus("Galeria de imagenes refrescada.", "ok");
    } catch (error) {
      setStatus(`No se pudo refrescar la galeria: ${error.message}`, "error");
    } finally {
      if (progressOpened) {
        closeImageSyncModal();
      }
    }
  }

  async function openImageReviewGalleryModal() {
    let progressOpened = false;
    const reportStep = ({ current = 0, total = 1, text = "" } = {}) => {
      if (!progressOpened) {
        progressOpened = openImageSyncModal(total || 1);
      }
      if (progressOpened) {
        updateImageSyncModalProgress({ current, total, label: "" });
        if (dom.imageSyncText) {
          dom.imageSyncText.textContent = String(text || "Cargando imagenes de sesion...");
        }
      }
    };

    try {
      reportStep({ current: 0, total: 4, text: "Preparando galeria de imagenes..." });
      await refreshSessionImagesForReview({ onStep: reportStep });
      const entries = (sessionImageEntries || []).map((entry) => ({ ...entry, deleted: false }));
      if (!entries.length) {
        setStatus("No hay imagenes en esta sesion para mostrar.", "error");
        return;
      }
      renderImageReviewGallery(entries);
      dom.imageReviewGalleryModal?.classList.remove("hidden");
    } catch (error) {
      setStatus(`No se pudo abrir la galeria: ${error.message}`, "error");
    } finally {
      if (progressOpened) {
        closeImageSyncModal();
      }
    }
  }

  function closeImageReviewGalleryModal() {
    dom.imageReviewGalleryModal?.classList.add("hidden");
  }

  function closeImageReviewModal() {
    clearImageReviewTimeout();
    reviewState.active = false;
    reviewState.isDragging = false;
    reviewState.selectionCanceled = false;
    reviewState.dragStart = null;
    reviewState.dragCurrent = null;
    reviewState.suggestionItems = [];
    reviewState.suggestionLoading = false;
    if (dom.imageSuggestionMeta) {
      dom.imageSuggestionMeta.textContent = "Selecciona un proveedor para cargar opciones relacionadas.";
    }
    renderSuggestionGrid();
    closeImagePendingModal();
    dom.imageReviewModal?.classList.add("hidden");
  }

  function openImageSyncModal(totalImages = 0) {
    if (!dom.imageSyncModal) return false;
    dom.imageSyncModal.classList.remove("hidden");
    if (dom.imageSyncText) {
      dom.imageSyncText.textContent = "Sincronizando imagenes para la vista previa...";
    }
    if (dom.imageSyncProgressBar) {
      dom.imageSyncProgressBar.style.width = "0%";
    }
    if (dom.imageSyncMeta) {
      dom.imageSyncMeta.textContent = `0 / ${Math.max(0, Number(totalImages) || 0)}`;
    }
    return true;
  }

  function updateImageSyncModalProgress({ current = 0, total = 0, label = "" } = {}) {
    if (!dom.imageSyncModal || dom.imageSyncModal.classList.contains("hidden")) return;
    const safeTotal = Math.max(0, Number(total) || 0);
    const safeCurrent = Math.min(safeTotal, Math.max(0, Number(current) || 0));
    const percent = safeTotal > 0 ? Math.round((safeCurrent / safeTotal) * 100) : 0;

    if (dom.imageSyncProgressBar) {
      dom.imageSyncProgressBar.style.width = `${percent}%`;
    }
    if (dom.imageSyncMeta) {
      dom.imageSyncMeta.textContent = `${safeCurrent} / ${safeTotal} (${percent}%)`;
    }
    if (dom.imageSyncText) {
      const prefix = label ? `Cargando: ${label}` : "Cargando imagenes...";
      dom.imageSyncText.textContent = safeTotal > 0 ? `${prefix} (${safeCurrent}/${safeTotal})` : prefix;
    }
  }

  function closeImageSyncModal() {
    if (!dom.imageSyncModal) return;
    dom.imageSyncModal.classList.add("hidden");
  }

  function openBingSearchModal(totalLabels = 0, provider = "bing") {
    if (!dom.bingSearchModal) return false;
    const providerLabel = getProviderLabel(provider);
    dom.bingSearchModal.classList.remove("hidden");
    if (dom.bingSearchProgressBar) dom.bingSearchProgressBar.style.width = "0%";
    if (dom.bingSearchTitle) dom.bingSearchTitle.textContent = `Buscando imagenes en ${providerLabel}`;
    if (dom.bingSearchText) dom.bingSearchText.textContent = `Iniciando busqueda en ${providerLabel}...`;
    if (dom.bingSearchMeta) dom.bingSearchMeta.textContent = `0 / ${Math.max(0, Number(totalLabels) || 0)}`;
    if (dom.btnStopBingSearch) {
      dom.btnStopBingSearch.disabled = false;
      dom.btnStopBingSearch.textContent = "Detener busqueda";
    }
    return true;
  }

  function updateBingSearchModalProgress(snapshot = {}) {
    if (!dom.bingSearchModal || dom.bingSearchModal.classList.contains("hidden")) return;
    const providerLabel = getProviderLabel(snapshot?.provider);
    const total = Math.max(0, Number(snapshot?.total_labels) || 0);
    const completed = Math.min(total, Math.max(0, Number(snapshot?.completed_labels) || 0));
    const percent = total > 0 ? Math.round((completed / total) * 100) : 0;

    if (dom.bingSearchProgressBar) dom.bingSearchProgressBar.style.width = `${percent}%`;
    if (dom.bingSearchMeta) {
      dom.bingSearchMeta.textContent = `${completed} / ${total} (${percent}%)`;
    }
    if (dom.bingSearchText) {
      const cached = Number(snapshot?.cached) || 0;
      const downloaded = Number(snapshot?.downloaded) || 0;
      const failed = Number(snapshot?.failed) || 0;
      const missing = Number(snapshot?.missing) || 0;
      const statusLabel = snapshot?.canceled
        ? "Busqueda detenida por el usuario."
        : snapshot?.status === "cancel_requested"
          ? "Deteniendo busqueda..."
          : snapshot?.done
            ? "Busqueda finalizada."
            : `Buscando imagenes en ${providerLabel}...`;
      dom.bingSearchText.textContent =
        `${statusLabel} Descargadas: ${downloaded}, cache: ${cached}, faltantes: ${missing}, fallidas: ${failed}.`;
    }
  }

  function closeBingSearchModal() {
    if (!dom.bingSearchModal) return;
    dom.bingSearchModal.classList.add("hidden");
    if (dom.btnStopBingSearch) {
      dom.btnStopBingSearch.disabled = false;
      dom.btnStopBingSearch.textContent = "Detener busqueda";
      dom.btnStopBingSearch.onclick = null;
    }
  }

  async function sleep(ms) {
    await new Promise((resolve) => setTimeout(resolve, ms));
  }

  async function initPy(forceReload = false) {
    if (state.pyReady && !forceReload) {
      setStatus("Motor Python ya inicializado.", "ok");
      return;
    }

    try {
      if (!state.pyodide) {
        setStatus("Inicializando Pyodide...");
        state.pyodide = await loadPyodide();
      }

      setStatus(forceReload ? "Recargando generador Python..." : "Pyodide inicializado. Cargando generador...");

      const cacheBust = forceReload ? `?v=${Date.now()}` : "";
      const scriptResponse = await fetch(`../codigo/Scripts/Mapas_mentales.py${cacheBust}`, {
        cache: "no-store"
      });
      if (!scriptResponse.ok) {
        throw new Error("No se pudo leer ../codigo/Scripts/Mapas_mentales.py. Abre el proyecto desde localhost.");
      }
      const mapScript = await scriptResponse.text();

      state.pyodide.globals.set("MAP_SCRIPT_SOURCE", mapScript);
      state.pyodide.runPython(`
import ast
import traceback
import pathlib
import types
import os
import sys

try:
    import PIL  # type: ignore
except Exception:
    pil_mod = types.ModuleType("PIL")
    image_mod = types.ModuleType("PIL.Image")
    class _ImageFallback:
        @staticmethod
        def open(*_args, **_kwargs):
            raise RuntimeError("Pillow no disponible en este runtime.")
    image_mod.open = _ImageFallback.open
    pil_mod.Image = image_mod
    sys.modules["PIL"] = pil_mod
    sys.modules["PIL.Image"] = image_mod

_runtime_module = types.ModuleType("mapas_mentales_runtime")
_runtime_module.__file__ = "codigo/Scripts/Mapas_mentales.py"
exec(MAP_SCRIPT_SOURCE, _runtime_module.__dict__)

def _to_plain(obj):
    if isinstance(obj, dict):
        return {str(k): _to_plain(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_to_plain(x) for x in obj]
    if isinstance(obj, pathlib.Path):
        return str(obj)
    if isinstance(obj, (str, int, float, bool)) or obj is None:
        return obj
    return str(obj)

def _parse_python_value(text):
    try:
        return ast.literal_eval(text)
    except Exception:
        allowed_globals = {"__builtins__": {}, "os": os, "Path": pathlib.Path}
        return eval(text, allowed_globals, {})

def parse_map_literals(config_text, mind_map_text):
    cfg = _parse_python_value(config_text)
    mmap = _parse_python_value(mind_map_text)
    if not isinstance(cfg, dict):
        raise ValueError("CONFIG debe ser un dict.")
    if not isinstance(mmap, dict):
        raise ValueError("mapa_ejemplo debe ser un dict.")
    return {"config": _to_plain(cfg), "mind_map": _to_plain(mmap)}

def generate_drawio_xml(config_text, mind_map_text):
    try:
        cfg = _parse_python_value(config_text)
        mmap = _parse_python_value(mind_map_text)
        out_path = _runtime_module.generar_mapa_mental(mmap, cfg)
        with open(out_path, "r", encoding="utf-8") as fh:
            xml = fh.read()
        return {"ok": True, "xml": xml, "out_path": out_path}
    except Exception as exc:
        return {"ok": False, "error": str(exc), "traceback": traceback.format_exc()}

def load_from_python_source(source_code, source_path="mapa_mental.py"):
    ns = {
        "__name__": "mapa_mental_ui_loader",
        "__file__": source_path or "mapa_mental.py",
    }
    exec(source_code, ns, ns)
    if "CONFIG" not in ns:
        raise ValueError("No se encontro CONFIG en el archivo Python.")
    if "mapa_ejemplo" not in ns:
        raise ValueError("No se encontro mapa_ejemplo en el archivo Python.")
    return {
        "config": _to_plain(ns["CONFIG"]),
        "mind_map": _to_plain(ns["mapa_ejemplo"]),
    }
`);

      state.pyReady = true;
      lastAutoImageSyncSignature = "";
      setStatus(
        forceReload
          ? "Generador recargado. Ya puedes generar preview."
          : "Motor Python listo. Ya puedes generar preview.",
        "ok"
      );
      if (!forceReload) {
        await tryLoadDefaultPyFromProject();
      }
    } catch (error) {
      setStatus(`Error al inicializar: ${error.message}`, "error");
    }
  }

  async function parseConfigTextToObject(text) {
    if (!state.pyReady) {
      throw new Error("Inicializa primero el motor Python.");
    }
    state.pyodide.globals.set("CONFIG_TEXT_INPUT", text);
    const resultProxy = state.pyodide.runPython("parse_map_literals(CONFIG_TEXT_INPUT, '{}')");
    const result = resultProxy.toJs({ dict_converter: Object.fromEntries });
    resultProxy.destroy();
    return result.config;
  }

  async function applyConfigFromEditor(showStatus = true) {
    const parsedConfig = await parseConfigTextToObject(dom.configEditor.value);
    state.currentConfig = normalizeConfig(constants.DEFAULT_CONFIG, parsedConfig);
    configFormApi.renderConfigForm();
    configFormApi.updateConfigTextFromState();
    if (showStatus) {
      setStatus("CONFIG avanzada aplicada al formulario.", "ok");
    }
  }

  async function tryLoadDefaultPyFromProject() {
    if (!state.pyReady) return;
    try {
      const response = await fetch("../codigo/vista/mapa_mental.py");
      if (!response.ok) {
        return;
      }
      const source = await response.text();
      await loadFromPythonSourceText(source, "codigo/vista/mapa_mental.py");
      setStatus("Motor Python listo y archivo base cargado automaticamente.", "ok");
    } catch (_) {
      setStatus("Motor Python listo. No se cargo automaticamente el archivo base.");
    }
  }

  async function loadFromPythonSourceText(sourceText, sourceLabel = "archivo .py") {
    if (!state.pyReady) throw new Error("Primero inicializa el motor Python.");
    state.pyodide.globals.set("SOURCE_CODE_TO_LOAD", sourceText);
    const sourcePath = String(sourceLabel || "mapa_mental.py").replaceAll("\\", "/");
    state.pyodide.globals.set("SOURCE_PATH_TO_LOAD", sourcePath);
    const resultProxy = state.pyodide.runPython("load_from_python_source(SOURCE_CODE_TO_LOAD, SOURCE_PATH_TO_LOAD)");
    const result = resultProxy.toJs({ dict_converter: Object.fromEntries });
    resultProxy.destroy();

    state.currentConfig = normalizeConfig(constants.DEFAULT_CONFIG, result.config);
    configFormApi.renderConfigForm();
    configFormApi.updateConfigTextFromState();
    dom.mindMapEditor.value = jsToPythonLiteral(result.mind_map);
    setStatus(`Se cargo CONFIG y mapa_ejemplo desde ${sourceLabel}.`, "ok");
  }

  async function applyGeminiToMindMap() {
    const instruction = String(dom.geminiPrompt?.value || "").trim();
    if (!instruction) {
      setStatus("Escribe una instruccion para Gemini.", "error");
      return;
    }

    const model = String(dom.geminiModel?.value || "").trim() || "gemini-2.5-flash-lite";

    try {
      dom.btnApplyGemini.disabled = true;
      setStatus("Consultando Gemini para actualizar mapa mental...");

      let response = await fetch("/api/ia/mind-map", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          instruction,
          model,
          mind_map_text: dom.mindMapEditor.value
        })
      });

      if (response.status === 404) {
        response = await fetch("/api/ia/concept-map", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            instruction,
            model,
            concept_map_text: dom.mindMapEditor.value
          })
        });
      }

      let payload = {};
      try {
        payload = await response.json();
      } catch (_) {
        payload = {};
      }

      if (!response.ok || payload.ok === false) {
        const errorMsg = payload.error || `Error HTTP ${response.status}`;
        throw new Error(errorMsg);
      }

      const nextMindMap = String(
        payload.mind_map_python || payload.mapa_mental_python || payload.concept_map_python || ""
      ).trim();
      if (!nextMindMap) {
        throw new Error("La respuesta de Gemini no incluyo mapa mental en formato Python.");
      }

      if (state.pyReady) {
        state.pyodide.globals.set("MIND_MAP_TEXT_INPUT", nextMindMap);
        const validateProxy = state.pyodide.runPython("parse_map_literals('{}', MIND_MAP_TEXT_INPUT)");
        validateProxy.destroy();
      }

      dom.mindMapEditor.value = nextMindMap;
      setStatus(`mapa_ejemplo actualizado con Gemini (${payload.model || model}).`, "ok");
    } catch (error) {
      setStatus(`No se pudo aplicar Gemini: ${error.message}`, "error");
    } finally {
      dom.btnApplyGemini.disabled = false;
    }
  }

  function normalizeRelativePath(pathText, fallback = constants.DEFAULT_CONFIG.IMAGE_DIR || "ImagenesMapaMental") {
    const raw = String(pathText ?? "").replaceAll("\\", "/").trim();
    const candidate = (raw || String(fallback || "ImagenesMapaMental")).replace(/^\/+|\/+$/g, "");
    if (/^[a-zA-Z]:\//.test(candidate)) {
      throw new Error("IMAGE_DIR no puede ser absoluto.");
    }
    const parts = candidate.split("/").filter(Boolean);
    if (!parts.length) {
      throw new Error("IMAGE_DIR no puede estar vacio.");
    }
    if (parts.some((part) => part === "." || part === "..")) {
      throw new Error("IMAGE_DIR no puede contener '.' o '..'.");
    }
    return parts.join("/");
  }

  function ensurePyodideDir(relativeDir) {
    const fs = state.pyodide?.FS;
    if (!fs) throw new Error("Pyodide no esta inicializado.");

    const parts = String(relativeDir).split("/").filter(Boolean);
    let current = "";
    parts.forEach((part) => {
      current = current ? `${current}/${part}` : part;
      const exists = fs.analyzePath(current).exists;
      if (!exists) fs.mkdir(current);
    });
  }

  async function syncImagesToPyodideFs(images, imageDir, options = {}) {
    if (!state.pyReady) {
      throw new Error("Inicializa primero el motor Python.");
    }
    const targetDir = normalizeRelativePath(imageDir);
    ensurePyodideDir(targetDir);
    const onProgress = typeof options?.onProgress === "function" ? options.onProgress : null;
    const imageList = Array.isArray(images) ? images : [];
    const total = imageList.length;

    if (onProgress && total > 0) {
      onProgress({ current: 0, total, label: "Preparando..." });
    }

    let synced = 0;
    let skipped = 0;
    let processed = 0;
    for (const imageInfo of imageList) {
      const webPath = String(imageInfo?.web_path || "").trim();
      const fileName = String(imageInfo?.file_name || "").trim();
      const label = fileName || String(imageInfo?.label || "").trim() || "imagen";
      if (!webPath || !fileName) {
        skipped += 1;
        processed += 1;
        if (onProgress) {
          onProgress({ current: processed, total, label });
        }
        continue;
      }

      const candidateUrls = buildCandidateImageUrls(webPath);

      let fileBytes = null;
      for (const url of candidateUrls) {
        let response = null;
        try {
          response = await fetch(url, { cache: "no-store" });
        } catch (_) {
          response = null;
        }
        if (!response || !response.ok) continue;
        fileBytes = new Uint8Array(await response.arrayBuffer());
        break;
      }

      if (!fileBytes) {
        skipped += 1;
        processed += 1;
        if (onProgress) {
          onProgress({ current: processed, total, label });
        }
        continue;
      }
      const safeName = fileName.replaceAll("\\", "/").split("/").filter(Boolean).pop();
      if (!safeName) {
        skipped += 1;
        processed += 1;
        if (onProgress) {
          onProgress({ current: processed, total, label });
        }
        continue;
      }
      const filePath = `${targetDir}/${safeName}`;
      state.pyodide.FS.writeFile(filePath, fileBytes);
      synced += 1;
      processed += 1;
      if (onProgress) {
        onProgress({ current: processed, total, label });
      }
    }
    return { synced, skipped, targetDir, total };
  }

  function getCurrentImageSyncSignature() {
    const imageDir = String(state.currentConfig?.IMAGE_DIR || constants.DEFAULT_CONFIG.IMAGE_DIR || "");
    const mapText = String(dom.mindMapEditor?.value || "");
    return `${imageDir}::${mapText}`;
  }

  async function requestSessionImageCatalog({
    downloadMissing = false,
    forceRefresh = false,
    maxLabels = null,
    suffix = null,
    silent = false,
    skipApplyConfig = false,
    onImageSyncProgress = null
  } = {}) {
    if (!skipApplyConfig) {
      await applyConfigFromEditor(false);
    }

    const requestPayload = {
      mind_map_text: dom.mindMapEditor.value,
      image_dir: state.currentConfig.IMAGE_DIR || constants.DEFAULT_CONFIG.IMAGE_DIR,
      provider: getSelectedImageProvider(),
      suffix: String(suffix || dom.bingSuffix?.value || "").trim(),
      force_refresh: Boolean(forceRefresh),
      download_missing: Boolean(downloadMissing)
    };
    if (Number.isInteger(maxLabels) && maxLabels > 0) {
      requestPayload.max_labels = maxLabels;
    }

    const response = await fetch("/api/images/search", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(requestPayload)
    });

    let payload = {};
    try {
      payload = await response.json();
    } catch (_) {
      payload = {};
    }

    if (response.status === 404) {
      if (silent) return null;
      throw new Error("API /api/images/search no disponible. Inicia servidor_mapa_mental.py.");
    }
    if (!response.ok || payload.ok === false) {
      if (silent) return null;
      throw new Error(payload.error || `Error HTTP ${response.status}`);
    }

    setSessionImageEntries(payload.images || [], payload.image_dir || requestPayload.image_dir);
    return payload;
  }

  function sanitizeFilenameLikePython(text) {
    return String(text || "")
      .replace(/[\\/:*?"<>|]+/g, "-")
      .trim();
  }

  function buildGoogleLinksHtml(labels, initialSuffix = "") {
    const total = Array.isArray(labels) ? labels.length : 0;
    const chips = (Array.isArray(labels) ? labels : [])
      .map((label) => {
        const safe = String(label || "").trim();
        const escaped = safe
          .replaceAll("&", "&amp;")
          .replaceAll("<", "&lt;")
          .replaceAll(">", "&gt;")
          .replaceAll('"', "&quot;");
        const suffixSafe = String(initialSuffix || "").trim();
        const queryText = suffixSafe ? `${safe} ${suffixSafe}` : safe;
        const query = encodeURIComponent(queryText);
        return `<a class="chip" href="https://www.google.com/search?tbm=isch&q=${query}" target="_blank" rel="noopener noreferrer" data-label="${escaped}">${escaped}</a>`;
      })
      .join("\n");

    return `<!doctype html>
<html lang="es"><head><meta charset="utf-8"><title>Enlaces Google Imagenes</title>
<style>
body{font-family:"Segoe UI",sans-serif;background:#0b1021;color:#e5e7eb;margin:0;padding:24px}
.wrap{max-width:1200px;margin:0 auto}
.top{display:flex;justify-content:space-between;align-items:baseline;gap:12px}
.count{color:#9ca3af;font-size:14px}
.suffix-row{display:grid;grid-template-columns:1fr auto;gap:8px;margin:8px 0 10px}
.suffix-row input{background:#111827;border:1px solid #374151;border-radius:8px;color:#e5e7eb;padding:10px}
.suffix-row button{background:#374151;border:1px solid #4b5563;border-radius:8px;color:#fff;padding:10px 14px;cursor:pointer}
.hint,#checkBtn{background:#111827;border:1px solid #1f2937;border-radius:10px;padding:12px;color:#9ca3af}
#checkBtn{display:block;width:100%;font-weight:700;color:#fff;background:#1d4ed8;border-color:#60a5fa;cursor:pointer;margin:10px 0 14px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:10px}
.chip{display:block;padding:10px;border-radius:8px;background:#1f2937;color:#e5e7eb;text-decoration:none;border:1px solid #374151}
.chip.downloaded{background:#166534;border-color:#22c55e;color:#d1fae5}
</style></head><body><div class="wrap">
<div class="top"><h2>Enlaces a Google Imagenes</h2><div class="count">${total} enlace(s)</div></div>
<p class="hint"><b>Paso 1:</b> Selecciona tu carpeta de imagenes del mapa mental.<br><b>Paso 2:</b> Los enlaces se pondran verdes si la imagen ya existe.</p>
<div class="suffix-row">
  <input id="suffixInput" type="text" placeholder="Sufijo de busqueda (opcional)" value="${String(initialSuffix || "").replaceAll('"', "&quot;")}">
  <button id="applySuffixBtn" type="button">Aplicar sufijo</button>
</div>
<button id="checkBtn">Verificar imagenes descargadas</button>
<div class="grid">${chips}</div></div>
<script>
let dirHandle=null;
const chips=[...document.querySelectorAll('.chip')];
const suffixInput=document.getElementById('suffixInput');
const applySuffixBtn=document.getElementById('applySuffixBtn');
const VALID_EXTENSIONS=[".jpg",".jpeg",".png",".webp",".gif",".svg"];
function sanitizeFilename(text){return String(text||"").replace(/[\\\\/:*?"<>|]/g,"-").trim();}
async function checkImageExists(label){
  if(!dirHandle) return false;
  const safe=sanitizeFilename(label);
  for(const ext of VALID_EXTENSIONS){
    try{await dirHandle.getFileHandle(safe+ext,{create:false}); return true;}catch(e){if(e.name!=="NotFoundError"){}}
  }
  return false;
}
async function updateAll(){
  if(!dirHandle) return;
  await Promise.all(chips.map(async(chip)=>{const ok=await checkImageExists(chip.dataset.label); chip.classList.toggle('downloaded',ok);}));
}
function updateChipLinksBySuffix(){
  const suffix=String(suffixInput?.value||"").trim();
  for(const chip of chips){
    const label=String(chip.dataset.label||"").trim();
    const query=suffix ? (label+" "+suffix) : label;
    chip.href="https://www.google.com/search?tbm=isch&q="+encodeURIComponent(query);
  }
}
applySuffixBtn?.addEventListener('click',()=>{updateChipLinksBySuffix(); if(dirHandle) updateAll();});
suffixInput?.addEventListener('keydown',(e)=>{if(e.key==='Enter'){e.preventDefault(); updateChipLinksBySuffix(); if(dirHandle) updateAll();}});
document.getElementById('checkBtn').addEventListener('click', async()=>{
  try{dirHandle=await window.showDirectoryPicker({id:'imagenes-mapa-mental-folder',mode:'read',startIn:'downloads'}); await updateAll();}catch(e){}
});
window.addEventListener('focus',()=>{if(dirHandle) updateAll();});
</script></body></html>`;
  }

  async function openGoogleLinksForMap() {
    const win = window.open("about:blank", "_blank");
    if (!win) {
      setStatus("El navegador bloqueo la ventana emergente. Permite popups para este sitio.", "error");
      return;
    }
    win.document.open();
    win.document.write(
      "<!doctype html><html lang='es'><head><meta charset='utf-8'><title>Cargando enlaces...</title></head>" +
        "<body style=\"font-family:Segoe UI,sans-serif;background:#0b1021;color:#e5e7eb;padding:20px\">" +
        "<h3>Cargando enlaces de imagenes...</h3></body></html>"
    );
    win.document.close();

    try {
      await applyConfigFromEditor(false);
      const response = await fetch(
        `/api/images/google-links?mind_map_text=${encodeURIComponent(String(dom.mindMapEditor?.value || ""))}`,
        { cache: "no-store" }
      );
      let payload = {};
      try {
        payload = await response.json();
      } catch (_) {
        payload = {};
      }
      if (!response.ok || payload.ok === false) {
        throw new Error(payload.error || `Error HTTP ${response.status}`);
      }
      const suffix = String(dom.bingSuffix?.value || "").trim();
      win.document.open();
      win.document.write(buildGoogleLinksHtml(payload.labels || [], suffix));
      win.document.close();
      setStatus(`Enlaces Google listos (${payload.total || 0} etiquetas).`, "ok");
    } catch (error) {
      try {
        win.document.open();
        win.document.write(
          "<!doctype html><html lang='es'><head><meta charset='utf-8'><title>Error</title></head>" +
            "<body style=\"font-family:Segoe UI,sans-serif;background:#0b1021;color:#fca5a5;padding:20px\">" +
            `<h3>No se pudo cargar enlaces Google</h3><p>${String(error.message || error)}</p></body></html>`
        );
        win.document.close();
      } catch (_) {
        // no-op
      }
      setStatus(`No se pudo abrir enlaces Google: ${error.message}`, "error");
    }
  }

  async function syncBingImagesIntoRuntime({
    downloadMissing = false,
    forceRefresh = false,
    maxLabels = null,
    suffix = null,
    silent = false,
    skipApplyConfig = false,
    onImageSyncProgress = null
  } = {}) {
    const payload = await requestSessionImageCatalog({
      downloadMissing,
      forceRefresh,
      maxLabels,
      suffix,
      silent,
      skipApplyConfig
    });
    if (!payload) return null;

    const syncResult = await syncImagesToPyodideFs(payload.images || [], payload.image_dir, {
      onProgress: onImageSyncProgress
    });
    return { payload, syncResult };
  }

  async function startBingSearchJob(requestPayload) {
    const response = await fetch("/api/images/search/start", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(requestPayload)
    });
    let payload = {};
    try {
      payload = await response.json();
    } catch (_) {
      payload = {};
    }
    if (response.status === 404) {
      throw new Error("API /api/images/search/start no disponible. Inicia servidor_mapa_mental.py.");
    }
    if (!response.ok || payload.ok === false) {
      throw new Error(payload.error || `Error HTTP ${response.status}`);
    }
    return payload;
  }

  async function getBingSearchJobStatus(jobId) {
    const response = await fetch(`/api/images/search/status?job_id=${encodeURIComponent(jobId)}`, {
      cache: "no-store"
    });
    let payload = {};
    try {
      payload = await response.json();
    } catch (_) {
      payload = {};
    }
    if (!response.ok || payload.ok === false) {
      throw new Error(payload.error || `Error HTTP ${response.status}`);
    }
    return payload;
  }

  async function cancelBingSearchJob(jobId) {
    if (!jobId) return;
    try {
      await fetch("/api/images/search/cancel", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ job_id: jobId })
      });
    } catch (_) {
      // Ignora errores de red al cancelar; el polling reflejara el estado final.
    }
  }

  async function ensureImagesVisibleInPreview(options = {}) {
    const showProgress = Boolean(options?.showProgress);
    const signature = getCurrentImageSyncSignature();
    if (signature === lastAutoImageSyncSignature) return;
    let modalOpened = false;
    const handleProgress = showProgress
      ? ({ current, total, label }) => {
        if (!modalOpened && total > 0) {
          modalOpened = openImageSyncModal(total);
        }
        if (modalOpened) {
          updateImageSyncModalProgress({ current, total, label });
        }
      }
      : null;

    try {
      const result = await syncBingImagesIntoRuntime({
        downloadMissing: false,
        forceRefresh: false,
        silent: true,
        skipApplyConfig: true,
        onImageSyncProgress: handleProgress
      });
      if (result) {
        lastAutoImageSyncSignature = signature;
      }
    } finally {
      if (modalOpened) {
        closeImageSyncModal();
      }
    }
  }

  async function runPuenteLocalSearch(requestPayload, maxLabels) {
    const modalOpened = openBingSearchModal(0, "Puente Local (DuckDuckGo)");
    try {
      const linkResp = await fetch(`/api/images/google-links?mind_map_text=${encodeURIComponent(requestPayload.mind_map_text)}`);
      const linkData = await linkResp.json();
      if (!linkData.ok) throw new Error(linkData.error || "No se pudieron obtener los nodos.");
      let labels = linkData.labels;
      if (maxLabels !== null) labels = labels.slice(0, maxLabels);

      let totals = { success: 0, missing: 0, failed: 0, cache: 0 };
      const rootContext = (labels.length > 0 && !requestPayload.suffix) ? labels[0] : requestPayload.suffix;
      
      updateBingSearchModalProgress({
         done: false,
         status: "running",
         total_labels: labels.length,
         processed_labels: 0,
         downloaded_count: 0,
         missing_count: 0,
         failed_count: 0,
         cache_count: 0
      });

      for (let i = 0; i < labels.length; i++) {
        if (bingSearchStopRequested) break;
        const label = labels[i];
        let urlToDownload = null;
        try {
          const query = encodeURIComponent(`${label} ${rootContext}`.trim());
          const bridgeResp = await fetch(`http://localhost:8765/api/search?q=${query}&provider=ddg`);
          const bridgeData = await bridgeResp.json();
          if (bridgeData.ok && bridgeData.results && bridgeData.results.length > 0) {
             urlToDownload = bridgeData.results[0];
          }
        } catch (e) {
          console.warn("Error contactando Puente Local", e);
        }

        if (urlToDownload) {
          try {
             const saveResp = await fetch("/api/images/save_from_url", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ label, url: urlToDownload, image_dir: requestPayload.image_dir })
             });
             const saveData = await saveResp.json();
             if (saveData.ok) totals.success++; else totals.failed++;
          } catch(e) {
             totals.failed++;
          }
        } else {
          totals.failed++;
        }

        updateBingSearchModalProgress({
           done: false,
           status: "running",
           total_labels: labels.length,
           processed_labels: i + 1,
           downloaded_count: totals.success,
           missing_count: 0,
           failed_count: totals.failed,
           cache_count: 0
        });
      }
      
      if (modalOpened) closeBingSearchModal();
      return { ok: true, status: "completed", downloaded_count: totals.success };
    } catch(e) {
      if (modalOpened) closeBingSearchModal();
      throw e;
    }
  }

  async function downloadBingImages() {
    if (bingSearchRunning) {
      setStatus("Ya hay una busqueda de imagenes en curso.", "error");
      return;
    }
    if (!state.pyReady) {
      await initPy();
      if (!state.pyReady) return;
    }

    const maxRaw = String(dom.bingMaxLabels?.value || "").trim();
    let maxLabels = null;
    if (maxRaw) {
      const parsed = Number(maxRaw);
      if (!Number.isFinite(parsed) || parsed <= 0 || !Number.isInteger(parsed)) {
        setStatus("Max nodos debe ser un entero mayor a 0.", "error");
        return;
      }
      maxLabels = parsed;
    }

    try {
      bingSearchRunning = true;
      bingSearchStopRequested = false;
      activeBingJobId = "";
      dom.btnBingImages.disabled = true;
      await applyConfigFromEditor(false);
      const selectedProvider = getSelectedImageProvider();
      const selectedProviderLabel = getProviderLabel(selectedProvider);
      setStatus(`Iniciando busqueda de imagenes con ${selectedProviderLabel}...`);

      const requestPayload = {
        mind_map_text: dom.mindMapEditor.value,
        image_dir: state.currentConfig.IMAGE_DIR || constants.DEFAULT_CONFIG.IMAGE_DIR,
        provider: selectedProvider,
        suffix: String(dom.bingSuffix?.value || "").trim(),
        force_refresh: false,
        download_missing: true
      };
      if (maxLabels !== null) {
        requestPayload.max_labels = maxLabels;
      }

      if (selectedProvider === "puente") {
        const finalSnapshot = await runPuenteLocalSearch(requestPayload, maxLabels);
        await refreshImageGallery();
        const msg = `Imagenes locales completadas: ${finalSnapshot.downloaded_count}`;
        setStatus(msg, "success");
        return;
      }

      const startPayload = await startBingSearchJob(requestPayload);
      activeBingJobId = String(startPayload.job_id || "").trim();
      if (!activeBingJobId) {
        throw new Error("No se recibio job_id de la busqueda.");
      }

      const modalOpened = openBingSearchModal(startPayload.total_labels || 0, startPayload.provider || selectedProvider);
      if (dom.btnStopBingSearch) {
        dom.btnStopBingSearch.onclick = async () => {
          if (bingSearchStopRequested) return;
          bingSearchStopRequested = true;
          dom.btnStopBingSearch.disabled = true;
          dom.btnStopBingSearch.textContent = "Deteniendo...";
          await cancelBingSearchJob(activeBingJobId);
        };
      }

      let finalSnapshot = null;
      while (true) {
        const snapshot = await getBingSearchJobStatus(activeBingJobId);
        finalSnapshot = snapshot;
        if (modalOpened) {
          updateBingSearchModalProgress(snapshot);
        }
        if (snapshot.done) break;
        if (bingSearchStopRequested) {
          await cancelBingSearchJob(activeBingJobId);
        }
        await sleep(450);
      }
      if (modalOpened) {
        closeBingSearchModal();
      }

      if (!finalSnapshot) {
        throw new Error("No se pudo obtener el resultado final de la busqueda.");
      }
      if (finalSnapshot.status === "error") {
        throw new Error(finalSnapshot.error || "Error en la busqueda de imagenes.");
      }

      setSessionImageEntries(finalSnapshot.images || [], finalSnapshot.image_dir || requestPayload.image_dir);
      const syncResult = await syncImagesToPyodideFs(finalSnapshot.images || [], finalSnapshot.image_dir || requestPayload.image_dir);
      lastAutoImageSyncSignature = getCurrentImageSyncSignature();
      await generatePreview({ silent: true, preserveViewport: true });

      if (finalSnapshot.canceled) {
        setStatus(
          `Busqueda detenida. Procesadas: ${finalSnapshot.completed_labels || 0}/${finalSnapshot.total_labels || 0}. ` +
            `Imagenes cargadas en runtime: ${syncResult.synced}. Vista previa actualizada automaticamente.`,
          "ok"
        );
      } else {
        setStatus(
          `Imagenes listas. Descargadas: ${finalSnapshot.downloaded || 0}, cache: ${finalSnapshot.cached || 0}, ` +
            `faltantes: ${finalSnapshot.missing || 0}, fallidas: ${finalSnapshot.failed || 0}, ` +
            `cargadas en runtime: ${syncResult.synced}. Vista previa actualizada automaticamente.`,
          "ok"
        );
      }
    } catch (error) {
      setStatus(`No se pudieron cargar imagenes: ${error.message}`, "error");
    } finally {
      if (bingSearchStopRequested && activeBingJobId) {
        await cancelBingSearchJob(activeBingJobId);
      }
      closeBingSearchModal();
      bingSearchRunning = false;
      bingSearchStopRequested = false;
      activeBingJobId = "";
      if (dom.btnStopBingSearch) {
        dom.btnStopBingSearch.disabled = false;
        dom.btnStopBingSearch.textContent = "Detener busqueda";
        dom.btnStopBingSearch.onclick = null;
      }
      dom.btnBingImages.disabled = false;
    }
  }

  async function generatePreview(options = {}) {
    const silent = Boolean(options?.silent);
    const preserveViewport = Boolean(options?.preserveViewport);
    const skipImageSync = Boolean(options?.skipImageSync);
    if (!state.pyReady) {
      setStatus("Motor Python aun no esta listo. Espera unos segundos.", "error");
      return;
    }
    try {
      await applyConfigFromEditor(false);
      if (!skipImageSync) {
        await ensureImagesVisibleInPreview({ showProgress: !silent });
      }
      if (!silent) {
        setStatus("Generando preview...");
      }
      state.pyodide.globals.set("CONFIG_TEXT_INPUT", jsToPythonLiteral(state.currentConfig));
      state.pyodide.globals.set("MIND_MAP_TEXT_INPUT", dom.mindMapEditor.value);
      const resultProxy = state.pyodide.runPython("generate_drawio_xml(CONFIG_TEXT_INPUT, MIND_MAP_TEXT_INPUT)");
      const result = resultProxy.toJs({ dict_converter: Object.fromEntries });
      resultProxy.destroy();

      if (!result.ok) {
        setStatus(`Error al generar:\n${result.error}\n\n${result.traceback}`, "error");
        return;
      }

      state.lastGeneratedXml = result.xml;
      state.lastOutputPath = result.out_path;
      previewApi.renderGraph(state.lastGeneratedXml, { preserveView: preserveViewport });
      dom.previewMeta.textContent = `Generado: ${state.lastOutputPath}`;
      if (!silent) {
        setStatus(`Preview generado correctamente.\nSalida runtime: ${state.lastOutputPath}`, "ok");
      }
    } catch (error) {
      setStatus(`Error inesperado al generar: ${error.message}`, "error");
    }
  }

  return {
    initPy,
    parseConfigTextToObject,
    applyConfigFromEditor,
    tryLoadDefaultPyFromProject,
    loadFromPythonSourceText,
    applyGeminiToMindMap,
    openGoogleLinksForMap,
    downloadBingImages,
    generatePreview,
    openImageReviewModal,
    openImagePendingModal,
    openImageReviewGalleryModal,
    closeImageReviewModal,
    closeImagePendingModal,
    closeImageReviewGalleryModal,
    refreshCurrentImageReview,
    refreshImageReviewGallery,
    loadOpenverseSuggestions,
    loadBingSuggestions,
    loadDdgSuggestions,
    imageReviewPrev,
    imageReviewNext,
    imageReviewDeleteCurrent,
    imageReviewCropBottom,
    undoImageReviewAction,
    imageReviewPasteFromClipboard,
    imageReviewReplaceCurrentFromClipboard,
    imageReviewSearchReplaceCurrent,
    imageReviewSearchReplacePending
  };
}


