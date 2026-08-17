export const dom = {
  configForm: document.getElementById("configForm"),
  configEditor: document.getElementById("configEditor"),
  mindMapEditor: document.getElementById("mindMapEditor"),
  statusBox: document.getElementById("statusBox"),
  graphContainer: document.getElementById("graph-container"),
  previewMeta: document.getElementById("previewMeta"),
  btnPreview: document.getElementById("btnPreview"),
  btnGenerateMap: document.getElementById("btnGenerateMap"),
  btnSaveAs: document.getElementById("btnSaveAs"),
  btnAdvanced: document.getElementById("btnAdvanced"),
  btnPasteMap: document.getElementById("btnPasteMap"),
  btnClearPreview: document.getElementById("btnClearPreview"),
  btnCloseAdvanced: document.getElementById("btnCloseAdvanced"),
  btnInitPyodide: document.getElementById("btnInitPyodide"),
  btnSaveOutput: document.getElementById("btnSaveOutput"),
  btnPickProjectDir: document.getElementById("btnPickProjectDir"),
  btnApplyConfigText: document.getElementById("btnApplyConfigText"),
  btnApplyGemini: document.getElementById("btnApplyGemini"),
  btnBingImages: document.getElementById("btnBingImages"),
  btnGoogleLinksImages: document.getElementById("btnGoogleLinksImages"),
  btnReviewImages: document.getElementById("btnReviewImages"),
  btnReviewImagesGallery: document.getElementById("btnReviewImagesGallery"),
  pyFileInput: document.getElementById("pyFileInput"),
  advancedModal: document.getElementById("advancedModal"),
  imageReviewModal: document.getElementById("imageReviewModal"),
  imagePendingModal: document.getElementById("imagePendingModal"),
  imageReviewGalleryModal: document.getElementById("imageReviewGalleryModal"),
  btnCloseImageReview: document.getElementById("btnCloseImageReview"),
  btnCloseImagePending: document.getElementById("btnCloseImagePending"),
  btnCloseImageReviewGallery: document.getElementById("btnCloseImageReviewGallery"),
  btnImageReviewUndo: document.getElementById("btnImageReviewUndo"),
  btnImageReviewPrev: document.getElementById("btnImageReviewPrev"),
  btnImageReviewNext: document.getElementById("btnImageReviewNext"),
  btnImageReviewRefresh: document.getElementById("btnImageReviewRefresh"),
  btnOpenPendingImages: document.getElementById("btnOpenPendingImages"),
  btnImageReviewDelete: document.getElementById("btnImageReviewDelete"),
  btnImageReviewCropBottom: document.getElementById("btnImageReviewCropBottom"),
  btnImageReviewGalleryRefresh: document.getElementById("btnImageReviewGalleryRefresh"),
  btnImageReviewPaste: document.getElementById("btnImageReviewPaste"),
  btnImageReviewReplace: document.getElementById("btnImageReviewReplace"),
  btnImageReviewSearchReplace: document.getElementById("btnImageReviewSearchReplace"),
  btnImageReviewSearchReplacePending: document.getElementById("btnImageReviewSearchReplacePending"),
  btnSuggestionOpenverse: document.getElementById("btnSuggestionOpenverse"),
  btnSuggestionBing: document.getElementById("btnSuggestionBing"),
  btnSuggestionDdg: document.getElementById("btnSuggestionDdg"),
  imageReviewCounter: document.getElementById("imageReviewCounter"),
  imageReviewFilename: document.getElementById("imageReviewFilename"),
  imageReviewCanvas: document.getElementById("imageReviewCanvas"),
  imagePendingCanvas: document.getElementById("imagePendingCanvas"),
  imageReviewHint: document.getElementById("imageReviewHint"),
  imageReviewPendingSuffix: document.getElementById("imageReviewPendingSuffix"),
  imageReviewPendingMeta: document.getElementById("imageReviewPendingMeta"),
  imageReviewPendingList: document.getElementById("imageReviewPendingList"),
  imageSuggestionMeta: document.getElementById("imageSuggestionMeta"),
  imageSuggestionGrid: document.getElementById("imageSuggestionGrid"),
  imageReviewGalleryList: document.getElementById("imageReviewGalleryList"),
  imageSyncModal: document.getElementById("imageSyncModal"),
  imageSyncText: document.getElementById("imageSyncText"),
  imageSyncProgressBar: document.getElementById("imageSyncProgressBar"),
  imageSyncMeta: document.getElementById("imageSyncMeta"),
  bingSearchModal: document.getElementById("bingSearchModal"),
  bingSearchTitle: document.getElementById("bingSearchTitle"),
  bingSearchText: document.getElementById("bingSearchText"),
  bingSearchProgressBar: document.getElementById("bingSearchProgressBar"),
  bingSearchMeta: document.getElementById("bingSearchMeta"),
  btnStopBingSearch: document.getElementById("btnStopBingSearch"),
  geminiPrompt: document.getElementById("geminiPrompt"),
  geminiModel: document.getElementById("geminiModel"),
  imageProvider: document.getElementById("imageProvider"),
  bingSuffix: document.getElementById("bingSuffix"),
  bingMaxLabels: document.getElementById("bingMaxLabels")
};

