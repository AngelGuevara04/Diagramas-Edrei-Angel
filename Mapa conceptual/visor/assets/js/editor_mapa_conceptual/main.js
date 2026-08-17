import { createConfigFormApi } from "./config-form.js";
import { createFileActionsApi } from "./file-actions.js";
import { createPreviewApi } from "./preview.js";
import { createRuntimeApi } from "./runtime.js";
import { constants, dom, state } from "./state.js";
import { closeAdvancedModal, openAdvancedModal, setStatus as setStatusBase } from "./ui.js";
import { jsToPythonLiteral, normalizeConfig } from "./utils.js";

let hasBooted = false;

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
    }, 280);
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
  dom.conceptEditor.value = constants.fallbackConceptMap;

  // Initialize CodeMirror and bind it to the live auto-preview
  const cmEditor = window.CodeMirror.fromTextArea(dom.conceptEditor, {
    mode: "python",
    theme: "dracula",
    lineNumbers: true,
    viewportMargin: Infinity
  });
  
  const originalDescriptor = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, 'value');
  Object.defineProperty(dom.conceptEditor, 'value', {
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
      "https://gemini.google.com/gem/1oaIjyTuFvjl6PP-qwCkAadrCzKhTJzDF?usp=sharing",
      "_blank",
      "noopener,noreferrer"
    );
  });
  dom.btnSaveAs.addEventListener("click", fileActionsApi.saveAs);
  if (dom.btnRandomizeStyle) {
    dom.btnRandomizeStyle.addEventListener("click", configFormApi.randomizeStyles);
  }
  dom.btnPasteMap.addEventListener("click", async () => {
    try {
      let nextConceptMap = "";

      if (navigator.clipboard?.readText) {
        try {
          nextConceptMap = String(await navigator.clipboard.readText()).trim();
        } catch (_) {
          nextConceptMap = "";
        }
      }

      if (!nextConceptMap) {
        const pastedManually = window.prompt(
          "Pega aqui el contenido de concept_map (lista Python o JSON).",
          dom.conceptEditor.value
        );
        if (pastedManually === null) {
          setStatus("Pegado cancelado.");
          return;
        }
        nextConceptMap = String(pastedManually).trim();
      }

      if (!nextConceptMap) {
        setStatus("No se detecto contenido para pegar.", "error");
        return;
      }

      dom.conceptEditor.value = nextConceptMap;
      setStatus("concept_map reemplazado. Generando preview...");
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
  dom.btnApplyGemini.addEventListener("click", runtimeApi.applyGeminiToConceptMap);

  dom.advancedModal.addEventListener("click", (event) => {
    if (event.target === dom.advancedModal) closeAdvancedModal(dom.advancedModal);
  });

  previewApi.bindPreviewEvents();

  window.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !dom.advancedModal.classList.contains("hidden")) {
      closeAdvancedModal(dom.advancedModal);
    }
  });

  window.addEventListener("load", () => {
    runtimeApi.initPy();
  });
}
