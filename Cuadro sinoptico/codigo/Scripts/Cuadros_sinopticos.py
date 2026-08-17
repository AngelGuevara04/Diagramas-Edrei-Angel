import importlib
import math
import os
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

# El codigo se basa en una variable llamada chart, que define todo el contenido jerarquico del cuadro sinoptico.
# La estructura es recursiva, por lo que puedes anidar tantos niveles como necesites.
#
# chart = {
#     "Tema general": {
#         "Tema 1": ["Idea 1", "Idea 2"],
#         "Tema 2": {
#             "Subtema A": ["Punto A", "Punto B"],
#             "Subtema B": {
#                 "Detalle 1": ["Explicacion 1"],
#                 "Detalle 2": []
#             }
#         }
#     }
# }
#
# Reglas basicas
# Cada clave (str) representa un titulo o tema.
# Cada valor puede ser:
# - Una lista (list)
# - Un diccionario (dict) -> crea otra llave a la derecha con subniveles.
# - Una lista vacia ([]) -> muestra solo el texto del tema, sin llave (ideal para temas finales).
#
# Caracteristicas:
# - Jerarquia ilimitada.
# - Ancho dinamico segun el texto (min/max controlados por configuracion).
# - Ajuste automatico de altura segun el texto.
# - Llaves opcionales (si una entrada es []).
# - Alineacion vertical automatica entre titulo y llave.

DEFAULT_CHART = {
    "Tema general": {
        "Tema 1": ["Idea 1", "Idea 2"],
        "Tema 2": {
            "Subtema A": ["Punto A", "Punto B"],
            "Subtema B": {
                "Detalle 1": ["Explicacion 1"],
                "Detalle 2": [],
            },
        },
    }
}

DEFAULT_CONFIG = {
    "archivo_de_salida": os.path.join("Mapas", "Cuadro_sinoptico.drawio"),
    "PX_PER_CHAR": 7.0,
    "LINE_H": 17,
    "PADDING_V": 20,
    "TOP_MARGIN": 40,
    "LEFT_MARGIN": 40,
    "SIBLING_GAP": 10,
    "SPACE_LABEL_TO_BRACE": 5,
    "SPACE_BRACE_TO_CONTENT": 5,
    "BRACE_W": 14,
    "TOP_MIN_LABEL_W": 100,
    "MIN_LABEL_W": 10,
    "MAX_LABEL_W": 250,
    "MAX_ITEM_W": 250,
    "BRACE_THICK": 1,
    "LABEL_ONLY_MIN_H": 30,
    "BRACE_STYLE": "rounded",  # "rounded" (redondeada) o "plain" (simple)
    "FONT_FAMILY": "Times New Roman",
    "FONT_COLOR": "#415D66",
    "BRACE_COLOR": "#4A4861",
}


def apply_config(config=None):
    """Carga configuracion externa sobre los valores por defecto."""
    cfg = dict(DEFAULT_CONFIG)
    if config:
        cfg.update(config)
    globals().update(cfg)
    return cfg


# Inicializa valores globales para que las funciones auxiliares tengan defaults.
apply_config()


