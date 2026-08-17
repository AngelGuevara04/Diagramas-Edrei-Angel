"""
Configuracion y datos para el generador de mapas conceptuales.
Edita este archivo para cambiar el contenido (concept_map) y los parametros de dibujo.
"""
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

NORMALIZAR_TUPLAS = False
PALABRAS_POR_POSICION = 2

concept_map = [
    {
        "titulo_principal": "Unidad 1. Desarrollo Móvil",
        "subtitulos": [
            {
                "titulo": "1. Introducción y Protocolos", # Este subtema es de ejemplo (No se relaciona con lo demás)
                "conector": "Fundamentos",
                "ramas": [
                    [
                        (None, "Surge por"), ("Evolución Tecnológica", "que causa"), ("Incremento complejidad", "y"), ("Heterogeneidad", "en"), ("Recursos", "para"), ("Interconectar equipos", "y"), ("Compartir servicios", "como"), ("Bases de datos", "o"), ("Almacenamiento", None)
                    ],
                    [
                        (None, "Monitorización básica"), ("Pinging", "basado en"), ("Datagrama Echo", "para"), ("Verificar conectividad", "si"), ("Hay réplica", "entonces"), ("Servidor activo", "si no"), ("Hay falla", None)
                    ],
                    [
                        {
                        "texto": "Protocolos Gestión",
                        "conector": "usa",
                        "bifurcaciones": [
                            [
                                (None, "TCP/IP"), ("SGMP", "para"), ("Pasarelas/Gateways", "y"), ("Sistemas UNIX", "requiere"), ("Conjunto datos", "para"), ("Iniciar", None)
                            ],
                            [
                                (None, "Estándar"), ("SNMP", "aparece en"), ("1988", "es"), ("Más complejo", "usa"), ("MIB", "base de"), ("Información gestión", "formada por"), ("Vendedores/Usuarios", None)
                            ],
                            [
                                (None, "Modelo ISO"), ("CMIS", "servicio de"), ("Monitorización", "usa"), ("Protocolos CMIP", "aún en"), ("Fase experimental", "no son"), ("Estándar oficial", None)
                            ]
                        ]
                        }
                    ]
                ],
            },
            {
                "titulo": "1.1. Dispositivos Móviles",
                "conector": "Computación portátil",
                "ramas": [
                    [
                        (None, "Definición"), ("Aparato pequeño", "con"), ("Capacidad proceso", "para"), ("Correr software", None),
                        {
                            "texto": "Sistemas Operativos",
                            "conector": "algunos",
                            "bifurcaciones": [
                                [
                                    (None, "Es"), ("Google Android", "basado"), ("En Kernel", "de"), ("Linux", "es"), ("Código abierto", "AOSP"), ("Lo que permite", "alta"), ("Personalización", "por"), ("Los fabricantes", "tiene"), ("Gran cuota", "de"), ("Mercado mundial", "y usa"), ("Google Play", "como"), ("Tienda principal", "su"), ("Entorno desarrollo", "es"), ("Android Studio", None)
                                ],
                                [
                                    (None, "También"), ("Apple iOS", "basado"), ("En Unix", "es"), ("Código cerrado", "y"), ("Altamente optimizado", "para"), ("Su hardware", "específico"), ("Ofrece alta", "seguridad"), ("Mediante sandboxing", "y"), ("Estricta revisión", "de"), ("Apps", "en"), ("La App Store", "su"), ("Interfaz gráfica", "sigue"), ("Guías HIG", "de"), ("Diseño", "muy"), ("Consistentes", None)
                                ],
                                [
                                    (None, "Y"), ("Otros", "como"), ("KaiOS", "para"), ("Teléfonos básicos", "con"), ("Funciones smart", "y"), ("HarmonyOS", "de"), ("Huawei", "enfocado"), ("En ecosistema", "de"), ("Dispositivos IoT", "busca"), ("Ser una", "alternativa"), ("A los", "dos"), ("Grandes dominadores", "del"), ("Mercado actual", "pero"), ("Con menor", "cuota"), ("De mercado", None)
                                ]
                            ]
                        }
                    ],
                    [
                        (None, "Evolución"), ("1G", "con"), ("Voz analógica", "y"), ("Grandes terminales", "luego"), ("2G", "trajo"), ("Voz digital", "y"), ("Mensajes SMS", "después"), ("2.5G GPRS", "habilitó"), ("Internet incipiente", "más tarde"), ("3G WCDMA", "permitió"), ("Navegación web", "y"), ("Videollamadas", "luego"), ("4G LTE", "masificó"), ("Streaming HD", "y"), ("Baja latencia", "abriendo"), ("Paso a 5G", "que"), ("Conecta todo", "con"), ("Velocidad gigabit", "y"), ("Mínima latencia", None)
                    ],
                    [
                        (None, "Portabilidad"), ("Factor clave", "que"), ("Permite llevarlo", "a"), ("Cualquier parte", "gracias"), ("A su peso", "muy"), ("Ligero", "y"), ("Tamaño compacto", "que"), ("Cabe en bolsillo", "facilitando"), ("Acceso instantáneo", "a"), ("Información vital", "y"), ("Herramientas de", "trabajo"), ("O comunicación", "sin"), ("Depender de", "un"), ("Lugar físico", "fomentando"), ("Flexibilidad", "y"), ("Productividad remota", None)
                    ],
                    [
                        (None, "Componentes"), ("SoC", None),
                        {
                            "texto": "Fabricantes SoC",
                            "conector": "fabricados por",
                            "bifurcaciones": [
                                [
                                    (None, "incluye"), ("Qualcomm", "domina"), ("Gama alta", "con"), ("Su serie", "Snapdragon"), ("Que integra", "CPU"), ("Kryo custom", "y"), ("GPU Adreno", "para"), ("Excelente rendimiento", "en"), ("Juegos 3D", "son"), ("Líderes en", "módems"), ("5G", "y"), ("Procesamiento", "de"), ("Inteligencia Artificial", "en"), ("Teléfonos Android", None)
                                ],
                                [
                                    (None, "también"), ("Apple", "diseña"), ("Sus propios", "chips"), ("Serie A", "para"), ("iPhone", "y"), ("Serie M", "para"), ("IPad/Mac", "logrando"), ("Integración vertical", "y"), ("Máxima eficiencia", "energética"), ("Su enfoque", "es"), ("Rendimiento", "por"), ("Vatio", "y"), ("Potentes núcleos", "de"), ("CPU y GPU", "que son"), ("propios", None)
                                ],
                                [
                                    (None, "por último"), ("MediaTek", "fuerte"), ("En gamas", "media"), ("Y de entrada", "con"), ("Su familia", "Dimensity"), ("Y Helio", "compite"), ("Fuertemente", "con"), ("Qualcomm", "ofreciendo"), ("Soluciones 5G", "más"), ("Asequibles", "han"), ("Mejorado mucho", "en"), ("Rendimiento", "y"), ("Eficiencia", "en"), ("Los últimos años", None)
                                ]
                            ]
                        }
                    ],
                    [
                        (None, "Sensores"), ("Acelerómetro", "mide"), ("Movimiento", "y"), ("Giroscopio", "detecta"), ("Orientación", "luego"), ("Magnetómetro", "actúa"), ("Como brújula", "y"), ("GPS", "obtiene"), ("Posición satelital", "también"), ("Barómetro", "mide"), ("Presión atmosférica", "para"), ("Calcular altitud", "además"), ("Sensor proximidad", "apaga"), ("Pantalla", "al"), ("Acercar rostro", "y"), ("Sensor luz", "ajusta"), ("Brillo pantalla", None)
                    ]
                ],
            },
            {
                "titulo": "1.2. Aplicaciones Móviles",
                "conector": "Software específico",
                "ramas": [
                    [
                        (None, "Concepto"), ("Programa informático", "diseñado"), ("Específicamente", "para"), ("Sistemas operativos", "móviles"), ("Que satisface", None),
                        {
                            "texto": "Categorías Populares",
                            "conector": "necesidades",
                            "bifurcaciones": [
                                [
                                    (None, "Las"), ("Redes Sociales", "permiten"), ("Crear perfiles", "y"), ("Compartir contenido", "como"), ("Fotos y videos", "conectan"), ("Amigos", "y"), ("Familiares", "forman"), ("Comunidades", "con"), ("Intereses comunes", "se"), ("Monetizan", "con"), ("Publicidad dirigida", "y"), ("Recopilación", "de"), ("Datos de usuario", None)
                                ],
                                [
                                    (None, "Los"), ("Juegos", "son"), ("Fuente principal", "de"), ("Entretenimiento", "hay"), ("Desde casuales", "hasta"), ("Títulos complejos", "con"), ("Gráficos avanzados", "utilizan"), ("Modelos", "de"), ("Monetización", "como"), ("Compras in-app", "para"), ("Obtener ventajas", "o"), ("Cosméticos", "son"), ("Muy populares", "en"), ("Todas las edades", None)
                                ],
                                [
                                    (None, "La"), ("Productividad", "ayudan"), ("A organizar", "el"), ("Trabajo diario", "incluyen"), ("Agendas", "y"), ("Calendarios", "también"), ("Gestores", "de"), ("Tareas", "y"), ("Proyectos", "permiten"), ("Tomar notas", "y"), ("Editar documentos", "desde"), ("Cualquier lugar", "aumentando"), ("La eficiencia", "personal y"), ("Profesional", None)
                                ]
                            ]
                        }
                    ],
                    {
                        "titulo": "1.2.1. Clasificación Apps",
                        "conector": "Tipos desarrollo",
                        "ramas": [
                            [
                                (None, "Nativas"), ("Desarrollo específico", "para"), ("Cada plataforma", None),
                                {
                                    "texto": "Lenguajes Nativos",
                                    "conector": "usando",
                                    "bifurcaciones": [
                                        [
                                            (None, "usando en"), ("Android", "usa"), ("Kotlin", "como"), ("Lenguaje principal", "respaldado"), ("Por Google", "es"), ("Interoperable", "con"), ("Java", "el"), ("Lenguaje anterior", "se"), ("Ejecuta sobre", "la"), ("Máquina virtual", "ART"), ("Y usa", "Gradle como"), ("Sistema", "de"), ("Construcción", None)
                                        ],
                                        [
                                            (None, "así como en"), ("iOS", "usa"), ("Swift", "un"), ("Lenguaje moderno", "y"), ("Seguro", "creado"), ("Por Apple", "es"), ("Más rápido", "que"), ("Su predecesor", "Objective-C"), ("Se compila", "directamente"), ("A código", "máquina"), ("Sin VM", "y"), ("Usa Xcode", "como"), ("Entorno", "de"), ("Desarrollo", None)
                                        ]
                                    ]
                                }
                            ],
                            [
                                (None, "Web Apps"), ("Corren sobre", "un"), ("Navegador web", "sin"), ("Necesidad de", "instalación"), ("Se adaptan", "a"), ("Cualquier dispositivo", "son"), ("Multiplataforma", "por"), ("Definición", "utilizan"), ("Tecnologías estándar", "HTML5"), ("CSS3", "y"), ("JavaScript", "pueden"), ("Ser PWAs", "para"), ("Funcionar offline", "y"), ("Enviar notificaciones", "pero"), ("Tienen acceso", "limitado"), ("Al hardware", None)
                            ],
                            [
                                (None, "Híbridas"), ("Combinan nativo", "y"), ("Web", None),
                                {
                                    "texto": "Frameworks Híbridos",
                                    "conector": "usando",
                                    "bifurcaciones": [
                                        [
                                            (None, "como"), ("React Native", "creado"), ("Por Facebook", "usa"), ("JavaScript", "y"), ("React", "para"), ("Controlar componentes", "nativos"), ("Traduce la", "lógica"), ("A través", "de"), ("Un puente", "asíncrono"), ("Logrando", "buen"), ("Rendimiento", "y"), ("Apariencia nativa", None)
                                        ],
                                        [
                                            (None, "así también"), ("Flutter", "desarrollado"), ("Por Google", "usa"), ("El lenguaje", "Dart"), ("No usa", "componentes"), ("Nativos", "sino"), ("Que renderiza", "su"), ("Propia interfaz", "con"), ("El motor", "Skia"), ("Logrando control", "total"), ("Del pixel", "y"), ("Alto rendimiento", "en"), ("Multiplataforma", None)
                                        ],
                                        [
                                            (None, "por último"), ("Ionic", "usa"), ("Tecnologías web", "HTML"), ("CSS", "y"), ("JavaScript", "para"), ("Construir la", "UI"), ("La envuelve", "en"), ("Un contenedor", "nativo"), ("Mediante Capacitor", "o"), ("Cordova", "para"), ("Acceder", "al"), ("Hardware", "del"), ("Dispositivo", None)
                                        ]
                                    ]
                                }
                            ]
                        ]
                    },
                    [
                        (None, "Distribución"), ("Principalmente vía", "tiendas"), ("De aplicaciones", "como"), ("Google Play", "para"), ("Android", "y"), ("App Store", "para"), ("iOS", "estas"), ("Plataformas ofrecen", "visibilidad"), ("Y seguridad", "pero"), ("Imponen reglas", "y"), ("Comisiones", "también"), ("Existe sideloading", "instalación"), ("Manual", "con"), ("Ciertos riesgos", "y"), ("Tiendas alternativas", None)
                    ],
                    [
                        (None, "Monetización"), ("Modelo freemium", "ofrece"), ("Funciones básicas", "gratis"), ("Y cobra", "por"), ("Características premium", "también"), ("Publicidad In-App", "muestra"), ("Anuncios", "a"), ("Cambio de", "uso"), ("Gratuito", "otro"), ("Modelo es", "suscripción"), ("Pagos recurrentes", "por"), ("Acceso a contenido", "o"), ("Servicios", "y"), ("Apps de pago", "requieren"), ("Compra inicial", None)
                    ],
                    [
                        (None, "Ciclo Vida"), ("Inicia con", "fase"), ("De idea", "y"), ("Planificación", "luego"), ("Diseño UX/UI", "y"), ("Codificación", None),
                        {
                            "texto": "Metodologías",
                            "conector": "usando",
                            "bifurcaciones": [
                                [
                                    (None, "como"), ("Cascada", "es"), ("Un enfoque", "secuencial"), ("Y lineal", "donde"), ("Cada fase", "debe"), ("Completarse", "antes"), ("De iniciar", "la"), ("Siguiente", "es"), ("Poco flexible", "a"), ("Cambios", "pero"), ("Fácil", "de"), ("Gestionar", "y"), ("Planificar", None)
                                ],
                                [
                                    (None, "también"), ("Ágil", "se"), ("Basa en", "ciclos"), ("Cortos e", "iterativos"), ("Llamados sprints", "fomenta"), ("La colaboración", "constante"), ("Con el", "cliente"), ("Y la", "adaptación"), ("A cambios", "durante"), ("El proceso", "prioriza"), ("Entregar valor", "rápido"), ("Y de", "forma"), ("Continua", None)
                                ],
                                [
                                    (None, "y"), ("DevOps", "es"), ("Una cultura", "que"), ("Une desarrollo", "Dev"), ("Y operaciones", "Ops"), ("Busca automatizar", "y"), ("Monitorear", "todo"), ("El ciclo", "de"), ("Vida del", "software"), ("Desde la", "integración"), ("Hasta la", "entrega"), ("Y el", "despliegue"), ("Continuo", None)
                                ]
                            ]
                        }
                    ]
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
    "NORMALIZAR_TUPLAS": False,
    "PALABRAS_POR_POSICION": 2,
    "NORMALIZAR_TUPLAS_EXTENSAS": True,
    "PALETTE": [
        ("#60a5fa", "#1e3a8a"),
        ("#a3e635", "#4d7c0f" ),
        ("#fca5a5", "#7f1d1d" ),
        ("#f0abfc", "#86198f" ),
    ],
    "START_X": 120,
    "START_Y": 40,
    "OUTPUT_FILE": os.path.join("Mapas", "Uni1_Actividad1.drawio"),
}


def run():
    """Permite ejecutar el generador directamente desde este archivo."""
    scripts_dir = os.path.join(BASE_DIR, "Scripts")
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)

    from Mapas_conceptuales import generar_mapa_conceptual

    out_path = generar_mapa_conceptual(concept_map, CONFIG)
    print(f"Mapa conceptual generado en: {out_path}")


if __name__ == "__main__":
    run()
