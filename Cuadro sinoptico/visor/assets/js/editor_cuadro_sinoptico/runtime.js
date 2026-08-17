import { jsToPythonLiteral, normalizeConfig } from "./utils.js";

export function createRuntimeApi({
  dom,
  state,
  constants,
  setStatus,
  configFormApi,
  previewApi
}) {
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
      const scriptResponse = await fetch(`../codigo/Scripts/Cuadros_sinopticos.py${cacheBust}`, {
        cache: "no-store"
      });
      if (!scriptResponse.ok) {
        throw new Error("No se pudo leer ../codigo/Scripts/Cuadros_sinopticos.py. Abre el proyecto desde localhost.");
      }
      const mapScript = await scriptResponse.text();

      state.pyodide.globals.set("MAP_SCRIPT_SOURCE", mapScript);
      state.pyodide.runPython(`
import ast
import traceback
import pathlib
import types
import os

_runtime_module = types.ModuleType("cuadro_sinoptico_runtime")
_runtime_module.__file__ = "codigo/Scripts/Cuadros_sinopticos.py"
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

def parse_map_literals(config_text, chart_text):
    cfg = _parse_python_value(config_text)
    chart = _parse_python_value(chart_text)
    if not isinstance(cfg, dict):
        raise ValueError("CONFIG debe ser un dict.")
    if not isinstance(chart, dict):
        raise ValueError("chart debe ser un dict.")
    return {"config": _to_plain(cfg), "chart": _to_plain(chart)}

def generate_drawio_xml(config_text, chart_text):
    try:
        cfg = _parse_python_value(config_text)
        chart = _parse_python_value(chart_text)
        out_path = _runtime_module.generar_cuadro_sinoptico(chart, cfg)
        with open(out_path, "r", encoding="utf-8") as fh:
            xml = fh.read()
        return {"ok": True, "xml": xml, "out_path": out_path}
    except Exception as exc:
        return {"ok": False, "error": str(exc), "traceback": traceback.format_exc()}

def load_from_python_source(source_code, source_path="cuadro_sinoptico.py"):
    ns = {
        "__name__": "cuadro_sinoptico_ui_loader",
        "__file__": source_path or "cuadro_sinoptico.py",
    }
    exec(source_code, ns, ns)
    if "CONFIG" not in ns:
        raise ValueError("No se encontro CONFIG en el archivo Python.")
    if "chart" not in ns:
        raise ValueError("No se encontro chart en el archivo Python.")
    return {
        "config": _to_plain(ns["CONFIG"]),
        "chart": _to_plain(ns["chart"]),
    }
`);

      state.pyReady = true;
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
      const response = await fetch("../codigo/vista/cuadro_sinoptico.py");
      if (!response.ok) {
        return;
      }
      const source = await response.text();
      await loadFromPythonSourceText(source, "codigo/vista/cuadro_sinoptico.py");
      setStatus("Motor Python listo y archivo base cargado automaticamente.", "ok");
    } catch (_) {
      setStatus("Motor Python listo. No se cargo automaticamente el archivo base.");
    }
  }

  async function loadFromPythonSourceText(sourceText, sourceLabel = "archivo .py") {
    if (!state.pyReady) throw new Error("Primero inicializa el motor Python.");
    state.pyodide.globals.set("SOURCE_CODE_TO_LOAD", sourceText);
    const sourcePath = String(sourceLabel || "cuadro_sinoptico.py").replaceAll("\\", "/");
    state.pyodide.globals.set("SOURCE_PATH_TO_LOAD", sourcePath);
    const resultProxy = state.pyodide.runPython("load_from_python_source(SOURCE_CODE_TO_LOAD, SOURCE_PATH_TO_LOAD)");
    const result = resultProxy.toJs({ dict_converter: Object.fromEntries });
    resultProxy.destroy();

    state.currentConfig = normalizeConfig(constants.DEFAULT_CONFIG, result.config);
    configFormApi.renderConfigForm();
    configFormApi.updateConfigTextFromState();
    dom.conceptEditor.value = jsToPythonLiteral(result.chart);
    setStatus(`Se cargo CONFIG y chart desde ${sourceLabel}.`, "ok");
  }

  async function applyGeminiToConceptMap() {
    setStatus("Asistente IA no habilitado para cuadro sinoptico en esta version.", "error");
  }

  async function generatePreview(options = {}) {
    const silent = Boolean(options?.silent);
    const preserveViewport = Boolean(options?.preserveViewport);
    if (!state.pyReady) {
      setStatus("Motor Python aun no esta listo. Espera unos segundos.", "error");
      return;
    }
    try {
      await applyConfigFromEditor(false);
      if (!silent) {
        setStatus("Generando preview...");
      }
      state.pyodide.globals.set("CONFIG_TEXT_INPUT", jsToPythonLiteral(state.currentConfig));
      state.pyodide.globals.set("CHART_TEXT_INPUT", dom.conceptEditor.value);
      const resultProxy = state.pyodide.runPython("generate_drawio_xml(CONFIG_TEXT_INPUT, CHART_TEXT_INPUT)");
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
    applyGeminiToConceptMap,
    generatePreview
  };
}
