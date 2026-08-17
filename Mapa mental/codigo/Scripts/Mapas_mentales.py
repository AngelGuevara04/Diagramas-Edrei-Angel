import base64
import importlib
import math
import os
import random
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from PIL import Image

# REQUIERE DE UNA CARPETA "ImagenesMapaMental" CON IMAGENES OPCIONALES
# CADA IMAGEN DEBE TENER NOMBRE SIMILAR AL TEXTO DEL NODO (IGNORANDO MAYUSCULAS,
# MINUSCULAS Y ESPACIOS EXTRAS). FORMATOS SOPORTADOS: .png, .jpg, .jpeg .webp

DEFAULT_CONFIG = {
    "CENTER_X": 800,
    "CENTER_Y": 600,
    "R_STEP": 360,
    # Ajusta el crecimiento radial en los primeros niveles (factor 1.05 = +5%)
    "R_STEP_BOOST": {"levels": 5, "factor": 1.05},
    "CURVED_EDGES": False,
    "EDGE_CONNECTOR_STYLE": "default",  # default | curved_block
    "IMAGE_DIR": Path("ImagenesMapaMental"),
    "IMAGE_WIDTH": 100,
    "IMAGE_HEIGHT": None,
    "TEXT_FONT_SIZE": 14,
    "TEXT_FONT_FAMILY": "Lucida Console",
    "TEXT_FONT_COLOR": "#000000",
    "TEXT_FONT_BORDER_COLOR": "none",
    "TEXT_BG_COLOR": "#FFFFFF",
    "TEXT_STROKE_COLOR": "none",
    "TEXT_STROKE_WIDTH": 1,
    "TEXT_FILL_COLOR": "none",
    "TEXT_BOLD": False,
    "TEXT_ITALIC": True,
    "TEXT_UNDERLINE": False,
    "TEXT_WRAP": False,
    "TEXT_ROUNDED": True,  # Permite ajustar el redondeado de los cuadros de texto
    "TEXT_ARC_SIZE": 10,   # Tamaño de las esquinas redondeadas (0 para esquinas rectas)
    "NODE_WIDTH": 120,
    "NODE_HEIGHT": 60,
    "POSITION_NOISE": 10,
    "EDGE_STROKE_WIDTH": 2,
    "EDGE_COLOR": "#2E21A7",
    "EDGE_CURVE_FACTOR": 0.09,
    # Flechas en ambos extremos de la linea: "none", "block", "classic", etc.
    "EDGE_LEFT_ARROW": "classic",
    "EDGE_RIGHT_ARROW": "block",
    "IMAGE_WIDTH_NOISE": 0.0,  # 0.0 = sin ruido, 0.1 = +/-10% del ancho
    # Offset radial para las imágenes respecto al centro del mapa (px). Positivo = más lejos del centro.
    "IMAGE_RADIUS_OFFSET": 0,
    "IMAGE_TEXT_PADDING": 18,
    "IMAGE_EDGE_PADDING": 10,
    # Paleta opcional: cada subtema principal hereda colores de su entrada.
    # Formato dict: {"fill": "...", "edge": "...", "text": "...", "label_bg": "...", "label_border": "...", "outline": "..."}
    #  - fill: relleno del cuadro de texto
    #  - outline: contorno del cuadro de texto (stroke)
    #  - edge: color de línea que conecta nodos (si no se define usa stroke, luego EDGE_COLOR)
    # Formato tupla: (fill, stroke, edge, text, label_bg, label_border, outline) (elementos posteriores son opcionales)
    "PALETTE": [
        {"fill": "#fff3c4", "edge": "#d97706", "text": "#111827", "outline": "#b45309"},
        {"fill": "#d8ffe5", "edge": "#15803d", "text": "#0f5132", "outline": "#0f5132"},
        {"fill": "#e0eeff", "edge": "#1d4ed8", "text": "#0f172a", "outline": "#1d4ed8"},
        {"fill": "#ffe4e6", "edge": "#be185d", "text": "#831843", "outline": "#be185d"},
    ],
    "USE_PALETTE": True,
    "RANDOM_SEED": 42,
    "OUTPUT_FILE": os.path.join("Mapas", "mapa_mental_radial_prueba.drawio"),
}

