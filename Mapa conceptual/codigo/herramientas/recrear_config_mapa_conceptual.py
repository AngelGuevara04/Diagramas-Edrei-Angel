"""
Script de respaldo para recrear archivos de configuracion de diagramas.
Verifica y crea:
- cuadro_sinoptico_config.py
- mapa_conceptual_config.py
- mapa_mental_config.py
"""
from pathlib import Path
from textwrap import dedent

BASE_DIR = Path(__file__).resolve().parents[1]
CUADRO_PATH = BASE_DIR / "vista" / "cuadro_sinoptico.py"
MAPA_PATH = BASE_DIR / "vista" / "mapa_conceptual.py"
MENTAL_PATH = BASE_DIR / "vista" / "mapa_mental.py"


CUADRO_CONTENT = dedent(
    '''\
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
        "BRACE_STYLE": "rounded",  # "rounded" o "plain"
        "FONT_FAMILY": "Times New Roman",
        "FONT_COLOR": "#415D66",
        "BRACE_COLOR": "#4A4861",
    }


    def run():
        """Permite ejecutar el generador directamente desde este archivo."""
        base_dir = os.path.dirname(os.path.dirname(__file__))
        scripts_dir = os.path.join(base_dir, "Scripts")
        if scripts_dir not in sys.path:
            sys.path.insert(0, scripts_dir)

        from Cuadros_sinopticos import generar_cuadro_sinoptico

        out_path = generar_cuadro_sinoptico(chart, CONFIG)
        print(f"Cuadro sinoptico generado en: {out_path}")


    if __name__ == "__main__":
        run()
    '''
)


MAPA_CONTENT = dedent(
    '''\
    """
    Configuracion y datos para el generador de mapas conceptuales.
    Edita este archivo para cambiar el contenido (concept_map) y los parametros de dibujo.
    """
    import os
    import sys

    NORMALIZAR_TUPLAS = False
    PALABRAS_POR_POSICION = 2

    concept_map = [
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
                            ("Robótica", None),
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

    if NORMALIZAR_TUPLAS:
        try:
            from utilidades.ajuste_mapa_conceptual import normalizar_concept_map

            concept_map = normalizar_concept_map(
                concept_map, palabras_por_slot=PALABRAS_POR_POSICION
            )
        except Exception as exc:  # pragma: no cover - solo para ayuda en runtime
            print(f"No se pudo normalizar concept_map: {exc}", file=sys.stderr)

    CONFIG = {
        "FONT_FAMILY": "Times New Roman", # Familia de fuente para las cajas
        "FONT_SIZE": 12, # Tamaño de fuente en puntos
        "FONT_COLOR": "#000000",  # Color de fuente 
        "FONT_BOLD": False,  # True para negrita
        "FONT_ITALIC": False,  # True para cursiva
        "STROKE_W": 2, # Grosor del borde de las cajas
        "EDGE_COLOR": "#60a5fa", # Color del borde de los conectores
        "BOX_ARC_SIZE": 0, # Radio de las esquinas redondeadas
        "BOX_SHADOW": False, # Sombra en las cajas
        "MAIN_FILL_COLOR": "#a7a6e9", # Color de relleno del título principal
        "MAIN_STROKE_COLOR": "#60a5fa", # Color del borde del título principal
        "SUBTITLE_FILL_COLOR": "#8AAEE0", # Color de relleno de los subtítulos
        "SUBTITLE_STROKE_COLOR": "#94a3b8", # Color del borde de los subtítulos
        "CONNECTOR_FONT_FAMILY": "Courier New", # Fuente de los conectores
        "CONNECTOR_FONT_SIZE": 9, # Tamaño de fuente de los conectores
        "CONNECTOR_FONT_COLOR": "#e2e8f0", # Color de fuente de los conectores
        "CONNECTOR_BG_COLOR": "#0f172a", # Color de fondo de los conectores
        "CONNECTOR_BORDER_COLOR": "#475569", # Color del borde de los conectores
        "CONNECTOR_SHADOW": False, # Sombra en los conectores
        "CONNECTOR_TEXT_SHADOW": True, # Sombra en el texto de los conectores
        "BOX_W": 100, # Ancho base de las cajas
        "BOX_H": 45, # Alto base de las cajas
        "X_STEP": 150, # Paso horizontal entre cajas
        "Y_STEP": 90, # Paso vertical entre cajas
        "POSITION_NOISE": 15, # Ruido aleatorio en la posición de las cajas
        "MAIN_TO_SUBTITLE": 130, # Distancia del título principal a los subtítulos
        "SUBTITLE_TO_BRANCH": 150, # Distancia de los subtítulos a las ramas
        "SUBTITLE_GAP": 80, # Separación entre subtítulos
        "GROUP_GAP": 800, # Separación entre grupos de ramas
        # Coloreo jerarquico
        "COLOR_SUBTITLE_GROUPS": False,  # True: todas las ramas de un subtitulo comparten color
        "COLOR_NESTED_SUBTOPICS": False,  # True: cada sub-tema anidado usa un color propio
        "PALETTE": [
            ("#60a5fa", "#1e3a8a"),
            ("#a3e635", "#4d7c0f" ),
            ("#fca5a5", "#7f1d1d" ),
            ("#f0abfc", "#86198f" ),
        ],
        "START_X": 120,
        "START_Y": 40,
        "OUTPUT_FILE": os.path.join("Mapas", "Mapa_conceptual.drawio"),
    }


    def run():
        """Permite ejecutar el generador directamente desde este archivo."""
        base_dir = os.path.dirname(os.path.dirname(__file__))
        scripts_dir = os.path.join(base_dir, "Scripts")
        if scripts_dir not in sys.path:
            sys.path.insert(0, scripts_dir)

        from Mapas_conceptuales import generar_mapa_conceptual

        out_path = generar_mapa_conceptual(concept_map, CONFIG)
        print(f"Mapa conceptual generado en: {out_path}")


    if __name__ == "__main__":
        run()
    '''
)


