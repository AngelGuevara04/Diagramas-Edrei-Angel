import { createConfigFormApi } from "./config-form.js";
import { createFileActionsApi } from "./file-actions.js";
import { createPreviewApi } from "./preview.js";
import { createRuntimeApi } from "./runtime.js?v=3";
import { constants, dom, state } from "./state.js";
import { closeAdvancedModal, openAdvancedModal, setStatus as setStatusBase } from "./ui.js";
import { jsToPythonLiteral, normalizeConfig } from "./utils.js";

let hasBooted = false;
const AUTO_PREVIEW_DELAY_MS = 2000;

export function bootEditorMapaConceptual() {
  if (hasBooted) return;
  hasBooted = true;

  const setStatus = (message, level = "info") => {
    setStatusBase(dom.statusBox, message, level);
  };

  let runtimeApi = null;
  let autoPreviewTimer = null;
  let autoPreviewInFlight = false;
  let autoPreviewQueued = false;

  const runAutoPreview = async () => {
    if (!runtimeApi || !state.pyReady) return;
    if (autoPreviewInFlight) {
      autoPreviewQueued = true;
      return;
    }

    autoPreviewInFlight = true;
    try {
      await runtimeApi.generatePreview({ silent: true, preserveViewport: true });
    } finally {
      autoPreviewInFlight = false;
      if (autoPreviewQueued) {
        autoPreviewQueued = false;
        runAutoPreview();
      }
    }
  };

  const scheduleAutoPreview = () => {
    if (autoPreviewTimer) {
      clearTimeout(autoPreviewTimer);
    }
    autoPreviewTimer = setTimeout(() => {
      autoPreviewTimer = null;
      runAutoPreview();
    }, AUTO_PREVIEW_DELAY_MS);
  };

  const configFormApi = createConfigFormApi({
    dom,
    state,
    constants,
    setStatus,
    onConfigChanged: scheduleAutoPreview
  });

  const previewApi = createPreviewApi({
    dom,
    state,
    constants
  });

  runtimeApi = createRuntimeApi({
    dom,
    state,
    constants,
    setStatus,
    configFormApi,
    previewApi
  });

  const fileActionsApi = createFileActionsApi({
    state,
    setStatus,
    runtimeApi
  });

  state.currentConfig = normalizeConfig(constants.DEFAULT_CONFIG, constants.DEFAULT_CONFIG);
  dom.configEditor.value = jsToPythonLiteral(state.currentConfig);
  dom.mindMapEditor.value = constants.fallbackMindMap;

  // Initialize CodeMirror and bind it to the live auto-preview
  const cmEditor = window.CodeMirror.fromTextArea(dom.mindMapEditor, {
    mode: "python",
    theme: "dracula",
    lineNumbers: true,
    viewportMargin: Infinity
  });
  
  const originalDescriptor = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, 'value');
  Object.defineProperty(dom.mindMapEditor, 'value', {
    get: function() {
      return cmEditor.getValue();
    },
    set: function(val) {
      if (cmEditor.getValue() !== val) {
        cmEditor.setValue(val);
      }
      originalDescriptor.set.call(this, val);
    }
  });

  cmEditor.on("change", () => {
    scheduleAutoPreview();
  });

  // Tabs Logic
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      document.querySelectorAll('.tab-btn').forEach(b => {
        b.classList.remove('active', 'btn-secondary');
        b.classList.add('btn-ghost');
      });
      e.target.classList.add('active', 'btn-secondary');
      e.target.classList.remove('btn-ghost');
      
      document.querySelectorAll('.tab-content').forEach(tc => tc.style.display = 'none');
      const targetId = e.target.getAttribute('data-tab');
      document.getElementById(targetId).style.display = 'block';
      
      if (targetId === 'tab-code') {
        setTimeout(() => cmEditor.refresh(), 10);
      }
    });
  });

  configFormApi.renderConfigForm();

  dom.pyFileInput.addEventListener("change", async () => {
    const file = dom.pyFileInput.files && dom.pyFileInput.files[0];
    if (!file) return;
    try {
      if (!state.pyReady) {
        setStatus("Inicializando Pyodide para cargar el archivo .py...");
        await runtimeApi.initPy();
      }
      const sourceText = await file.text();
      await runtimeApi.loadFromPythonSourceText(sourceText, file.name);
    } catch (error) {
      setStatus(`Error al cargar el .py: ${error.message}`, "error");
    } finally {
      dom.pyFileInput.value = "";
    }
  });

  dom.btnPreview.addEventListener("click", runtimeApi.generatePreview);
  dom.btnGenerateMap.addEventListener("click", () => {
    window.open(
      "https://gemini.google.com/gem/1RxilJOzqXHsfFv39rSkvbjL4qyM-r-XS?usp=sharing",
      "_blank",
      "noopener,noreferrer"
    );
  });
  dom.btnSaveAs.addEventListener("click", fileActionsApi.saveAs);
  dom.btnPasteMap.addEventListener("click", async () => {
    try {
      let nextMindMap = "";

      if (navigator.clipboard?.readText) {
        try {
          nextMindMap = String(await navigator.clipboard.readText()).trim();
        } catch (_) {
          nextMindMap = "";
        }
      }

      if (!nextMindMap) {
        const pastedManually = window.prompt(
          "Pega aqui el contenido de mapa_ejemplo (dict Python o JSON).",
          dom.mindMapEditor.value
        );
        if (pastedManually === null) {
          setStatus("Pegado cancelado.");
          return;
        }
        nextMindMap = String(pastedManually).trim();
      }

      if (!nextMindMap) {
        setStatus("No se detecto contenido para pegar.", "error");
        return;
      }

      dom.mindMapEditor.value = nextMindMap;
      setStatus("mapa_ejemplo reemplazado. Generando preview...");
      await runtimeApi.generatePreview();
    } catch (error) {
      setStatus(`No se pudo pegar el mapa: ${error.message}`, "error");
    }
  });
  dom.btnClearPreview.addEventListener("click", () => {
    state.lastGeneratedXml = "";
    state.lastOutputPath = "";
    previewApi.clearPreview();
    setStatus("Preview limpiada.");
  });

  dom.btnAdvanced.addEventListener("click", () => openAdvancedModal(dom.advancedModal));
  dom.btnCloseAdvanced.addEventListener("click", () => closeAdvancedModal(dom.advancedModal));
  dom.btnInitPyodide.addEventListener("click", () => runtimeApi.initPy(true));
  dom.btnSaveOutput.addEventListener("click", fileActionsApi.saveWithOutputFile);
  dom.btnPickProjectDir.addEventListener("click", fileActionsApi.pickProjectDir);
  dom.btnApplyConfigText.addEventListener("click", async () => {
    try {
      await runtimeApi.applyConfigFromEditor(true);
    } catch (error) {
      setStatus(`CONFIG no valida: ${error.message}`, "error");
    }
  });
  dom.btnApplyGemini.addEventListener("click", runtimeApi.applyGeminiToMindMap);
  dom.btnGoogleLinksImages?.addEventListener("click", runtimeApi.openGoogleLinksForMap);
  dom.btnBingImages.addEventListener("click", runtimeApi.downloadBingImages);
  dom.btnReviewImages.addEventListener("click", runtimeApi.openImageReviewModal);
  dom.btnReviewImagesGallery.addEventListener("click", runtimeApi.openImageReviewGalleryModal);
  dom.btnCloseImageReview.addEventListener("click", runtimeApi.closeImageReviewModal);
  dom.btnCloseImageReviewGallery.addEventListener("click", runtimeApi.closeImageReviewGalleryModal);
  dom.btnImageReviewUndo.addEventListener("click", runtimeApi.undoImageReviewAction);
  dom.btnImageReviewPrev.addEventListener("click", runtimeApi.imageReviewPrev);
  dom.btnImageReviewNext.addEventListener("click", runtimeApi.imageReviewNext);
  dom.btnImageReviewRefresh.addEventListener("click", runtimeApi.refreshCurrentImageReview);
  dom.btnOpenPendingImages?.addEventListener("click", runtimeApi.openImagePendingModal);
  dom.btnImageReviewDelete.addEventListener("click", runtimeApi.imageReviewDeleteCurrent);
  dom.btnImageReviewCropBottom.addEventListener("click", runtimeApi.imageReviewCropBottom);
  dom.btnImageReviewGalleryRefresh.addEventListener("click", runtimeApi.refreshImageReviewGallery);
  dom.btnImageReviewPaste.addEventListener("click", runtimeApi.imageReviewPasteFromClipboard);
  dom.btnImageReviewReplace.addEventListener("click", runtimeApi.imageReviewReplaceCurrentFromClipboard);
  dom.btnImageReviewSearchReplace.addEventListener("click", runtimeApi.imageReviewSearchReplaceCurrent);
  dom.btnImageReviewSearchReplacePending?.addEventListener("click", runtimeApi.imageReviewSearchReplacePending);
  dom.btnCloseImagePending?.addEventListener("click", runtimeApi.closeImagePendingModal);
  dom.btnSuggestionOpenverse?.addEventListener("click", runtimeApi.loadOpenverseSuggestions);
  dom.btnSuggestionBing?.addEventListener("click", runtimeApi.loadBingSuggestions);
  dom.btnSuggestionDdg?.addEventListener("click", runtimeApi.loadDdgSuggestions);

  dom.advancedModal.addEventListener("click", (event) => {
    if (event.target === dom.advancedModal) closeAdvancedModal(dom.advancedModal);
  });
  dom.imageReviewModal.addEventListener("click", (event) => {
    if (event.target === dom.imageReviewModal) runtimeApi.closeImageReviewModal();
  });
  dom.imagePendingModal?.addEventListener("click", (event) => {
    if (event.target === dom.imagePendingModal) runtimeApi.closeImagePendingModal();
  });
  dom.imageReviewGalleryModal.addEventListener("click", (event) => {
    if (event.target === dom.imageReviewGalleryModal) runtimeApi.closeImageReviewGalleryModal();
  });

  previewApi.bindPreviewEvents();

  window.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !dom.advancedModal.classList.contains("hidden")) {
      closeAdvancedModal(dom.advancedModal);
    }
    if (event.key === "Escape" && dom.imageReviewModal && !dom.imageReviewModal.classList.contains("hidden")) {
      runtimeApi.closeImageReviewModal();
    }
    if (event.key === "Escape" && dom.imagePendingModal && !dom.imagePendingModal.classList.contains("hidden")) {
      runtimeApi.closeImagePendingModal();
    }
    if (
      event.key === "Escape" &&
      dom.imageReviewGalleryModal &&
      !dom.imageReviewGalleryModal.classList.contains("hidden")
    ) {
      runtimeApi.closeImageReviewGalleryModal();
    }
  });

  window.addEventListener("load", () => {
    runtimeApi.initPy();
  });
}