DEFAULT_MAPA_EJEMPLO = {
    "Redes de computadoras": {
        "Capas del modelo OSI": {
            "Capa fisica": {
                "Medios de transmision": {
                    "Par trenzado": {},
                    "Fibra optica": {},
                    "Coaxial": {},
                },
                "Codificacion de senal": {
                    "NRZ": {},
                    "Manchester": {},
                },
            },
            "Capa de enlace de datos": {
                "Protocolos": {
                    "Ethernet": {},
                    "PPP": {},
                    "HDLC": {},
                },
                "Control de errores": {
                    "Deteccion": {
                        "CRC": {},
                        "Checksum": {},
                    },
                    "Correccion": {
                        "ARQ": {},
                    },
                },
            },
            "Capa de red": {
                "Protocolos": {
                    "IPv4": {},
                    "IPv6": {},
                },
                "Enrutamiento": {
                    "Estatico": {},
                    "Dinamico": {
                        "RIP": {},
                        "OSPF": {},
                        "EIGRP": {},
                    },
                },
            },
            "Capas superiores": {
                "Transporte": {
                    "TCP": {},
                    "UDP": {},
                },
                "Aplicacion": {
                    "HTTP": {},
                    "DNS": {},
                    "FTP": {},
                    "SMTP": {},
                },
            },
        },
        "Dispositivos de red": {
            "Dispositivos finales": {
                "PC": {},
                "Laptop": {},
                "Smartphone": {},
                "Servidor": {},
            },
            "Dispositivos intermedios": {
                "Switch": {
                    "Conmutacion": {},
                    "Tabla MAC": {},
                },
                "Router": {
                    "Tabla de enrutamiento": {},
                    "Interfaces": {},
                },
                "Access Point": {
                    "Cobertura WiFi": {},
                    "Seguridad inalambrica": {},
                },
                "Firewall": {
                    "Listas de control de acceso": {},
                    "Inspeccion de trafico": {},
                },
            },
        },
        "Tecnologias LAN": {
            "Ethernet": {
                "Topologias": {
                    "Estrella": {},
                    "Bus (historico)": {},
                },
                "Velocidades": {
                    "Fast Ethernet": {},
                    "Gigabit Ethernet": {},
                    "10 Gigabit": {},
                },
            },
            "Redes inalambricas": {
                "Estandares": {
                    "802.11n": {},
                    "802.11ac": {},
                    "802.11ax": {},
                },
                "Seguridad": {
                    "WPA2": {},
                    "WPA3": {},
                },
            },
            "Segmentacion": {
                "VLAN": {
                    "VLAN por departamento": {},
                    "VLAN por funcion": {},
                },
                "Trunking": {
                    "802.1Q": {},
                },
            },
        },
        "Tecnologias WAN": {
            "Enlaces dedicados": {
                "Fibra oscura": {},
                "Enlaces punto a punto": {},
            },
            "Tecnologias clasicas": {
                "Frame Relay": {},
                "ATM": {},
            },
            "VPN": {
                "VPN sitio a sitio": {},
                "VPN de acceso remoto": {},
                "Tuneles": {
                    "IPsec": {},
                    "SSL": {},
                },
            },
            "Redes modernas": {
                "MPLS": {},
                "SD-WAN": {},
                "Enlaces satelitales": {},
            },
        },
        "Seguridad": {
            "Amenazas": {
                "Malware": {
                    "Virus": {},
                    "Ransomware": {},
                },
                "Ataques de red": {
                    "DoS/DDoS": {},
                    "Man-in-the-middle": {},
                    "Phishing": {},
                },
            },
            "Mecanismos de proteccion": {
                "Autenticacion": {
                    "Contrasenas seguras": {},
                    "Doble factor": {},
                },
                "Cifrado": {
                    "TLS/SSL": {},
                    "VPN cifradas": {},
                },
                "Segmentacion": {
                    "DMZ": {},
                    "VLAN de seguridad": {},
                },
            },
            "Politicas": {
                "Politica de contrasenas": {},
                "Uso aceptable de la red": {},
                "Respaldos": {},
            },
        },
        "Herramientas y monitoreo": {
            "Herramientas de diagnostico": {
                "ping": {},
                "traceroute": {},
                "ipconfig/ifconfig": {},
            },
            "Monitoreo": {
                "SNMP": {},
                "Syslog": {},
                "NetFlow": {},
            },
            "Simulacion y practica": {
                "Cisco Packet Tracer": {},
                "GNS3": {},
                "Wireshark": {},
            },
        },
    }
}


def apply_config(config=None):
    """Carga configuracion externa sobre los valores por defecto y reconstruye estilos."""
    cfg = dict(DEFAULT_CONFIG)
    if config:
        cfg.update(config)

    seed = cfg.get("RANDOM_SEED")
    if seed is not None:
        random.seed(seed)

    # Normaliza ruta de imagenes
    image_dir = cfg.get("IMAGE_DIR", DEFAULT_CONFIG["IMAGE_DIR"])
    if isinstance(image_dir, str):
        cfg["IMAGE_DIR"] = Path(image_dir)

    globals().update(cfg)
    rebuild_styles(cfg)
    return cfg


