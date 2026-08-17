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
    FONT_FAMILY: "Times New Roman",
    FONT_SIZE: 12,
    FONT_COLOR: "#000000",
    FONT_BOLD: false,
    FONT_ITALIC: false,
    STROKE_W: 2,
    EDGE_COLOR: "#60a5fa",
    BOX_ARC_SIZE: 0,
    BOX_SHADOW: false,
    MAIN_FILL_COLOR: "#a7a6e9",
    MAIN_STROKE_COLOR: "#60a5fa",
    SUBTITLE_FILL_COLOR: "#8AAEE0",
    SUBTITLE_STROKE_COLOR: "#94a3b8",
    CONNECTOR_FONT_FAMILY: "Courier New",
    CONNECTOR_FONT_SIZE: 9,
    CONNECTOR_FONT_COLOR: "#e2e8f0",
    CONNECTOR_BG_COLOR: "#0f172a",
    CONNECTOR_BORDER_COLOR: "#475569",
    CONNECTOR_SHADOW: false,
    CONNECTOR_TEXT_SHADOW: true,
    BOX_W: 100,
    BOX_H: 45,
    X_STEP: 150,
    Y_STEP: 90,
    POSITION_NOISE: 15,
    MAIN_TO_SUBTITLE: 130,
    SUBTITLE_TO_BRANCH: 150,
    SUBTITLE_GAP: 80,
    GROUP_GAP: 800,
    COLOR_SUBTITLE_GROUPS: false,
    COLOR_NESTED_SUBTOPICS: false,
    NORMALIZAR_TUPLAS: false,
    PALABRAS_POR_POSICION: 2,
    NORMALIZAR_TUPLAS_EXTENSAS: true,
    PALETTE: [
      ["#60a5fa", "#1e3a8a"],
      ["#a3e635", "#4d7c0f"],
      ["#fca5a5", "#7f1d1d"],
      ["#f0abfc", "#86198f"]
    ],
    START_X: 120,
    START_Y: 40,
    OUTPUT_FILE: "salidas/Mapa_conceptual.drawio"
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
  fallbackConceptMap: `[
  {
    "titulo_principal": "Tema principal",
    "subtitulos": [
      {
        "titulo": "Subtitulo de ejemplo",
        "conector": "se divide en",
        "ramas": [
          [
            [None, "incluye"],
            ["Concepto A", "con"],
            ["Detalle", None]
          ],
          [
            [None, "tambien"],
            ["Concepto B", "aporta"],
            ["Resultado", None]
          ]
        ]
      }
    ]
  }
]`,
  CONFIG_SECTIONS: [
    {
      title: "Tipografia",
      fields: [
        { key: "FONT_FAMILY", label: "Fuente cajas", type: "select", options: "FONT_OPTIONS" },
        { key: "FONT_SIZE", label: "Tamano fuente", type: "number", step: "1" },
        { key: "FONT_COLOR", label: "Color fuente", type: "color" },
        { key: "FONT_BOLD", label: "Negrita", type: "boolean" },
        { key: "FONT_ITALIC", label: "Cursiva", type: "boolean" },
        { key: "CONNECTOR_FONT_FAMILY", label: "Fuente conectores", type: "select", options: "FONT_OPTIONS" },
        { key: "CONNECTOR_FONT_SIZE", label: "Tamano conectores", type: "number", step: "1" },
        { key: "CONNECTOR_FONT_COLOR", label: "Color texto conectores", type: "color" }
      ]
    },
    {
      title: "Colores",
      fields: [
        { key: "EDGE_COLOR", label: "Color de conectores", type: "color" },
        { key: "MAIN_FILL_COLOR", label: "Relleno titulo principal", type: "color" },
        { key: "MAIN_STROKE_COLOR", label: "Borde titulo principal", type: "color" },
        { key: "SUBTITLE_FILL_COLOR", label: "Relleno subtitulos", type: "color" },
        { key: "SUBTITLE_STROKE_COLOR", label: "Borde subtitulos", type: "color" },
        { key: "CONNECTOR_BG_COLOR", label: "Fondo conectores", type: "color" },
        { key: "CONNECTOR_BORDER_COLOR", label: "Borde conectores", type: "color" }
      ]
    },
    {
      title: "Bordes y estilo",
      fields: [
        { key: "STROKE_W", label: "Grosor borde", type: "number", step: "0.1" },
        { key: "BOX_ARC_SIZE", label: "Radio esquinas", type: "number", step: "1" },
        { key: "BOX_SHADOW", label: "Sombra cajas", type: "boolean" },
        { key: "CONNECTOR_SHADOW", label: "Sombra conectores", type: "boolean" },
        { key: "CONNECTOR_TEXT_SHADOW", label: "Sombra texto conectores", type: "boolean" }
      ]
    },
    {
      title: "Tamano y separaciones",
      fields: [
        { key: "BOX_W", label: "Ancho caja", type: "number", step: "1" },
        { key: "BOX_H", label: "Alto caja", type: "number", step: "1" },
        { key: "X_STEP", label: "Paso horizontal", type: "number", step: "1" },
        { key: "Y_STEP", label: "Paso vertical", type: "number", step: "1" },
        { key: "POSITION_NOISE", label: "Ruido posicion", type: "number", step: "1" },
        { key: "MAIN_TO_SUBTITLE", label: "Titulo a subtitulo", type: "number", step: "1" },
        { key: "SUBTITLE_TO_BRANCH", label: "Subtitulo a rama", type: "number", step: "1" },
        { key: "SUBTITLE_GAP", label: "Separacion subtitulos", type: "number", step: "1" },
        { key: "GROUP_GAP", label: "Separacion grupos", type: "number", step: "1" },
        { key: "START_X", label: "Inicio X", type: "number", step: "1" },
        { key: "START_Y", label: "Inicio Y", type: "number", step: "1" }
      ]
    },
    {
      title: "Comportamiento",
      fields: [
        { key: "COLOR_SUBTITLE_GROUPS", label: "Color por subtitulo", type: "boolean" },
        { key: "COLOR_NESTED_SUBTOPICS", label: "Color subtemas anidados", type: "boolean" },
        { key: "NORMALIZAR_TUPLAS", label: "Normalizar tuplas", type: "boolean" },
        { key: "PALABRAS_POR_POSICION", label: "Palabras por posicion", type: "number", step: "1" },
        { key: "NORMALIZAR_TUPLAS_EXTENSAS", label: "Normalizar tuplas extensas", type: "boolean" },
        { key: "OUTPUT_FILE", label: "Archivo de salida", type: "text" }
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
