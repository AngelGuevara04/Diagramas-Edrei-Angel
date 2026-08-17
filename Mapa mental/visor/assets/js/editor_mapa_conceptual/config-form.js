import { isColorDisabledValue, jsToPythonLiteral, safeColor } from "./utils.js";

export function createConfigFormApi({
  dom,
  state,
  constants,
  setStatus,
  onConfigChanged = () => {}
}) {
  function getValueByPath(source, keyPath, fallback = undefined) {
    const parts = String(keyPath || "").split(".").filter(Boolean);
    if (!parts.length) return source ?? fallback;
    let cursor = source;
    for (const part of parts) {
      if (!cursor || typeof cursor !== "object" || !(part in cursor)) {
        return fallback;
      }
      cursor = cursor[part];
    }
    return cursor === undefined ? fallback : cursor;
  }

  function setValueByPath(target, keyPath, value) {
    const parts = String(keyPath || "").split(".").filter(Boolean);
    if (!parts.length) return;
    let cursor = target;
    for (let i = 0; i < parts.length - 1; i += 1) {
      const part = parts[i];
      if (!cursor[part] || typeof cursor[part] !== "object" || Array.isArray(cursor[part])) {
        cursor[part] = {};
      }
      cursor = cursor[part];
    }
    cursor[parts[parts.length - 1]] = value;
  }

  function updateConfigTextFromState() {
    if (state.isRenderingForm) return;
    dom.configEditor.value = jsToPythonLiteral(state.currentConfig);
  }

  function onFormValueChange(key, rawValue, type) {
    if (type === "number") {
      const text = String(rawValue ?? "").trim();
      // Evita aplicar mientras el usuario limpia/escribe un numero incompleto.
      if (!text || text === "-" || text === "." || text === "-.") return;
      const n = Number(text);
      if (!Number.isFinite(n)) return;
      setValueByPath(state.currentConfig, key, n);
    } else if (type === "boolean") {
      setValueByPath(state.currentConfig, key, Boolean(rawValue));
    } else {
      setValueByPath(state.currentConfig, key, String(rawValue ?? ""));
    }
    updateConfigTextFromState();
    onConfigChanged();
  }

  function makeField(field) {
    const wrap = document.createElement("div");
    wrap.className = "field";

    if (field.type === "boolean") {
      const box = document.createElement("div");
      box.className = "checkbox-field";
      const input = document.createElement("input");
      input.type = "checkbox";
      input.checked = Boolean(getValueByPath(state.currentConfig, field.key));
      input.id = `cfg_${field.key}`;
      input.addEventListener("change", () => onFormValueChange(field.key, input.checked, "boolean"));
      const label = document.createElement("label");
      label.setAttribute("for", input.id);
      label.textContent = field.label;
      box.appendChild(input);
      box.appendChild(label);
      wrap.appendChild(box);
      return wrap;
    }

    const label = document.createElement("label");
    label.textContent = field.label;
    label.setAttribute("for", `cfg_${field.key}`);
    wrap.appendChild(label);

    if (field.type === "color") {
      const line = document.createElement("div");
      line.className = "color-line";

      const currentValue = getValueByPath(state.currentConfig, field.key);
      const disabledByValue = isColorDisabledValue(currentValue);
      const defaultColor = safeColor(getValueByPath(constants.DEFAULT_CONFIG, field.key), "#000000");
      const initialColor = safeColor(
        disabledByValue ? defaultColor : currentValue,
        defaultColor
      );

      const colorInput = document.createElement("input");
      colorInput.type = "color";
      colorInput.id = `cfg_${field.key}`;
      colorInput.value = initialColor;

      const toggleWrap = document.createElement("label");
      toggleWrap.className = "color-toggle";

      const toggleInput = document.createElement("input");
      toggleInput.type = "checkbox";
      toggleInput.checked = !disabledByValue;
      toggleInput.id = `cfg_toggle_${field.key}`;

      const toggleText = document.createElement("span");
      toggleText.textContent = "";

      let lastColor = initialColor;

      const applyColorToggle = () => {
        const enabled = toggleInput.checked;
        colorInput.disabled = !enabled;
        if (enabled) {
          const activeColor = safeColor(lastColor, defaultColor);
          colorInput.value = activeColor;
          setValueByPath(state.currentConfig, field.key, activeColor);
        } else {
          lastColor = colorInput.value;
          setValueByPath(state.currentConfig, field.key, "none");
        }
        updateConfigTextFromState();
        onConfigChanged();
      };

      colorInput.addEventListener("input", () => {
        lastColor = colorInput.value;
        if (toggleInput.checked) {
          onFormValueChange(field.key, colorInput.value, "text");
        }
      });
      toggleInput.addEventListener("change", applyColorToggle);

      colorInput.disabled = !toggleInput.checked;
      if (!toggleInput.checked) {
        setValueByPath(state.currentConfig, field.key, "none");
      }

      toggleWrap.appendChild(toggleInput);
      toggleWrap.appendChild(toggleText);

      line.appendChild(colorInput);
      line.appendChild(toggleWrap);
      wrap.appendChild(line);
      return wrap;
    }

    if (field.type === "select") {
      const select = document.createElement("select");
      select.id = `cfg_${field.key}`;
      const currentValue = String(getValueByPath(state.currentConfig, field.key) ?? "");
      const optionsRef = typeof field.options === "string" ? constants[field.options] : field.options;
      const normalizedOptions = Array.isArray(optionsRef) ? optionsRef : [];
      const optionValues = new Set();

      normalizedOptions.forEach((entry) => {
        const value = String(entry?.value ?? entry ?? "");
        const labelText = String(entry?.label ?? value);
        if (!value) return;
        optionValues.add(value);
        const option = document.createElement("option");
        option.value = value;
        option.textContent = labelText;
        option.style.fontFamily = value;
        select.appendChild(option);
      });

      if (currentValue && !optionValues.has(currentValue)) {
        const customOption = document.createElement("option");
        customOption.value = currentValue;
        customOption.textContent = `Actual: ${currentValue}`;
        customOption.style.fontFamily = currentValue;
        select.insertBefore(customOption, select.firstChild);
      }

      select.value = currentValue;
      select.style.fontFamily = currentValue || "";
      select.addEventListener("change", () => {
        onFormValueChange(field.key, select.value, "text");
        select.style.fontFamily = select.value || "";
      });
      wrap.appendChild(select);
      return wrap;
    }

    const input = document.createElement("input");
    input.id = `cfg_${field.key}`;
    input.type = field.type;
    if (field.type === "number") {
      input.step = field.step || "1";
      input.value = String(getValueByPath(state.currentConfig, field.key) ?? "");
      input.addEventListener("input", () => onFormValueChange(field.key, input.value, "number"));
    } else {
      input.value = String(getValueByPath(state.currentConfig, field.key) ?? "");
      input.addEventListener("input", () => onFormValueChange(field.key, input.value, "text"));
    }
    wrap.appendChild(input);
    return wrap;
  }

  function makeCollapsibleSection(title, bodyContent, defaultOpen = false) {
    const key = String(title || "Seccion");
    if (!state.sectionVisibility.has(key)) {
      state.sectionVisibility.set(key, defaultOpen);
    }

    const isOpen = Boolean(state.sectionVisibility.get(key));
    const section = document.createElement("div");
    section.className = "config-section";
    if (!isOpen) section.classList.add("collapsed");

    const toggle = document.createElement("button");
    toggle.type = "button";
    toggle.className = "section-toggle";
    toggle.setAttribute("aria-expanded", String(isOpen));

    const titleSpan = document.createElement("span");
    titleSpan.textContent = key;

    const iconSpan = document.createElement("span");
    iconSpan.className = "section-toggle-icon";
    iconSpan.textContent = isOpen ? "v" : ">";

    toggle.appendChild(titleSpan);
    toggle.appendChild(iconSpan);

    const body = document.createElement("div");
    body.className = "config-body";
    body.appendChild(bodyContent);

    toggle.addEventListener("click", () => {
      const currentlyOpen = !section.classList.contains("collapsed");
      const nextOpen = !currentlyOpen;
      state.sectionVisibility.set(key, nextOpen);
      section.classList.toggle("collapsed", !nextOpen);
      toggle.setAttribute("aria-expanded", String(nextOpen));
      iconSpan.textContent = nextOpen ? "v" : ">";
    });

    section.appendChild(toggle);
    section.appendChild(body);
    return section;
  }

  function makePaletteEditor() {
    const sectionTitle = "Paleta de ramas";
    const editor = document.createElement("div");
    editor.className = "palette-editor";

    const ensurePaletteEntry = (entry, fallbackEntry) => {
      if (entry && typeof entry === "object" && !Array.isArray(entry)) {
        return {
          fill: safeColor(entry.fill, safeColor(fallbackEntry.fill, "#000000")),
          edge: safeColor(entry.edge, safeColor(fallbackEntry.edge, "#000000")),
          text: safeColor(entry.text, safeColor(fallbackEntry.text, "#000000")),
          outline: safeColor(entry.outline, safeColor(fallbackEntry.outline, "#000000"))
        };
      }

      if (Array.isArray(entry)) {
        return {
          fill: safeColor(entry[0], safeColor(fallbackEntry.fill, "#000000")),
          edge: safeColor(entry[2] || entry[1], safeColor(fallbackEntry.edge, "#000000")),
          text: safeColor(entry[3], safeColor(fallbackEntry.text, "#000000")),
          outline: safeColor(entry[6] || entry[1], safeColor(fallbackEntry.outline, "#000000"))
        };
      }

      return {
        fill: safeColor(fallbackEntry.fill, "#000000"),
        edge: safeColor(fallbackEntry.edge, "#000000"),
        text: safeColor(fallbackEntry.text, "#000000"),
        outline: safeColor(fallbackEntry.outline, "#000000")
      };
    };

    const getDefaultEntry = () => {
      const fallback = Array.isArray(constants.DEFAULT_CONFIG.PALETTE) && constants.DEFAULT_CONFIG.PALETTE.length
        ? constants.DEFAULT_CONFIG.PALETTE[constants.DEFAULT_CONFIG.PALETTE.length - 1]
        : { fill: "#fff3c4", edge: "#d97706", text: "#111827", outline: "#b45309" };
      return ensurePaletteEntry(fallback, { fill: "#fff3c4", edge: "#d97706", text: "#111827", outline: "#b45309" });
    };

    if (!Array.isArray(state.currentConfig.PALETTE)) {
      state.currentConfig.PALETTE = [getDefaultEntry()];
    }

    const addPaletteEntry = () => {
      const fallback = getDefaultEntry();
      const source = state.currentConfig.PALETTE[state.currentConfig.PALETTE.length - 1];
      const nextEntry = ensurePaletteEntry(source, fallback);
      state.currentConfig.PALETTE.push(nextEntry);
      renderConfigForm();
      updateConfigTextFromState();
      onConfigChanged();
    };

    const removePaletteEntry = (index) => {
      if (!Array.isArray(state.currentConfig.PALETTE) || state.currentConfig.PALETTE.length <= 1) {
        setStatus("La paleta debe tener al menos 1 color.", "error");
        return;
      }
      state.currentConfig.PALETTE.splice(index, 1);
      renderConfigForm();
      updateConfigTextFromState();
      onConfigChanged();
    };

    state.currentConfig.PALETTE = state.currentConfig.PALETTE.map((entry) => ensurePaletteEntry(entry, getDefaultEntry()));

    state.currentConfig.PALETTE.forEach((entry, index) => {
      const row = document.createElement("div");
      row.className = "palette-row";

      const tag = document.createElement("span");
      tag.className = "palette-tag";
      tag.textContent = `Rama ${index + 1}`;

      const fillInput = document.createElement("input");
      fillInput.type = "color";
      fillInput.value = safeColor(entry.fill, "#000000");

      const edgeInput = document.createElement("input");
      edgeInput.type = "color";
      edgeInput.value = safeColor(entry.edge, "#000000");

      const textInput = document.createElement("input");
      textInput.type = "color";
      textInput.value = safeColor(entry.text, "#000000");

      const outlineInput = document.createElement("input");
      outlineInput.type = "color";
      outlineInput.value = safeColor(entry.outline, "#000000");

      const removeBtn = document.createElement("button");
      removeBtn.type = "button";
      removeBtn.className = "btn-ghost palette-btn";
      removeBtn.textContent = "Eliminar";
      removeBtn.disabled = state.currentConfig.PALETTE.length <= 1;
      removeBtn.title = removeBtn.disabled
        ? "La paleta debe tener al menos 1 color."
        : "Eliminar este color";

      fillInput.addEventListener("input", () => {
        state.currentConfig.PALETTE[index].fill = fillInput.value;
        updateConfigTextFromState();
        onConfigChanged();
      });
      edgeInput.addEventListener("input", () => {
        state.currentConfig.PALETTE[index].edge = edgeInput.value;
        updateConfigTextFromState();
        onConfigChanged();
      });
      textInput.addEventListener("input", () => {
        state.currentConfig.PALETTE[index].text = textInput.value;
        updateConfigTextFromState();
        onConfigChanged();
      });
      outlineInput.addEventListener("input", () => {
        state.currentConfig.PALETTE[index].outline = outlineInput.value;
        updateConfigTextFromState();
        onConfigChanged();
      });
      removeBtn.addEventListener("click", () => {
        removePaletteEntry(index);
      });

      row.appendChild(tag);
      row.appendChild(fillInput);
      row.appendChild(edgeInput);
      row.appendChild(textInput);
      row.appendChild(outlineInput);
      row.appendChild(removeBtn);
      editor.appendChild(row);
    });

    const actions = document.createElement("div");
    actions.className = "palette-actions";

    const addBtn = document.createElement("button");
    addBtn.type = "button";
    addBtn.className = "btn-ghost palette-btn";
    addBtn.textContent = "Agregar color";
    addBtn.addEventListener("click", addPaletteEntry);

    actions.appendChild(addBtn);
    editor.appendChild(actions);
    return makeCollapsibleSection(sectionTitle, editor, false);
  }

  function renderConfigForm() {
    state.isRenderingForm = true;
    dom.configForm.innerHTML = "";

    constants.CONFIG_SECTIONS.forEach((sectionDef) => {
      const grid = document.createElement("div");
      grid.className = "config-grid";
      sectionDef.fields.forEach((field) => grid.appendChild(makeField(field)));

      const section = makeCollapsibleSection(
        sectionDef.title,
        grid,
        sectionDef.title === "Estructura radial"
      );
      dom.configForm.appendChild(section);
    });

    dom.configForm.appendChild(makePaletteEditor());
    state.isRenderingForm = false;
  }

  return {
    renderConfigForm,
    updateConfigTextFromState
  };
}