def build_label_style(cfg, colors=None):
    """Construye el estilo de etiqueta usando overrides de color opcionales."""
    colors = colors or {}
    rounded_flag = "1" if cfg.get("TEXT_ROUNDED", True) else "0"
    arc_size = cfg.get("TEXT_ARC_SIZE")
    arc_part = f"arcSize={arc_size};" if arc_size is not None else ""

    stroke_color = colors.get("stroke", cfg["TEXT_STROKE_COLOR"])
    fill_color = colors.get("fill", cfg["TEXT_FILL_COLOR"])
    font_color = colors.get("text", cfg["TEXT_FONT_COLOR"])
    bg_color = colors.get("label_bg", cfg["TEXT_BG_COLOR"])
    border_color = colors.get("label_border", cfg["TEXT_FONT_BORDER_COLOR"])

    base_style = (
        f"align=center;verticalAlign=middle;"
        f"strokeColor={stroke_color};strokeWidth={cfg['TEXT_STROKE_WIDTH']};"
        f"fillColor={fill_color};fontSize={cfg['TEXT_FONT_SIZE']};"
        f"fontColor={font_color};fontFamily={cfg['TEXT_FONT_FAMILY']};"
        f"fontStyle={build_font_style(cfg)};labelBackgroundColor={bg_color};"
        f"labelBorderColor={border_color};"
    )

    if cfg['TEXT_WRAP']:
        return (
            f"shape=rectangle;rounded={rounded_flag};{arc_part}whiteSpace=wrap;html=1;{base_style}"
        )
    return f"shape=label;{base_style}"


def build_palette_styles(cfg):
    """Genera estilos preconstruidos para cada entrada de la paleta."""
    if not cfg.get("USE_PALETTE", True):
        return []
    styles = []
    palette_cfg = cfg.get("PALETTE") or []
    for entry in palette_cfg:
        fill = stroke = edge_color = text = label_bg = label_border = outline = None
        if isinstance(entry, dict):
            fill = entry.get("fill")
            stroke = entry.get("stroke")
            edge_color = entry.get("edge")
            text = entry.get("text")
            label_bg = entry.get("label_bg")
            label_border = entry.get("label_border")
            outline = entry.get("outline") or entry.get("border")
        elif isinstance(entry, (list, tuple)):
            fill = entry[0] if len(entry) > 0 else None
            stroke = entry[1] if len(entry) > 1 else None
            edge_color = entry[2] if len(entry) > 2 else None
            text = entry[3] if len(entry) > 3 else None
            label_bg = entry[4] if len(entry) > 4 else None
            label_border = entry[5] if len(entry) > 5 else None
            outline = entry[6] if len(entry) > 6 else None

        label_stroke = outline or stroke or cfg["TEXT_STROKE_COLOR"]
        overrides = {
            "fill": fill or cfg["TEXT_FILL_COLOR"],
            "stroke": label_stroke,
            "edge": edge_color or stroke or cfg["EDGE_COLOR"],
            "text": text or cfg["TEXT_FONT_COLOR"],
            "label_bg": label_bg or cfg["TEXT_BG_COLOR"],
            "label_border": label_border or cfg["TEXT_FONT_BORDER_COLOR"],
        }

        label_style = build_label_style(cfg, overrides)
        edge_style = build_edge_style(cfg, overrides["edge"])
        styles.append({"label": label_style, "edge": edge_style})
    return styles


def rebuild_styles(cfg):
    global LABEL_STYLE, EDGE_STYLE, PALETTE_STYLES

    LABEL_STYLE = build_label_style(cfg)
    EDGE_STYLE = build_edge_style(cfg)
    PALETTE_STYLES = build_palette_styles(cfg)


def build_font_style(cfg):
    """Devuelve el flag fontStyle de mxGraph combinando negrita/italica/subrayado."""
    style = 0
    if cfg["TEXT_BOLD"]:
        style |= 1
    if cfg["TEXT_ITALIC"]:
        style |= 2
    if cfg["TEXT_UNDERLINE"]:
        style |= 4
    return style


def estimate_text_width(text, font_size, font_family):
    """Estima el ancho de un texto basado en la fuente y tamano."""
    if not text:
        return 0
    # El factor de ajuste depende de la fuente. 0.62 es una buena aproximacion
    # para fuentes monoespaciadas como Lucida Console o Courier New.
    # Para fuentes proporcionales, se necesitaria un calculo mas complejo.
    is_monospaced = "console" in font_family.lower() or "courier" in font_family.lower()
    factor = 0.62 if is_monospaced else 0.5  # 0.5 es una conjetura para proporcionales
    return len(text) * font_size * factor


