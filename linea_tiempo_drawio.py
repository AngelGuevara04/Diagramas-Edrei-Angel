from __future__ import annotations

import argparse
import base64
import json
import mimetypes
from dataclasses import dataclass
from pathlib import Path
import xml.etree.ElementTree as ET

from utilidades.imagenes import descargar_imagen_bing, is_valid_image_file, sanitize_filename

VALID_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp")


@dataclass
class TimelinePoint:
    title: str
    date: str = ""
    query: str = ""


@dataclass
class TimelineImage:
    path: Path | None
    downloaded: bool


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Genera una linea del tiempo en .drawio a partir de puntos importantes, "
            "descargando imagenes desde Bing."
        )
    )
    parser.add_argument(
        "--input",
        help="Archivo de entrada (.txt o .json).",
    )
    parser.add_argument(
        "--points",
        help="Puntos inline separados por ';'. Formato por punto: 'fecha|titulo|query' o solo 'titulo'.",
    )
    parser.add_argument(
        "--output",
        default="linea_tiempo.drawio",
        help="Ruta del archivo .drawio de salida.",
    )
    parser.add_argument(
        "--images-dir",
        default="linea_tiempo_imagenes",
        help="Directorio donde se guardan las imagenes descargadas.",
    )
    parser.add_argument(
        "--suffix",
        default="icono",
        help="Sufijo extra para mejorar la busqueda en Bing (ej: 'icono', 'foto historica').",
    )
    parser.add_argument(
        "--no-download",
        action="store_true",
        help="No descarga imagenes; solo usa las que ya existan en --images-dir.",
    )
    return parser.parse_args()


def parse_point_text(raw: str) -> TimelinePoint | None:
    text = str(raw or "").strip()
    if not text:
        return None

    parts = [part.strip() for part in text.split("|")]
    if len(parts) == 1:
        return TimelinePoint(title=parts[0], date="", query="")
    if len(parts) == 2:
        return TimelinePoint(title=parts[1], date=parts[0], query="")
    return TimelinePoint(title=parts[1], date=parts[0], query=parts[2])


def load_points_from_txt(path: Path) -> list[TimelinePoint]:
    points: list[TimelinePoint] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        point = parse_point_text(line)
        if point and point.title:
            points.append(point)
    return points


def load_points_from_json(path: Path) -> list[TimelinePoint]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    out: list[TimelinePoint] = []

    if isinstance(payload, list):
        for item in payload:
            if isinstance(item, str):
                point = parse_point_text(item)
                if point and point.title:
                    out.append(point)
                continue
            if isinstance(item, dict):
                title = str(item.get("title") or "").strip()
                if not title:
                    continue
                date = str(item.get("date") or "").strip()
                query = str(item.get("query") or "").strip()
                out.append(TimelinePoint(title=title, date=date, query=query))
    else:
        raise ValueError("El JSON debe ser una lista de strings o objetos.")

    return out


def load_points(args: argparse.Namespace) -> list[TimelinePoint]:
    if args.points:
        out: list[TimelinePoint] = []
        for piece in str(args.points).split(";"):
            point = parse_point_text(piece)
            if point and point.title:
                out.append(point)
        return out

    if not args.input:
        raise ValueError("Debes indicar --input o --points.")

    input_path = Path(args.input)
    if not input_path.exists():
        raise FileNotFoundError(f"No existe el archivo de entrada: {input_path}")

    ext = input_path.suffix.lower()
    if ext == ".json":
        return load_points_from_json(input_path)
    return load_points_from_txt(input_path)


def find_existing_image(images_dir: Path, stem: str) -> Path | None:
    base = images_dir / stem
    for ext in VALID_EXTENSIONS:
        candidate = base.with_suffix(ext)
        if candidate.exists() and is_valid_image_file(candidate):
            return candidate

    for candidate in images_dir.glob(f"{stem}.*"):
        if candidate.suffix.lower() in VALID_EXTENSIONS and is_valid_image_file(candidate):
            return candidate
    return None


def resolve_query(point: TimelinePoint, suffix: str) -> str:
    base = point.query.strip() if point.query.strip() else point.title.strip()
    suffix_text = str(suffix or "").strip()
    if suffix_text:
        return f"{base} {suffix_text}".strip()
    return base