MENTAL_CONTENT = dedent(
    '''\
    """
    Configuracion y datos para el generador de mapas mentales.
    Edita este archivo para cambiar el contenido (mapa_ejemplo) y los parametros de dibujo.
    """
    import os
    import sys
    from pathlib import Path

    mapa_ejemplo = {
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

    CONFIG = {
        "CENTER_X": 800,
        "CENTER_Y": 600,
        "R_STEP": 360,
        # Ajusta el crecimiento radial en los primeros niveles (factor 1.05 = +5%)
        "R_STEP_BOOST": {"levels": 5, "factor": 1.05},
        "CURVED_EDGES": False,
        "EDGE_CONNECTOR_STYLE": "curved_block",  # default | curved_block
        "EDGE_CURVE_FACTOR": 0.09, # Factor de curvatura de las aristas
        "IMAGE_DIR": Path("ImagenesMapaMental"),
        "IMAGE_RADIUS_OFFSET": 200, # Offset radial para las imágenes respecto al centro del mapa (px). Positivo = más lejos del centro.
        "IMAGE_WIDTH": 100,
        "IMAGE_WIDTH_NOISE": 0.0,  # 0.0 = sin ruido, 0.1 = +/-10% del ancho
        "IMAGE_HEIGHT": None,
        "TEXT_FONT_SIZE": 14, # Tamaño de la fuente del texto
        "TEXT_FONT_FAMILY": "Helvetica",
        "TEXT_FONT_COLOR": "#000000", # Color del texto
        "TEXT_FONT_BORDER_COLOR": "none", # Color del borde del texto
        "TEXT_BG_COLOR": "none", # Color de fondo del texto
        "TEXT_STROKE_COLOR": "#000000", # Color del contorno del cuadro de texto
        "TEXT_STROKE_WIDTH": 2, # Ancho del contorno del cuadro de texto
        "TEXT_FILL_COLOR": "none", # Color de relleno del cuadro de texto
        "TEXT_ROUNDED": True,  # Permite ajustar el redondeado de los cuadros de texto
        "TEXT_ARC_SIZE": 50,   # Tamaño de las esquinas redondeadas (0 para esquinas rectas)
        "TEXT_BOLD": True, # Negrita
        "TEXT_ITALIC": False, # Cursiva
        "TEXT_UNDERLINE": False, # Subrayado
        "TEXT_WRAP": True, # Ajuste de texto dentro de cuadros de texto
        "NODE_WIDTH": 120,  # Ancho del nodo
        "NODE_HEIGHT": 40, # Alto del nodo
        "POSITION_NOISE": 300, # Ruido aleatorio en la posición de los nodos
        "RANDOM_SEED": 42, # Semilla para reproducibilidad
        "EDGE_STROKE_WIDTH": 2, # Ancho de las aristas
        "EDGE_COLOR": "#000000", # Color de las aristas
        # Flechas en ambos extremos de la linea: "none", "block", "classic", etc.
        "EDGE_LEFT_ARROW": "classic",
        "EDGE_RIGHT_ARROW": "block",
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
        "OUTPUT_FILE": os.path.join("Mapas", "mapa_mental_prueba.drawio"),
    }

    def run():
        """Permite ejecutar el generador directamente desde este archivo."""
        base_dir = os.path.dirname(os.path.dirname(__file__))
        scripts_dir = os.path.join(base_dir, "Scripts")
        if scripts_dir not in sys.path:
            sys.path.insert(0, scripts_dir)

        from Mapas_mentales import generar_mapa_mental

        out_path = generar_mapa_mental(mapa_ejemplo, CONFIG)
        print(f"Mapa mental generado en: {out_path}")


    if __name__ == "__main__":
        run()
    '''
)


def recreate(path: Path, content: str):
    path.write_text(content, encoding="utf-8", newline="\n")
    print(f"Archivo {path} creado o recreado.")


def main():
    if not CUADRO_PATH.exists():
        recreate(CUADRO_PATH, CUADRO_CONTENT)
    else:
        print(f"{CUADRO_PATH} ya existe. No se modifica.")

    if not MAPA_PATH.exists():
        recreate(MAPA_PATH, MAPA_CONTENT)
    else:
        print(f"{MAPA_PATH} ya existe. No se modifica.")

    if not MENTAL_PATH.exists():
        recreate(MENTAL_PATH, MENTAL_CONTENT)
    else:
        print(f"{MENTAL_PATH} ya existe. No se modifica.")


if __name__ == "__main__":
    main()