def estimate_text_height(text, width, font_size, font_family):
    """Estima la altura requerida para un texto dado un ancho fijo."""
    if not text:
        return 0

    words = text.split()
    if not words:
        return font_size * 1.2 + 20

    # Restar padding horizontal del ancho disponible para el texto
    text_width = width - 20
    lines = 1
    current_line_width = 0
    space_width = estimate_text_width(" ", font_size, font_family)

    for word in words:
        word_width = estimate_text_width(word, font_size, font_family)
        if current_line_width + word_width <= text_width:
            current_line_width += word_width + space_width
        else:
            lines += 1
            current_line_width = word_width + space_width
    
    # La altura de linea es aprox. 1.2 * tamano de fuente. Anadir padding vertical.
    line_height = font_size * 1.2
    estimated_height = lines * line_height + 20  # 10px padding superior e inferior
    return estimated_height


def build_edge_style(cfg, edge_color=None):
    """Arma el estilo de la linea segun la configuracion de curvas."""
    color = edge_color if edge_color is not None else cfg["EDGE_COLOR"]
    base = f"strokeWidth={cfg['EDGE_STROKE_WIDTH']};strokeColor={color};"

    left_arrow = cfg.get("EDGE_LEFT_ARROW", "none")
    right_arrow = cfg.get("EDGE_RIGHT_ARROW", "none")
    arrows = f"startArrow={left_arrow};endArrow={right_arrow};"

    # Estilo inspirado en el conector curvo de prueba.drawio
    if cfg.get("EDGE_CONNECTOR_STYLE") == "curved_block":
        return f"curved=1;rounded=0;{arrows}{base}"

    curved = "1" if cfg["CURVED_EDGES"] else "0"
    rounded = "0" if cfg["CURVED_EDGES"] else "1"
    if cfg["CURVED_EDGES"]:
        return f"edgeStyle=orthogonalEdgeStyle;curved={curved};rounded={rounded};{arrows}{base}"
    return f"curved={curved};rounded={rounded};{arrows}{base}"


# Inicializa estilos con defaults
apply_config()


def resolve_output_path(path_like) -> str:
    """Devuelve la ruta absoluta para OUTPUT_FILE y crea la carpeta destino."""
    project_root = Path(__file__).resolve().parent.parent
    candidate = Path(path_like)
    out_path = candidate if candidate.is_absolute() else project_root / candidate
    out_path.parent.mkdir(parents=True, exist_ok=True)
    return str(out_path)


def normalize_label(label):
    """Limpia y normaliza una etiqueta para que coincida con un nombre de archivo."""
    # Reemplaza caracteres no validos en nombres de archivo con un guion
    sanitized = re.sub(r'[\\/:\*\?"<>\|]', '-', label)
    # Normaliza espacios y convierte a minusculas
    return " ".join(sanitized.split()).casefold()


def file_to_data_uri(path: Path):
    """Convierte un archivo de imagen en data URI para draw.io."""
    ext = path.suffix.lower()
    if ext not in {".png", ".jpg", ".jpeg", '.webp'}:
        return None
    mime = "image/png" if ext == ".png" else "image/jpeg"
    data_b64 = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{data_b64}"


def load_images_map(cfg):
    if "IMAGES_URL_MAP" in cfg:
        return cfg["IMAGES_URL_MAP"]
    images = {}
    folder = Path(cfg["IMAGE_DIR"])
    if not folder.is_dir():
        return images
    allowed = {".png", ".jpg", ".jpeg", '.webp'}
    for path in folder.iterdir():
        if path.suffix.lower() in allowed:
            key = normalize_label(path.stem)
            uri = file_to_data_uri(path)
            if not uri:
                continue
            try:
                with Image.open(path) as im:
                    w, h = im.size
                if cfg["IMAGE_HEIGHT"] is not None:
                    target_h = cfg["IMAGE_HEIGHT"]
                else:
                    target_h = int(round(h * (cfg["IMAGE_WIDTH"] / w))) if w else h
            except Exception:
                target_h = cfg["IMAGE_HEIGHT"] if cfg["IMAGE_HEIGHT"] is not None else cfg["IMAGE_WIDTH"]
            images[key] = {"uri": uri.replace(";", "%3B"), "height": target_h}
    return images


