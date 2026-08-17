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
        "titulo_principal": "Unidad 4. Aplicaciones IA",
        "subtitulos": [
            {
                "titulo": "4.1. Robótica",
                "conector": "Integra mecánica y",
                "ramas": [
                    {
                        "titulo": "4.1.1. Conceptos básicos",
                        "conector": "Se define por",
                        "ramas": [
                            [
                                (None, "Agentes físicos"), ("Programables", "que poseen"), ("Sensores", "para"), ("Percibir entorno", "y"), ("Actuadores", "para"), ("Modificarlo", "mediante"), ("Movimiento", "busca la"), ("Autonomía", "en"), ("Tareas complejas", "requiere"), ("Cinemática", "para"), ("Calcular posiciones", "y"), ("Dinámica", "para"), ("Fuerzas y torques", "usa"), ("Control de lazo", "cerrado con"), ("Retroalimentación", "para"), ("Corregir errores", "en"), ("Tiempo real", "integrando"), ("Inteligencia Artificial", "para"), ("Decisiones adaptativas", None)
                            ]
                        ]
                    },
                    {
                        "titulo": "4.1.2. Clasificación",
                        "conector": "Se dividen en",
                        "ramas": [
                            [
                                (None, "Robots industriales"), ("Brazos articulados", "para"), ("Soldadura y pintura", "en"), ("Líneas montaje", "y"), ("Robots de servicio", "para"), ("Uso doméstico", "como"), ("Aspiradoras", "o"), ("Uso médico", "para"), ("Cirugía asistida", "también"), ("Robots móviles", "con"), ("Ruedas u orugas", "para"), ("Logística", "y"), ("Androides", "con"), ("Morfología humana", "para"), ("Interacción social", "y"), ("Drones (VANT)", "para"), ("Vigilancia aérea", None)
                            ]
                        ]
                    },
                    {
                        "titulo": "4.1.3. Desarrollos",
                        "conector": "Avances recientes",
                        "ramas": [
                            [
                                (None, "Exploración espacial"), ("Rovers en Marte", "con"), ("Navegación autónoma", "y"), ("Vehículos autónomos", "coches"), ("Sin conductor", "usando"), ("Lidar y cámaras", "para"), ("Evitar obstáculos", "también"), ("Exoesqueletos", "para"), ("Rehabilitación motora", "o"), ("Fuerza aumentada", "y"), ("Cobots", "diseñados para"), ("Colaboración segura", "con"), ("Humanos", "en"), ("Entornos fabriles flexibles", None)
                            ]
                        ]
                    }
                ],
            },
            {
                "titulo": "4.2. Redes Neuronales",
                "conector": "Modelos inspirados en",
                "ramas": [
                    {
                        "titulo": "4.2.1. Conceptos básicos",
                        "conector": "Elementos clave",
                        "ramas": [
                            [
                                (None, "Biología cerebral"), ("Neurona artificial", "suma"), ("Entradas ponderadas", "por"), ("Pesos sinápticos", "y aplica"), ("Función activación", "como"), ("Sigmoide o ReLU", "para"), ("No linealidad", "se organizan en"), ("Capas", "de entrada"), ("Ocultas", "y"), ("Salida", "aprenden por"), ("Backpropagation", "ajustando"), ("Pesos", "para"), ("Minimizar error", "usando"), ("Gradiente descendente", "y"), ("Datos de entrenamiento", None)
                            ]
                        ]
                    },
                    {
                        "titulo": "4.2.2. Clasificación",
                        "conector": "Tipos principales",
                        "ramas": [
                            [
                                (None, "Perceptrón simple"), ("Clasificador lineal", "y"), ("Perceptrón multicapa", "para"), ("Problemas complejos", "y"), ("Convolucionales (CNN)", "especializadas en"), ("Procesar imágenes", "detectando"), ("Bordes y formas", "y"), ("Recurrentes (RNN)", "con"), ("Memoria temporal", "para"), ("Secuencias y texto", "y"), ("Transformers", "basados en"), ("Mecanismo atención", "para"), ("Modelos lenguaje grandes",  None)
                            ]
                        ]
                    },
                    {
                        "titulo": "4.2.3. Desarrollos",
                        "conector": "Aplicaciones modernas",
                        "ramas": [
                            [
                                (None, "Deep Learning"), ("Aprendizaje profundo", "para"), ("Reconocimiento facial", "y"), ("Generación de arte", "con"), ("Modelos difusivos", "y"), ("Diagnóstico médico", "analizando"), ("Radiografías", "con"), ("Alta precisión", "y"), ("AlphaFold", "para"), ("Plegamiento proteínas", "en"), ("Biología molecular", "y"), ("Juegos estrategia", "superando a"), ("Humanos", "en"), ("Go y Ajedrez", None)
                            ]
                        ]
                    }
                ],
            },
            {
                "titulo": "4.3. Visión Artificial",
                "conector": "Permite a máquinas",
                "ramas": [
                    {
                        "titulo": "4.3.1. Conceptos básicos",
                        "conector": "Proceso de",
                        "ramas": [
                            [
                                (None, "Adquisición imagen"), ("Sensores digitales", "luego"), ("Preprocesamiento", "para"), ("Reducir ruido", "y"), ("Mejorar contraste", "sigue"), ("Segmentación", "separando"), ("Objetos del fondo", "mediante"), ("Detección bordes", "y"), ("Extracción características", "identificando"), ("Patrones clave", "y"), ("Clasificación", "usando"), ("Machine Learning", "para"), ("Interpretar escena", "y"), ("Tomar decisiones", None)
                            ]
                        ]
                    },
                    {
                        "titulo": "4.3.2. Desarrollos",
                        "conector": "Usos prácticos",
                        "ramas": [
                            [
                                (None, "Biometría"), ("Desbloqueo facial", "y"), ("Control de acceso", "en"), ("Aeropuertos", "también"), ("Inspección industrial", "detectando"), ("Defectos fabricación", "a"), ("Alta velocidad", "y"), ("Agricultura precisión", "monitoreando"), ("Salud cultivos", "con"), ("Drones", "y"), ("Realidad Aumentada", "superponiendo"), ("Información digital", "en"), ("Mundo real", None)
                            ]
                        ]
                    }
                ],
            },
            {
                "titulo": "4.4. Lógica Difusa",
                "conector": "Razonamiento con",
                "ramas": [
                    {
                        "titulo": "4.4.1. Conceptos básicos",
                        "conector": "Maneja la",
                        "ramas": [
                            [
                                (None, "Incertidumbre"), ("Verdad parcial", "valores"), ("Entre 0 y 1", "usa"), ("Conjuntos difusos", "sin"), ("Límites estrictos", "y"), ("Variables lingüísticas", "como"), ("Alto o Bajo", "aplica"), ("Reglas Si-Entonces", "para"), ("Inferencia", "proceso de"), ("Fusificación", "convierte"), ("Dato a difuso", "luego"), ("Evaluación reglas", "y"), ("Defusificación", "obtiene"), ("Valor", "concreto"), ("de salida", None)
                            ]
                        ]
                    },
                    {
                        "titulo": "4.4.2. Desarrollos",
                        "conector": "Sistemas de control",
                        "ramas": [
                            [
                                (None, "Electrodomésticos"), ("Lavadoras", "ajustan"), ("Ciclo de lavado", "según"), ("Carga y suciedad", "y"), ("Aires acondicionados", "regulan"), ("Temperatura suave", "y"), ("Cámaras digitales", "con"), ("Autoenfoque estabilizado", "en"), ("Automotriz", "sistemas"), ("Frenos ABS", "y"), ("Control crucero", "para"), ("Conducción suave", "y"), ("Eficiencia energética", None)
                            ]
                        ]
                    }
                ],
            },
            {
                "titulo": "4.5. PLN",
                "conector": "Interacción mediante",
                "ramas": [
                    {
                        "titulo": "4.5.1. Conceptos básicos",
                        "conector": "Niveles de análisis",
                        "ramas": [
                            [
                                (None, "Lenguaje humano"), ("Morfología", "estructura"), ("De palabras", "y"), ("Sintaxis", "reglas"), ("Gramaticales", "y"), ("Semántica", "significado"), ("Del texto", "y"), ("Pragmática", "contexto"), ("De uso", "requiere"), ("Tokenización", "dividir"), ("En unidades", "y"), ("Eliminación ruido", "como"), ("Stop-words", "usa"), ("Embeddings", "vectores"), ("Numéricos", "para"), ("Representar palabras", None)
                            ]
                        ]
                    },
                    {
                        "titulo": "4.5.2. Desarrollos",
                        "conector": "Tecnologías clave",
                        "ramas": [
                            [
                                (None, "Traducción automática"), ("Neural", "como"), ("Google Translate", "y"), ("Asistentes voz", "tipo"), ("Siri o Alexa", "que"), ("Entienden comandos", "y"), ("Análisis sentimientos", "en"), ("Redes sociales", "para"), ("Opinión pública", "y"), ("Modelos LLM", "como"), ("GPT", "para"), ("Generación texto", "y"), ("Resumen automático", "de"), ("Documentos largos", None)
                            ]
                        ]
                    }
                ],
            },
            {
                "titulo": "4.6. Sistemas Expertos",
                "conector": "Emulan al",
                "ramas": [
                    {
                        "titulo": "4.6.1. Conceptos básicos",
                        "conector": "Componentes del SE",
                        "ramas": [
                            [
                                (None, "Experto humano"), ("Base de conocimiento", "guarda"), ("Hechos y reglas", "y"), ("Motor de inferencia", "aplica"), ("Lógica", "para"), ("Deducir respuestas", "y"), ("Interfaz usuario", "para"), ("Consultas", "incluye"), ("Módulo explicación", "justifica"), ("El razonamiento", "y"), ("Módulo adquisición", "para"), ("Añadir saber", "del"), ("Dominio específico", None)
                            ]
                        ]
                    },
                    {
                        "titulo": "4.6.2. Clasificación",
                        "conector": "Tipos de inferencia",
                        "ramas": [
                            [
                                (None, "Basados en reglas"), ("Lógica determinista", "si-entonces"), ("Fáciles de leer", "y"), ("Basados en casos", "CBR"), ("Usan historia", "de"), ("Problemas previos", "y"), ("Basados en redes", "Bayesianas"), ("Probabilísticos", "para"), ("Incertidumbre", "y"), ("Sistemas híbridos", "combinan"), ("Reglas y IA", "para"), ("Mayor robustez", None)
                            ]
                        ]
                    },
                    {
                        "titulo": "4.6.3. Desarrollos",
                        "conector": "Áreas de uso",
                        "ramas": [
                            [
                                (None, "Diagnóstico médico"), ("Sistemas como", "MYCIN"), ("Identifican bacterias", "y"), ("Finanzas", "para"), ("Aprobación créditos", "y"), ("Detección fraude", "en"), ("Transacciones", "y"), ("Soporte técnico", "para"), ("Troubleshooting", "de"), ("Maquinaria compleja", "y"), ("Configuración sistemas", "planificación"), ("De recursos empresariales",  None)
                            ]
                        ]
                    }
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
    "PALETTE": [
        ("#60a5fa", "#1e3a8a"),
        ("#a3e635", "#4d7c0f" ),
        ("#fca5a5", "#7f1d1d" ),
        ("#f0abfc", "#86198f" ),
    ],
    "START_X": 120,
    "START_Y": 40,
    "OUTPUT_FILE": os.path.join("Mapas", "Mapa_conceptual_OBED_IA_U4.drawio"),
}


def run():
    """Permite ejecutar el generador directamente desde este archivo."""
    base_dir = os.path.dirname(__file__)
    scripts_dir = os.path.join(base_dir, "Scripts")
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)

    from Mapas_conceptuales import generar_mapa_conceptual

    out_path = generar_mapa_conceptual(concept_map, CONFIG)
    print(f"Mapa conceptual generado en: {out_path}")


if __name__ == "__main__":
    run()
