import importlib
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
from datetime import datetime, timezone
import os
import random
import sys

# ================= CONFIGURACION POR DEFECTO =================
DEFAULT_CONFIG = {
    # Tipografia
    "FONT_FAMILY": "Courier New",
    "FONT_SIZE": 12,
    "FONT_COLOR": "#1f2937",
    "FONT_BOLD": False,  # True para negrita
    "FONT_ITALIC": False,  # True para cursiva
    # Bordes y conectores
    "STROKE_W": 1.2,
    "EDGE_COLOR": "#38579b",
    # Nodos
    "BOX_ARC_SIZE": 30,
    "BOX_SHADOW": True,
    # Colores de titulo y subtitulos
    "MAIN_FILL_COLOR": "#dbeafe",
    "MAIN_STROKE_COLOR": "#1d4ed8",
    "SUBTITLE_FILL_COLOR": "#e2e8f0",
    "SUBTITLE_STROKE_COLOR": "#475569",
    # Texto de conectores
    "CONNECTOR_FONT_FAMILY": "Verdana",
    "CONNECTOR_FONT_SIZE": 9,
    "CONNECTOR_FONT_COLOR": "#111827",
    "CONNECTOR_BG_COLOR": "#f8fafc",
    "CONNECTOR_BORDER_COLOR": "#cbd5e1",
    "CONNECTOR_SHADOW": False,
    "CONNECTOR_TEXT_SHADOW": True,
    # Tamano de nodos
    "BOX_W": 100,
    "BOX_H": 70,
    # Separaciones basicas
    "X_STEP": 150,
    "Y_STEP": 110,
    # Ruido opcional en posiciones para un look menos rigido
    "POSITION_NOISE": 0,
    # Separaciones jerarquicas
    "MAIN_TO_SUBTITLE": 130,
    "SUBTITLE_TO_BRANCH": 150,
    "SUBTITLE_GAP": 80,
    "GROUP_GAP": 200,
    # Coloreo jerarquico
    "COLOR_SUBTITLE_GROUPS": False,  # True: todas las ramas de un subtitulo comparten color
    "COLOR_NESTED_SUBTOPICS": False,  # True: cada sub-tema anidado usa un color propio
    # Normalizacion por palabras (global) y correccion puntual de tuplas extensas.
    "NORMALIZAR_TUPLAS": False,
    "PALABRAS_POR_POSICION": 2,
    "NORMALIZAR_TUPLAS_EXTENSAS": True,
    # Paleta de ramas
    "PALETTE": [
        ("#fff3c4", "#d97706"),
        ("#d8ffe5", "#15803d"),
        ("#e0eeff", "#1d4ed8"),
        ("#ffead2", "#c2410c"),
    ],
    # Posicion inicial y archivo de salida
    "START_X": 120,
    "START_Y": 40,
    "OUTPUT_FILE": os.path.join("Mapas", "Mapa_conceptual.drawio"),
}

DEFAULT_CONCEPT_MAP = [
    {
        "titulo_principal": "Aplicaciones con tecnicas de IA",
        "subtitulos": [
            {
                "titulo": "Robotica",
                "conector": "se compone de",
                "ramas": [
                    [
                        (None, "La"),
                        ("Robotica", "es una"),
                        ("Rama", "de la"),
                        ("Ingenieria", None),
                    ],
                    [
                        (None, "La"),
                        ("Robotica", "aplica"),
                        ("Tecnicas de IA", "para"),
                        ("Resolver problemas", None),
                    ],
                    [
                        (None, "Los"),
                        ("Conceptos basicos", "incluyen"),
                        ("Sensores", "que son"),
                        ("Dispositivos entrada", None),
                    ],
                    [
                        (None, "La"),
                        ("Robótica", "se divide"),
                        {
                            "texto": "Tipos",           # nodo donde se abre la bifurcación
                            "conector": "se divide en",  # conector obligatorio que verás entre Robótica y Tipos
                            "bifurcaciones": [
                                [(None,"como"),("Industrial", "opera en"), ("Fábricas", None)],
                                [(None,"también"),("Doméstica", "trabaja en"), ("Hogar", None)],
                                [(None, "además"),("Médica", "aplica a"), ("Hospitales", None)],
                            ],
                        },
                    ],
                ],
            },
            {
                "titulo": "Nuevas tecnologias",
                "conector": "integra las",
                "ramas": [
                    [
                        (None, "Los"),
                        ("Desarrollos actuales", "incluyen"),
                        ("Robots colaborativos", None),
                    ],
                    [
                        (None, "Las"),
                        ("Aplicaciones", "actuales"),
                        ("Son", "Vehiculos autonomos"),
                        ("Coches", None),
                    ],
                ],
            },
        ],
    }
]


