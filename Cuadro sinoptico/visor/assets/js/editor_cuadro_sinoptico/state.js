export const dom = {
  configForm: document.getElementById("configForm"),
  configEditor: document.getElementById("configEditor"),
  conceptEditor: document.getElementById("conceptEditor"),
  statusBox: document.getElementById("statusBox"),
  graphContainer: document.getElementById("graph-container"),
  previewMeta: document.getElementById("previewMeta"),
  btnPreview: document.getElementById("btnPreview"),
  btnGenerateMap: document.getElementById("btnGenerateMap"),
  btnSaveAs: document.getElementById("btnSaveAs"),
  btnAdvanced: document.getElementById("btnAdvanced"),
  btnRandomizeStyle: document.getElementById("btnRandomizeStyle"),
  btnPasteMap: document.getElementById("btnPasteMap"),
  btnClearPreview: document.getElementById("btnClearPreview"),
  btnCloseAdvanced: document.getElementById("btnCloseAdvanced"),
  btnInitPyodide: document.getElementById("btnInitPyodide"),
  btnSaveOutput: document.getElementById("btnSaveOutput"),
  btnPickProjectDir: document.getElementById("btnPickProjectDir"),
  btnApplyConfigText: document.getElementById("btnApplyConfigText"),
  btnApplyGemini: document.getElementById("btnApplyGemini"),
  pyFileInput: document.getElementById("pyFileInput"),
  advancedModal: document.getElementById("advancedModal"),
  geminiPrompt: document.getElementById("geminiPrompt"),
  geminiModel: document.getElementById("geminiModel")
};

export const constants = {
  GRAPH_ZOOM_MIN: 0.25,
  GRAPH_ZOOM_MAX: 6,
  DEFAULT_CONFIG: {
    archivo_de_salida: "salidas/Cuadro_sinoptico.drawio",
    PX_PER_CHAR: 7.0,
    LINE_H: 17,
    PADDING_V: 20,
    TOP_MARGIN: 40,
    LEFT_MARGIN: 40,
    SIBLING_GAP: 10,
    SPACE_LABEL_TO_BRACE: 5,
    SPACE_BRACE_TO_CONTENT: 5,
    BRACE_W: 14,
    TOP_MIN_LABEL_W: 100,
    MIN_LABEL_W: 10,
    MAX_LABEL_W: 250,
    MAX_ITEM_W: 250,
    BRACE_THICK: 1,
    LABEL_ONLY_MIN_H: 30,
    BRACE_STYLE: "rounded",
    FONT_FAMILY: "Times New Roman",
    FONT_COLOR: "#415D66",
    BRACE_COLOR: "#4A4861"
  },
  FONT_OPTIONS: [
    { value: "Arial", label: "Arial" },
    { value: "Verdana", label: "Verdana" },
    { value: "Tahoma", label: "Tahoma" },
    { value: "Trebuchet MS", label: "Trebuchet MS" },
    { value: "Times New Roman", label: "Times New Roman" },
    { value: "Georgia", label: "Georgia" },
    { value: "Garamond", label: "Garamond" },
    { value: "Palatino Linotype", label: "Palatino Linotype" },
    { value: "Courier New", label: "Courier New" },
    { value: "Lucida Console", label: "Lucida Console" },
    { value: "Consolas", label: "Consolas" },
    { value: "Segoe UI", label: "Segoe UI" },
    { value: "Calibri", label: "Calibri" },
    { value: "Cambria", label: "Cambria" },
    { value: "Impact", label: "Impact" },
    { value: "Comic Sans MS", label: "Comic Sans MS" }
  ],
  fallbackConceptMap: `{
  "Tema general": {
    "Tema 1": ["Idea 1", "Idea 2"],
    "Tema 2": {
      "Subtema A": ["Punto A", "Punto B"],
      "Subtema B": {
        "Detalle 1": ["Explicacion 1"],
        "Detalle 2": []
      }
    }
  }
}`,
  CONFIG_SECTIONS: [
    {
      title: "Texto y estilo",
      fields: [
        { key: "FONT_FAMILY", label: "Fuente", type: "select", options: "FONT_OPTIONS" },
        { key: "FONT_COLOR", label: "Color de texto", type: "color" },
        { key: "BRACE_COLOR", label: "Color de llave", type: "color" },
        { key: "BRACE_STYLE", label: "Estilo de llave", type: "text" },
        { key: "BRACE_THICK", label: "Grosor de llave", type: "number", step: "1" }
      ]
    },
    {
      title: "Tamano base",
      fields: [
        { key: "PX_PER_CHAR", label: "Pixeles por caracter", type: "number", step: "0.1" },
        { key: "LINE_H", label: "Alto de linea", type: "number", step: "1" },
        { key: "PADDING_V", label: "Padding vertical", type: "number", step: "1" },
        { key: "TOP_MARGIN", label: "Margen superior", type: "number", step: "1" },
        { key: "LEFT_MARGIN", label: "Margen izquierdo", type: "number", step: "1" },
        { key: "LABEL_ONLY_MIN_H", label: "Alto minimo sin llave", type: "number", step: "1" }
      ]
    },
    {
      title: "Separaciones",
      fields: [
        { key: "SIBLING_GAP", label: "Separacion entre hermanos", type: "number", step: "1" },
        { key: "SPACE_LABEL_TO_BRACE", label: "Espacio texto-llave", type: "number", step: "1" },
        { key: "SPACE_BRACE_TO_CONTENT", label: "Espacio llave-contenido", type: "number", step: "1" },
        { key: "BRACE_W", label: "Ancho de llave", type: "number", step: "1" }
      ]
    },
    {
      title: "Anchos",
      fields: [
        { key: "TOP_MIN_LABEL_W", label: "Ancho minimo titulo", type: "number", step: "1" },
        { key: "MIN_LABEL_W", label: "Ancho minimo etiqueta", type: "number", step: "1" },
        { key: "MAX_LABEL_W", label: "Ancho maximo etiqueta", type: "number", step: "1" },
        { key: "MAX_ITEM_W", label: "Ancho maximo item", type: "number", step: "1" }
      ]
    },
    {
      title: "Salida",
      fields: [
        { key: "archivo_de_salida", label: "Archivo de salida", type: "text" }
      ]
    }
  ]
};

export const state = {
  pyodide: null,
  pyReady: false,
  lastGeneratedXml: "",
  lastOutputPath: "",
  projectDirHandle: null,
  isRenderingForm: false,
  graphZoom: 1,
  currentConfig: null,
  sectionVisibility: new Map(),
  touchState: {
    mode: "none",
    startX: 0,
    startY: 0,
    startScrollLeft: 0,
    startScrollTop: 0,
    pinchStartDist: 0,
    pinchStartZoom: 1,
    pinchCenterX: 0,
    pinchCenterY: 0
  },
  mousePanState: {
    active: false,
    mode: "none",
    startX: 0,
    startY: 0,
    startScrollLeft: 0,
    startScrollTop: 0
  }
};