export const constants = {
  GRAPH_ZOOM_MIN: 0.25,
  GRAPH_ZOOM_MAX: 6,
  DEFAULT_CONFIG: {
    CENTER_X: 800,
    CENTER_Y: 600,
    R_STEP: 360,
    R_STEP_BOOST: {
      levels: 5,
      factor: 1.05
    },
    CURVED_EDGES: false,
    EDGE_CONNECTOR_STYLE: "curved_block",
    IMAGE_DIR: "ImagenesMapaMental",
    IMAGE_WIDTH: 100,
    IMAGE_HEIGHT: null,
    IMAGE_WIDTH_NOISE: 0,
    IMAGE_TEXT_PADDING: 24,
    IMAGE_EDGE_PADDING: 12,
    IMAGE_RADIUS_OFFSET: 0,
    TEXT_FONT_SIZE: 14,
    TEXT_FONT_FAMILY: "Lucida Console",
    TEXT_FONT_COLOR: "#000000",
    TEXT_FONT_BORDER_COLOR: "none",
    TEXT_BG_COLOR: "#FFFFFF",
    TEXT_STROKE_COLOR: "none",
    TEXT_STROKE_WIDTH: 1,
    TEXT_FILL_COLOR: "none",
    TEXT_BOLD: false,
    TEXT_ITALIC: true,
    TEXT_UNDERLINE: false,
    TEXT_WRAP: false,
    TEXT_ROUNDED: true,
    TEXT_ARC_SIZE: 10,
    NODE_WIDTH: 120,
    NODE_HEIGHT: 60,
    POSITION_NOISE: 10,
    EDGE_STROKE_WIDTH: 2,
    EDGE_COLOR: "#2E21A7",
    EDGE_CURVE_FACTOR: 0.09,
    EDGE_LEFT_ARROW: "classic",
    EDGE_RIGHT_ARROW: "block",
    RANDOM_SEED: 42,
    PALETTE: [
      { fill: "#fff3c4", edge: "#d97706", text: "#111827", outline: "#b45309" },
      { fill: "#d8ffe5", edge: "#15803d", text: "#0f5132", outline: "#0f5132" },
      { fill: "#e0eeff", edge: "#1d4ed8", text: "#0f172a", outline: "#1d4ed8" },
      { fill: "#ffe4e6", edge: "#be185d", text: "#831843", outline: "#be185d" }
    ],
    USE_PALETTE: true,
    OUTPUT_FILE: "Mapas/mapa_mental.drawio"
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
  CONNECTOR_STYLE_OPTIONS: [
    { value: "default", label: "default" },
    { value: "curved_block", label: "curved_block" }
  ],
  ARROW_OPTIONS: [
    { value: "none", label: "none" },
    { value: "block", label: "block" },
    { value: "classic", label: "classic" },
    { value: "open", label: "open" },
    { value: "oval", label: "oval" }
  ],
  fallbackMindMap: `{
  "Tema principal": {
    "Rama 1": {
      "Subtema 1.1": {},
      "Subtema 1.2": {}
    },
    "Rama 2": {
      "Subtema 2.1": {
        "Detalle": {}
      }
    }
  }
}`,
  CONFIG_SECTIONS: [
    {
      title: "Estructura radial",
      fields: [
        { key: "CENTER_X", label: "Centro X", type: "number", step: "1" },
        { key: "CENTER_Y", label: "Centro Y", type: "number", step: "1" },
        { key: "R_STEP", label: "Paso radial", type: "number", step: "1" },
        { key: "R_STEP_BOOST.levels", label: "Boost niveles", type: "number", step: "1" },
        { key: "R_STEP_BOOST.factor", label: "Boost factor", type: "number", step: "0.01" },
        { key: "POSITION_NOISE", label: "Ruido posicion", type: "number", step: "1" },
        { key: "RANDOM_SEED", label: "Semilla aleatoria", type: "number", step: "1" }
      ]
    },
    {
      title: "Aristas",
      fields: [
        { key: "EDGE_CONNECTOR_STYLE", label: "Estilo de conexion", type: "select", options: "CONNECTOR_STYLE_OPTIONS" },
        { key: "CURVED_EDGES", label: "Curvas basicas", type: "boolean" },
        { key: "EDGE_CURVE_FACTOR", label: "Factor de curva", type: "number", step: "0.01" },
        { key: "EDGE_STROKE_WIDTH", label: "Grosor de arista", type: "number", step: "0.1" },
        { key: "EDGE_COLOR", label: "Color de arista", type: "color" },
        { key: "EDGE_LEFT_ARROW", label: "Flecha izquierda", type: "select", options: "ARROW_OPTIONS" },
        { key: "EDGE_RIGHT_ARROW", label: "Flecha derecha", type: "select", options: "ARROW_OPTIONS" }
      ]
    },
    {
      title: "Texto y nodos",
      fields: [
        { key: "NODE_WIDTH", label: "Ancho de nodo", type: "number", step: "1" },
        { key: "NODE_HEIGHT", label: "Alto de nodo", type: "number", step: "1" },
        { key: "TEXT_FONT_FAMILY", label: "Fuente de texto", type: "select", options: "FONT_OPTIONS" },
        { key: "TEXT_FONT_SIZE", label: "Tamano fuente", type: "number", step: "1" },
        { key: "TEXT_FONT_COLOR", label: "Color de texto", type: "color" },
        { key: "TEXT_BG_COLOR", label: "Fondo del texto", type: "color" },
        { key: "TEXT_STROKE_COLOR", label: "Color contorno", type: "color" },
        { key: "TEXT_STROKE_WIDTH", label: "Grosor contorno", type: "number", step: "0.1" },
        { key: "TEXT_FILL_COLOR", label: "Relleno cuadro", type: "color" },
        { key: "TEXT_FONT_BORDER_COLOR", label: "Borde de fuente", type: "color" },
        { key: "TEXT_BOLD", label: "Negrita", type: "boolean" },
        { key: "TEXT_ITALIC", label: "Cursiva", type: "boolean" },
        { key: "TEXT_UNDERLINE", label: "Subrayado", type: "boolean" },
        { key: "TEXT_WRAP", label: "Ajustar texto", type: "boolean" },
        { key: "TEXT_ROUNDED", label: "Esquinas redondeadas", type: "boolean" },
        { key: "TEXT_ARC_SIZE", label: "Tamano redondeado", type: "number", step: "1" }
      ]
    },
    {
      title: "Imagenes",
      fields: [
        { key: "IMAGE_DIR", label: "Carpeta imagenes", type: "text" },
        { key: "IMAGE_WIDTH", label: "Ancho imagen", type: "number", step: "1" },
        { key: "IMAGE_HEIGHT", label: "Alto imagen (opcional)", type: "number", step: "1" },
        { key: "IMAGE_WIDTH_NOISE", label: "Ruido ancho imagen", type: "number", step: "0.01" },
        { key: "IMAGE_TEXT_PADDING", label: "Padding texto-imagen", type: "number", step: "1" },
        { key: "IMAGE_EDGE_PADDING", label: "Padding imagen-arista", type: "number", step: "1" },
        { key: "IMAGE_RADIUS_OFFSET", label: "Offset radial imagen", type: "number", step: "1" }
      ]
    },
    {
      title: "Comportamiento",
      fields: [
        { key: "USE_PALETTE", label: "Usar paleta por ramas", type: "boolean" },
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