def apply_config(config=None):
    """Carga configuracion externa sobre los valores por defecto."""
    cfg = dict(DEFAULT_CONFIG)
    if config:
        cfg.update(config)
    globals().update(cfg)
    return cfg


# Inicializa globals para estilos
apply_config()


def resolve_output_path(path_str: str) -> str:
    """Devuelve la ruta absoluta para OUTPUT_FILE y crea la carpeta destino."""
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    candidate = str(path_str)
    out_path = candidate if os.path.isabs(candidate) else os.path.join(project_root, candidate)
    out_dir = os.path.dirname(out_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    return out_path


def prettify(elem):
    rough_string = tostring(elem, "utf-8")
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def estimate_text_width(text, font_size, is_monospaced=True):
    """Estima el ancho de un texto basado en la fuente y tamano."""
    if not text:
        return 0
    # Factor de ajuste. Para Courier New (monoespaciado), 0.62 es una buena aproximacion.
    # Para fuentes proporcionales, esto seria mas complejo.
    factor = 0.62
    return len(text) * font_size * factor


def font_style_code():
    """Devuelve el valor fontStyle de draw.io segun la config."""
    bold = 1 if globals().get("FONT_BOLD", False) else 0
    italic = 2 if globals().get("FONT_ITALIC", False) else 0
    return str(bold + italic)


def make_vertex_style(fill, stroke, arc=None, shadow=None):
    arc_val = BOX_ARC_SIZE if arc is None else arc
    shadow_val = BOX_SHADOW if shadow is None else shadow
    return (
        f"rounded=1;whiteSpace=wrap;html=1;shadow={'1' if shadow_val else '0'};"
        f"arcSize={arc_val};"
        f"fillColor={fill};strokeColor={stroke};strokeWidth={STROKE_W};"
        f"fontStyle={font_style_code()};fontFamily={FONT_FAMILY};fontSize={FONT_SIZE};fontColor={FONT_COLOR};"
        "align=center;verticalAlign=middle;"
    )


def make_edge_style(
    stroke=None,
    label_font_color=None,
    label_bg_color=None,
    label_border_color=None,
    label_edge_shadow=None,
    label_font_family=None,
    label_font_size=None,
    label_text_shadow=None,
):
    stroke_val = stroke if stroke is not None else EDGE_COLOR
    bg_val = label_bg_color if label_bg_color is not None else CONNECTOR_BG_COLOR
    border_val = label_border_color if label_border_color is not None else CONNECTOR_BORDER_COLOR
    shadow_val = label_edge_shadow if label_edge_shadow is not None else CONNECTOR_SHADOW
    text_shadow_val = label_text_shadow if label_text_shadow is not None else CONNECTOR_TEXT_SHADOW
    font_family_val = label_font_family if label_font_family is not None else CONNECTOR_FONT_FAMILY or FONT_FAMILY
    # Prioriza el tamaño configurado para conectores y permite override puntual.
    if label_font_size is not None:
        font_size_val = label_font_size
    elif globals().get("CONNECTOR_FONT_SIZE") is not None:
        font_size_val = CONNECTOR_FONT_SIZE
    else:
        font_size_val = max(12, int(FONT_SIZE * 0.9))
    font_color_val = label_font_color if label_font_color is not None else CONNECTOR_FONT_COLOR

    parts = [
        "edgeStyle=elbowEdgeStyle;elbow=vertical;rounded=1;",
        "orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;endFill=1;",
        f"strokeColor={stroke_val};strokeWidth=1.15;",
        f"fontFamily={font_family_val};",
        f"fontSize={font_size_val};",
        f"fontStyle={font_style_code()};",
        f"fontColor={font_color_val};",
    ]
    if bg_val:
        parts.append(f"labelBackgroundColor={bg_val};")
    if border_val:
        parts.append(f"labelBorderColor={border_val};")
    if shadow_val:
        parts.append("shadow=1;")
    if text_shadow_val:
        parts.append("textShadow=1;")
    parts.append("labelPadding=4;")
    return "".join(parts)


def create_document():
    mxfile = Element(
        "mxfile",
        attrib={
            "host": "app.diagrams.net",
            "modified": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "agent": "python-generator",
            "version": "22.0.8",
            "editor": "www.draw.io",
            "type": "device",
        },
    )
    diagram = SubElement(mxfile, "diagram", attrib={"id": "diagram-1", "name": "Mapa conceptual"})
    mxGraphModel = SubElement(
        diagram,
        "mxGraphModel",
        attrib={
            "dx": "1920",
            "dy": "1080",
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
            "pageHeight": "2600",
            "math": "0",
            "shadow": "0",
        },
    )
    root = SubElement(mxGraphModel, "root")
    SubElement(root, "mxCell", attrib={"id": "0"})
    SubElement(root, "mxCell", attrib={"id": "1", "parent": "0"})

    cell_id = 2

    def next_id():
        nonlocal cell_id
        cell_id += 1
        return cell_id - 1

    def add_vertex(value, x, y, w=BOX_W, h=BOX_H, style=None):
        style_local = style if style is not None else make_vertex_style("#fff2cc", "#d6b656")

        noise_amount = globals().get("POSITION_NOISE", 0)
        if noise_amount:
            jitter = noise_amount / 2
            x += random.uniform(-jitter, jitter)
            y += random.uniform(-jitter, jitter)

        # Ajuste automatico de ancho basado en la palabra mas larga
        words = str(value).split()
        longest_word = max(words, key=len) if words else ""

        is_mono = "courier" in FONT_FAMILY.lower()
        # El padding se anade para que el texto no toque los bordes.
        estimated_width = estimate_text_width(longest_word, FONT_SIZE, is_mono) + 20

        final_w = w
        final_x = x
        if estimated_width > w:
            width_increase = estimated_width - w
            final_w = estimated_width
            final_x = x - (width_increase / 2)  # Centrar el cuadro

        v_id = next_id()
        cell = SubElement(
            root,
            "mxCell",
            attrib={
                "id": str(v_id),
                "value": value,
                "style": style_local,
                "vertex": "1",
                "parent": "1",
            },
        )
        geo = SubElement(
            cell,
            "mxGeometry",
            attrib={"x": str(final_x), "y": str(y), "width": str(final_w), "height": str(h)},
        )
        geo.set("as", "geometry")
        return cell.get("id")

    def add_edge(value, source_id, target_id, style=None, place_label_at_target=False):
        style_local = style if style is not None else make_edge_style()
        e_id = next_id()
        cell = SubElement(
            root,
            "mxCell",
            attrib={
                "id": str(e_id),
                "value": value if value else "",
                "style": style_local,
                "edge": "1",
                "parent": "1",
                "source": str(source_id),
                "target": str(target_id),
            },
        )
        geo_attrs = {"relative": "1"}
        if place_label_at_target:
            geo_attrs["x"] = "0.9"
            geo_attrs["y"] = "22"
        geo = SubElement(cell, "mxGeometry", attrib=geo_attrs)
        if place_label_at_target:
            SubElement(geo, "mxPoint", attrib={"x": "-22", "y": "-20", "as": "offset"})
        geo.set("as", "geometry")
        return cell.get("id")

    return mxfile, root, add_vertex, add_edge


def branch_block_width(branch_count: int) -> float:
    """Ancho horizontal de las ramas de un subtitulo."""
    if branch_count <= 0:
        return BOX_W
    return BOX_W + (branch_count - 1) * X_STEP

def is_inline_fork(entry):
    """Detecta nodos de bifurcacion embebidos dentro de una rama."""
    return isinstance(entry, dict) and ("bifurcaciones" in entry or "forks" in entry)


def branch_slot_usage(branch):
    """Calcula cuantas columnas necesita una rama considerando bifurcaciones internas."""
    slots = 1
    for entry in branch:
        if is_inline_fork(entry):
            forks = entry.get("bifurcaciones") or entry.get("forks") or []
            fork_width = 0
            for fork_branch in forks:
                fork_width += max(1, branch_slot_usage(fork_branch))
            slots = max(slots, fork_width or 1)
    return max(1, slots)


def count_branch_slots(subtitle):
    """Devuelve cuantas columnas necesita un subtitulo (soporta ramas anidadas y bifurcaciones)."""
    slots = 0
    for rama in subtitle.get("ramas", []):
        if isinstance(rama, dict) and not is_inline_fork(rama):
            nested_width = sum(max(1, branch_slot_usage(r)) for r in rama.get("ramas", [])) or 1
            slots += nested_width
        elif isinstance(rama, list):
            slots += branch_slot_usage(rama)
        else:
            slots += 1
    return max(1, slots)


def _merge_concept_parts(parts_iterable):
    parts = []
    for piece in parts_iterable:
        if piece is None:
            continue
        text = str(piece).strip()
        if text:
            parts.append(text)
    merged = " ".join(parts).strip()
    return merged if merged else None


def normalize_extended_tuples_in_concept_map(concept_map_data):
    """Normaliza entradas tipo tupla/lista con mas de 2 elementos a 2 elementos."""
    normalized_count = 0

    def normalize_entry(entry):
        nonlocal normalized_count

        if is_inline_fork(entry):
            forks = entry.get("bifurcaciones") or entry.get("forks") or []
            if isinstance(forks, list):
                for fork_branch in forks:
                    if isinstance(fork_branch, list):
                        normalize_branch(fork_branch)
            return entry

        if isinstance(entry, (tuple, list)) and len(entry) > 2:
            concept = _merge_concept_parts(entry[:-1])
            connector = entry[-1]
            normalized_count += 1
            return (concept, connector)

        return entry

    def normalize_branch(branch):
        for idx, entry in enumerate(branch):
            branch[idx] = normalize_entry(entry)

    def normalize_branch_list(branch_list):
        if not isinstance(branch_list, list):
            return
        for branch in branch_list:
            if isinstance(branch, dict) and not is_inline_fork(branch):
                normalize_branch_list(branch.get("ramas", []))
                continue
            if isinstance(branch, list):
                normalize_branch(branch)

    if not isinstance(concept_map_data, list):
        return 0

    for group in concept_map_data:
        if not isinstance(group, dict):
            continue
        subtitles = group.get("subtitulos", [])
        if not isinstance(subtitles, list):
            continue
        for subtitle in subtitles:
            if not isinstance(subtitle, dict):
                continue
            normalize_branch_list(subtitle.get("ramas", []))

    return normalized_count


def validate_concept_map_data(concept_map_data):
    """Valida la estructura de datos del mapa conceptual y acumula todos los errores."""
    errors = []

    def add_error(message):
        errors.append(message)

    if not isinstance(concept_map_data, list):
        raise ValueError("La estructura principal del mapa debe ser una lista.")

    for g_idx, group in enumerate(concept_map_data):
        if not isinstance(group, dict):
            add_error(
                f"Error En Grupo #{g_idx+1}: Cada grupo debe ser un dict, pero se encontro un {type(group).__name__}."
            )
            continue

        g_title = group.get('titulo_principal', f'Grupo #{g_idx+1}')
        subtitles = group.get('subtitulos', [])
        if not isinstance(subtitles, list):
            add_error(
                f"Error En Grupo '{g_title}': 'subtitulos' debe ser una lista, pero se encontro un {type(subtitles).__name__}."
            )
            continue

        for s_idx, subtitle in enumerate(subtitles):
            if not isinstance(subtitle, dict):
                add_error(
                    f"Error En Grupo '{g_title}' -> Subtitulo #{s_idx+1}: Cada subtitulo debe ser un dict, pero se encontro un {type(subtitle).__name__}."
                )
                continue

            s_title = subtitle.get('titulo', f'Subtitulo #{s_idx+1}')

            def check_branch_list(branch_list, context_path):
                if not isinstance(branch_list, list):
                    add_error(
                        f"Error {context_path}: 'ramas' debe ser una lista, pero se encontro un {type(branch_list).__name__}."
                    )
                    return

                for b_idx, branch in enumerate(branch_list):
                    branch_context = f"{context_path} -> Rama #{b_idx+1}"
                    if isinstance(branch, dict) and not is_inline_fork(branch):  # Sub-tema anidado
                        sub_topic_title = branch.get('titulo', f'Sub-tema #{b_idx+1}')
                        check_branch_list(branch.get('ramas', []), f"{branch_context} ('{sub_topic_title}')")
                        continue

                    if not isinstance(branch, list):
                        add_error(
                            f"Error {branch_context}: Cada rama debe ser una lista de tuplas o una bifurcacion interna."
                        )
                        continue

                    def check_inline_entry(entry, entry_context):
                        if is_inline_fork(entry):
                            forks = entry.get("bifurcaciones") or entry.get("forks")
                            if not isinstance(forks, list) or not forks:
                                add_error(
                                    f"Error {entry_context}: 'bifurcaciones' debe ser una lista con al menos dos ramas."
                                )
                                return
                            if len(forks) < 2:
                                add_error(
                                    f"Error {entry_context}: Se requieren dos o mas bifurcaciones para un nodo de bifurcacion."
                                )
                            if not entry.get("conector"):
                                add_error(
                                    f"Error {entry_context}: Toda bifurcacion debe definir explicitamente un campo 'conector'."
                                )
                            for f_idx, fork_branch in enumerate(forks):
                                fork_context = f"{entry_context} -> Bifurcacion #{f_idx+1}"
                                if not isinstance(fork_branch, list):
                                    add_error(f"Error {fork_context}: Cada bifurcacion debe ser una lista de tuplas.")
                                    continue
                                for sub_e_idx, sub_entry in enumerate(fork_branch):
                                    check_inline_entry(sub_entry, f"{fork_context} -> Elemento #{sub_e_idx+1}")
                                return

                        if not isinstance(entry, (tuple, list)):
                            add_error(
                                f"Error {entry_context}: Cada elemento de una rama debe ser una tupla o una bifurcacion, pero se encontro un {type(entry).__name__}."
                            )
                            return

                        if len(entry) != 2:
                            add_error(
                                f"Error {entry_context}: La tupla {entry} debe tener exactamente 2 elementos (concepto, conector). Se encontraron {len(entry)}."
                            )

                    for e_idx, entry in enumerate(branch):
                        entry_context = f"{branch_context} -> Elemento #{e_idx+1}"
                        check_inline_entry(entry, entry_context)

            check_branch_list(subtitle.get('ramas', []), f"En Grupo '{g_title}' -> Subtitulo '{s_title}'")

    if errors:
        details = "\n".join(f"{idx+1}. {msg}" for idx, msg in enumerate(errors))
        raise ValueError(f"Se encontraron {len(errors)} errores de validacion:\n{details}")


def generar_mapa_conceptual(concept_map_data=None, config=None):
    """Genera el archivo drawio con el concept_map y configuracion indicados."""
    cfg = apply_config(config)
    data = concept_map_data or DEFAULT_CONCEPT_MAP

    if cfg.get("NORMALIZAR_TUPLAS_EXTENSAS", True):
        normalize_extended_tuples_in_concept_map(data)

    validate_concept_map_data(data)

    if not isinstance(data, list) or len(data) == 0:
        raise ValueError("concept_map debe ser una lista con al menos un grupo")

    mxfile, root, add_vertex, add_edge = create_document()

    col_styles = [make_vertex_style(fill, stroke) for fill, stroke in PALETTE]
    edge_styles = [make_edge_style(EDGE_COLOR) for _ in PALETTE]
    palette_len = max(1, len(col_styles))

    main_title_style = make_vertex_style(MAIN_FILL_COLOR, MAIN_STROKE_COLOR)
    subtitle_style = make_vertex_style(SUBTITLE_FILL_COLOR, SUBTITLE_STROKE_COLOR)
    main_edge_style = make_edge_style(EDGE_COLOR)

    def draw_branch(branch, x, start_y, v_style, e_style, subtitle_id, initial_label="", context_path="Rama"):
        y = start_y
        prev_id = subtitle_id
        pending_label = initial_label
        for idx, entry in enumerate(branch):
            if is_inline_fork(entry):
                forks = entry.get("bifurcaciones") or entry.get("forks") or []
                if idx != len(branch) - 1:
                    raise ValueError(f"{context_path}: Las bifurcaciones internas deben ser el último elemento de la rama (elemento #{idx+1}).")

                text = entry.get("texto") or entry.get("titulo") or ""
                connector = entry.get("conector")
                connector_val = connector if connector is not None else pending_label
                if connector_val is None or connector_val == "":
                    raise ValueError(f"{context_path}: Falta el campo 'conector' antes del nodo de bifurcación (elemento #{idx+1}).")

                node_id = add_vertex(text, x, y, style=v_style)
                add_edge(connector_val, prev_id, node_id, style=e_style, place_label_at_target=True)

                total_width = sum(max(1, branch_slot_usage(fork)) for fork in forks) or 1
                start_x = x - (total_width - 1) * X_STEP / 2

                slot_cursor = 0
                for fork_idx, fork_branch in enumerate(forks, start=1):
                    width = max(1, branch_slot_usage(fork_branch))
                    fork_x = start_x + (slot_cursor + (width - 1) / 2) * X_STEP
                    child_context = f"{context_path} -> Bifurcación (elemento #{idx+1}) -> Rama hija #{fork_idx}"
                    # Se pasa el conector de la bifurcacion como etiqueta inicial hacia la primera caja hija.
                    draw_branch(
                        fork_branch,
                        fork_x,
                        y + Y_STEP,
                        v_style,
                        e_style,
                        node_id,
                        initial_label=connector_val,
                        context_path=child_context,
                    )
                    slot_cursor += width
                pending_label = ""
                prev_id = node_id
                y += Y_STEP
                continue

            # La validacion previa garantiza que 'entry' es una tupla de 2 elementos
            text, connector_text = entry
            connector = connector_text if connector_text is not None else ""

            if text is None:
                pending_label = connector
                continue

            node_id = add_vertex(text, x, y, style=v_style)
            add_edge(pending_label, prev_id, node_id, style=e_style, place_label_at_target=True)
            prev_id = node_id
            pending_label = connector
            y += Y_STEP

    def render_concept_map(concept_map_inner):
        start_x = cfg.get("START_X", 120)
        start_y = cfg.get("START_Y", 40)
        current_x = start_x
        color_cursor = 0
        color_by_subtitle = cfg.get("COLOR_SUBTITLE_GROUPS", False)
        color_nested = cfg.get("COLOR_NESTED_SUBTOPICS", False)

        def next_color_idx():
            nonlocal color_cursor
            idx = color_cursor % palette_len
            color_cursor += 1
            return idx

        for group in concept_map_inner:
            subtitles = group.get("subtitulos", [])
            branch_counts = [count_branch_slots(s) for s in subtitles]
            widths = [branch_block_width(count) for count in branch_counts]
            total_width = sum(widths) + SUBTITLE_GAP * max(0, len(subtitles) - 1)

            main_center_x = current_x + total_width / 2
            main_x = main_center_x - BOX_W / 2
            main_title = group.get("titulo_principal", "Tema principal")
            main_id = add_vertex(main_title, main_x, start_y, style=main_title_style)

            subtitle_y = start_y + MAIN_TO_SUBTITLE
            branch_start_y = subtitle_y + SUBTITLE_TO_BRANCH
            cursor_x = current_x

            for subtitle, width, branch_count in zip(subtitles, widths, branch_counts):
                # Selecciona color base para el subtitulo si se agrupan colores por subtitulo.
                subtitle_color_idx = next_color_idx() if color_by_subtitle else None

                sub_center_x = cursor_x + width / 2
                sub_x = sub_center_x - BOX_W / 2
                sub_title = subtitle.get("titulo", "Subtitulo")
                sub_id = add_vertex(sub_title, sub_x, subtitle_y, style=subtitle_style)

                add_edge(
                    subtitle.get("conector", ""),
                    main_id,
                    sub_id,
                    style=main_edge_style,
                    place_label_at_target=True,
                )

                slot_cursor = 0
                for b_idx, branch in enumerate(subtitle.get("ramas", []), start=1):
                    branch_context = f"Grupo '{group.get('titulo_principal', '')}' -> Subtítulo '{sub_title}' -> Rama #{b_idx}"
                    if isinstance(branch, dict) and not is_inline_fork(branch):
                        # Color del sub-tema anidado: propio si se pide, o el del subtitulo (si aplica),
                        # de lo contrario toma el siguiente de la paleta.
                        if color_nested:
                            nested_color_idx = next_color_idx()
                        elif color_by_subtitle:
                            nested_color_idx = subtitle_color_idx
                        else:
                            nested_color_idx = next_color_idx()

                        nested_widths = [max(1, branch_slot_usage(r)) for r in branch.get("ramas", [])]
                        nested_slots = sum(nested_widths) or 1
                        branch_x = cursor_x + (slot_cursor + (nested_slots - 1) / 2) * X_STEP
                        # Los sub-temas anidados se dibujan con el estilo de subtitulo
                        nested_id = add_vertex(branch.get("titulo", "Subtema"), branch_x, branch_start_y, style=subtitle_style)
                        add_edge(
                            branch.get("conector", ""),
                            sub_id,
                            nested_id,
                            style=main_edge_style,
                            place_label_at_target=True,
                        )
                        # Las ramas bajo este sub-tema usan la paleta de colores
                        nested_cursor = slot_cursor
                        for idx, (nested_branch, n_width) in enumerate(zip(branch.get("ramas", []), nested_widths), start=1):
                            v_style = col_styles[nested_color_idx % palette_len]
                            e_style = edge_styles[nested_color_idx % palette_len]
                            nested_x = cursor_x + (nested_cursor + (n_width - 1) / 2) * X_STEP
                            nested_context = f"{branch_context} -> Sub-tema '{branch.get('titulo', 'Subtema')}' -> Rama #{idx}"
                            draw_branch(
                                nested_branch,
                                nested_x,
                                branch_start_y + Y_STEP,
                                v_style,
                                e_style,
                                nested_id,
                                context_path=nested_context,
                            )
                            nested_cursor += n_width
                            # Si no se colorea por subtitulo, los sub-temas anidados pueden compartir color
                            # segun la configuracion anterior; no se avanza aqui porque ya se avanzo en nested_color_idx.
                        if not branch.get("ramas") and not color_by_subtitle and not color_nested:
                            # Avanza para no repetir color en el siguiente elemento secuencial.
                            color_cursor += 1
                        slot_cursor += nested_slots
                    else:
                        width_slots = branch_slot_usage(branch) if isinstance(branch, list) else 1
                        # Las ramas normales usan la paleta de colores
                        if color_by_subtitle:
                            branch_color_idx = subtitle_color_idx
                        else:
                            branch_color_idx = next_color_idx()
                        v_style = col_styles[branch_color_idx % palette_len]
                        e_style = edge_styles[branch_color_idx % palette_len]
                        branch_x = cursor_x + (slot_cursor + (width_slots - 1) / 2) * X_STEP
                        draw_branch(branch, branch_x, branch_start_y, v_style, e_style, sub_id, context_path=branch_context)
                        slot_cursor += width_slots

                cursor_x += width + SUBTITLE_GAP

            current_x += total_width + GROUP_GAP

    render_concept_map(data)

    xml_content = prettify(mxfile)
    if cfg.get("RETURN_XML", False):
        return xml_content

    out_path = resolve_output_path(cfg.get("OUTPUT_FILE", "Mapa_conceptual.drawio"))
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(xml_content)
    return os.path.abspath(out_path).replace("\\", "/")


def cargar_config_externa(module_names=None):
    """Intenta cargar concept_map y CONFIG desde modulos externos conocidos."""
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    names = module_names or [
        "mapa_conceptual_config",
        "vista.mapa_conceptual",
        "codigo.vista.mapa_conceptual",
    ]
    for module_name in names:
        try:
            external = importlib.import_module(module_name)
            return getattr(external, "concept_map", None), getattr(external, "CONFIG", {})
        except ModuleNotFoundError:
            continue
    return None, {}


def main():
    concept_map_data, config = cargar_config_externa()
    try:
        out_path = generar_mapa_conceptual(concept_map_data, config)
        print(f"Mapa conceptual generado en: {out_path}")
    except ValueError as exc:
        # Muestra solo el mensaje amigable (por ejemplo, tuplas mal formadas) sin stacktrace completo.
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