class IdGen:
    def __init__(self, start=2):
        self.current = start

    def next(self):
        self.current += 1
        return str(self.current)


class Node:
    def __init__(self, label, depth):
        self.label = label
        self.depth = depth
        self.children = []
        self.angle = 0.0


def dict_to_nodes(label, children_dict, depth=0):
    """Convierte el dict anidado en un arbol de Node."""
    node = Node(label, depth)
    if isinstance(children_dict, dict):
        for child_label, grand_children in children_dict.items():
            if not isinstance(grand_children, dict):
                grand_children = {}
            child_node = dict_to_nodes(child_label, grand_children, depth + 1)
            node.children.append(child_node)
    return node


def assign_angles_subtree(node, start_angle, end_angle):
    """Asigna angulos dentro de un sector [start_angle, end_angle]."""
    if not node.children:
        node.angle = (start_angle + end_angle) / 2.0
        return
    k = len(node.children)
    sector = (end_angle - start_angle) / k
    for i, child in enumerate(node.children):
        child_start = start_angle + i * sector
        child_end = child_start + sector
        assign_angles_subtree(child, child_start, child_end)
    node.angle = sum(c.angle for c in node.children) / k


def assign_angles_radial(root_node):
    """Distribuye cada rama principal alrededor de la raiz."""
    if not root_node.children:
        root_node.angle = 0.0
        return
    n = len(root_node.children)
    angle_step = 2 * math.pi / n
    base = -math.pi / 2.0
    for i, child in enumerate(root_node.children):
        start = base + i * angle_step
        end = start + angle_step
        assign_angles_subtree(child, start, end)
    root_node.angle = 0.0


def compute_vertex_geometry(label, x, y):
    width = NODE_WIDTH if TEXT_WRAP else 15
    height = NODE_HEIGHT if TEXT_WRAP else 15

    if TEXT_WRAP:
        words = str(label).split()
        longest_word = max(words, key=len) if words else ""
        estimated_width = estimate_text_width(longest_word, TEXT_FONT_SIZE, TEXT_FONT_FAMILY) + 20
        width = max(width, estimated_width)
        estimated_height = estimate_text_height(label, width, TEXT_FONT_SIZE, TEXT_FONT_FAMILY)
        height = max(height, estimated_height)

    pos_x = x - width / 2
    pos_y = y - height / 2
    return {"x": pos_x, "y": pos_y, "width": width, "height": height}


def add_vertex(root_xml, node_id, label, x, y, label_style):
    geom_data = compute_vertex_geometry(label, x, y)
    cell = ET.SubElement(
        root_xml,
        "mxCell",
        id=node_id,
        value=label,
        style=label_style,
        vertex="1",
        parent="1",
    )
    geom = ET.SubElement(
        cell,
        "mxGeometry",
        x=str(geom_data["x"]),
        y=str(geom_data["y"]),
        width=str(geom_data["width"]),
        height=str(geom_data["height"]),
    )
    geom.set("as", "geometry")


def add_image(root_xml, node_id, x, y, image_uri, width, height):
    cell = ET.SubElement(
        root_xml,
        "mxCell",
        id=node_id,
        style=(
            "shape=image;imageAspect=1;"
            "verticalAlign=middle;horizontalAlign=center;"
            f"image={image_uri};"
        ),
        vertex="1",
        parent="1",
    )
    geom = ET.SubElement(
        cell,
        "mxGeometry",
        x=str(float(x)),
        y=str(float(y)),
        width=str(width),
        height=str(height),
    )
    geom.set("as", "geometry")


def compute_image_width(base_width, cfg):
    noise_level = cfg.get("IMAGE_WIDTH_NOISE", 0.0) or 0.0
    if noise_level > 0:
        factor = 1.0 + random.uniform(-noise_level, noise_level)
        return max(1, int(round(base_width * factor)))
    return base_width


def build_image_anchor(x, y, cfg):
    """Calcula un ancla radial para la imagen, manteniendo el offset configurado."""
    offset = cfg.get("IMAGE_RADIUS_OFFSET", 0) or 0
    if offset == 0:
        return float(x), float(y)

    dx = x - cfg.get("CENTER_X", 0)
    dy = y - cfg.get("CENTER_Y", 0)
    dist = math.hypot(dx, dy)
    if dist > 0:
        x += dx / dist * offset
        y += dy / dist * offset
    return float(x), float(y)


