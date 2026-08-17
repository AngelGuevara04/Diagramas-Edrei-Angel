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

  const normalizePaletteEntry = (entry, fallbackEntry) => {
    if (entry && typeof entry === "object" && !Array.isArray(entry)) {
      const normalized = {};
      Object.entries(entry).forEach(([key, value]) => {
        if (value === undefined || value === null) return;
        normalized[String(key)] = typeof value === "string" ? value : String(value);
      });
      return Object.keys(normalized).length ? normalized : deepClone(fallbackEntry);
    }

    if (Array.isArray(entry)) {
      return entry.map((value) => {
        if (value === undefined || value === null) return null;
        return typeof value === "string" ? value : String(value);
      });
    }

    return deepClone(fallbackEntry);
  };

  const normalizedPalette = srcPalette.map((entry, idx) => {
    const fallbackEntry = defaultPalette[idx] || defaultPalette[defaultPalette.length - 1] || [];
    return normalizePaletteEntry(entry, fallbackEntry);
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
