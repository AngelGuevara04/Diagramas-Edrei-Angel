import { clamp } from "./utils.js";

export function createPreviewApi({ dom, state, constants }) {
  function syncGraphOverflowForZoom(graphEl, zoomValue, usingCssZoom) {
    if (usingCssZoom) {
      graphEl.style.marginRight = "";
      graphEl.style.marginBottom = "";
      return;
    }

    // En navegadores sin soporte de CSS zoom se usa transform: scale().
    // La transformacion no aumenta el area de scroll por si sola, asi que
    // agregamos margen para reflejar el tamano visual escalado.
    const baseWidth = Math.max(graphEl.scrollWidth, graphEl.clientWidth, 0);
    const baseHeight = Math.max(graphEl.scrollHeight, graphEl.clientHeight, 0);
    const extraWidth = Math.max(0, Math.round((zoomValue - 1) * baseWidth));
    const extraHeight = Math.max(0, Math.round((zoomValue - 1) * baseHeight));

    graphEl.style.marginRight = `${extraWidth}px`;
    graphEl.style.marginBottom = `${extraHeight}px`;
  }

  function applyGraphZoom(nextZoom, focusClientX = null, focusClientY = null) {
    const graphEl = dom.graphContainer.querySelector(".mxgraph");
    if (!graphEl) return;

    const previousZoom = state.graphZoom || 1;
    const resolvedZoom = clamp(nextZoom, constants.GRAPH_ZOOM_MIN, constants.GRAPH_ZOOM_MAX);
    state.graphZoom = resolvedZoom;

    const rect = dom.graphContainer.getBoundingClientRect();
    const pointerX = focusClientX ?? rect.left + rect.width / 2;
    const pointerY = focusClientY ?? rect.top + rect.height / 2;
    const localX = pointerX - rect.left;
    const localY = pointerY - rect.top;

    const contentX = dom.graphContainer.scrollLeft + localX;
    const contentY = dom.graphContainer.scrollTop + localY;

    const usingCssZoom = Boolean(window.CSS && CSS.supports && CSS.supports("zoom", "1"));
    if (usingCssZoom) {
      graphEl.style.zoom = String(resolvedZoom);
      graphEl.style.transform = "";
      graphEl.style.transformOrigin = "";
    } else {
      graphEl.style.zoom = "";
      graphEl.style.transformOrigin = "top left";
      graphEl.style.transform = `scale(${resolvedZoom})`;
    }
    syncGraphOverflowForZoom(graphEl, resolvedZoom, usingCssZoom);

    const scaleRatio = resolvedZoom / previousZoom;
    dom.graphContainer.scrollLeft = contentX * scaleRatio - localX;
    dom.graphContainer.scrollTop = contentY * scaleRatio - localY;
  }

  function handleGraphWheelZoom(event) {
    const graphEl = dom.graphContainer.querySelector(".mxgraph");
    if (!graphEl) return;

    // Pinza/ctrl+wheel: zoom.
    if (event.ctrlKey) {
      event.preventDefault();
      const zoomFactor = Math.exp(-event.deltaY * 0.0016);
      applyGraphZoom(state.graphZoom * zoomFactor, event.clientX, event.clientY);
      return;
    }

    // Deja el scroll nativo para touchpad (mejor inercia y ejes en la mayoria de navegadores).
    // Solo se intercepta el caso Shift+wheel para forzar desplazamiento horizontal.
    const legacyDeltaX = typeof event.wheelDeltaX === "number" ? -event.wheelDeltaX : 0;
    const deltaX = Math.abs(event.deltaX) > 0.01 ? event.deltaX : legacyDeltaX;
    const deltaY = event.deltaY || 0;
    if (event.shiftKey && Math.abs(deltaX) <= 0.01) {
      event.preventDefault();
      dom.graphContainer.scrollLeft += deltaY;
      return;
    }

    // Si el visor interno ya anulo el evento, aplicamos pan manual para no perder el gesto.
    if (event.defaultPrevented) {
      dom.graphContainer.scrollLeft += deltaX;
      dom.graphContainer.scrollTop += deltaY;
    }
  }

  function getTouchDistance(t1, t2) {
    const dx = t2.clientX - t1.clientX;
    const dy = t2.clientY - t1.clientY;
    return Math.hypot(dx, dy);
  }

  function getTouchCenter(t1, t2) {
    return {
      x: (t1.clientX + t2.clientX) / 2,
      y: (t1.clientY + t2.clientY) / 2
    };
  }

  function handleGraphTouchStart(event) {
    const graphEl = dom.graphContainer.querySelector(".mxgraph");
    if (!graphEl) return;

    if (event.touches.length >= 2) {
      const t1 = event.touches[0];
      const t2 = event.touches[1];
      const center = getTouchCenter(t1, t2);
      state.touchState.mode = "pinch";
      state.touchState.pinchStartDist = getTouchDistance(t1, t2);
      state.touchState.pinchStartZoom = state.graphZoom;
      state.touchState.pinchCenterX = center.x;
      state.touchState.pinchCenterY = center.y;
      event.preventDefault();
      return;
    }

    if (event.touches.length === 1) {
      const t = event.touches[0];
      state.touchState.mode = "pan";
      state.touchState.startX = t.clientX;
      state.touchState.startY = t.clientY;
      state.touchState.startScrollLeft = dom.graphContainer.scrollLeft;
      state.touchState.startScrollTop = dom.graphContainer.scrollTop;
    }
  }

  function handleGraphTouchMove(event) {
    const graphEl = dom.graphContainer.querySelector(".mxgraph");
    if (!graphEl) return;

    if (event.touches.length >= 2) {
      const t1 = event.touches[0];
      const t2 = event.touches[1];
      if (state.touchState.mode !== "pinch") {
        const center = getTouchCenter(t1, t2);
        state.touchState.mode = "pinch";
        state.touchState.pinchStartDist = getTouchDistance(t1, t2);
        state.touchState.pinchStartZoom = state.graphZoom;
        state.touchState.pinchCenterX = center.x;
        state.touchState.pinchCenterY = center.y;
      }
      const dist = getTouchDistance(t1, t2);
      if (state.touchState.pinchStartDist > 0) {
        const scale = dist / state.touchState.pinchStartDist;
        applyGraphZoom(
          state.touchState.pinchStartZoom * scale,
          state.touchState.pinchCenterX,
          state.touchState.pinchCenterY
        );
      }
      event.preventDefault();
      return;
    }

    if (event.touches.length === 1 && state.touchState.mode === "pan") {
      const t = event.touches[0];
      const dx = t.clientX - state.touchState.startX;
      const dy = t.clientY - state.touchState.startY;
      dom.graphContainer.scrollLeft = state.touchState.startScrollLeft - dx;
      dom.graphContainer.scrollTop = state.touchState.startScrollTop - dy;
      event.preventDefault();
    }
  }

  function handleGraphTouchEnd(event) {
    if (event.touches.length >= 2) {
      const t1 = event.touches[0];
      const t2 = event.touches[1];
      const center = getTouchCenter(t1, t2);
      state.touchState.mode = "pinch";
      state.touchState.pinchStartDist = getTouchDistance(t1, t2);
      state.touchState.pinchStartZoom = state.graphZoom;
      state.touchState.pinchCenterX = center.x;
      state.touchState.pinchCenterY = center.y;
      return;
    }
    if (event.touches.length === 1) {
      const t = event.touches[0];
      state.touchState.mode = "pan";
      state.touchState.startX = t.clientX;
      state.touchState.startY = t.clientY;
      state.touchState.startScrollLeft = dom.graphContainer.scrollLeft;
      state.touchState.startScrollTop = dom.graphContainer.scrollTop;
      return;
    }
    state.touchState.mode = "none";
  }

  function getMousePanMode(event) {
    // Solo clic izquierdo: pan libre (horizontal + vertical).
    if (event.button === 0) return "free";
    return "none";
  }

  function isInteractivePreviewTarget(target) {
    if (!(target instanceof Element)) return false;
    return Boolean(target.closest("a, button, input, select, textarea, label, [role='button']"));
  }

  function handleMousePanStart(event) {
    const graphEl = dom.graphContainer.querySelector(".mxgraph");
    if (!graphEl) return;
    const mode = getMousePanMode(event);
    if (mode === "none") return;
    if (isInteractivePreviewTarget(event.target)) return;

    state.mousePanState.active = true;
    state.mousePanState.mode = mode;
    state.mousePanState.startX = event.clientX;
    state.mousePanState.startY = event.clientY;
    state.mousePanState.startScrollLeft = dom.graphContainer.scrollLeft;
    state.mousePanState.startScrollTop = dom.graphContainer.scrollTop;
    dom.graphContainer.classList.add("is-dragging");
    event.preventDefault();
  }

  function applyMousePanFromEvent(event) {
    const dx = event.clientX - state.mousePanState.startX;
    const dy = event.clientY - state.mousePanState.startY;
    // Clic izquierdo sostenido: pan libre (horizontal + vertical).
    dom.graphContainer.scrollLeft = state.mousePanState.startScrollLeft - dx;
    dom.graphContainer.scrollTop = state.mousePanState.startScrollTop - dy;
  }

  function handleMousePanMove(event) {
    if (!state.mousePanState.active) return;
    applyMousePanFromEvent(event);
    event.preventDefault();
  }

  function handleWindowMousePanMove(event) {
    if (!state.mousePanState.active) return;
    const requiredButton = 1;
    if ((event.buttons & requiredButton) !== requiredButton) {
      endMousePan();
      return;
    }
    applyMousePanFromEvent(event);
    event.preventDefault();
  }

  function endMousePan() {
    if (!state.mousePanState.active) return;
    state.mousePanState.active = false;
    state.mousePanState.mode = "none";
    dom.graphContainer.classList.remove("is-dragging");
  }

  function renderGraph(xml, options = {}) {
    const previousView = {
      zoom: state.graphZoom || 1,
      scrollLeft: dom.graphContainer.scrollLeft,
      scrollTop: dom.graphContainer.scrollTop
    };
    const preserveView = Boolean(options.preserveView);

    dom.graphContainer.innerHTML = "";
    state.graphZoom = preserveView ? previousView.zoom : 1;
    const div = document.createElement("div");
    div.className = "mxgraph";
    const graphData = {
      highlight: "#2d7ff9",
      nav: true,
      resize: false,
      toolbar: "zoom layers lightbox",
      fit: "0",
      page: "0",
      border: 4,
      edit: null,
      xml
    };
    div.setAttribute("data-mxgraph", JSON.stringify(graphData));
    dom.graphContainer.appendChild(div);
    GraphViewer.processElements();
    setTimeout(() => {
      applyGraphZoom(state.graphZoom);
      if (preserveView) {
        dom.graphContainer.scrollLeft = previousView.scrollLeft;
        dom.graphContainer.scrollTop = previousView.scrollTop;
      } else {
        const maxScrollLeft = Math.max(0, dom.graphContainer.scrollWidth - dom.graphContainer.clientWidth);
        const maxScrollTop = Math.max(0, dom.graphContainer.scrollHeight - dom.graphContainer.clientHeight);
        dom.graphContainer.scrollLeft = Math.round(maxScrollLeft / 2);
        dom.graphContainer.scrollTop = Math.round(maxScrollTop / 2);
      }
    }, 0);
  }

  function clearPreview() {
    dom.graphContainer.innerHTML = `
      <div id="graph-placeholder">
        Preview limpiada. Genera nuevamente para visualizar cambios.
      </div>
    `;
    state.graphZoom = 1;
    dom.previewMeta.textContent = "Sin generar";
  }

  function bindPreviewEvents() {
    dom.graphContainer.addEventListener("wheel", handleGraphWheelZoom, { passive: false });
    dom.graphContainer.addEventListener("mousedown", handleMousePanStart);
    dom.graphContainer.addEventListener("mousemove", handleMousePanMove);
    dom.graphContainer.addEventListener("mouseleave", endMousePan);
    dom.graphContainer.addEventListener("contextmenu", (event) => {
      if (state.mousePanState.active) event.preventDefault();
    });
    window.addEventListener("mouseup", endMousePan);
    window.addEventListener("mousemove", handleWindowMousePanMove);
    dom.graphContainer.addEventListener("touchstart", handleGraphTouchStart, { passive: false });
    dom.graphContainer.addEventListener("touchmove", handleGraphTouchMove, { passive: false });
    dom.graphContainer.addEventListener("touchend", handleGraphTouchEnd, { passive: false });
    dom.graphContainer.addEventListener("touchcancel", handleGraphTouchEnd, { passive: false });
  }

  return {
    renderGraph,
    clearPreview,
    bindPreviewEvents
  };
}