def ensure_images(
    points: list[TimelinePoint], images_dir: Path, suffix: str, no_download: bool
) -> list[TimelineImage]:
    images_dir.mkdir(parents=True, exist_ok=True)
    results: list[TimelineImage] = []

    for idx, point in enumerate(points, start=1):
        stem = f"{idx:02d}_{sanitize_filename(point.title, fallback=f'evento_{idx:02d}')[:90]}"
        existing = find_existing_image(images_dir, stem)
        if existing is not None:
            results.append(TimelineImage(path=existing, downloaded=False))
            continue

        if no_download:
            results.append(TimelineImage(path=None, downloaded=False))
            continue

        query = resolve_query(point, suffix)
        downloaded_ok = descargar_imagen_bing(query, stem, str(images_dir))
        found = find_existing_image(images_dir, stem) if downloaded_ok else None
        results.append(TimelineImage(path=found, downloaded=bool(found)))

    return results


def data_uri_for_image(path: Path) -> str:
    mime, _ = mimetypes.guess_type(str(path))
    if not mime:
        ext = path.suffix.lower()
        if ext in (".jpg", ".jpeg"):
            mime = "image/jpeg"
        elif ext == ".png":
            mime = "image/png"
        elif ext == ".webp":
            mime = "image/webp"
        else:
            mime = "application/octet-stream"

    raw = path.read_bytes()
    encoded = base64.b64encode(raw).decode("ascii")
    # draw.io stores embedded images in styles as image=data:image/png,<base64>
    # instead of the standard data URI form with ;base64.
    return f"data:{mime},{encoded}"


def new_cell(root_xml: ET.Element, *, cell_id: int, **attrs: str) -> ET.Element:
    attr = {"id": str(cell_id)}
    attr.update({k: str(v) for k, v in attrs.items()})
    return ET.SubElement(root_xml, "mxCell", attr)


def add_vertex(
    root_xml: ET.Element,
    *,
    cell_id: int,
    value: str,
    style: str,
    x: float,
    y: float,
    width: float,
    height: float,
) -> ET.Element:
    cell = new_cell(
        root_xml,
        cell_id=cell_id,
        value=value,
        style=style,
        vertex="1",
        parent="1",
    )
    ET.SubElement(
        cell,
        "mxGeometry",
        {
            "x": str(round(x, 2)),
            "y": str(round(y, 2)),
            "width": str(round(width, 2)),
            "height": str(round(height, 2)),
            "as": "geometry",
        },
    )
    return cell


def add_edge(
    root_xml: ET.Element,
    *,
    cell_id: int,
    source: int,
    target: int,
    style: str,
) -> ET.Element:
    cell = new_cell(
        root_xml,
        cell_id=cell_id,
        value="",
        style=style,
        edge="1",
        parent="1",
        source=str(source),
        target=str(target),
    )
    ET.SubElement(cell, "mxGeometry", {"relative": "1", "as": "geometry"})
    return cell


