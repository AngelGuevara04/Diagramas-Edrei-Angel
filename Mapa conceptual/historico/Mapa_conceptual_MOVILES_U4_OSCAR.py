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
        "titulo_principal": "Unidad 4. Persistencia",
        "subtitulos": [
            {
                "titulo": "4.1. Ficheros",
                "conector": "Persistencia local",
                "ramas": [
                    [
                        (None, "Almacenamiento fisico"), ("De datos", "en"), ("Discos magneticos", "o"), ("Estado solido", "usa"), ("Sistema de archivos", "para"), ("Organizar bytes", "mediante"), ("Rutas (Paths)", "y"), ("Nombres unicos", "requiere"), ("Gestion de flujos", "streams"), ("De entrada", "y"), ("Salida", "para"), ("Leer o escribir", "informacion"),
                        {
                            "texto": "Operaciones",
                            "conector": "implica ciclo de",
                            "bifurcaciones": [
                                [
                                    (None, "fase"), ("Apertura", "solicita"), ("Recurso al SO", "y"), ("Verifica permisos", "de"), ("Lectura/Escritura", None)
                                ],
                                [
                                    (None, "fase"), ("Procesamiento", "realiza"), ("Lectura secuencial", "byte"), ("A byte", "o"), ("Acceso aleatorio", "con"), ("Punteros (Seek)", None)
                                ],
                                [
                                    (None, "fase"), ("Cierre", "libera"), ("Memoria buffer", "y"), ("Desbloquea archivo", "para"), ("Otros procesos", None)
                                ]
                            ]
                        }
                    ],
                    [
                        (None, "Tipos de"), ("Ficheros", "se clasifican en"),
                        {
                            "texto": "Tipos Ficheros",
                            "conector": "se clasifican en",
                            "bifurcaciones": [
                                [
                                    (None, "formato"), ("Texto plano", "almacena"), ("Secuencias de caracteres", "codificados"), ("Como ASCII", "o"), ("Unicode (UTF-8)", "son"), ("Legibles directamente", "por"), ("Seres humanos", "sin"), ("Software especial", "su"), ("Estructura es", "secuencial"), ("Y simple", "delimitadores"), ("Como saltos", "de"), ("Linea (\\n)", "organizan"), ("El contenido", "ejemplos"), ("Codigo fuente", ".txt"), (".csv, .json", None)
                                ],
                                [
                                    (None, "formato"), ("Binarios", "almacenan"), ("Datos en bytes", "sin"), ("Interpretacion de texto", "requieren"), ("Software especifico", "para"), ("Ser leidos", "correctamente"), ("Su estructura", "es"), ("Definida por", "un"), ("Encabezado (header)", "que"), ("Describe el contenido", "son"), ("Muy eficientes", "en"), ("Espacio y velocidad", "ejemplos"), ("Ejecutables, imagenes", ".zip"), (".mp3, .png", None)
                                ]
                            ]
                        }
                    ],
                    [
                        (None, "Metadatos"), (" describen ficheros", "como"), ("Fecha creacion", "y"), ("Fecha modificacion", "registran"), ("Cambios temporales", "tambien"), ("Permisos acceso", "controlan"), ("Lectura/Escritura", "para"), ("Usuarios/Grupos", "ademas"), ("Tamaño archivo", "indica"), ("Espacio ocupado", "y"), ("Tipo MIME", "identifica"), ("Contenido real", "ej"), ("image/jpeg", "o"), ("text/plain", "util"), ("Para SO", "y"), ("Aplicaciones", None)
                    ],
                    [
                        (None, "Journaling"), (" tecnica fs", "para"), ("Evitar corrupcion", "ante"), ("Fallas hardware", "mantiene"), ("Un log", "de"), ("Operaciones pendientes", "antes"), ("De escribirlas", "a"), ("Disco principal", "si"), ("Hay un fallo", "el"), ("Sistema reinicia", "y"), ("Revisa el log", "para"), ("Completar/deshacer", "transacciones"), ("Incompletas", "garantiza"), ("Estado consistente", "del"), ("Sistema de archivos", None)
                    ],
                    [
                        (None, "VFS"), (" capa abstraccion", "del"), ("Kernel del SO", "provee"), ("Interfaz unica", "para"), ("Multiples tipos", "de"), ("Sistemas de archivos", "sean"), ("Locales (ext4)", "o"), ("Red (NFS)", "asi"), ("Aplicaciones usan", "llamadas estandar"), ("open, read, write", "sin"), ("Conocer detalles", "de"), ("Implementacion fisica", "permite"), ("Montar dispositivos", "de"), ("Forma transparente", "unifica"), ("Todo bajo", "un"), ("Arbol de directorios", None)
                    ]
                ],
            },
            {
                "titulo": "4.2. REST",
                "conector": "Arquitectura Web",
                "ramas": [
                    [
                        (None, "Estilo arquitectónico"), ("Para sistemas", "distribuidos"), ("Usa HTTP", "como"), ("Protocolo transporte", "es"), ("Stateless", "sin"), ("Memoria sesión", "en"), ("El servidor", "cada"), ("Petición contiene", "toda"), ("La información", "necesaria"), ("Recursos", "son"), ("Nombres sustantivos", "identificados"), ("Por URIs", "únicas"),
                        {
                            "texto": "Métodos HTTP",
                            "conector": "mapean a CRUD",
                            "bifurcaciones": [
                                [
                                    (None, "verbo"), ("GET", "para"), ("Leer recursos", "es"), ("Idempotente", "y"), ("Cacheable", None)
                                ],
                                [
                                    (None, "verbo"), ("POST", "para"), ("Crear nuevos", "no"), ("Es idempotente", None)
                                ],
                                [
                                    (None, "verbo"), ("PUT", "para"), ("Actualizar todo", "el"), ("Recurso", None)
                                ],
                                [
                                    (None, "verbo"), ("DELETE", "para"), ("Borrar recurso", "del"), ("Servidor", None)
                                ]
                            ]
                        }
                    ],
                    [
                        (None, "Codigos Estado"), (" indican resultado", "de"), ("Peticion HTTP", "se"), ("Agrupan en clases", "1xx"), ("Informativo", "2xx"), ("Exito", "ej"), ("200 OK", "o"), ("201 Created", "3xx"), ("Redireccion", "4xx"), ("Error Cliente", "ej"), ("404 No Encontrado", "o"), ("401 No Autorizado", "5xx"), ("Error Servidor", "ej"), ("500 Internal Error", "esencial para"), ("Manejo de errores", "en"), ("cliente",None)
                    ],
                    [
                        (None, "HATEOAS"), (" Hypermedia como", "motor"), ("Estado de aplicacion", "principio"), ("Clave de REST", "respuesta"), ("Incluye enlaces", "a"), ("Acciones posibles", "cliente"), ("Navega la API", "dinamicamente"), ("Sin conocimiento", "previo"), ("De las URIs", "desacopla"), ("Cliente del servidor", "aumenta"), ("Flexibilidad", "y"), ("Evolucion de API", "sin"), ("Romper ", "clientes"), ("existentes",None)
                    ],
                    [
                        (None, "Versionado API"), (" gestiona cambios", "que"), ("Rompen compatibilidad", "estrategias"), ("Comunes incluyen", "version"), ("En la URI", "ej"), ("/v1/recurso", "o"), ("En cabecera", "HTTP"), ("Accept Header", "o"), ("Query Param", "ej"), ("?version=1", "permite"), ("Clientes antiguos", "seguir"), ("Funcionando", "mientras"), ("Nuevos clientes", "usan"), ("Funcionalidad", "más" ), ("reciente",None)
                    ],
                    {
                        "titulo": "4.2.1. JSON",
                        "conector": "Formato intercambio",
                        "ramas": [
                            [
                                (None, "JavaScript Object"), ("Notation", "es"), ("Texto ligero", "basado"), ("En pares", "de"), ("Clave : Valor", "es"), ("Independiente", "del"), ("Lenguaje", "fácil"), ("De parsear", "por"), ("Máquinas", "y"), ("Humanos", "reemplaza"), ("A XML", "en"), ("APIs modernas", "soporta"), ("Anidamiento", "de"), ("Estructuras", None),
                                {
                                    "texto": "Tipos Datos",
                                    "conector": "soporta nativos",
                                    "bifurcaciones": [
                                        [
                                            (None, "tipo"), ("Cadenas", "entre"), ("Comillas dobles", None)
                                        ],
                                        [
                                            (None, "tipo"), ("Números", "enteros"), ("O flotantes", None)
                                        ],
                                        [
                                            (None, "tipo"), ("Booleanos", "true"), ("O false", None)
                                        ],
                                        [
                                            (None, "tipo"), ("Arreglos", "listas"), ("Ordenadas []", None)
                                        ],
                                        [
                                            (None, "tipo"), ("Objetos", "colección"), ("Desordenada {}", None)
                                        ]
                                    ]
                                }
                            ],
                            [
                                (None, "JSON Schema"), ("es", "un vocabulario"), ("que valida", "la estructura"), ("de documentos", "JSON"), ("define tipos", "y formatos"), ("establece reglas", "de validacion"), ("como longitud", "minima"), ("o patrones", "regex"), ("es crucial", "para garantizar"), ("la calidad", "e integridad"), ("de los datos", "en una API"), (None, None)
                            ],
                            [
                                (None, "JSON vs XML"), ("ambos son", "formatos de texto"), ("pero JSON", "es mas ligero"), ("no usa", "etiquetas de cierre"), ("lo que", "reduce el tamaño"), ("es mas", "facil de leer"), ("y se mapea", "directo a objetos"), ("en lenguajes", "de programacion"), ("haciendolo", "mas rapido"), ("de procesar", None)
                            ],
                            [
                                (None, "JWT"), ("es un", "estandar abierto"), ("para crear", "tokens de acceso"), ("basados en", "JSON"), ("se usan", "para transmitir"), ("informacion", "de forma segura"), ("un JWT", "consta de"), ("tres partes", "header,"), ("payload", "y firma"), ("garantiza autenticidad", "e integridad"), ("del contenido", "del token"), (None, None)
                            ]
                        ]
                    }
                ],
            },
            {
                "titulo": "4.3. Servicios Nube",
                "conector": "Infraestructura IT",
                "ramas": [
                    [
                        (None, "Modelo servicio"), ("Bajo demanda", "a"), ("Través de internet", "ofrece"), ("Elasticidad", "crece"), ("O decrece", "según"), ("Carga", "modelo"), ("Pago por uso", "OPEX"), ("Sin inversión", "inicial"), ("CAPEX", "proveedores"), ("AWS, Azure, GCP", "gestionan"), ("Datacenters", "físicos"),
                        {
                            "texto": "Categorías",
                            "conector": "niveles gestión",
                            "bifurcaciones": [
                                [
                                    (None, "nivel"), ("IaaS", "infraestructura"), ("Como servicio", "ejemplo"), ("EC2, VMs", None)
                                ],
                                [
                                    (None, "nivel"), ("PaaS", "plataforma"), ("Como servicio", "ejemplo"), ("App Engine", None)
                                ],
                                [
                                    (None, "nivel"), ("SaaS", "software"), ("Como servicio", "ejemplo"), ("Gmail, Drive", None)
                                ]
                            ]
                        }
                    ],
                    [
                        (None, "Nube Pública"),
                        ("es un", "Modelo de despliegue"),
                        ("donde", "Recursos como servidores"),
                        ("y", "Almacenamiento son"),
                        ("propiedad", "De un proveedor"),
                        ("externo", "Que los ofrece"),
                        ("al", "Público general"),
                        ("vía", "Internet"),
                        ("se", "Accede bajo"),
                        ("demanda", "Pagando solo"),
                        ("por", "El uso real"),
                        ("es", "Altamente escalable"),
                        ("y", "Elástica"),
                        ("sin", "Inversión inicial"),
                        ("fuerte", "Ejemplos son"),
                        ("AWS", "Azure y GCP")
                    ],
                    [
                        (None, "Nube Privada"),
                        ("infraestructura", "dedicada a"),
                        ("Una sola", "organización"),
                        ("no", "Comparte recursos"),
                        ("físicos", "Con otros"),
                        ("clientes", "Puede estar"),
                        ("alojada", "En el datacenter"),
                        ("propio", "(on-premise)"),
                        ("o", "Gestionada por"),
                        ("terceros", "Ofrece control"),
                        ("y", "Seguridad máximos"),
                        ("sobre", "Datos y apps"),
                        ("ideal", "Para industrias"),
                        ("reguladas", "Pero requiere"),
                        ("mayor", "Inversión y"),
                        ("mantenimiento", "Constante")
                    ],
                    [
                        (None, "Nube Híbrida"),
                        ("combina", "una"),
                        ("Nube privada", "con"),
                        ("Una o más", "nubes"),
                        ("Públicas", "permite"),
                        ("La portabilidad", "de"),
                        ("Datos y apps", "entre"),
                        ("Ambos entornos", "se"),
                        ("Usa para", "extender"),
                        ("Capacidad", "(bursting)"),
                        ("o", "Mantener datos"),
                        ("críticos", "On-premise"),
                        ("mientras", "Se aprovecha"),
                        ("la", "Escalabilidad pública"),
                        ("otorga", "Flexibilidad"),
                        ("pero", "Aumenta la"),
                        ("complejidad", "De gestión")
                    ],
                    {
                        "titulo": "4.3.1. Almacenamiento",
                        "conector": "Persistencia Cloud",
                        "ramas": [
                            [
                                (None, "Gestión remota"), ("De datos", "con"), ("Alta disponibilidad", "y"), ("Durabilidad", "masiva"),
                                {
                                    "texto": "Tipos Storage",
                                    "conector": "se divide en",
                                    "bifurcaciones": [
                                        [
                                            (None, "tipo"), ("Objetos (S3)", "para"), ("No estructurados", "como"), ("Fotos/Videos", "acceso"), ("Por API HTTP", None)
                                        ],
                                        [
                                            (None, "tipo"), ("Bloques (EBS)", "para"), ("Discos virtuales", "de"), ("Sistemas operativos", "baja"), ("Latencia", None)
                                        ],
                                        [
                                            (None, "tipo"), ("Archivos (EFS)", "para"), ("Directorios compartidos", "tipo"), ("NFS en red", None)
                                        ]
                                    ]
                                }
                            ],
                            [
                                (None, "Cold Storage"),
                                ("almacenamiento de", "Bajo costo"),
                                ("para", "Datos de archivo"),
                                ("que", "Se acceden"),
                                ("infrecuentemente", "Ideal para"),
                                ("backups", "Y retención"),
                                ("a", "Largo plazo"),
                                ("tiene", "Tiempos de recuperación"),
                                ("más", "Lentos (horas)"),
                                ("a", "Cambio de"),
                                ("un", "Costo muy bajo"),
                                ("ejemplo", "Amazon S3 Glacier")
                            ],
                            [
                                (None, "CDN"),
                                ("red de entrega", "De contenidos"),
                                ("distribuye", "Copias del contenido"),
                                ("en", "Servidores caché"),
                                ("globales", "(Edge Locations)"),
                                ("reduce", "La latencia"),
                                ("para", "Usuarios finales"),
                                ("al", "Servir contenido"),
                                ("desde", "La ubicación"),
                                ("más", "Cercana"),
                                ("mejora", "Rendimiento y"),
                                ("disponibilidad", "De sitios web")
                            ],
                            [
                                (None, "DBaaS"),
                                ("bases de datos", "Gestionadas por"),
                                ("el", "Proveedor de nube"),
                                ("automatiza", "Tareas como"),
                                ("parches", "Backups y"),
                                ("escalado", "Permite a"),
                                ("desarrolladores", "Focalizarse en"),
                                ("la", "Aplicación"),
                                ("no", "En la administración"),
                                ("de", "La BD"),
                                ("soportan", "Tanto SQL"),
                                ("como", "NoSQL"),
                                ("ejemplo", "Amazon RDS")
                            ]
                        ]
                    },
                    {
                        "titulo": "4.3.2. Autenticación",
                        "conector": "Seguridad acceso",
                        "ramas": [
                            [
                                (None, "Gestión identidad"), ("IAM", "controla"), ("Quién entra", "Authentication"), ("Y qué hace", "Authorization"), ("Usa roles", "y"), ("Políticas JSON", "para"), ("Permisos finos", None),
                                {
                                    "texto": "Mecanismos",
                                    "conector": "implementa",
                                    "bifurcaciones": [
                                        [
                                            (None, "uso"), ("OAuth2 / OIDC", "para"), ("Federación identidad", "con"), ("Google/Facebook", None)
                                        ],
                                        [
                                            (None, "uso"), ("MFA", "factor"), ("Múltiple", "algo"), ("Que sabes", "más"), ("Algo que tienes", None)
                                        ],
                                        [
                                            (None, "uso"), ("Tokens JWT", "para"), ("Sesiones stateless", "en"), ("APIs REST", None)
                                        ]
                                    ]
                                }
                            ],
                            [
                                (None, "SSO"),
                                ("Single Sign-On", "permite a usuarios"),
                                ("iniciar sesión", "una sola vez"),
                                ("para acceder", "a múltiples"),
                                ("aplicaciones", "y servicios"),
                                ("Mejora la", "experiencia de usuario"),
                                ("y reduce", "la fatiga de"),
                                ("contraseñas", "El proveedor"),
                                ("de identidad", "(IdP)"),
                                ("se encarga", "de la autenticación"),
                                ("y emite", "tokens o aserciones"),
                                ("a los", "proveedores de servicio"),
                                ("(SP)", "ejemplo SAML"),
                                ("y OpenID", "Connect")
                            ],
                            [
                                (None, "Gestión Secretos"),
                                ("manejo seguro", "de credenciales"),
                                ("como", "claves de API"),
                                ("tokens y", "certificados"),
                                ("Evita hardcodear", "secretos en"),
                                ("el código", "fuente"),
                                ("Utiliza servicios", "centralizados como"),
                                ("AWS Secrets Manager", "o HashiCorp"),
                                ("Vault", "Estos servicios"),
                                ("gestionan la", "rotación automática"),
                                ("de secretos", "y auditan"),
                                ("su uso", "para"),
                                ("mejorar la", "postura de"),
                                ("seguridad", "general")
                            ],
                            [
                                (None, "Menor Privilegio"),
                                ("es un", "principio de seguridad"),
                                ("que dicta", "que cada"),
                                ("usuario o", "componente"),
                                ("debe tener", "solo los"),
                                ("permisos mínimos", "necesarios"),
                                ("para realizar", "su función"),
                                ("Reduce la", "superficie de ataque"),
                                ("en caso", "de una brecha"),
                                ("Se implementa", "mediante políticas"),
                                ("IAM detalladas", "(granulares)"),
                                ("y roles", "específicos"),
                                ("para cada", "tarea"),
                                ("evitando permisos", "demasiado amplios")
                            ]
                        ]
                    },
                    {
                        "titulo": "4.3.3. Mensajería",
                        "conector": "Comunicación Asíncrona",
                        "ramas": [
                            [
                                (None, "Desacoplamiento"), ("Entre servicios", "mejora"), ("Resiliencia", "ante"), ("Fallos temporales", None),
                                {
                                    "texto": "Patrones",
                                    "conector": "modelos flujo",
                                    "bifurcaciones": [
                                        [
                                            (None, "modelo"), ("Colas (SQS)", "Punto"), ("A punto", "un"), ("Productor", "un"), ("Consumidor", None)
                                        ],
                                        [
                                            (None, "modelo"), ("Pub/Sub (SNS)", "Publicar"), ("Suscribir", "un"), ("Productor", "muchos"), ("Consumidores", None)
                                        ],
                                        [
                                            (None, "modelo"), ("Event Bus", "bus"), ("De eventos", "para"), ("Arquitecturas reactivas", None)
                                        ]
                                    ]
                                }
                            ],
                            [
                                (None, "Dead-Letter Queue"),
                                ("es una", "cola secundaria"),
                                ("para manejar", "mensajes que"),
                                ("no pueden", "ser procesados"),
                                ("correctamente", "Tras varios"),
                                ("intentos fallidos", "el mensaje"),
                                ("se mueve", "a la DLQ"),
                                ("para su", "análisis posterior"),
                                ("Evita que", "mensajes con errores"),
                                ("bloqueen la", "cola principal"),
                                ("y permite", "depurar problemas"),
                                ("de forma", "aislada"),
                                ("sin detener", "el flujo normal")
                            ],
                            [
                                (None, "Patrón Fan-out"),
                                ("un mensaje", "publicado en"),
                                ("un topic", "de Pub/Sub"),
                                ("se envía", "a múltiples"),
                                ("colas suscritas", "en paralelo"),
                                ("Cada cola", "representa un"),
                                ("microservicio o", "componente"),
                                ("interesado en", "el evento"),
                                ("Permite el", "procesamiento paralelo"),
                                ("y desacoplado", "de un"),
                                ("mismo evento", "por diferentes"),
                                ("partes del", "sistema"),
                                ("Es fundamental", "en arquitecturas"),
                                ("dirigidas por", "eventos")
                            ],
                            [
                                (None, "Message Streaming"),
                                ("procesamiento continuo", "de flujos"),
                                ("de datos", "en tiempo real"),
                                ("A diferencia de", "las colas"),
                                ("los streams", "persisten los mensajes"),
                                ("durante más", "tiempo"),
                                ("y permiten", "que múltiples"),
                                ("consumidores lean", "el mismo"),
                                ("flujo de", "datos"),
                                ("de forma", "independiente"),
                                ("Servicios como", "Amazon Kinesis"),
                                ("o Apache Kafka", "son usados para"),
                                ("analítica en", "tiempo real")
                            ]
                        ]
                    }
                ],
            },
            {
                "titulo": "4.4. Proyectos Cloud",
                "conector": "Desarrollo moderno",
                "ramas": [
                    [
                        (None, "Enfoque nativo"), ("Cloud Native", "usa"), ("Microservicios", "pequeños"), ("Componentes aislados", "y"), ("Contenedores", "Docker"), ("Para empaquetar", "y"), ("Kubernetes", "para"), ("Orquestar", "aplica"), ("Serverless", "FaaS"), ("Código sin", "servidor"), ("Ejecuta eventos", "ahorra"), ("Costos inactivos", None),
                        {
                            "texto": "Ciclo DevOps",
                            "conector": "automatización total",
                            "bifurcaciones": [
                                [
                                    (None, "etapa"), ("CI (Integración)", "build"), ("Y test", "automático"), ("En", "cada"), ("Commit",None)
                                ],
                                [
                                    (None, "etapa"), ("CD (Entrega)", "despliegue"), ("A producción", "sin"), ("Intervención", "manual"),("Rápido",None)
                                ],
                                [
                                    (None, "etapa"), ("IaC", "infraestructura"), ("Como código", "usa"), ("Terraform/CloudFormation", "para"), ("Provisionar","los"),("Recursos",None)
                                ]
                            ]
                        }
                    ],
                    [
                        (None, "FinOps"),
                        ("práctica de", "gestión financiera"),
                        ("en la nube", "busca maximizar"),
                        ("el valor", "del negocio"),
                        ("combina", "finanzas e ingeniería"),
                        ("para optimizar", "costos"),
                        ("Implica monitoreo", "constante del gasto"),
                        ("asignación de", "costos a equipos"),
                        ("y uso", "de instancias"),
                        ("reservadas o", "Spot"),
                        ("para reducir", "la factura"),
                        ("Fomenta una", "cultura de"),
                        ("responsabilidad", "financiera")
                    ],
                    [
                        (None, "Observabilidad"),
                        ("capacidad de", "entender el"),
                        ("estado interno", "de un sistema"),
                        ("a partir", "de sus"),
                        ("datos externos", "Se basa en"),
                        ("tres pilares", "Logs (registros)"),
                        ("Métricas (mediciones)", "y Trazas (traces)"),
                        ("Permite depurar", "problemas complejos"),
                        ("en sistemas", "distribuidos"),
                        ("y entender", "el rendimiento"),
                        ("de las", "aplicaciones"),
                        ("Herramientas como", "Prometheus"),
                        ("Grafana y", "Jaeger")
                    ],
                    [
                        (None, "Multi-Cloud"),
                        ("uso de", "servicios de"),
                        ("múltiples proveedores", "de nube"),
                        ("pública", "(AWS, Azure, GCP)"),
                        ("para una", "misma aplicación"),
                        ("Busca evitar", "la dependencia"),
                        ("de un", "solo proveedor"),
                        ("(vendor lock-in)", "y aprovechar"),
                        ("las mejores", "características"),
                        ("de cada", "nube"),
                        ("Aumenta la", "resiliencia ante"),
                        ("caídas de", "un proveedor"),
                        ("pero incrementa", "la complejidad")
                    ]
                ],
            },
            {
                "titulo": "4.5. NoSQL",
                "conector": "Datos Flexibles",
                "ramas": [
                    [
                        (None, "Not Only SQL"), ("Diseño distribuido", "para"), ("Grandes volúmenes", "Big Data"), ("Alta velocidad", "baja"), ("Latencia", "esquema"), ("Dinámico", "sin"), ("Tablas fijas", "escalado"), ("Horizontal", "sharding"), ("En clúster", "teorema"), ("CAP", "elige"), ("Dos de tres", "Consistencia"), ("Disponibilidad", "Partición"),
                        {
                            "texto": "Modelos NoSQL",
                            "conector": "tipos principales",
                            "bifurcaciones": [
                                [
                                    (None, "modelo"), ("Clave-Valor", "Redis"), ("Diccionario simple", "muy"), ("Rápido", "para"), ("Caché/Sesiones", None)
                                ],
                                [
                                    (None, "modelo"), ("Documental", "MongoDB"), ("Guarda JSON", "índices"), ("Flexibles", "para"), ("CMS/Catálogos", None)
                                ],
                                [
                                    (None, "modelo"), ("Grafos", "Neo4j"), ("Nodos y Aristas", "para"), ("Relaciones complejas", "redes"), ("Sociales/Fraude", None)
                                ]
                            ]
                        }
                    ],
                    [
                        (None, "Bases Columnares"),
                        ("optimizadas para", "cargas de trabajo"),
                        ("analíticas", "(OLAP)"),
                        ("Almacenan datos", "por columnas"),
                        ("en lugar", "de por filas"),
                        ("Esto permite", "una compresión"),
                        ("muy eficiente", "y lecturas"),
                        ("rápidas de", "subconjuntos de"),
                        ("columnas", "Son ideales"),
                        ("para data", "warehousing"),
                        ("y business", "intelligence"),
                        ("Ejemplos son", "Amazon Redshift"),
                        ("y Google", "BigQuery")
                    ],
                    [
                        (None, "Series Temporales"),
                        ("especializadas en", "datos con"),
                        ("marca de tiempo", "(timestamp)"),
                        ("Optimizadas para", "alta ingesta"),
                        ("y consultas", "eficientes"),
                        ("sobre rangos", "de tiempo"),
                        ("Usadas comúnmente", "para monitoreo"),
                        ("de sistemas", "(métricas, logs)"),
                        ("datos de", "sensores (IoT)"),
                        ("y mercados", "financieros"),
                        ("Funciones integradas", "para análisis"),
                        ("temporal como", "agregaciones"),
                        ("y downsampling", "Ej: InfluxDB")
                    ],
                    [
                        (None, "Consistencia Eventual"),
                        ("modelo de", "consistencia usado"),
                        ("en sistemas", "distribuidos NoSQL"),
                        ("Garantiza que", "si no se"),
                        ("hacen nuevas", "actualizaciones"),
                        ("eventualmente todas", "las réplicas"),
                        ("convergerán al", "mismo valor"),
                        ("Prioriza la", "disponibilidad (A)"),
                        ("y tolerancia", "a particiones (P)"),
                        ("sobre la", "consistencia inmediata (C)"),
                        ("del teorema", "CAP"),
                        ("Las lecturas", "pueden devolver"),
                        ("datos obsoletos", "(stale reads)")
                    ],
                    {
                        "titulo": "4.5.1. Clave - Valor",
                        "conector": "Simplicidad extrema",
                        "ramas": [
                            [
                                (None, "Estructura map"), ("Hash distribuido", "acceso"), ("O(1)", "directo"), ("Por clave", "valor"), ("Es blob", "opaco"), ("Para la BD", "operaciones"), ("PUT, GET, DEL", "ejemplos"), ("DynamoDB", "y"), ("Memcached", None)
                            ],
                            [
                                (None, "Casos de Uso"),
                                ("son ideales", "para cachés"),
                                ("de alta", "velocidad"),
                                ("almacenamiento de", "sesiones de usuario"),
                                ("y carritos", "de compra"),
                                ("También para", "tablas de clasificación"),
                                ("(leaderboards) en", "juegos online"),
                                ("y como", "almacén de"),
                                ("preferencias de", "usuario"),
                                ("Su simplicidad", "y rendimiento"),
                                ("son clave", "en estas"),
                                ("aplicaciones", "de baja latencia")
                            ],
                            [
                                (None, "Escalabilidad"),
                                ("escalan horizontalmente", "con facilidad"),
                                ("añadiendo más", "nodos al clúster"),
                                ("La partición", "(sharding)"),
                                ("distribuye el", "conjunto de claves"),
                                ("entre los", "nodos disponibles"),
                                ("El acceso", "directo por clave"),
                                ("evita consultas", "costosas"),
                                ("logrando un", "rendimiento O(1)"),
                                ("para operaciones", "básicas"),
                                ("de lectura", "y escritura")
                            ],
                            [
                                (None, "Limitaciones"),
                                ("no ofrecen", "capacidades de consulta"),
                                ("complejas sobre", "los valores"),
                                ("ya que", "el valor es"),
                                ("un blob", "opaco para la BD"),
                                ("Cualquier filtrado", "o búsqueda"),
                                ("debe hacerse", "en la aplicación"),
                                ("No soportan", "relaciones complejas"),
                                ("entre datos", "ni transacciones"),
                                ("ACID", "tradicionales"),
                                ("Su modelo", "es simple"),
                                ("y no", "apto para"),
                                ("cualquier tipo", "de problema")
                            ]
                        ]
                    },
                    {
                        "titulo": "4.5.2. Documentos",
                        "conector": "Jerarquía datos",
                        "ramas": [
                            [
                                (None, "Almacena docs"), ("Auto-descriptivos", "formato"), ("BSON/JSON", "permite"), ("Consultas ricas", "sobre"), ("Campos internos", "sin"), ("Joins costosos", "ejemplos"), ("Firestore", "y"), ("Couchbase", None)
                            ],
                            [
                                (None, "Indexación Flexible"),
                                ("permiten crear", "índices secundarios"),
                                ("en cualquier", "campo del documento"),
                                ("incluso en", "campos anidados"),
                                ("o dentro", "de arreglos"),
                                ("Esto acelera", "enormemente las"),
                                ("consultas sin", "necesidad de"),
                                ("escanear la", "colección completa"),
                                ("Soportan índices", "geoespaciales"),
                                ("de texto", "completo (full-text)"),
                                ("y TTL", "(Time To Live)")
                            ],
                            [
                                (None, "Casos de Uso"),
                                ("son excelentes", "para sistemas"),
                                ("de gestión", "de contenido (CMS)"),
                                ("catálogos de", "productos de e-commerce"),
                                ("y perfiles", "de usuario"),
                                ("Su esquema", "flexible permite"),
                                ("evolucionar la", "aplicación fácilmente"),
                                ("almacenando documentos", "con diferentes"),
                                ("estructuras en", "la misma"),
                                ("colección", "Son muy"),
                                ("populares para", "aplicaciones web"),
                                ("y móviles", "modernas")
                            ],
                            [
                                (None, "Agregaciones"),
                                ("permiten procesar", "múltiples documentos"),
                                ("y devolver", "resultados computados"),
                                ("Se construyen", "como un pipeline"),
                                ("con múltiples", "etapas (stages)"),
                                ("Cada etapa", "transforma los"),
                                ("documentos a", "medida que pasan"),
                                ("a través", "de ella"),
                                ("Etapas comunes", "son $match"),
                                ("$group, $sort", "y $project"),
                                ("Son el", "equivalente a"),
                                ("GROUP BY", "en SQL")
                            ]
                        ]
                    },
                    {
                        "titulo": "4.5.3. Grafos",
                        "conector": "Conexiones puras",
                        "ramas": [
                            [
                                (None, "Modelo de red"), ("Entidades son", "Nodos"), ("Relaciones son", "Aristas"), ("Con propiedades", "consulta"), ("Patrones", "como"), ("'Amigo de'", "ejemplos"), ("Amazon Neptune", "y"), ("JanusGraph", None)
                            ],
                            [
                                (None, "Lenguajes Consulta"),
                                ("utilizan lenguajes", "declarativos"),
                                ("especializados en", "recorrer relaciones"),
                                ("Cypher de Neo4j", "es uno popular"),
                                ("con sintaxis", "tipo ASCII-art"),
                                ("para describir", "patrones de nodos"),
                                ("y aristas", "Otro es"),
                                ("Gremlin de", "Apache TinkerPop"),
                                ("un lenguaje", "funcional de"),
                                ("recorrido de", "grafos"),
                                ("Ambos permiten", "consultas muy"),
                                ("expresivas y", "eficientes")
                            ],
                            [
                                (None, "Casos de Uso"),
                                ("son perfectas", "para modelar"),
                                ("redes sociales", "(amigos, seguidores)"),
                                ("detección de", "fraude financiero"),
                                ("motores de", "recomendación"),
                                ("(ej: 'clientes que", "compraron X también"),
                                ("compraron Y')", "y análisis"),
                                ("de redes", "de conocimiento"),
                                ("Su fortaleza", "es encontrar"),
                                ("caminos y", "conexiones"),
                                ("indirectas entre", "nodos distantes")
                            ],
                            [
                                (None, "Tipos de Grafos"),
                                ("existen dos", "modelos principales"),
                                ("Grafo de", "Propiedades (Property Graph)"),
                                ("usado por", "Neo4j y Neptune"),
                                ("donde nodos", "y aristas"),
                                ("tienen propiedades", "en formato clave-valor"),
                                ("Y el modelo", "RDF (Resource"),
                                ("Description Framework)", "usado en"),
                                ("la web", "semántica"),
                                ("Se basa", "en tripletas"),
                                ("sujeto-predicado-objeto", "para definir"),
                                ("hechos y", "relaciones")
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
    "OUTPUT_FILE": os.path.join("Mapas", "Mapa_conceptual_MOVILES_U4_OSCAR.drawio"),
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
