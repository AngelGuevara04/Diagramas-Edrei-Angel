export function createFileActionsApi({
  state,
  setStatus,
  runtimeApi
}) {
  function splitRelativePath(pathText) {
    const normalized = String(pathText || "").replaceAll("\\\\", "/").replaceAll("\\", "/").trim();
    if (!normalized) return [];
    if (/^[a-zA-Z]:\//.test(normalized) || normalized.startsWith("/")) {
      throw new Error("OUTPUT_FILE absoluto no se puede guardar directo desde navegador. Usa 'Guardar como...'.");
    }
    const parts = normalized.split("/").filter(Boolean);
    if (parts.some((p) => p === "." || p === "..")) {
      throw new Error("OUTPUT_FILE contiene rutas no permitidas ('.' o '..').");
    }
    return parts;
  }

  async function ensurePreview() {
    if (!state.lastGeneratedXml) {
      await runtimeApi.generatePreview();
    }
    if (!state.lastGeneratedXml) {
      throw new Error("No hay XML generado para guardar.");
    }
  }

  async function saveWithOutputFile() {
    try {
      if (!state.projectDirHandle) {
        throw new Error("Primero elige la carpeta proyecto.");
      }
      await runtimeApi.applyConfigFromEditor(false);
      await ensurePreview();
      const outputFile = state.currentConfig.OUTPUT_FILE || "salidas/Mapa_conceptual.drawio";
      const parts = splitRelativePath(outputFile);
      if (!parts.length) {
        throw new Error("OUTPUT_FILE vacio.");
      }
      const fileName = parts[parts.length - 1];
      let currentDir = state.projectDirHandle;
      for (let i = 0; i < parts.length - 1; i += 1) {
        currentDir = await currentDir.getDirectoryHandle(parts[i], { create: true });
      }
      const fileHandle = await currentDir.getFileHandle(fileName, { create: true });
      const writable = await fileHandle.createWritable();
      await writable.write(state.lastGeneratedXml);
      await writable.close();
      setStatus(`Archivo guardado en ${outputFile}`, "ok");
    } catch (error) {
      setStatus(`No se pudo guardar segun OUTPUT_FILE: ${error.message}`, "error");
    }
  }

  async function saveAs() {
    try {
      await runtimeApi.applyConfigFromEditor(false);
      await ensurePreview();
      let suggestedName = "Mapa_conceptual.drawio";
      try {
        const outputFile = String(state.currentConfig.OUTPUT_FILE || "");
        const parts = outputFile.replaceAll("\\\\", "/").replaceAll("\\", "/").split("/").filter(Boolean);
        if (parts.length) suggestedName = parts[parts.length - 1];
      } catch (_) {
        // ignora nombre no valido
      }

      if (window.showSaveFilePicker) {
        const handle = await window.showSaveFilePicker({
          suggestedName,
          types: [
            {
              description: "Draw.io",
              accept: { "application/xml": [".drawio", ".xml"] }
            }
          ]
        });
        const writable = await handle.createWritable();
        await writable.write(state.lastGeneratedXml);
        await writable.close();
        setStatus("Archivo guardado correctamente (Guardar como).", "ok");
      } else {
        const blob = new Blob([state.lastGeneratedXml], { type: "application/xml;charset=utf-8" });
        const a = document.createElement("a");
        a.href = URL.createObjectURL(blob);
        a.download = suggestedName;
        document.body.appendChild(a);
        a.click();
        a.remove();
        URL.revokeObjectURL(a.href);
        setStatus("El navegador no soporta showSaveFilePicker. Se descargo el archivo.", "ok");
      }
    } catch (error) {
      setStatus(`No se pudo guardar: ${error.message}`, "error");
    }
  }

  async function pickProjectDir() {
    if (!window.showDirectoryPicker) {
      setStatus("Tu navegador no soporta File System Access API. Usa Chrome/Edge recientes.", "error");
      return;
    }
    try {
      state.projectDirHandle = await window.showDirectoryPicker();
      setStatus("Carpeta proyecto seleccionada. Ya puedes usar 'Guardar segun OUTPUT_FILE'.", "ok");
    } catch (error) {
      setStatus(`No se selecciono carpeta: ${error.message}`);
    }
  }

  return {
    saveWithOutputFile,
    saveAs,
    pickProjectDir
  };
}