def resolve_output_path(path_str: str) -> str:
    """Devuelve la ruta absoluta del archivo de salida y crea la carpeta destino."""
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    candidate = str(path_str)
    out_path = candidate if os.path.isabs(candidate) else os.path.join(project_root, candidate)
    out_dir = os.path.dirname(out_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    return out_path


def _new_id():
    _new_id.counter += 1
    return _new_id.counter


_new_id.counter = 1


def new_cell(parent, id_, value, style, vertex=True, edge=False, x=0, y=0, w=0, h=0):
    cell = ET.SubElement(
        parent,
        "mxCell",
        {
            "id": str(id_),
            "value": value if value is not None else "",
            "style": style,
            "vertex": "1" if vertex else "0",
            "edge": "1" if edge else "0",
            "parent": "1",
        },
    )
    ET.SubElement(
        cell,
        "mxGeometry",
        {"x": str(x), "y": str(y), "width": str(w), "height": str(h), "as": "geometry"},
    )
    return cell


def _escape_drawio_value(text: str) -> str:
    s = str(text)
    s = s.replace("&", "&amp;")
    s = s.replace("<", "&lt;").replace(">", "&gt;")
    return s


def add_text(parent, text, x, y, w, h, align="left", valign="middle"):
    style = f"text;html=1;whiteSpace=wrap;align={align};verticalAlign={valign};"
    if FONT_FAMILY:
        style += f"fontFamily={FONT_FAMILY};"
    if FONT_COLOR:
        style += f"fontColor={FONT_COLOR};"
    safe_text = _escape_drawio_value(text)
    return new_cell(parent, _new_id(), safe_text, style, x=x, y=y, w=w, h=h)


def _compose_brace_style(
    base_style: str, direction: str, stroke_width: int, stroke_color: str | None = None
) -> str:
    if "html=1" not in base_style:
        base_style += ";html=1"
    if "whiteSpace=wrap" not in base_style:
        base_style += ";whiteSpace=wrap"
    parts = [
        p
        for p in base_style.strip(";").split(";")
        if p
        and not p.startswith("direction=")
        and not p.startswith("strokeWidth=")
        and not p.startswith("strokeColor=")
    ]
    parts += [f"direction={direction}", f"strokeWidth={stroke_width}"]
    if stroke_color:
        parts += [f"strokeColor={stroke_color}"]
    return ";".join(parts) + ";"


def add_brace_rounded(parent, x, y, w, h, direction="east"):
    base = "shape=curlyBracket;rounded=1;whiteSpace=wrap;html=1;"
    style = _compose_brace_style(
        base, direction=direction, stroke_width=BRACE_THICK, stroke_color=BRACE_COLOR
    )
    return new_cell(parent, _new_id(), "", style, x=x, y=y, w=w, h=h)


def add_brace_plain(parent, x, y, w, h, direction="east"):
    style = f"shape=curlyBracket;direction={direction};whiteSpace=wrap;strokeWidth={BRACE_THICK};"
    if BRACE_COLOR:
        style += f"strokeColor={BRACE_COLOR};"
    return new_cell(parent, _new_id(), "", style, x=x, y=y, w=w, h=h)


def add_brace(parent, x, y, w, h, direction="east"):
    return (
        add_brace_plain(parent, x, y, w, h, direction)
        if BRACE_STYLE == "plain"
        else add_brace_rounded(parent, x, y, w, h, direction)
    )


def text_width(text, min_w, max_w):
    est = int(len(text) * PX_PER_CHAR) + 18
    return min(max(min_w, est), max_w)


def items_width(items):
    if not items:
        return 200
    est = max(int(len(s) * PX_PER_CHAR) + 18 for s in items)
    return min(max(200, est), MAX_ITEM_W)


def estimate_item_lines(text, box_width):
    chars_per_line = max(10, int(box_width / PX_PER_CHAR))
    return max(1, math.ceil(len(text) / chars_per_line))


def list_block_height(items, box_width):
    if not items:
        return LABEL_ONLY_MIN_H + PADDING_V
    total = 0
    for s in items:
        total += estimate_item_lines(s, box_width) * LINE_H
    return max(LINE_H, total) + PADDING_V


def node_height(node):
    if isinstance(node, list):
        width = items_width(node)
        return list_block_height(node, width)
    if isinstance(node, dict):
        h = 0
        first = True
        for _, child in node.items():
            ch = node_height(child)
            if not first:
                h += SIBLING_GAP
            h += ch
            first = False
        return h + 20
    return list_block_height([str(node)], items_width([str(node)]))


def render_node(root, label, node, x, y, level=1):
    min_w = TOP_MIN_LABEL_W if level == 0 else MIN_LABEL_W
    label_w = text_width(label, min_w=min_w, max_w=MAX_LABEL_W)

    content_h = node_height(node)
    brace_x = x + label_w + SPACE_LABEL_TO_BRACE
    brace_y = y

    draw_self_brace = not (isinstance(node, list) and len(node) == 0)
    if draw_self_brace:
        add_brace(root, brace_x, brace_y, BRACE_W, content_h, direction="east")

    label_h = 28 if level == 0 else 24
    label_y = brace_y + (content_h - label_h) / 2
    add_text(root, label, x, label_y, label_w, label_h)

    content_x = brace_x + (BRACE_W if draw_self_brace else 0) + SPACE_BRACE_TO_CONTENT
    current_y = brace_y + 10

    if isinstance(node, list):
        if len(node) == 0:
            return (content_x - x), content_h
        max_w = items_width(node)
        for s in node:
            lines = estimate_item_lines(s, max_w)
            add_text(root, "" + s, content_x, current_y, max_w, lines * LINE_H)
            current_y += lines * LINE_H
        return (content_x - x) + max_w, content_h
    if isinstance(node, dict):
        max_child_right = 0
        first = True
        for child_label, child_node in node.items():
            if not first:
                current_y += SIBLING_GAP
            w_child, h_child = render_node(
                root, child_label, child_node, content_x, current_y, level + 1
            )
            current_y += h_child
            max_child_right = max(max_child_right, w_child)
            first = False
        return max_child_right + (content_x - x), content_h
    w = items_width([str(node)])
    lines = estimate_item_lines(str(node), w)
    add_text(root, "" + str(node), content_x, current_y, w, lines * LINE_H)
    return (content_x - x) + w, content_h


def generar_cuadro_sinoptico(chart_data=None, config=None):
    """Genera el drawio con el chart y configuracion indicados."""
    cfg = apply_config(config)
    out_path = resolve_output_path(cfg["archivo_de_salida"])
    _new_id.counter = 1
    data = chart_data or DEFAULT_CHART
    if not isinstance(data, dict) or len(data) == 0:
        raise ValueError("chart debe ser un diccionario con al menos una entrada")

    first_label, first_node = next(iter(data.items()))

    mxfile = ET.Element(
        "mxfile",
        {
            "modified": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "agent": "Synoptic Optional Braces",
            "version": "24.7.7",
        },
    )
    diagram = ET.SubElement(mxfile, "diagram", {"name": "Optional Braces"})
    mxGraphModel = ET.SubElement(
        diagram,
        "mxGraphModel",
        {
            "dx": "1220",
            "dy": "730",
            "grid": "1",
            "gridSize": "10",
            "guides": "1",
            "tooltips": "1",
            "connect": "1",
            "arrows": "1",
            "fold": "1",
            "page": "1",
            "pageScale": "1",
            "pageWidth": "2200",
            "pageHeight": "1400",
            "math": "0",
            "shadow": "0",
        },
    )
    root = ET.SubElement(mxGraphModel, "root")
    ET.SubElement(root, "mxCell", {"id": "0"})
    ET.SubElement(root, "mxCell", {"id": "1", "parent": "0"})
    render_node(root, first_label, first_node, LEFT_MARGIN, TOP_MARGIN, level=0)
    ET.indent(mxfile, space="  ")
    ET.ElementTree(mxfile).write(out_path, encoding="utf-8", xml_declaration=True)
    return os.path.abspath(out_path).replace("\\", "/")


def cargar_config_externa(module_name="cuadro_sinoptico_config"):
    """Intenta cargar chart y CONFIG desde un modulo externo en la carpeta raiz."""
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    try:
        external = importlib.import_module(module_name)
    except ModuleNotFoundError:
        return None, {}
    return getattr(external, "chart", None), getattr(external, "CONFIG", {})


def main():
    chart_data, config = cargar_config_externa()
    out_path = generar_cuadro_sinoptico(chart_data, config)
    print(f"Cuadro sinoptico generado en: {out_path}")


if __name__ == "__main__":
    main()
