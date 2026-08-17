export function deepClone(value) {
  return JSON.parse(JSON.stringify(value));
}

export function isHexColor(value) {
  return typeof value === "string" && /^#([0-9a-fA-F]{6})$/.test(value.trim());
}

export function isColorDisabledValue(value) {
  if (value === null || value === undefined) return true;
  return typeof value === "string" && value.trim().toLowerCase() === "none";
}

export function safeColor(value, fallback = "#000000") {
  return isHexColor(value) ? value.trim() : fallback;
}

export function normalizeConfig(defaultConfig, config) {
  const merged = { ...deepClone(defaultConfig), ...(config || {}) };
  const defaultPalette = deepClone(defaultConfig.PALETTE);
  const srcPalette = Array.isArray(merged.PALETTE) ? merged.PALETTE : defaultPalette;
  const normalizedPalette = srcPalette.map((pair, idx) => {
    const fallbackPair = defaultPalette[idx] || ["#000000", "#000000"];
    if (!Array.isArray(pair)) return fallbackPair;
    const fill = typeof pair[0] === "string" ? pair[0] : fallbackPair[0];
    const stroke = typeof pair[1] === "string" ? pair[1] : fallbackPair[1];
    return [fill, stroke];
  });
  merged.PALETTE = normalizedPalette.length ? normalizedPalette : defaultPalette;
  return merged;
}

export function jsToPythonLiteral(value) {
  if (value === undefined || value === null) return "None";
  if (typeof value === "boolean") return value ? "True" : "False";
  if (typeof value === "number") {
    if (!Number.isFinite(value)) throw new Error("Numero no valido en CONFIG.");
    return String(value);
  }
  if (typeof value === "string") return JSON.stringify(value);
  if (value instanceof Map) {
    const entries = Array.from(value.entries()).map(([k, v]) => `${JSON.stringify(String(k))}: ${jsToPythonLiteral(v)}`);
    return `{${entries.join(", ")}}`;
  }
  if (Array.isArray(value)) {
    return `[${value.map((item) => jsToPythonLiteral(item)).join(", ")}]`;
  }
  if (typeof value === "object") {
    const entries = Object.entries(value).map(([k, v]) => `${JSON.stringify(k)}: ${jsToPythonLiteral(v)}`);
    return `{${entries.join(", ")}}`;
  }
  throw new Error("Tipo no soportado al convertir a literal Python.");
}

export function clamp(value, min, max) {
  return Math.min(Math.max(value, min), max);
}
