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
        "titulo_principal": "Unidad 4. IA Aplicada",
        "subtitulos": [
            {
                "titulo": "4.1. Robótica",
                "conector": "Sinergia de ingeniería",
                "ramas": [
                    {
                        "titulo": "4.1.1. Conceptos básicos",
                        "conector": "Ciclo de control",
                        "ramas": [
                            [
                                (None, "Máquina programable"), ("Multifuncional", "capaz de"), ("Manipular materias", "mediante"), ("Trayectorias variables", "sigue el"), ("Ciclo SPA", "Sense-Plan-Act"), ("Sentir el mundo", "con"), ("Percepción sensorial", "luego"), ("Planificar acción", "usando"), ("Algoritmos control", "y"), ("Modelos del mundo", "para"), ("Ejecutar tarea", "con"), ("Efectores finales", "como"), ("Pinzas o herramientas", "requiere"), ("Grados de libertad", "para"), ("Movimiento espacial", "en"), ("Espacio de trabajo", "y"), ("Fuente de energía", "eléctrica"), ("O hidráulica", "buscando"), ("Interacción física", "segura"), ("Con el entorno", None)
                            ]
                        ]
                    },
                    {
                        "titulo": "4.1.2. Clasificación",
                        "conector": "Categorías por",
                        "ramas": [
                            [
                                (None, "Por autonomía"), ("Teleoperados", "controlados por"), ("Humano remoto", "o"), ("Semiautónomos", "con"), ("Supervisión humana", "y"), ("Autónomos puros", "con"), ("IA embarcada", "también"), ("Por entorno", "como"), ("Terrestres (UGV)", "con"), ("Ruedas o patas", "y"), ("Aéreos (UAV)", "de"), ("Ala fija o rotatoria", "y"), ("Submarinos (AUV)", "para"), ("Alta presión", "además"), ("Por generación", "desde"), ("Repetidores simples", "hasta"), ("Cognitivos", "que"), ("Aprenden tareas", None)
                            ]
                        ]
                    },
                    {
                        "titulo": "4.1.3. Desarrollos",
                        "conector": "Tendencias punta",
                        "ramas": [
                            [
                                (None, "Robótica de enjambre"), ("Coordinación grupal", "inspirada en"), ("Insectos", "para"), ("Tareas distribuidas", "y"), ("Robótica blanda", "usando"), ("Materiales flexibles", "como"), ("Silicona", "para"), ("Manipulación delicada", "de"), ("Frutas o tejidos", "y"), ("Nanobots", "para"), ("Medicina interna", "navegando"), ("Flujo sanguíneo", "y"), ("Robots humanoides", "como"), ("Atlas o Tesla Bot", "para"), ("Entornos humanos", "usando"), ("Equilibrio dinámico", "y"), ("Visión estéreo", "avanzada"), ("Para navegación", None)
                            ]
                        ]
                    }
                ],
            },
            {
                "titulo": "4.2. Redes Neuronales",
                "conector": "Computación conexionista",
                "ramas": [
                    {
                        "titulo": "4.2.1. Conceptos básicos",
                        "conector": "Funcionamiento interno",
                        "ramas": [
                            [
                                (None, "Procesamiento paralelo"), ("Masivo", "simula"), ("Sinapsis biológicas", "donde"), ("El conocimiento", "reside en"), ("Fuerza de conexión", "o"), ("Pesos numéricos", "requiere"), ("Entrenamiento", "por"), ("Épocas iterativas", "calculando"), ("Función de pérdida", "que mide"), ("Error cometido", "y usa"), ("Optimizador", "como"), ("Adam o SGD", "para"), ("Actualizar pesos", "evitando"), ("Sobreajuste (Overfitting)", "con"), ("Regularización", "como"), ("Dropout", "para"), ("Generalizar bien", "ante"), ("Datos nuevos", None)
                            ]
                        ]
                    },
                    {
                        "titulo": "4.2.2. Clasificación",
                        "conector": "Arquitecturas clave",
                        "ramas": [
                            [
                                (None, "Feedforward"), ("Unidireccionales", "flujo"), ("Entrada a salida", "sin"), ("Ciclos internos", "vs"), ("Recurrentes (LSTM)", "con"), ("Bucles de retroalimentación", "para"), ("Recordar contexto", "y"), ("Autoencoders", "para"), ("Compresión datos", "aprendiendo"), ("Representación latente", "y"), ("GANs", "adversarias"), ("Generativas", "con"), ("Generador y discriminador", "compitiendo"), ("Para crear", "datos sintéticos"), ("Realistas", "desde"), ("Ruido aleatorio", None)
                            ]
                        ]
                    },
                    {
                        "titulo": "4.2.3. Desarrollos",
                        "conector": "Impacto actual",
                        "ramas": [
                            [
                                (None, "Modelos fundacionales"), ("Pre-entrenados", "con"), ("Big Data", "como"), ("GPT-4 o Llama", "para"), ("Razonamiento complejo", "y"), ("Difusión estable", "para"), ("Texto a imagen", "y"), ("Conducción autónoma", "procesando"), ("Sensores en vivo", "para"), ("Predicción trayectorias", "y"), ("Descubrimiento fármacos", "prediciendo"), ("Afinidad química", "acelerando"), ("Ensayos clínicos", "y"), ("Detección deepfakes", "analizando"), ("Artefactos digitales", "en"), ("Videos manipulados", None)
                            ]
                        ]
                    }
                ],
            },
            {
                "titulo": "4.3. Visión Artificial",
                "conector": "Interpretación visual",
                "ramas": [
                    {
                        "titulo": "4.3.1. Conceptos básicos",
                        "conector": "Cadena de proceso",
                        "ramas": [
                            [
                                (None, "Matriz de píxeles"), ("Representa imagen", "con"), ("Canales de color", "RGB"), ("Requiere filtrado", "para"), ("Suavizar texturas", "y"), ("Detección rasgos", "como"), ("Esquinas o bordes", "usando"), ("Operadores matemáticos", "como"), ("Sobel o Canny", "para"), ("Mapa de características", "luego"), ("Emparejamiento", "comparando"), ("Con base datos", "o"), ("Redes convolucionales", "para"), ("Abstracción jerárquica", "desde"), ("Líneas simples", "hasta"), ("Objetos completos", None)
                            ]
                        ]
                    },
                    {
                        "titulo": "4.3.2. Desarrollos",
                        "conector": "Soluciones reales",
                        "ramas": [
                            [
                                (None, "Diagnóstico por imagen"), ("Detecta tumores", "en"), ("Resonancias magnéticas", "con"), ("Mayor sensibilidad", "que"), ("Ojo humano", "también"), ("Supervisión urbana", "para"), ("Gestión tráfico", "leyendo"), ("Matrículas", "y"), ("Flujo vehicular", "en"), ("Smart Cities", "y"), ("Retail inteligente", "como"), ("Amazon Go", "sin"), ("Cajeros físicos", "rastreando"), ("Productos tomados", "y"), ("Control calidad", "en"), ("Fábricas", "descartando"), ("Piezas defectuosas", None)
                            ]
                        ]
                    }
                ],
            },
            {
                "titulo": "4.4. Lógica Difusa",
                "conector": "Matemática vaga",
                "ramas": [
                    {
                        "titulo": "4.4.1. Conceptos básicos",
                        "conector": "Grados de verdad",
                        "ramas": [
                            [
                                (None, "Lógica multivaluada"), ("Rompe binarismo", "del"), ("Cero y uno", "acepta"), ("Pertenencia parcial", "como"), ("70% Caliente", "usa"), ("Funciones de membresía", "triangulares"), ("O trapezoidales", "para"), ("Modelar lenguaje", "natural"), ("Como 'Muy rápido'", "o"), ("'Poco costoso'", "permite"), ("Reglas heurísticas", "de"), ("Expertos humanos", "sin"), ("Fórmulas exactas", "ideal para"), ("Sistemas no lineales", "o"), ("Difíciles", "de"), ("modelar matemáticamente", None)
                            ]
                        ]
                    },
                    {
                        "titulo": "4.4.2. Desarrollos",
                        "conector": "Control robusto",
                        "ramas": [
                            [
                                (None, "Trenes bala"), ("Metro Sendai", "suaviza"), ("Aceleración y freno", "para"), ("Confort pasajeros", "y"), ("Hornos industriales", "mantienen"), ("Temperatura estable", "ahorrando"), ("Combustible", "y"), ("Transmisiones coche", "eligen"), ("Marcha óptima", "según"), ("Estilo conducción", "y"), ("Pendiente carretera", "también"), ("Enfoque cámaras", "ajusta"), ("Lentes", "bajo"), ("Luz variable", "y"), ("Sistemas de riego", "según"), ("Humedad suelo", None)
                            ]
                        ]
                    }
                ],
            },
            {
                "titulo": "4.5. PLN",
                "conector": "Puente hombre-máquina",
                "ramas": [
                    {
                        "titulo": "4.5.1. Conceptos básicos",
                        "conector": "Desafíos lingüísticos",
                        "ramas": [
                            [
                                (None, "Ambigüedad léxica"), ("Palabras polisémicas", "requieren"), ("Desambiguación", "por"), ("Contexto cercano", "usa"), ("Corpus de texto", "para"), ("Entrenar modelos", "aplica"), ("Stemming", "cortar"), ("Raíces palabras", "y"), ("Lematización", "buscar"), ("Forma base", "analiza"), ("Entidades nombradas", "como"), ("Personas y lugares", "NER"), ("Análisis sintáctico", "árbol"), ("De dependencias", "quién"), ("Hace qué", "a"), ("quién", None)
                            ]
                        ]
                    },
                    {
                        "titulo": "4.5.2. Desarrollos",
                        "conector": "Herramientas diarias",
                        "ramas": [
                            [
                                (None, "Chatbots atención"), ("24/7", "resuelven"), ("Dudas frecuentes", "y"), ("Filtro de Spam", "detecta"), ("Patrones maliciosos", "en"), ("Correos", "y"), ("Resumen legal", "extracta"), ("Cláusulas clave", "de"), ("Contratos largos", "y"), ("Corrección gramatical", "estilo"), ("Grammarly", "mejora"), ("Redacción", "y"), ("Búsqueda semántica", "entiende"), ("Intención usuario", "no solo"), ("Palabras ", "clave"), ("exactas", None)
                            ]
                        ]
                    }
                ],
            },
            {
                "titulo": "4.6. Sistemas Expertos",
                "conector": "Conocimiento codificado",
                "ramas": [
                    {
                        "titulo": "4.6.1. Conceptos básicos",
                        "conector": "Arquitectura clásica",
                        "ramas": [
                            [
                                (None, "Captura pericia"), ("De especialistas", "para"), ("Resolver problemas", "específicos"), ("Separa conocimiento", "de la"), ("Máquina inferencia", "que es el"), ("Motor lógico", "usa"), ("Encadenamiento", "hacia"), ("Adelante (datos a meta)", "o"), ("Atrás (meta a datos)", "para"), ("Validar hipótesis", "es"), ("Consistente", "y"), ("No se cansa", "pero"), ("Carece de intuición", "o"), ("Sentido común", "general"), ("fuera de", "su"), ("Dominio acotado", None)
                            ]
                        ]
                    },
                    {
                        "titulo": "4.6.2. Clasificación",
                        "conector": "Estilos de diseño",
                        "ramas": [
                            [
                                (None, "Probabilísticos"), ("Usan Teorema Bayes", "para"), ("Evidencia incierta", "y"), ("Sistemas de pizarra", "múltiples"), ("Fuentes conocimiento", "escriben en"), ("Memoria compartida", "para"), ("Colaborar", "y"), ("Sistemas difusos", "reglas con"), ("Vaguedad", "y"), ("Sistemas de cuadros", "frames"), ("Estructuras jerárquicas", "con"), ("Herencia propiedades", "para"), ("Organizar objetos", "y"), ("Conceptos", None)
                            ]
                        ]
                    },
                    {
                        "titulo": "4.6.3. Desarrollos",
                        "conector": "Nichos de uso",
                        "ramas": [
                            [
                                (None, "Configuración PC"), ("Como XCON", "validaba"), ("Componentes VAX", "y"), ("Geología", "como"), ("PROSPECTOR", "para"), ("Hallar minerales", "y"), ("Asesoría legal", "generando"), ("Documentos estándar", "y"), ("Diagnóstico fallas", "en"), ("Redes eléctricas", "o"), ("Locomotoras", "también"), ("Planificación vuelos", "asignando"), ("Puertas y pistas", "en"), ("Aeropuertos saturados", None)
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
    "FONT_FAMILY": "Tahoma", # Familia de fuente para las cajas
    "FONT_SIZE": 12, # Tamaño de fuente en puntos
    "FONT_BOLD": False,  # True para negrita
    "FONT_ITALIC": True,  # True para cursiva
    "FONT_COLOR": "#000000",  # Color de fuente 
    "STROKE_W": 3, # Grosor del borde de las cajas
    "EDGE_COLOR": "#000000", # Color del borde de las flechas
    "BOX_ARC_SIZE": 25, # Radio de las esquinas redondeadas
    "BOX_SHADOW": True, # Sombra en las cajas
    "MAIN_FILL_COLOR": "#ffffff", # Color de relleno del título principal
    "MAIN_STROKE_COLOR": "#000000", # Color del borde del título principal
    "SUBTITLE_FILL_COLOR": "#FFFFFF", # Color de relleno de los subtítulos
    "SUBTITLE_STROKE_COLOR": "#9e9e9e", # Color del borde de los subtítulos
    "CONNECTOR_FONT_FAMILY": "Courier New", # Fuente de los conectores
    "CONNECTOR_FONT_SIZE": 9, # Tamaño de fuente de los conectores
    "CONNECTOR_FONT_COLOR": "#184f96", # Color de fuente de los conectores
    "CONNECTOR_BG_COLOR": "#ffffff", # Color de fondo de los conectores
    "CONNECTOR_BORDER_COLOR": "#FFFFFF", # Color del borde de los conectores
    "CONNECTOR_SHADOW": False, # Sombra en los conectores
    "CONNECTOR_TEXT_SHADOW": False, # Sombra en el texto de los conectores
    "BOX_W": 100, # Ancho base de las cajas
    "BOX_H": 40, # Alto base de las cajas
    "X_STEP": 130, # Paso horizontal entre cajas
    "Y_STEP": 90, # Paso vertical entre cajas
    "POSITION_NOISE": 7, # Ruido aleatorio en la posición de las cajas
    "MAIN_TO_SUBTITLE": 130, # Distancia del título principal a los subtítulos
    "SUBTITLE_TO_BRANCH": 150, # Distancia de los subtítulos a las ramas
    "SUBTITLE_GAP": 40, # Separación entre subtítulos
    "GROUP_GAP": 70, # Separación entre grupos de ramas
    "PALETTE": [
        ("#FFFFFF", "#1e3a8a"),
        ("#FFFFFF", "#1e3a8a" ),
        ("#FFFFFF", "#7f1d1d" ),
        ("#FFFFFF", "#7f1d1d" ),
    ],
    "START_X": 120,
    "START_Y": 40,
    "OUTPUT_FILE": os.path.join("Mapas", "Mapa_conceptual_IA_MARIO_U4.drawio"),
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
