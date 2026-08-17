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
        "titulo_principal": "Unidad 2. Rep. Conocimiento IA",
        "subtitulos": [
            {
                "titulo": "2.1 Principios y Metodología",
                "conector": "Fundamentos de IA",
                "ramas": [
                    [
                        (None, "Definición IA"), ("Ciencia e ingeniería", "de"), ("Hacer máquinas", "que"), ("Requieren inteligencia", "si"), ("Fuesen humanos", "busca"), ("Simular procesos", "cognitivos"),
                        {
                            "texto": "Metas principales",
                            "conector": "se enfoca en",
                            "bifurcaciones": [
                                [
                                    (None, "Enfoque cognitivo"), ("Busca entender", "la mente"), ("Modelando", "procesos mentales"), ("Como la", "percepción"), ("Y el", "aprendizaje"), ("Usa herramientas", "como fMRI"), ("Para validar", "modelos"), ("Inspirado en", "psicología cognitiva"), ("Y neurociencia", "computacional"), ("Resultando en", "arquitecturas cognitivas"), ("Ciencia cognitiva", None)
                                ],
                                [
                                    (None, "Enfoque conductual"), ("Define IA", "por su conducta"), ("Si pasa la", "Prueba de Turing"), ("Un interrogador", "es engañado"), ("Creyendo que", "es humano"), ("Requiere capacidades", "como PNL"), ("Representar", "conocimiento"), ("Razonamiento", "automático"), ("Y aprendizaje", "continuo"), ("Para adaptarse", "a la conversación"), ("Aprendizaje automático", None)
                                ],
                                [
                                    (None, "Enfoque lógico"), ("Codifica el", "pensamiento racional"), ("En sistemas", "formales"), ("Usando lógica", "de predicados"), ("Para representar", "el conocimiento"), ("Un agente", "infiere lógicamente"), ("Nuevas conclusiones", "de hechos"), ("Base de los", "sistemas expertos"), ("Aunque frágil", "ante incertidumbre"), ("Resolución de problemas", None)
                                ],
                                [
                                    (None, "Enfoque racional"), ("Define un", "agente ideal"), ("Que actúa para", "lograr metas"), ("Dada su", "percepción"), ("Maximiza una", "medida de rendimiento"), ("Llamada", "utilidad esperada"), ("Aplica teoría", "de la decisión"), ("Y teoría de", "juegos"), ("Para elegir", "la mejor acción"), ("En entornos", "competitivos"), ("Toma de decisiones", None)
                                ]
                            ]
                        }
                    ],
                    [
                        (None, "Metodología AI"), ("Punto de", "partida"), ("Observación", "de un"), ("Fenómeno", "inteligente"), ("Ya sea", "humano"), ("O en la", "naturaleza"), ("Luego viene", "la"), ("Formulación", "de una"), ("Hipótesis", "explicativa"), ("Que se", "traduce en"), ("Un modelo", "formal"), ("Usando", "matemáticas"), ("O un", "algoritmo"), ("Implementado en", "software"), ("Se realiza", "experimentación"), ("Para recoger", "datos"), ("Que permitan", "validar"), ("O refutar", "el modelo"), ("Llevando a", "refinar teoría"), ("Ciclo iterativo", None)
                    ]
                ],
            },
            {
                "titulo": "2.2 Paradigmas IA",
                "conector": "Enfoques clásicos",
                "ramas": [
                    [
                        (None, "Paradigma Simbólico"), ("También llamado", "GOFAI"), ("Se basa en", "la hipótesis"), ("Del sistema", "de símbolos"), ("La inteligencia", "es"), ("Manipulación", "de símbolos"), ("Mediante", "reglas formales"), ("Como en", "la lógica"), ("Y la", "matemática"), ("El conocimiento", "es explícito"), ("Representado", "en bases"), ("De conocimiento", "y ontologías"), ("Usa algoritmos", "de búsqueda"), ("Para encontrar", "soluciones"), ("En un espacio", "de estados"), ("Es un enfoque", "de arriba-abajo"), ("Fuerte en", "razonamiento"), ("Y en", "planificación"), ("Pero frágil", "con incertidumbre"), ("Y percepción", "sensorial"), ("Planificación", None)
                    ],
                    [
                        (None, "Paradigma Conexionista"), ("Llamado", "sub-simbólico"), ("Inspirado en", "el cerebro"), ("Se basa en", "redes"), ("De neuronas", "artificiales"), ("Interconectadas", "en capas"), ("El conocimiento", "está implícito"), ("En los pesos", "de conexión"), ("Aprende de", "los datos"), ("Mediante un", "entrenamiento"), ("Ajustando los", "pesos"), ("Para minimizar", "el error"), ("Algoritmo clave", "es"), ("La retropropagación", "(backpropagation)"), ("Procesamiento", "masivo"), ("En paralelo", "y distribuido"), ("Es un enfoque", "de abajo-arriba"), ("Excelente en", "percepción"), ("Reconocimiento", "de patrones"), ("Visión y", "habla"), ("Deep Learning", None)
                    ],
                    [
                        (None, "Paradigma Evolutivo"), ("Inspirado en", "la evolución"), ("Biológica de", "Darwin"), ("Usa una", "población"), ("De soluciones", "candidatas"), ("Evaluadas con", "una función"), ("De aptitud", "(fitness)"), ("Los mejores", "se reproducen"), ("Usando cruce", "(crossover)"), ("Y mutación", "aleatoria"), ("Para explorar", "el espacio"), ("De búsqueda", "grande"),
                        {
                            "texto": "Otros híbridos",
                            "conector": "combinan técnicas",
                            "bifurcaciones": [
                                [
                                    (None, "Híbrido"), ("Neuro-simbólico", "une"), ("Redes neuronales", "con"), ("Lógica formal", "lo mejor"), ("De dos mundos", None)
                                ],
                                [
                                    (None, "Híbrido"), ("Lógica difusa", "maneja"), ("Información", "imprecisa"), ("Permite control", "gradual"), ("Sistemas de control", None)
                                ]
                            ]
                        }
                    ]
                ],
            },
            {
                "titulo": "2.3 Mapas Conceptuales",
                "conector": "Herramienta visual",
                "ramas": [
                    [
                        (None, "Estructura Gráfica"), ("Es un", "diagrama de nodos"), ("Y enlaces", "dirigidos"), ("Los nodos", "o círculos"), ("Contienen", "conceptos clave"), ("Generalmente", "sustantivos"), ("Los enlaces", "o flechas"), ("Muestran la", "relación"), ("Etiquetados con", "palabras enlace"), ("Como verbos", "o preposiciones"), ("Nodo-Enlace-Nodo", "forma una"), ("Proposición", "con significado"), ("Se organiza", "jerárquicamente"), ("Lo más general", "arriba"), ("Y lo específico", "abajo"), ("Permite", "enlaces cruzados"), ("Entre diferentes", "segmentos"), ("Fomenta el", "aprendizaje"), ("Significativo", "al conectar"), ("Ideas nuevas", "con previas"), ("Conocimiento previo", None)
                    ],
                    [
                        (None, "Uso en IA"), ("Es una", "herramienta"), ("De ingeniería", "del conocimiento"), ("Para modelar", "dominios"), ("De forma", "estructurada"), ("Facilita la", "adquisición"), ("De conocimiento", "tácito"), ("Que un experto", "posee"), ("Pero no puede", "articular"), ("El mapa sirve", "como puente"), ("Entre el experto", "y el ingeniero"), ("Ayuda a", "identificar"), ("Conceptos y", "relaciones"), ("Fundamentales", "del dominio"), ("Base para", "construir"), ("Ontologías", "formales"), ("Y bases de", "conocimiento"), ("Para alimentar", "sistemas"), ("Expertos y", "agentes"), ("Inteligentes", "que razonan"), ("Sobre el dominio", None)
                    ],
                    [
                        (None, "Proceso de Creación"), ("Inicia con", "una pregunta"), ("De enfoque", "clara"), ("Que define", "el contexto"), ("Y el", "problema"), ("Luego se hace", "una lluvia"), ("De ideas", "(brainstorming)"), ("Para listar", "conceptos"), ("Clave", "relevantes"), ("Se ordenan", "los conceptos"), ("De forma", "jerárquica"), ("Desde lo", "más general"), ("A lo más", "específico"), ("Se construye", "un mapa"), ("Preliminar", "conectando"), ("Conceptos con", "enlaces"), ("Finalmente se", "revisa"), ("Y refina", "el mapa"), ("Buscando enlaces", "cruzados"), ("Y mejorando", "proposiciones"), ("Mapa final", None)
                    ]
                ],
            },
            {
                "titulo": "2.4 Redes Semánticas",
                "conector": "Grafo de conocimiento",
                "ramas": [
                    [
                        (None, "Componentes"), ("Nodos", "son"), ("Objetos o conceptos", "y"), ("Arcos", "son"), ("Relaciones binarias", "etiquetadas"), ("Dirigidas", "forman"), ("Malla asociativa", "similar"), ("Memoria humana", None),
                        {
                            "texto": "Tipos Relación",
                            "conector": "enlaces comunes",
                            "bifurcaciones": [
                                [
                                    (None, "Relación ES-UN"), ("Conocida como", "IS-A"), ("Establece una", "jerarquía"), ("De tipo", "clase-subclase"), ("Por ejemplo", "un perro"), ("ES-UN", "mamífero"), ("La subclase", "hereda"), ("Propiedades de", "la superclase"), ("Permite la", "inferencia"), ("Y la", "generalización"), ("Fundamental para", "crear"), ("Taxonomías", None)
                                ],
                                [
                                    (None, "Relación INSTANCIA-DE"), ("Conocida como", "INSTANCE-OF"), ("Conecta un", "individuo"), ("Con su", "clase"), ("Por ejemplo", "Fido"), ("ES-INSTANCIA-DE", "la clase Perro"), ("Representa la", "pertenencia"), ("A un", "conjunto"), ("El individuo", "es un"), ("Ejemplar concreto", "de un concepto"), ("Diferente de", "IS-A que es"), ("Entre clases", None)
                                ],
                                [
                                    (None, "Relación TIENE-UN"), ("Conocida como", "HAS-A"), ("Describe una", "propiedad"), ("O una", "composición"), ("Es una", "relación parte-todo"), ("Por ejemplo", "un perro"), ("TIENE-UNA", "cola"), ("O describe", "un atributo"), ("Como", "un perro"), ("TIENE-UN", "color"), ("Es clave para", "definir"), ("Las características", None)
                                ]
                            ]
                        }
                    ],
                    [
                        (None, "Inferencia en Redes"), ("Es el proceso", "de derivar"), ("Nuevos hechos", "de los ya"), ("Representados", "en la red"), ("El mecanismo", "principal"), ("Es la", "herencia"), ("De propiedades", "a través"), ("De los enlaces", "IS-A"), ("Un nodo hereda", "los rasgos"), ("De sus", "superclases"), ("Esto permite", "economía"), ("Cognitiva y de", "almacenamiento"), ("También maneja", "excepciones"), ("Donde info", "más específica"), ("Invalida la", "heredada"), ("Ejemplo", "un avestruz"), ("Es un", "ave"), ("Hereda 'tiene alas'", "pero"), ("Sobreescribe", "el rasgo"), ("De 'puede volar'", "con 'no vuela'"), ("Razonamiento por defecto", None)
                    ],
                    [
                        (None, "Ventajas y Contras"), ("Como ventaja", "son"), ("Muy intuitivas", "y fáciles"), ("De entender", "visualmente"), ("La estructura", "es flexible"), ("Y permite", "múltiples"), ("Tipos de", "relaciones"), ("La herencia", "simplifica"), ("El almacenamiento", "de datos"), ("Como desventaja", "carecen"), ("De una", "semántica"), ("Formal y", "estándar"), ("El significado", "depende"), ("De la", "interpretación"), ("Del programa", "que la usa"), ("Esto lleva a", "ambigüedad"), ("La inferencia", "es limitada"), ("Computacionalmente", "puede"), ("Ser muy", "costosa"), ("En redes", "muy grandes"), ("Problema de escalabilidad", None)
                    ],
                    [
                        (None, "Aplicaciones Clave"), ("Fueron pioneras", "en el"), ("Procesamiento de", "Lenguaje Natural"), ("Para representar", "el significado"), ("De palabras", "y frases"), ("Un ejemplo", "es WordNet"), ("Una gran base", "de datos léxica"), ("Del idioma", "inglés"), ("También se", "usan en"), ("Sistemas de", "recuperación"), ("De información", "para mejorar"), ("La precisión", "de búsquedas"), ("Y en sistemas", "de tutoría"), ("Inteligente", "para modelar"), ("El conocimiento", "del estudiante"), ("Son la base", "conceptual"), ("De los modernos", "grafos"), ("De conocimiento", "(Knowledge Graphs)"), ("Usados por", "Google"), ("Y otras", "grandes techs"), ("Web Semántica", None)
                    ]
                ],
            },
            {
                "titulo": "2.5 Razonamiento Monótono",
                "conector": "Lógica clásica",
                "ramas": [
                    [
                        (None, "Definición"), ("Es un", "razonamiento"), ("Que sigue", "la propiedad"), ("De la", "monotonicidad"), ("El conjunto", "de conclusiones"), ("Solo puede", "aumentar"), ("Nunca disminuir", "o cambiar"), ("Al agregar", "nueva información"), ("Si una", "conclusión es"), ("Válida", "lo será"), ("Para siempre", "sin importar"), ("Qué nuevos", "hechos"), ("Se añadan", "a la base"), ("De conocimiento", "es decir"), ("Las viejas", "verdades"), ("Nunca se", "retractan"), ("Es el pilar", "de la lógica"), ("Clásica y", "las matemáticas"), ("Donde el conocimiento", "es acumulativo"), ("Y no hay", "incertidumbre"), ("Acumulación de verdad", None)
                    ],
                    [
                        (None, "Características"), ("Se basa en", "sistemas"), ("Lógicos formales", "que tienen"), ("Propiedades", "deseables"), ("Como la", "solidez"), ("(Soundness)", "toda conclusión"), ("Derivada", "es verdadera"), ("Y la", "completitud"), ("(Completness)", "toda verdad"), ("Puede ser", "demostrada"), ("Utiliza", "lógica"), ("Proposicional", "para hechos"), ("Simples", "y conectivas"), ("Y lógica de", "predicados"), ("De primer orden", "para"), ("Hablar de", "objetos"), ("Y sus", "relaciones"), ("El razonamiento", "es decidible"), ("En muchos casos", "útiles"), ("Aunque limitado", "para el"), ("Mundo real", None)
                    ],
                    [
                        (None, "Reglas Inferencia"), ("Son patrones", "de inferencia"), ("Lógica", "garantizados"), ("Para preservar", "la verdad"), ("Son la base", "de la deducción"), ("En sistemas", "formales"), ("Dos ejemplos", "clásicos son"),
                        {
                            "texto": "Ejemplos",
                            "conector": "como",
                            "bifurcaciones": [
                                [
                                    (None, "Modus Ponens"), ("Modo que", "afirma"), ("Se basa", "en una regla"), ("Si P implica Q", "es verdad"), ("Y se sabe", "que P"), ("También es", "verdad"), ("Se concluye", "que Q"), ("Es verdad", "necesariamente"), ("Ejemplo:", "Si es humano"), ("Es mortal", "(P -> Q)"), ("Sócrates es", "humano (P)"), ("Por lo tanto", "Sócrates"), ("Es mortal (Q)", None)
                                ],
                                [
                                    (None, "Modus Tollens"), ("Modo que", "niega"), ("Se basa", "en una regla"), ("Si P implica Q", "es verdad"), ("Y se sabe", "que no-Q"), ("Es decir Q", "es falso"), ("Se concluye", "que no-P"), ("Es decir P", "es falso"), ("Ejemplo:", "Si es humano"), ("Es mortal", "(P -> Q)"), ("Zeus no es", "mortal (no-Q)"), ("Por lo tanto", "Zeus"), ("No es humano (no-P)", None)
                                ]
                            ]
                        }
                    ]
                ],
            },
            {
                "titulo": "2.7 Conocimiento No-Monótono",
                "conector": "Lógica flexible",
                "ramas": [
                    [
                        (None, "Definición"), ("Retractable", "nuevos"), ("Hechos", "pueden"), ("Invalidar", "conclusiones"), ("Anteriores", "maneja"), ("Información incompleta", "o"), ("Cambiante", "simula"), ("Sentido común", "humano"),
                        {
                            "texto": "Ejemplo Clásico",
                            "conector": "caso del pájaro",
                            "bifurcaciones": [
                                [
                                    (None, "Escenario Inicial"), ("Tengo una", "base de"), ("Conocimiento", "con una"), ("Regla por", "defecto"), ("Que dice", "que los"), ("Pájaros", "normalmente vuelan"), ("Aparece un", "nuevo hecho"), ("Hecho 1:", "Tweety es"), ("Un pájaro", "aplico la"), ("Regla general", "y concluyo"), ("Provisionalmente", "que Tweety"), ("Puede volar", None)
                                ],
                                [
                                    (None, "Llega Nueva Evidencia"), ("Aparece un", "segundo hecho"), ("Más específico", "que el"), ("Anterior", "Hecho 2:"), ("Tweety es", "un pingüino"), ("Mi conocimiento", "contiene"), ("La regla de", "que los"), ("Pingüinos", "no vuelan"), ("Esta regla", "es una"), ("Excepción", "a la general"), ("Retracto mi", "conclusión"), ("Anterior", None)
                                ]
                            ]
                        }
                    ],
                    [
                        (None, "Formalismos"), ("Son sistemas", "lógicos"), ("Diseñados para", "capturar"), ("El razonamiento", "de sentido"), ("Común", "algunos"), ("De los más", "importantes son"),
                        {
                            "texto": "Tipos",
                            "conector": "tales como",
                            "bifurcaciones": [
                                [
                                    (None, "Lógica por Defecto"), ("Propuesta por", "Raymond Reiter"), ("Aumenta la", "lógica clásica"), ("Con reglas", "de inferencia"), ("Llamadas", "reglas por defecto"), ("Tienen una", "estructura"), ("De Prerrequisito", "Justificación"), ("Y Consecuente", "Si A es verdad"), ("Y es consistente", "asumir B"), ("Entonces se", "concluye C"), ("Permite formalizar", "el 'a menos que'"), ("Maneja múltiples", "extensiones"), ("Posibles del", "conocimiento"), ("Base del", "razonamiento"), ("plausible", None)
                                ],
                                [
                                    (None, "Circunscripción"), ("Propuesta por", "John McCarthy"), ("Es un", "formalismo"), ("De la", "lógica de"), ("Segundo orden", "que formaliza"), ("El principio", "de asumir"), ("Solo lo", "mínimo"), ("Se asume que", "los objetos"), ("Que satisfacen", "un predicado"), ("Son los", "únicos que lo hacen"), ("Minimiza la", "extensión"), ("De predicados", "de 'anormalidad'"), ("Es una forma", "de suposición"), ("De mundo cerrado", None)
                                ],
                                [
                                    (None, "Lógica Autoepistémica"), ("Propuesta por", "Robert C. Moore"), ("Modela las", "creencias"), ("De un agente", "que razona"), ("Sobre sus", "propias creencias"), ("Introduce un", "operador modal"), ("Llamado 'K' o 'L'", "que significa"), ("'se conoce que...'", "o 'se cree que...'"), ("Un agente", "puede concluir"), ("Algo si", "NO conoce"), ("Lo contrario", "por ejemplo"), ("Si no supiera", "que tengo un hermano"), ("Concluiría que", "soy hijo único"), ("Base de la introspección", None)
                                ]
                            ]
                        }
                    ]
                ],
            },
            {
                "titulo": "2.8 Razonamiento Probabilístico",
                "conector": "Manejo incertidumbre",
                "ramas": [
                    [
                        (None, "Causas de Incertidumbre"), ("El mundo real", "es incierto"), ("Por varias", "razones"), ("Primero", "la pereza"), ("Es mucho trabajo", "listar todas"), ("Las reglas", "y antecedentes"), ("Segundo", "la ignorancia"), ("Teórica", "no conocemos"), ("Todas las", "leyes del universo"), ("Tercero", "la ignorancia"), ("Práctica", "aunque sepamos"), ("Las reglas", "no tenemos"), ("Todos los datos", "necesarios"), ("Los sensores", "son limitados"), ("Tienen ruido", "y se dañan"), ("Los datos pueden", "ser erróneos"), ("O estar", "incompletos"), ("Por esto", "la lógica"), ("Clásica no es", "suficiente"), ("Se necesitan", "grados de creencia"), ("En lugar de", "certeza"), (" absoluta",None)
                    ],
                    [
                        (None, "Teoría de Probabilidad"), ("Es el lenguaje", "de la incertidumbre"), ("Usa variables", "aleatorias"), ("Que representan", "eventos"), ("Con un dominio", "de valores"), ("Cada valor", "tiene una"), ("Probabilidad", "asignada"), ("Que va de", "0 (imposible)"), ("A 1 (seguro)", "la suma"), ("Debe ser 1", "sobre todos"), ("Los resultados", "posibles"), ("La probabilidad", "a priori"), ("Refleja creencia", "inicial"), ("Y la condicional", "P(A|B)"), ("Actualiza creencia", "con nueva"), ("Evidencia", "la distribución"), ("De probabilidad", "conjunta"), ("Especifica la", "probabilidad"), ("De cada", "evento atómico"), ("Es el modelo", "completo del"), ("Mundo", None)
                    ]
                ],
            },
            {
                "titulo": "2.9 Teorema de Bayes",
                "conector": "Inferencia estadística",
                "ramas": [
                    [
                        (None, "Fórmula base"), ("P(A|B)", "probabilidad"), ("Posterior", "dado"), ("Evidencia B", "es"), ("Igual a", "P(B|A)"), ("Likelihood", "por"), ("P(A)", "Prior"), ("Sobre", "P(B)"), ("Evidencia total", "permite"), ("Actualizar creencia", "tras"), ("Observar datos", "nuevos"),
                        {
                            "texto": "Aplicaciones",
                            "conector": "se usa en",
                            "bifurcaciones": [
                                [
                                    (None, "Diagnóstico Médico"), ("Calcula la", "probabilidad"), ("De una", "enfermedad"), ("Dados ciertos", "síntomas"), ("P(Enfermedad|Síntoma)", "se infiere"), ("A partir de", "la evidencia"), ("Y el conocimiento", "médico previo"), ("Apoyo a decisiones", None)
                                ],
                                [
                                    (None, "Filtros de Spam"), ("Clasifica un", "correo"), ("Como spam", "o no-spam"), ("Basado en", "las palabras"), ("Que contiene", "la probabilidad"), ("De ser spam", "se actualiza"), ("Con cada", "palabra 'sospechosa'"), ("Clasificación Bayesiana", None)
                                ],
                                [
                                    (None, "Redes Bayesianas"), ("Son modelos", "gráficos"), ("Que representan", "un conjunto"), ("De variables", "aleatorias"), ("Y sus", "dependencias"), ("Condicionales", "mediante un"), ("Grafo dirigido", "acíclico"), ("Inferencia eficiente", None)
                                ]
                            ]
                        }
                    ],
                    [
                        (None, "Componentes del Teorema"), ("El teorema", "relaciona"), ("Cuatro", "cantidades"), ("Probabilísticas", "que son"),
                        {
                            "texto": "Componentes",
                            "conector": "...",
                            "bifurcaciones": [
                                [
                                    (None, "a Priori P(H)"), ("Representa el", "conocimiento"), ("O creencia", "que tenemos"), ("Sobre una", "hipótesis H"), ("Antes de", "considerar"), ("La evidencia", "actual"), ("Es el punto", "de partida"), ("Del razonamiento", "bayesiano"), ("Puede basarse", "en datos"), ("Históricos o", "estudios previos"), ("O ser una", "estimación"), ("Subjetiva de", "un experto"), ("Si no hay", "información"), ("Se puede", "usar un"), ("Prior no", "informativo"), ("Como una ", "distribución"),("uniforme",None)
                                ],
                                [
                                    (None, "Verosimilitud P(E|H)"), ("También llamada", "Likelihood"), ("Cuantifica qué", "tan bien"), ("La hipótesis H", "explica"), ("La evidencia E", "observada"), ("No es una", "probabilidad"), ("Sobre H", "sino sobre E"), ("Responde a", "la pregunta:"), ("Si mi hipótesis", "es cierta"), ("Qué tan probable", "era"), ("Ver estos", "datos?"), ("Es el componente", "que conecta"), ("El modelo", "del mundo (H)"), ("Con los datos", "observados (E)"), ("Es el motor", "de la"), ("Actualización bayesiana", None)
                                ],
                                [
                                    (None, "a Posteriori P(H|E)"), ("Es el", "resultado final"), ("Del teorema", "de Bayes"), ("Y lo que", "normalmente"), ("Queremos", "calcular"), ("Representa nuestra", "creencia"), ("Revisada sobre", "la hipótesis H"), ("Una vez que", "hemos tenido"), ("En cuenta", "la evidencia E"), ("Es la combinación", "ponderada"), ("De nuestra", "creencia a priori"), ("Con la", "verosimilitud"), ("De los datos", "el posterior"), ("De hoy puede", "ser el prior"), ("De mañana", "en un proceso"), ("De aprendizaje continuo", None)
                                ],
                                [
                                    (None, "Evidencia P(E)"), ("También llamada", "probabilidad"), ("Marginal de", "la evidencia"), ("Es la", "probabilidad total"), ("De observar", "los datos E"), ("Independientemente", "de cualquier"), ("Hipótesis", "se calcula"), ("Sumando (o integrando)", "sobre"), ("Todas las", "hipótesis posibles"), ("El producto de", "P(E|H) * P(H)"), ("Su función", "principal"), ("Es la de ser", "una constante"), ("De normalización", "que asegura"), ("Que el posterior", "sume 1"), ("A menudo es", "la parte más"), ("Difícil de calcular", None)
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
    "OUTPUT_FILE": os.path.join("Mapas", "Mapa_conceptual_U2_IA_OSCAR.drawio"),
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
