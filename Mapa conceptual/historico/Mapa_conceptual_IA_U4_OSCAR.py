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
        "titulo_principal": "Unidad 4. Aplicaciones con técnicas de IA.",
        "subtitulos": [
            {
                "titulo": "4.1. Robótica",
                "conector": "Automata físico",
                "ramas": [
                    {
                        "titulo": "4.1.1. Conceptos básicos",
                        "conector": "Componentes clave",
                        "ramas": [
                            [
                                (None, "Estructura mecánica"), ("Eslabones rígidos", "unidos por"), ("Articulaciones", "que dan"), ("Movilidad", "medida en"), ("Grados de Libertad", "o DOF"), ("Sistema sensorial", "usa"), ("Propioceptivos", "estado interno"), ("Batería o calor", "y"), ("Exteroceptivos", "entorno externo"), ("Cámaras o Lidar", "sistema de"), ("Locomoción", "mediante"), ("Ruedas", "o"), ("Piernas", "para"), ("Desplazamiento", "controlado por"), ("Microcontroladores", "que ejecutan"), ("Lógica de control", "en"), ("Tiempo real", "garantizando"), ("Estabilidad dinámica", "y"), ("Precisión", "en"), ("Trayectorias complejas", None)
                            ],
                            [
                                (None, "Actuadores físicos"), ("Motores eléctricos", "DC o Paso"), ("Servomotores", "para"), ("Posición precisa", "y"), ("Hidráulica", "para"), ("Alta fuerza", "en"), ("Robots pesados", "y"), ("Neumática", "para"), ("Movimientos rápidos", "usando"), ("Aire comprimido", "accionan"), ("Efectores finales", "como"), ("Pinzas o grippers", "para"), ("Manipulación", "o"), ("Herramientas", "como"), ("Soldadores", "o"), ("Pistolas pintura", "requieren"), ("Drivers de potencia", "para"), ("Controlar voltaje", "y"), ("Corriente", "segura"), ("Del sistema", None)
                            ]
                        ]
                    },
                    {
                        "titulo": "4.1.2. Clasificación",
                        "conector": "Tipología general",
                        "ramas": [
                            [
                                (None, "Poliarticulados"), ("Brazos fijos", "con"), ("Espacio limitado", "y"), ("Móviles", "plataformas con"), ("Navegación libre", "y"), ("Zoomórficos", "imitan a"), ("Animales", "para"), ("Terrenos difíciles", "y"), ("Híbridos", "combinan"), ("Ruedas y patas", "para"), ("Versatilidad", "y"), ("Nano-robots", "nivel"), ("Molecular", "para"), ("Precisión extrema", "y"), ("Androides", "con"), ("Forma humana", "para"), ("Interacción social", "y"), ("Exoesqueletos", "para"), ("Potenciar fuerza", "del"), ("Usuario humano", None)
                            ],
                            [
                                (None, "Por entorno"), ("Industriales", "entornos"), ("Controlados", "y"), ("De servicio", "entornos"), ("Humanos", "no estructurados"), ("Médicos", "quirófanos"), ("Alta precisión", "y"), ("Militares", "campo de"), ("Batalla", "y"), ("Espaciales", "gravedad"), ("Cero o vacío", "y"), ("Educativos", "aulas"), ("Para enseñanza", "y"), ("Domésticos", "hogar"), ("Limpieza", "según"), ("Su autonomía", "son"), ("Teleoperados", "o"), ("Autónomos", "o"), ("Semiautónomos", None)
                            ]
                        ]
                    },
                    {
                        "titulo": "4.1.3. Desarrollos",
                        "conector": "Estado del arte",
                        "ramas": [
                            [
                                (None, "Robótica Colaborativa"), ("Cobots seguros", "trabajan"), ("Junto a humanos", "sin"), ("Jaulas de seguridad", "gracias a"), ("Sensores de fuerza", "y"), ("Domótica avanzada", "robots"), ("Limpiadores", "y"), ("Cocineros", "y"), ("Logística autónoma", "almacenes con"), ("AGVs", "que mueven"), ("Estanterías enteras", "optimizando"), ("Flujo de pedidos", "usando"), ("SLAM visual", "para"), ("Mapeo constante", "y"), ("Evitación obstáculos", "dinámicos"), ("En tiempo real", "reduciendo"), ("Accidentes laborales", "y"), ("Costos operativos", "de"), ("Bodega", None)
                            ],
                            [
                                (None, "Robótica blanda"), ("Materiales flexibles", "como"), ("Silicona o goma", "para"), ("Agarre suave", "de"), ("Objetos frágiles", "como"), ("Frutas o tejidos", "inspirado en"), ("Pulpos o gusanos", "usa"), ("Fluidos a presión", "para"), ("Deformación controlada", "permite"), ("Adaptabilidad", "a"), ("Formas irregulares", "y"), ("Seguridad inherente", "al"), ("No lastimar", "ideal para"), ("Rehabilitación", "y"), ("Prótesis cómodas", "y"), ("Exploración", "en"), ("Espacios estrechos", "donde"), ("Metal rígido", "no entra"), ("Fácilmente", None)
                            ]
                        ]
                    }
                ],
            },
            {
                "titulo": "4.2. Redes Neuronales",
                "conector": "Cerebro digital",
                "ramas": [
                    {
                        "titulo": "4.2.1. Conceptos básicos",
                        "conector": "Modelo matemático",
                        "ramas": [
                            [
                                (None, "Unidad básica"), ("Perceptrón", "recibe"), ("Vector de entrada", "multiplicado por"), ("Matriz de pesos", "más un"), ("Sesgo (Bias)", "pasa por"), ("Función no lineal", "tipo"), ("Sigmoide", "o"), ("Tangente hiperbólica", "generando"), ("Activación", "propagada hacia"), ("Capas siguientes", "hasta la"), ("Salida final", "comparada con"), ("Valor esperado", "para calcular"), ("Gradiente", "del error"), ("Global", "mediante"), ("Backpropagation", "que"), ("Ajusta pesos", "hacia"), ("Atrás", "para"), ("Minimizar pérdida", "en"), ("Entrenamiento", None)
                            ],
                            [
                                (None, "Hiperparámetros"), ("Tasa aprendizaje", "controla"), ("Velocidad ajuste", "del"), ("Gradiente", "el"), ("Tamaño de lote", "define"), ("Muestras por paso", "las"), ("Épocas", "número de"), ("Vueltas completas", "al"), ("Dataset", "la"), ("Función de pérdida", "mide"), ("Desempeño", "como"), ("Error cuadrático", "o"), ("Entropía cruzada", "y el"), ("Optimizador", "como"), ("Adam o SGD", "guía la"), ("Convergencia", "evitando"), ("Mínimos locales", "y"), ("Overfitting", "usando"), ("Dropout", "aleatorio"), ("Regularización L2", None)
                            ]
                        ]
                    },
                    {
                        "titulo": "4.2.2. Clasificación",
                        "conector": "Topologías",
                        "ramas": [
                            [
                                (None, "Monocapa"), ("Resolución simple", "solo"), ("Linealmente separables", "y"), ("Multicapa", "resuelve"), ("Problemas no lineales", "como"), ("XOR", "y"), ("Radiales (RBF)", "basadas en"), ("Distancia al centro", "para"), ("Interpolación", "y"), ("Mapas Kohonen", "auto-organizativos"), ("No supervisados", "para"), ("Clustering visual", "de"), ("Datos complejos", "y"), ("Convolucionales CNN", "filtros"), ("Deslizantes", "para"), ("Imágenes", "y"), ("Recurrentes RNN", "bucles"), ("Temporales", "para"), ("Series de tiempo", "o"), ("Secuencias texto", None)
                            ],
                            [
                                (None, "Arquitecturas Gen"), ("Autoencoders", "comprimen"), ("Datos a latente", "y"), ("Reconstruyen", "para"), ("Reducir ruido", "y"), ("GANs", "redes"), ("Adversarias", "generador vs"), ("Discriminador", "crean"), ("Datos sintéticos", "realistas"), ("Transformers", "mecanismo"), ("Atención", "paralelizable"), ("Para NLP", "y"), ("Vision Transformers", "patches"), ("De imagen", "como"), ("Tokens", "y"), ("LSTMs", "memoria"), ("Largo plazo", "evita"), ("Desvanecimiento", "del"), ("Gradiente", "antiguo"), ("Problema RNN", None)
                            ]
                        ]
                    },
                    {
                        "titulo": "4.2.3. Desarrollos",
                        "conector": "Usos modernos",
                        "ramas": [
                            [
                                (None, "Visión por computador"), ("YOLO", "detecta"), ("Objetos en vivo", "y"), ("Procesamiento de audio", "elimina"), ("Ruido de fondo", "en"), ("Llamadas", "y"), ("Predicción financiera", "analiza"), ("Series temporales", "de"), ("La bolsa", "y"), ("Juegos", "NPCs con"), ("Comportamiento humano", "adaptativo"), ("En tiempo real", "y"), ("Diagnóstico médico", "detecta"), ("Cáncer en RX", "mejor que"), ("Radiólogos", "y"), ("Deepfakes", "crea"), ("Videos falsos", "requiere"), ("Ética", "y"), ("Regulación", "estricta"), ("Mundial", None)
                            ],
                            [
                                (None, "Aceleración Hardware"), ("TPUs de Google", "matrices"), ("Tensoriales", "y"), ("GPUs de NVIDIA", "paralelismo"), ("CUDA", "para"), ("Entrenamiento masivo", "y"), ("NPUs móviles", "en"), ("Teléfonos", "para"), ("IA en borde", "sin"), ("Nube", "y"), ("Chips neuromórficos", "imitan"), ("Neuronas físicas", "como"), ("Loihi de Intel", "ahorran"), ("Energía", "y"), ("FPGAs", "hardware"), ("Reprogramable", "para"), ("Inferencia rápida", "y"), ("Latencia baja", "en"), ("Coches autónomos", "críticos"), ("Seguridad", None)
                            ]
                        ]
                    }
                ],
            },
            {
                "titulo": "4.3. Visión Artificial",
                "conector": "Ojos electrónicos",
                "ramas": [
                    {
                        "titulo": "4.3.1. Conceptos básicos",
                        "conector": "Etapas análisis",
                        "ramas": [
                            [
                                (None, "Captura digital"), ("Muestreo espacial", "y"), ("Cuantización color", "define"), ("Resolución", "sigue el"), ("Filtrado", "aplicando"), ("Convolución", "con"), ("Kernels", "para"), ("Realzar bordes", "luego"), ("Segmentación", "por"), ("Umbralización", "separa"), ("Fondo y figura", "finalmente"), ("Reconocimiento", "etiquetando"), ("Regiones", "con"), ("Semántica", "usando"), ("Clasificadores", "entrenados"), ("Previamente", "para"), ("Identificar", "personas"), ("Coches", "o"), ("Defectos", "visuales"), ("Patrones", None)
                            ],
                            [
                                (None, "Técnicas avanzadas"), ("Flujo óptico", "rastrea"), ("Movimiento píxeles", "entre"), ("Fotogramas", "y"), ("Visión estéreo", "usa"), ("Dos cámaras", "para"), ("Calcular profundidad", "mapa"), ("Disparidad", "y"), ("SLAM", "localización"), ("Y mapeo", "simultáneo"), ("Para robots", "y"), ("Fotogrametría", "reconstruye"), ("Modelos 3D", "desde"), ("Fotos 2D", "y"), ("Detección puntos", "clave"), ("SIFT o ORB", "para"), ("Emparejar imágenes", "en"), ("Panorámicas", "o"), ("Reconocimiento objetos", "rotados"), ("Escalados", None)
                            ]
                        ]
                    },
                    {
                        "titulo": "4.3.2. Desarrollos",
                        "conector": "Aplicación real",
                        "ramas": [
                            [
                                (None, "Control calidad"), ("Detecta grietas", "en"), ("Metalurgia", "y"), ("Lectura OCR", "digitaliza"), ("Documentos físicos", "a"), ("Texto editable", "y"), ("Seguridad vial", "detecta"), ("Fatiga conductor", "por"), ("Parpadeo ojos", "y"), ("Realidad Mixta", "ancla"), ("Objetos virtuales", "en"), ("Superficies reales", "y"), ("Agricultura", "monitoriza"), ("Salud cultivos", "por"), ("Color hojas", "y"), ("Retail", "tiendas"), ("Sin cajeros", "rastrea"), ("Productos cogidos", "y"), ("Cobro automático", "al"), ("Salir", None)
                            ],
                            [
                                (None, "Medicina digital"), ("Segmentación tumores", "en"), ("Resonancias", "y"), ("Conteo células", "en"), ("Microscopio", "automático"), ("Cirugía asistida", "guía"), ("Instrumentos", "con"), ("Realidad aumentada", "sobre"), ("El paciente", "y"), ("Dermatología", "analiza"), ("Lunares", "para"), ("Detección melanoma", "temprano"), ("Endoscopia", "detecta"), ("Pólipos", "en"), ("Tiempo real", "y"), ("Análisis marcha", "para"), ("Rehabilitación", "motora"), ("Diagnóstico preciso", "no"), ("Invasivo", None)
                            ]
                        ]
                    }
                ],
            },
            {
                "titulo": "4.4. Lógica Difusa",
                "conector": "Control flexible",
                "ramas": [
                    {
                        "titulo": "4.4.1. Conceptos básicos",
                        "conector": "Teoría de conjuntos",
                        "ramas": [
                            [
                                (None, "Conjuntos clásicos"), ("Bordes nítidos", "vs"), ("Conjuntos difusos", "con"), ("Bordes graduales", "usa"), ("Variables lingüísticas", "ejemplo"), ("Temperatura", "valores como"), ("Frío, Tibio, Caliente", "define"), ("Reglas IF-THEN", "si"), ("Error es grande", "entonces"), ("Acción es fuerte", "permite"), ("Razonamiento aproximado", "similar al"), ("Humano", "sin"), ("Ecuaciones diferenciales", "exactas"), ("Maneja incertidumbre", "y"), ("Vaguedad", "del"), ("Mundo real", "donde"), ("Todo es relativo", "y"), ("No binario", "cero"), ("O uno", None)
                            ],
                            [
                                (None, "Sistema inferencia"), ("Fusificación", "convierte"), ("Dato crisp", "a"), ("Grado pertenencia", "0 a 1"), ("Base de reglas", "conocimiento"), ("Experto", "codificado"), ("Motor inferencia", "aplica"), ("Implicación", "tipo"), ("Mamdani", "o"), ("Sugeno", "agrega"), ("Resultados difusos", "y"), ("Defusificación", "convierte"), ("Salida difusa", "a"), ("Valor concreto", "usando"), ("Centroide", "o"), ("Promedio ponderado", "para"), ("Actuadores físicos", "como"), ("Motores", "o"), ("Válvulas", "reales"), ("Analógicas", None)
                            ]
                        ]
                    },
                    {
                        "titulo": "4.4.2. Desarrollos",
                        "conector": "Implementaciones",
                        "ramas": [
                            [
                                (None, "Ascensores inteligentes"), ("Suavizan parada", "y"), ("Optimizan espera", "y"), ("Lavaplatos", "ajustan"), ("Detergente", "según"), ("Turbidez del agua", "y"), ("Enfoque de cámaras", "estabiliza"), ("Imagen", "ante"), ("Movimiento mano", "y"), ("Control de tráfico", "ajusta"), ("Semáforos", "según"), ("Densidad coches", "y"), ("Transmisión auto", "elige"), ("Marcha óptima", "según"), ("Pendiente", "y"), ("Estilo conductor", "y"), ("Frenos ABS", "evita"), ("Bloqueo rueda", "en"), ("Superficie mixta", "hielo"), ("Asfalto", None)
                            ],
                            [
                                (None, "Toma decisiones"), ("Evaluación riesgo", "bancario"), ("Clientes dudosos", "y"), ("Diagnóstico médico", "síntomas"), ("Vagos", "como"), ("'Dolor leve'", "y"), ("Control industrial", "hornos"), ("Cementeros", "con"), ("Dinámica lenta", "y"), ("Sistemas aire", "acondicionado"), ("Inverter", "mantiene"), ("Confort", "sin"), ("Picos consumo", "y"), ("Videojuegos", "IA"), ("Enemigos", "toman"), ("Decisiones creíbles", "no"), ("Perfectas", "para"), ("Jugabilidad", "más"), ("Orgánica", None)
                            ]
                        ]
                    }
                ],
            },
            {
                "titulo": "4.5. PLN",
                "conector": "Entendimiento texto",
                "ramas": [
                    {
                        "titulo": "4.5.1. Conceptos básicos",
                        "conector": "Estructura lenguaje",
                        "ramas": [
                            [
                                (None, "Fonología"), ("Sonidos del habla", "y"), ("Morfología", "formación de"), ("Palabras", "y"), ("Sintaxis", "orden y"), ("Gramática", "y"), ("Semántica (significado literal)", "y"), ("Pragmática (intención comunicativa)", "usa"), ("Corpus lingüístico", "gran"), ("Base de datos", "de"), ("Textos reales", "para"), ("Estadística", "y"), ("Aprendizaje", "resuelve"), ("Ambigüedad", "polisemia"), ("Banco asiento", "vs"), ("Banco dinero", "y"), ("Correferencia", "quién"), ("Es 'él'", "en"), ("La frase", "contexto"), ("Previo", None)
                            ],
                            [
                                (None, "Preprocesamiento"), ("Tokenización", "divide"), ("Texto en palabras", "o"), ("Tokens", "luego"), ("Stopwords", "elimina"), ("Artículos y preposiciones", "sin"), ("Carga semántica", "y"), ("Stemming", "recorta"), ("Sufijos", "a"), ("Raíz", "y"), ("Lematización", "busca"), ("Forma diccionario", "y"), ("Vectorización", "convierte"), ("Texto a números", "Bag of Words"), ("TF-IDF", "o"), ("Embeddings", "Word2Vec"), ("Captura relación", "rey"), ("Menos hombre", "más"), ("Mujer es", "reina"), ("Vectorial", None)
                            ]
                        ]
                    },
                    {
                        "titulo": "4.5.2. Desarrollos",
                        "conector": "Herramientas uso",
                        "ramas": [
                            [
                                (None, "Motores de búsqueda"), ("Rankean resultados", "por"), ("Relevancia semántica", "y"), ("Clasificación de spam", "filtra"), ("Correos basura", "y"), ("Resumen automático", "condensa"), ("Noticias", "en"), ("Titulares", "y"), ("Corrector ortográfico", "sugiere"), ("Cambios gramaticales", "en"), ("Procesadores texto", "y"), ("Minería de opinión", "en"), ("Reviews de productos", "saber"), ("Si es positiva", "o"), ("Negativa", "y"), ("Extracción información", "saca"), ("Fechas y nombres", "de"), ("Contratos legales", "para"), ("Bases de datos", "estructuradas"), ("Automáticas", None)
                            ],
                            [
                                (None, "Modelos Lenguaje"), ("Grandes LLMs", "como"), ("GPT-4", "generan"), ("Texto coherente", "y"), ("Código programación", "y"), ("Traducción automática", "neural"), ("Entre idiomas", "y"), ("Chatbots", "atención"), ("Al cliente", "24/7"), ("Responden dudas", "y"), ("Asistentes voz", "Alexa"), ("Siri", "convierten"), ("Voz a texto", "ASR"), ("Y texto a voz", "TTS"), ("Ejecutan comandos", "domóticos"), ("O búsquedas", "y"), ("Análisis sentimientos", "monitoriza"), ("Reputación marca", "en"), ("Redes sociales", "tiempo"), ("Real", None)
                            ]
                        ]
                    }
                ],
            },
            {
                "titulo": "4.6. Sistemas Expertos",
                "conector": "Consultores digitales",
                "ramas": [
                    {
                        "titulo": "4.6.1. Conceptos básicos",
                        "conector": "Estructura interna",
                        "ramas": [
                            [
                                (None, "Base de hechos"), ("Datos del caso", "actual"), ("Memoria de trabajo", "guarda"), ("Estado intermedio", "y"), ("Base de conocimiento", "reglas del"), ("Dominio experto", "y"), ("Motor de inferencia", "navega"), ("El árbol lógico", "para"), ("Llegar a conclusión", "y"), ("Interfaz explicativa", "muestra"), ("El 'por qué'", "de la"), ("Decisión final", "al"), ("Usuario", "no"), ("Es caja negra", "da"), ("Confianza", "y"), ("Módulo adquisición", "permite"), ("Al ingeniero", "añadir"), ("Nuevas reglas", "sin"), ("Reescribir código", "del"), ("Motor", None)
                            ],
                            [
                                (None, "Ingeniería Conocimiento"), ("Extraer saber", "del"), ("Experto humano", "mediante"), ("Entrevistas", "y"), ("Observación", "luego"), ("Representación", "codificar"), ("En lógica", "o"), ("Reglas formales", "y"), ("Validación", "probar"), ("Casos test", "para"), ("Verificar precisión", "y"), ("Mantenimiento", "actualizar"), ("Reglas obsoletas", "es"), ("Costoso", "y"), ("Lento", "el"), ("Cuello de botella", "de"), ("Estos sistemas", "pero"), ("Muy fiable", "en"), ("Su nicho", None)
                            ]
                        ]
                    },
                    {
                        "titulo": "4.6.2. Clasificación",
                        "conector": "Métodos resolución",
                        "ramas": [
                            [
                                (None, "Reglas de producción"), ("Si-Entonces", "lógica"), ("Modus Ponens", "y"), ("Redes semánticas", "nodos y"), ("Relaciones", "tipo"), ("'Es un'", "y"), ("Marcos (Frames)", "objetos con"), ("Atributos", "y"), ("Valores por defecto", "y"), ("Árboles de decisión", "preguntas binarias"), ("Hasta la hoja final", "y"), ("Lógica proposicional", "verdadero"), ("O falso", "y"), ("Lógica predicados", "más"), ("Expresiva", "con"), ("Variables", "y"), ("Cuantificadores", "para"), ("Relaciones complejas", "entre"), ("Objetos", None)
                            ],
                            [
                                (None, "Estrategia control"), ("Encadenamiento adelante", "desde"), ("Datos a meta", "data-driven"), ("Descubre consecuencias", "y"), ("Encadenamiento atrás", "desde"), ("Meta a datos", "goal-driven"), ("Verifica hipótesis", "como"), ("Médico diagnosticando", "y"), ("Búsqueda profundidad", "explora"), ("Una rama", "totalmente"), ("Búsqueda anchura", "explora"), ("Nivel por nivel", "y"), ("Heurística", "atajos"), ("Para podar", "ramas"), ("Improbables", "y"), ("Acelerar respuesta", "en"), ("Árboles grandes", "de"), ("Búsqueda", None)
                            ]
                        ]
                    },
                    {
                        "titulo": "4.6.3. Desarrollos",
                        "conector": "Campos aplicación",
                        "ramas": [
                            [
                                (None, "Mesa de ayuda"), ("Diagnóstico PC", "y"), ("Redes", "guía al"), ("Operador humano", "y"), ("Impuestos", "calcula"), ("Deducciones complejas", "según"), ("Ley vigente", "y"), ("Agricultura", "detecta"), ("Plagas", "y sugiere"), ("Tratamiento", "y"), ("Control aéreo", "asigna"), ("Rutas seguras", "evitando"), ("Colisiones", "y"), ("Configuración", "sistemas"), ("Complejos", "como"), ("Servidores", "o"), ("Maquinaria", "y"), ("Geología", "prospector"), ("Minerales", "evalúa"), ("Yacimientos", None)
                            ],
                            [
                                (None, "Integración moderna"), ("Sistemas híbridos", "usan"), ("Redes neuronales", "para"), ("Percibir", "y"), ("Sistemas expertos", "para"), ("Razonar", "y"), ("Web semántica", "reglas"), ("En ontologías", "OWL"), ("Para internet", "y"), ("Soporte decisión", "clínica"), ("En hospitales", "alerta"), ("Interacciones fármacos", "y"), ("Protocolos", "y"), ("Compliance legal", "audita"), ("Procesos", "contra"), ("Normativas", "y"), ("Ciberseguridad", "reglas"), ("De firewall", "y"), ("Detección intrusos", "basada"), ("En firmas", None)
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
    "FONT_FAMILY": "Arial", # Familia de fuente para las cajas
    "FONT_SIZE": 8, # Tamaño de fuente en puntos
    "FONT_COLOR": "#000000",  # Color de fuente 
    "FONT_BOLD": False,  # True para negrita
    "FONT_ITALIC": False,  # True para cursiva
    "STROKE_W": 1, # Grosor del borde de las cajas
    "EDGE_COLOR": "#676363", # Color del borde de los conectores    
    "BOX_ARC_SIZE": 8, # Radio de las esquinas redondeadas
    "BOX_SHADOW": False, # Sombra en las cajas
    "MAIN_FILL_COLOR": "#e67c4f", # Color de relleno del título principal
    "MAIN_STROKE_COLOR": "#000000", # Color del borde del título principal
    "SUBTITLE_FILL_COLOR": "#8AAEE0", # Color de relleno de los subtítulos
    "SUBTITLE_STROKE_COLOR": "#000000", # Color del borde de los subtítuloss
    "CONNECTOR_FONT_FAMILY": "Arial", # Fuente de los conectores
    "CONNECTOR_FONT_SIZE": 8, # Tamaño de fuente de los conectores
    "CONNECTOR_FONT_COLOR": "#000000", # Color de fuente de los conectores
    "CONNECTOR_BG_COLOR": "#FFFFFF", # Color de fondo de los conectores
    "CONNECTOR_BORDER_COLOR": "none", # Color del borde de los conectores
    "CONNECTOR_SHADOW": False, # Sombra en los conectores
    "CONNECTOR_TEXT_SHADOW": False, # Sombra en el texto de los conectores
    "BOX_W": 70, # Ancho base de las cajas
    "BOX_H": 45, # Alto base de las cajas
    "X_STEP": 100, # Paso horizontal entre cajas
    "Y_STEP": 90, # Paso vertical entre cajas
    "POSITION_NOISE": 1, # Ruido aleatorio en la posición de las cajas
    "MAIN_TO_SUBTITLE": 130, # Distancia del título principal a los subtítulos
    "SUBTITLE_TO_BRANCH": 150, # Distancia de los subtítulos a las ramas
    "SUBTITLE_GAP": 80, # Separación entre subtítulos
    "GROUP_GAP": 600, # Separación entre grupos de ramas
    # Coloreo jerarquico
    "COLOR_SUBTITLE_GROUPS": True,  # True: todas las ramas de un subtitulo comparten color
    "COLOR_NESTED_SUBTOPICS": False,  # True: cada sub-tema anidado usa un color propio
    "PALETTE": [
        ("#b7d3f6", "#000000"),
        ("#d9f3b0", "#000000" ),
        ("#f3caca", "#000000" ),
        ("#eccff1", "#000000" ),
    ],
    "START_X": 120,
    "START_Y": 40,
    "OUTPUT_FILE": os.path.join("Mapas", "Mapa_conceptual_IA_U4_OSCAR.drawio"),
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
