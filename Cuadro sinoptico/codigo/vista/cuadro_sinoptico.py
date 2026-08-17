"""
Configuracion y datos para el generador de cuadros sinopticos.
Edita este archivo para cambiar el contenido (chart) y los parametros de dibujo.
"""
import os
import sys

chart = {
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

# Todos los valores son opcionales; solo sobreescribe lo que necesites.
CONFIG = {
    "archivo_de_salida": os.path.join("Mapas", "Cuadro_sinoptico1.drawio"),
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
    "BRACE_STYLE": "rounded",  # "rounded" o "plain"
    "FONT_FAMILY": "Times New Roman",
    "FONT_COLOR": "#415D66",
    "BRACE_COLOR": "#4A4861",
}


def run():
    """Permite ejecutar el generador directamente desde este archivo."""
    # Directorio del proyecto (carpeta que contiene "Scripts" y "vista")
    base_dir = os.path.dirname(os.path.dirname(__file__))
    scripts_dir = os.path.join(base_dir, "Scripts")
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)

    from Cuadros_sinopticos import generar_cuadro_sinoptico

    out_path = generar_cuadro_sinoptico(chart, CONFIG)
    print(f"Cuadro sinoptico generado en: {out_path}")


if __name__ == "__main__":
    run()