def add_edge(root_xml, edge_id, source_id, target_id, edge_style, control_points=None):
    cell = ET.SubElement(
        root_xml,
        "mxCell",
        id=edge_id,
        style=edge_style,
        edge="1",
        parent="1",
        source=source_id,
        target=target_id,
    )
    geom = ET.SubElement(cell, "mxGeometry", relative="1")
    geom.set("as", "geometry")

    # Si hay puntos de control, los agregamos como Array -> mxPoint
    if control_points:
        arr = ET.SubElement(geom, "Array", as_="points")  # as="points" en XML
        # xml.etree no permite atributo 'as', así que usamos as_ y luego corregimos:
        arr.attrib["as"] = "points"
        for (px, py) in control_points:
            ET.SubElement(arr, "mxPoint", x=str(px), y=str(py))


def rects_overlap(a, b, padding=0.0):
    return not (
        a["x"] + a["w"] + padding <= b["x"]
        or b["x"] + b["w"] + padding <= a["x"]
        or a["y"] + a["h"] + padding <= b["y"]
        or b["y"] + b["h"] + padding <= a["y"]
    )


def distance_point_to_segment(px, py, x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if dx == 0 and dy == 0:
        return math.hypot(px - x1, py - y1)
    t = ((px - x1) * dx + (py - y1) * dy) / float(dx * dx + dy * dy)
    t = max(0.0, min(1.0, t))
    proj_x = x1 + t * dx
    proj_y = y1 + t * dy
    return math.hypot(px - proj_x, py - proj_y)


def distance_rect_to_segment(rect, segment):
    x, y, w, h = rect["x"], rect["y"], rect["w"], rect["h"]
    x1, y1, x2, y2 = segment
    corners = [(x, y), (x + w, y), (x, y + h), (x + w, y + h)]
    distances = [distance_point_to_segment(px, py, x1, y1, x2, y2) for px, py in corners]
    center_x = x + w / 2.0
    center_y = y + h / 2.0
    distances.append(distance_point_to_segment(center_x, center_y, x1, y1, x2, y2))
    return min(distances)


def edge_to_segments(x1, y1, x2, y2, control_points=None):
    if not control_points:
        return [(x1, y1, x2, y2)]
    segments = []
    prev_x, prev_y = x1, y1
    for ctrl_x, ctrl_y in control_points:
        segments.append((prev_x, prev_y, ctrl_x, ctrl_y))
        prev_x, prev_y = ctrl_x, ctrl_y
    segments.append((prev_x, prev_y, x2, y2))
    return segments


def normalize_vector(dx, dy):
    dist = math.hypot(dx, dy)
    if dist <= 1e-9:
        return (1.0, 0.0)
    return (dx / dist, dy / dist)


def choose_image_position(
    x,
    y,
    node_bbox,
    width,
    height,
    cfg,
    occupied_text_boxes,
    occupied_image_boxes,
    edge_segments,
):
    text_padding = float(cfg.get("IMAGE_TEXT_PADDING", 18) or 18)
    edge_padding = float(cfg.get("IMAGE_EDGE_PADDING", 10) or 10)

    anchor_x, anchor_y = build_image_anchor(x, y, cfg)
    anchor_center = (anchor_x + width / 2.0, anchor_y + height / 2.0)

    radial = normalize_vector(
        anchor_center[0] - cfg.get("CENTER_X", 0),
        anchor_center[1] - cfg.get("CENTER_Y", 0),
    )
    tangential = (-radial[1], radial[0])

    node_radius = max(node_bbox["w"], node_bbox["h"]) / 2.0
    image_radius = max(width, height) / 2.0
    base_gap = node_radius + image_radius + text_padding

    def as_rect(top_left_x, top_left_y):
        return {"x": float(top_left_x), "y": float(top_left_y), "w": float(width), "h": float(height)}

    candidates = [as_rect(anchor_x, anchor_y), as_rect(anchor_x - width / 2.0, anchor_y - height / 2.0)]

    direction_vectors = [
        radial,
        tangential,
        (-tangential[0], -tangential[1]),
        (-radial[0], -radial[1]),
        normalize_vector(radial[0] + tangential[0], radial[1] + tangential[1]),
        normalize_vector(radial[0] - tangential[0], radial[1] - tangential[1]),
    ]
    for ring in (1.0, 1.6, 2.2):
        jump = base_gap * ring
        for dx, dy in direction_vectors:
            center_x = anchor_center[0] + dx * jump
            center_y = anchor_center[1] + dy * jump
            candidates.append(as_rect(center_x - width / 2.0, center_y - height / 2.0))

    best_rect = None
    best_score = None
    for rect in candidates:
        text_hits = sum(1 for box in occupied_text_boxes if rects_overlap(rect, box, text_padding))
        image_hits = sum(1 for box in occupied_image_boxes if rects_overlap(rect, box, text_padding * 0.5))
        edge_hits = sum(1 for seg in edge_segments if distance_rect_to_segment(rect, seg) < edge_padding)
        dist_penalty = math.hypot(
            (rect["x"] + rect["w"] / 2.0) - anchor_center[0],
            (rect["y"] + rect["h"] / 2.0) - anchor_center[1],
        )
        score = text_hits * 1000 + image_hits * 700 + edge_hits * 500 + dist_penalty * 0.01
        if best_score is None or score < best_score:
            best_score = score
            best_rect = rect
        if score == 0:
            break

    assert best_rect is not None
    return best_rect


def compute_curve_control_point(px, py, cx, cy, cfg):
    """
    Calcula un punto de control para un arco entre (px, py) y (cx, cy)
    de forma que la curva se incline hacia afuera del centro.
    """
    dx = cx - px
    dy = cy - py
    dist = math.hypot(dx, dy)
    if dist == 0:
        return None

    # Punto medio del segmento
    mx = (px + cx) / 2.0
    my = (py + cy) / 2.0

    # Vector perpendicular a la arista
    nx = -dy
    ny = dx
    nlen = math.hypot(nx, ny)
    if nlen == 0:
        return None
    nx /= nlen
    ny /= nlen

    # Queremos que la curva salga hacia afuera del centro del mapa
    cx_vec = mx - cfg["CENTER_X"]
    cy_vec = my - cfg["CENTER_Y"]
    dot = nx * cx_vec + ny * cy_vec
    # Si apunta hacia adentro, invertimos
    if dot < 0:
        nx = -nx
        ny = -ny

    # Factor de curvatura definido en la configuracion
    curve_factor = cfg["EDGE_CURVE_FACTOR"]
    offset = curve_factor * dist

    ctrl_x = mx + nx * offset
    ctrl_y = my + ny * offset
    return (ctrl_x, ctrl_y)


def compute_radial_distance(depth, cfg):
    """Devuelve la distancia radial para un nivel, considerando el boost configurable."""
    if depth <= 0:
        return 0
    base_step = cfg["R_STEP"]
    boost_cfg = cfg.get("R_STEP_BOOST") or {}
    boost_levels = boost_cfg.get("levels", 0) or 0
    boost_factor = boost_cfg.get("factor", 1.0) or 1.0
    step = base_step * (boost_factor if depth <= boost_levels else 1.0)
    return step * depth


def place_nodes_and_edges(root_node, root_xml, idgen, images_map, cfg):
    """Crea las celdas de draw.io recorriendo el arbol."""

    uses_curved_block = cfg.get("EDGE_CONNECTOR_STYLE") == "curved_block"
    use_palette = cfg.get("USE_PALETTE", True)
    palette_styles = globals().get("PALETTE_STYLES", []) if use_palette else []
    occupied_text_boxes = []
    occupied_image_boxes = []
    edge_segments = []

    def _rec(node, parent_id=None, parent_pos=None, label_style=None, edge_style=None):
        node_label_style = label_style or LABEL_STYLE
        node_edge_style = edge_style or EDGE_STYLE
        node_id = idgen.next()

        # Posicion del nodo
        if node.depth == 0:
            x, y = cfg["CENTER_X"], cfg["CENTER_Y"]
        else:
            r = compute_radial_distance(node.depth, cfg)
            x = cfg["CENTER_X"] + r * math.cos(node.angle)
            y = cfg["CENTER_Y"] + r * math.sin(node.angle)

            # Ruido para look mas organico
            if cfg["POSITION_NOISE"] > 0:
                noise_amount = cfg["POSITION_NOISE"]
                x += random.uniform(-noise_amount / 2, noise_amount / 2)
                y += random.uniform(-noise_amount / 2, noise_amount / 2)

        # Si hay padre, creamos arista
        if parent_id is not None:
            edge_id = idgen.next()
            control_points = None

            # Solo calculamos curva si el estilo es curvo
            if "curved=1" in node_edge_style:
                if uses_curved_block:
                    ctrl = compute_curve_control_point(
                        parent_pos[0], parent_pos[1],
                        x, y,
                        cfg
                    )
                    if ctrl is not None:
                        control_points = [ctrl]
                # Para CURVED_EDGES (no curved_block) evitamos anadir el punto de control extra

            add_edge(root_xml, edge_id, parent_id, node_id, node_edge_style, control_points)
            edge_segments.extend(edge_to_segments(parent_pos[0], parent_pos[1], x, y, control_points))

        vertex_geom = compute_vertex_geometry(node.label, x, y)
        current_text_box = {
            "x": float(vertex_geom["x"]),
            "y": float(vertex_geom["y"]),
            "w": float(vertex_geom["width"]),
            "h": float(vertex_geom["height"]),
        }
        occupied_text_boxes.append(current_text_box)

        # Recorremos hijos, pasando nuestra posicion como parent_pos
        for idx, child in enumerate(node.children):
            child_label_style = node_label_style
            child_edge_style = node_edge_style
            if node.depth == 0 and palette_styles:
                palette_entry = palette_styles[idx % len(palette_styles)]
                child_label_style = palette_entry["label"]
                child_edge_style = palette_entry["edge"]
            _rec(child, node_id, (x, y), child_label_style, child_edge_style)

        # Imagen opcional
        img_info = images_map.get(normalize_label(node.label))
        if img_info:
            img_id = idgen.next()
            image_width = compute_image_width(cfg["IMAGE_WIDTH"], cfg)
            image_height = float(img_info["height"])
            selected_rect = choose_image_position(
                x=x,
                y=y,
                node_bbox=current_text_box,
                width=image_width,
                height=image_height,
                cfg=cfg,
                occupied_text_boxes=occupied_text_boxes,
                occupied_image_boxes=occupied_image_boxes,
                edge_segments=edge_segments,
            )
            occupied_image_boxes.append(selected_rect)
            add_image(
                root_xml,
                img_id,
                selected_rect["x"],
                selected_rect["y"],
                img_info["uri"],
                image_width,
                image_height,
            )

        # Nodo de texto
        add_vertex(root_xml, node_id, node.label, x, y, node_label_style)

    _rec(root_node, label_style=LABEL_STYLE, edge_style=EDGE_STYLE)



def crear_drawio_desde_arbol_radial(arbol, nombre_archivo, cfg):
    """
    arbol: dict con un solo elemento raiz.
    """
    if len(arbol) != 1:
        raise ValueError("El arbol debe tener exactamente un titulo principal.")

    root_title, root_children = next(iter(arbol.items()))
    root_node = dict_to_nodes(root_title, root_children, depth=0)
    assign_angles_radial(root_node)

    mxfile = ET.Element("mxfile", host="app.diagrams.net")
    diagram = ET.SubElement(mxfile, "diagram", id="diagram1", name="Pagina-1")
    model = ET.SubElement(
        diagram,
        "mxGraphModel",
        dx="1000",
        dy="1000",
        grid="1",
        gridSize="10",
        guides="1",
        tooltips="1",
        connect="1",
        arrows="1",
        fold="1",
        page="1",
        pageScale="1",
        pageWidth="1600",
        pageHeight="1200",
        math="0",
        shadow="0",
    )
    root_xml = ET.SubElement(model, "root")
    ET.SubElement(root_xml, "mxCell", id="0")
    ET.SubElement(root_xml, "mxCell", id="1", parent="0")

    idgen = IdGen(start=2)
    images_map = load_images_map(cfg)
    place_nodes_and_edges(root_node, root_xml, idgen, images_map, cfg)

    xml_bytes = ET.tostring(mxfile, encoding="utf-8", xml_declaration=True)
    if cfg.get("RETURN_XML", False):
        return ET.tostring(mxfile, encoding="unicode")
    with open(nombre_archivo, "wb") as f:
        f.write(xml_bytes)
    return os.path.abspath(nombre_archivo).replace("\\", "/")


def generar_mapa_mental(mapa=None, config=None):
    """Genera el .drawio a partir de mapa (dict) y config (dict)."""
    cfg = apply_config(config)
    mapa_data = mapa or DEFAULT_MAPA_EJEMPLO
    if not isinstance(mapa_data, dict) or len(mapa_data) != 1:
        raise ValueError("mapa debe ser un dict con un unico titulo principal.")
    out_path = resolve_output_path(cfg["OUTPUT_FILE"])
    return crear_drawio_desde_arbol_radial(mapa_data, out_path, cfg)


def cargar_config_externa(module_name="mapa_mental_config"):
    """Intenta cargar mapa_ejemplo y CONFIG desde un modulo externo en la carpeta raiz."""
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    try:
        external = importlib.import_module(module_name)
    except ModuleNotFoundError:
        return None, {}
    return getattr(external, "mapa_ejemplo", None), getattr(external, "CONFIG", {})


def main():
    mapa_ext, cfg_ext = cargar_config_externa()
    out_path = generar_mapa_mental(mapa_ext, cfg_ext)
    print(f"Mapa mental generado en: {out_path}")


if __name__ == "__main__":
    main()