def build_drawio(points: list[TimelinePoint], images: list[TimelineImage], output_file: Path) -> None:
    n = len(points)
    if n == 0:
        raise ValueError("No hay puntos para generar la linea del tiempo.")

    spacing = 220
    margin_x = 150
    axis_y = 270
    label_w = 190
    label_h = 82
    img_w = 150
    img_h = 100

    first_x = margin_x
    last_x = margin_x + (n - 1) * spacing
    page_width = max(1800, last_x + 240)
    page_height = 760

    mxfile = ET.Element("mxfile", host="app.diagrams.net")
    diagram = ET.SubElement(mxfile, "diagram", id="timeline-1", name="Linea de tiempo")
    mx_graph = ET.SubElement(
        diagram,
        "mxGraphModel",
        {
            "dx": "1600",
            "dy": "900",
            "grid": "1",
            "gridSize": "10",
            "guides": "1",
            "tooltips": "1",
            "connect": "1",
            "arrows": "1",
            "fold": "1",
            "page": "1",
            "pageScale": "1",
            "pageWidth": str(page_width),
            "pageHeight": str(page_height),
            "math": "0",
            "shadow": "0",
        },
    )
    root_xml = ET.SubElement(mx_graph, "root")
    ET.SubElement(root_xml, "mxCell", id="0")
    ET.SubElement(root_xml, "mxCell", id="1", parent="0")

    next_id = 2

    # Base horizontal timeline.
    add_vertex(
        root_xml,
        cell_id=next_id,
        value="",
        style="shape=line;strokeWidth=3;strokeColor=#334155;",
        x=first_x,
        y=axis_y,
        width=max(1, last_x - first_x),
        height=1,
    )
    next_id += 1

    edge_style = "edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=none;strokeColor=#64748b;strokeWidth=1.5;"
    label_style = (
        "rounded=1;arcSize=14;whiteSpace=wrap;html=1;strokeColor=#1d4ed8;"
        "fillColor=#dbeafe;fontColor=#0f172a;fontSize=12;fontFamily=Helvetica;"
        "align=center;verticalAlign=middle;"
    )
    dot_style = "ellipse;whiteSpace=wrap;html=1;strokeColor=#0f172a;fillColor=#0f172a;"
    placeholder_style = (
        "rounded=1;arcSize=12;whiteSpace=wrap;html=1;strokeColor=#94a3b8;"
        "fillColor=#f8fafc;fontColor=#334155;fontSize=11;fontFamily=Helvetica;"
        "align=center;verticalAlign=middle;"
    )

    for idx, (point, image_info) in enumerate(zip(points, images)):
        center_x = margin_x + idx * spacing

        label_text = point.title
        if point.date:
            label_text = f"{point.date}\n{point.title}"

        label_id = next_id
        add_vertex(
            root_xml,
            cell_id=label_id,
            value=label_text,
            style=label_style,
            x=center_x - (label_w / 2),
            y=110,
            width=label_w,
            height=label_h,
        )
        next_id += 1

        dot_id = next_id
        add_vertex(
            root_xml,
            cell_id=dot_id,
            value="",
            style=dot_style,
            x=center_x - 7,
            y=axis_y - 7,
            width=14,
            height=14,
        )
        next_id += 1

        img_id = next_id
        if image_info.path and image_info.path.exists():
            image_data_uri = data_uri_for_image(image_info.path)
            image_style = (
                "shape=image;html=1;verticalLabelPosition=bottom;verticalAlign=top;"
                "imageAspect=1;aspect=fixed;align=center;image="
                + image_data_uri
                + ";"
            )
            add_vertex(
                root_xml,
                cell_id=img_id,
                value="",
                style=image_style,
                x=center_x - (img_w / 2),
                y=330,
                width=img_w,
                height=img_h,
            )
        else:
            add_vertex(
                root_xml,
                cell_id=img_id,
                value="Sin imagen",
                style=placeholder_style,
                x=center_x - (img_w / 2),
                y=330,
                width=img_w,
                height=img_h,
            )
        next_id += 1

        add_edge(root_xml, cell_id=next_id, source=label_id, target=dot_id, style=edge_style)
        next_id += 1
        add_edge(root_xml, cell_id=next_id, source=dot_id, target=img_id, style=edge_style)
        next_id += 1

    xml_text = ET.tostring(mxfile, encoding="unicode")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(xml_text, encoding="utf-8")


def verify_drawio_images(output_file: Path) -> dict[str, int]:
    text = output_file.read_text(encoding="utf-8")
    root = ET.fromstring(text)

    image_cells = 0
    embedded_image_cells = 0
    placeholder_cells = 0

    for cell in root.iter("mxCell"):
        style = str(cell.attrib.get("style", ""))
        value = str(cell.attrib.get("value", ""))
        if "shape=image" in style:
            image_cells += 1
            if "image=data:image/" in style:
                embedded_image_cells += 1
        elif value == "Sin imagen":
            placeholder_cells += 1

    return {
        "image_cells": image_cells,
        "embedded_image_cells": embedded_image_cells,
        "placeholder_cells": placeholder_cells,
        "embedded_refs_in_xml": text.count("image=data:image/"),
    }


def print_summary(points: list[TimelinePoint], images: list[TimelineImage], output_file: Path) -> None:
    total = len(points)
    with_image = sum(1 for item in images if item.path is not None)
    downloaded = sum(1 for item in images if item.downloaded)
    cached = with_image - downloaded
    missing = total - with_image
    verification = verify_drawio_images(output_file)

    print(f"Linea de tiempo creada: {output_file}")
    print(f"Eventos: {total}")
    print(f"Imagenes descargadas: {downloaded}")
    print(f"Imagenes en cache: {cached}")
    print(f"Eventos sin imagen: {missing}")
    print(f"Celdas de imagen en drawio: {verification['image_cells']}")
    print(f"Imagenes embebidas en drawio: {verification['embedded_image_cells']}")
    print(f"Referencias image=data:image/ en XML: {verification['embedded_refs_in_xml']}")


def main() -> int:
    args = parse_args()

    points = load_points(args)
    if not points:
        raise ValueError("No se encontraron puntos validos.")

    images_dir = Path(args.images_dir)
    images = ensure_images(
        points=points,
        images_dir=images_dir,
        suffix=str(args.suffix or ""),
        no_download=bool(args.no_download),
    )

    output_file = Path(args.output)
    build_drawio(points, images, output_file)
    print_summary(points, images, output_file)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Error: {exc}")
        raise SystemExit(1)
