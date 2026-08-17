import { isColorDisabledValue, jsToPythonLiteral, safeColor } from "./utils.js";

export function createConfigFormApi({
  dom,
  state,
  constants,
  setStatus,
  onConfigChanged = () => {}
}) {
  function randomHexColor() {
    const value = Math.floor(Math.random() * 0xffffff);
    return `#${value.toString(16).padStart(6, "0")}`;
  }

  function randomFontFamily() {
    const fontOptions = Array.isArray(constants.FONT_OPTIONS) ? constants.FONT_OPTIONS : [];
    if (!fontOptions.length) return "Arial";
    const randomIndex = Math.floor(Math.random() * fontOptions.length);
    const selected = fontOptions[randomIndex];
    return String(selected?.value ?? selected ?? "Arial");
  }

  function randomizeStyles() {
    const colorKeys = [
      "FONT_COLOR",
      "EDGE_COLOR",
      "MAIN_FILL_COLOR",
      "MAIN_STROKE_COLOR",
      "SUBTITLE_FILL_COLOR",
      "SUBTITLE_STROKE_COLOR",
      "CONNECTOR_FONT_COLOR",
      "CONNECTOR_BG_COLOR",
      "CONNECTOR_BORDER_COLOR"
    ];

    state.currentConfig.FONT_FAMILY = randomFontFamily();
    if ("CONNECTOR_FONT_FAMILY" in state.currentConfig) {
      state.currentConfig.CONNECTOR_FONT_FAMILY = randomFontFamily();
    }
    if ("FONT_BOLD" in state.currentConfig) {
      state.currentConfig.FONT_BOLD = Math.random() >= 0.5;
    }
    if ("FONT_ITALIC" in state.currentConfig) {
      state.currentConfig.FONT_ITALIC = Math.random() >= 0.5;
    }

    colorKeys.forEach((key) => {
      state.currentConfig[key] = randomHexColor();
    });

    if (Array.isArray(state.currentConfig.PALETTE) && state.currentConfig.PALETTE.length) {
      state.currentConfig.PALETTE = state.currentConfig.PALETTE.map(() => [
        randomHexColor(),
        randomHexColor()
      ]);
    }

    renderConfigForm();
    updateConfigTextFromState();
    onConfigChanged();
    setStatus("Estilo randomizado: colores y fuentes actualizados.", "ok");
  }

  function updateConfigTextFromState() {
    if (state.isRenderingForm) return;
    dom.configEditor.value = jsToPythonLiteral(state.currentConfig);
  }

  function onFormValueChange(key, rawValue, type) {
    if (type === "number") {
      const n = Number(rawValue);
      if (!Number.isFinite(n)) return;
      state.currentConfig[key] = n;
    } else if (type === "boolean") {
      state.currentConfig[key] = Boolean(rawValue);
    } else {
      state.currentConfig[key] = String(rawValue ?? "");
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
      input.checked = Boolean(state.currentConfig[field.key]);
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

      const disabledByValue = isColorDisabledValue(state.currentConfig[field.key]);
      const defaultColor = safeColor(constants.DEFAULT_CONFIG[field.key], "#000000");
      const initialColor = safeColor(
        disabledByValue ? defaultColor : state.currentConfig[field.key],
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
          state.currentConfig[field.key] = activeColor;
        } else {
          lastColor = colorInput.value;
          state.currentConfig[field.key] = "none";
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
        state.currentConfig[field.key] = "none";
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
      const currentValue = String(state.currentConfig[field.key] ?? "");
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
      input.value = String(state.currentConfig[field.key] ?? "");
      input.addEventListener("input", () => onFormValueChange(field.key, input.value, "number"));
    } else {
      input.value = String(state.currentConfig[field.key] ?? "");
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
    const sectionTitle = "Paleta (relleno y borde)";
    const editor = document.createElement("div");
    editor.className = "palette-editor";

    const getDefaultPair = () => {
      const fallback = Array.isArray(constants.DEFAULT_CONFIG.PALETTE) && constants.DEFAULT_CONFIG.PALETTE.length
        ? constants.DEFAULT_CONFIG.PALETTE[constants.DEFAULT_CONFIG.PALETTE.length - 1]
        : ["#60a5fa", "#1e3a8a"];
      return [
        safeColor(fallback[0], "#000000"),
        safeColor(fallback[1], "#000000")
      ];
    };

    const addPalettePair = () => {
      const source = state.currentConfig.PALETTE[state.currentConfig.PALETTE.length - 1] || getDefaultPair();
      const nextPair = [
        safeColor(source[0], "#000000"),
        safeColor(source[1], "#000000")
      ];
      state.currentConfig.PALETTE.push(nextPair);
      renderConfigForm();
      updateConfigTextFromState();
      onConfigChanged();
    };

    const removePalettePair = (index) => {
      if (!Array.isArray(state.currentConfig.PALETTE) || state.currentConfig.PALETTE.length <= 1) {
        setStatus("La paleta debe tener al menos 1 par.", "error");
        return;
      }
      state.currentConfig.PALETTE.splice(index, 1);
      renderConfigForm();
      updateConfigTextFromState();
      onConfigChanged();
    };

    state.currentConfig.PALETTE.forEach((pair, index) => {
      const row = document.createElement("div");
      row.className = "palette-row";

      const tag = document.createElement("span");
      tag.className = "palette-tag";
      tag.textContent = `Par ${index + 1}`;

      const fillInput = document.createElement("input");
      fillInput.type = "color";
      fillInput.value = safeColor(pair[0], "#000000");

      const strokeInput = document.createElement("input");
      strokeInput.type = "color";
      strokeInput.value = safeColor(pair[1], "#000000");

      const removeBtn = document.createElement("button");
      removeBtn.type = "button";
      removeBtn.className = "btn-ghost palette-btn";
      removeBtn.textContent = "Eliminar";
      removeBtn.disabled = state.currentConfig.PALETTE.length <= 1;
      removeBtn.title = removeBtn.disabled
        ? "La paleta debe tener al menos 1 par."
        : "Eliminar este par";

      fillInput.addEventListener("input", () => {
        state.currentConfig.PALETTE[index][0] = fillInput.value;
        updateConfigTextFromState();
        onConfigChanged();
      });
      strokeInput.addEventListener("input", () => {
        state.currentConfig.PALETTE[index][1] = strokeInput.value;
        updateConfigTextFromState();
        onConfigChanged();
      });
      removeBtn.addEventListener("click", () => {
        removePalettePair(index);
      });

      row.appendChild(tag);
      row.appendChild(fillInput);
      row.appendChild(strokeInput);
      row.appendChild(removeBtn);
      editor.appendChild(row);
    });

    const actions = document.createElement("div");
    actions.className = "palette-actions";

    const addBtn = document.createElement("button");
    addBtn.type = "button";
    addBtn.className = "btn-ghost palette-btn";
    addBtn.textContent = "Agregar par";
    addBtn.addEventListener("click", addPalettePair);

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
        sectionDef.title === "Tipografia"
      );
      dom.configForm.appendChild(section);
    });

    if (Array.isArray(state.currentConfig.PALETTE)) {
      dom.configForm.appendChild(makePaletteEditor());
    }
    state.isRenderingForm = false;
  }

  return {
    renderConfigForm,
    updateConfigTextFromState,
    randomizeStyles
  };
}
