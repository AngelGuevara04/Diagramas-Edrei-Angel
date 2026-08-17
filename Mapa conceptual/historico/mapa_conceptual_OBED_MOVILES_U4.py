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
        "titulo_principal": "Unidad 4. Persistencia de Datos",
        "subtitulos": [
            {
                "titulo": "4.1. Ficheros",
                "conector": "Manejo básico de",
                "ramas": [
                    [
                        (None, "Son mecanismos"), ("De persistencia", "guardan"), ("Datos en disco", "usando"), ("Rutas de archivo", "para"), ("Localizar bytes", "su acceso es"), ("Secuencial", "o"), ("Aleatorio", "dependiendo de"), ("La necesidad", "requieren"), ("Abrir stream", "y"), ("Gestión de errores", "por si"), ("Archivo no existe", "o"), ("Faltan permisos", "es vital"), ("Cerrar recursos", "para"), ("Liberar memoria", "y evitar"), ("Bloqueos de SO", "se usan en"), ("Configuraciones", "y"), ("Logs del sistema", "aunque"), ("Son más lentos", "que la"), ("Memoria RAM", "garantizan"), ("Durabilidad simple", "tras"), ("Apagar el equipo", None)
                    ],
                    [
                        (None, "Existen formatos"), ("Texto plano", "como"), ("CSV o TXT", "fáciles de"), ("Leer por humanos", "pero"), ("Ocupan espacio", "y están los"), ("Binarios", "que son"), ("Más eficientes", "requieren"), ("Serialización", "para"), ("Guardar objetos", "y"), ("Deserialización", "para"), ("Recuperar estado", "las operaciones"), ("Son lectura", "y"), ("Escritura", "o"), ("Append (agregar)", "cuidado con"), ("La concurrencia", "si hay"), ("Múltiples hilos", "necesita"), ("Bloqueo de archivo", "para"), ("Integridad de datos", "evitando"), ("Corrupción", "al escribir"), ("Simultáneamente", None)
                    ],
                ],
            },
            {
                "titulo": "4.2. REST",
                "conector": "Arquitectura web",
                "ramas": [
                    [
                        (None, "Estilo arquitectónico"), ("Para la web", "basado en"), ("Protocolo HTTP", "usa"), ("Verbos estándar", "como"), ("GET y POST", "para"), ("Leer y crear", "y"), ("PUT y DELETE", "para"), ("Actualizar y borrar", "es totalmente"), ("Stateless", "sin"), ("Sesión servidor", "cada petición"), ("Es independiente", "y contiene"), ("Todo lo necesario", "mejora la"), ("Escalabilidad", "en"), ("Sistemas distribuidos", "usa"), ("URIs únicas", "para"), ("Identificar recursos", "como"), ("Objetos de negocio", "facilita"), ("Interoperabilidad", "entre"), ("Distintas plataformas", "y lenguajes"), ("Diferentes", None)
                    ],
                    [
                        (None, "Interfaz uniforme"),("que", "desacopla"), ("Cliente y servidor", "permite"), ("Evolución separada", "soporta"), ("Caché HTTP", "para"), ("Mejorar velocidad", "y"), ("Reducir latencia", "las respuestas"), ("Tienen metadatos", "en"), ("Headers HTTP", "como"), ("Content-Type", "o"), ("Status Codes", "ejemplo"), ("200 OK", "o"), ("404 Not Found", "implementa"), ("HATEOAS", "para"), ("Navegación dinámica", "descubriendo"), ("Enlaces relacionados", "en el"), ("Cuerpo de respuesta", "haciendo la"), ("API navegable", "por máquinas"), ("Automáticamente", None)
                    ],
                    {
                        "titulo": "4.2.1. JSON",
                        "conector": "Formato estándar",
                        "ramas": [
                            [
                                (None, "Formato ligero"), ("Intercambio datos", "basado en"), ("Texto plano", "fácil de"), ("Leer y escribir", "estructura de"), ("Pares clave-valor", "donde"), ("Claves son strings", "y"), ("Valores variados", "como"), ("Números o booleanos", "o"), ("Arrays y objetos", "usa"), ("Llaves {}", "para"), ("Objetos", "y"), ("Corchetes []", "para"), ("Listas", "es"), ("Menos verboso", "que"), ("XML", "ahorra"), ("Ancho de banda", "en"), ("Redes móviles", "el parseo"), ("Es nativo", "en JavaScript"), ("Muy rápido", None)
                            ],
                            [
                                (None, "Estándar actual en" ), ("APIs REST", "y"), ("Archivos config", "es"), ("Independiente", "del lenguaje"), ("Soportado por", "Python y Java,"), ("C# y PHP", "permite"), ("Estructuras anidadas", "para"), ("Datos complejos", "como"), ("Árboles", "no soporta"), ("Comentarios", "ni"), ("Funciones", "solo"), ("Datos puros", "requiere"), ("Codificación UTF-8", "para"), ("Caracteres especiales", "ideal para"), ("AJAX", "y"), ("Single Page Apps", "modernas"), ("React o Angular", None)
                            ],
                        ],
                    }
                ],
            },
            {
                "titulo": "4.3. Servicios Nube",
                "conector": "Infraestructura como",
                "ramas": [
                     {
                        "titulo": "4.3.1. Almacenamiento",
                        "conector": "Tipos de guardado",
                        "ramas": [
                            [
                                (None, "Guarda datos en"), ("La nube", "ofrece"), ("Object Storage", "como"), ("S3 o Blob", "para"), ("Archivos planos", "imágenes"), ("Y videos", "y"), ("Block Storage", "para"), ("Discos de VM", "con alta"), ("Velocidad IOPS", "y"), ("File Storage", "tipo"), ("NFS compartido", "para"), ("Múltiples servidores", "es"), ("Elástico", "crece"), ("Automáticamente", "pagas por"), ("Uso real", "sin"), ("Pre-aprovisionar", "hardware"), ("Físico", None)
                            ],
                            [
                                (None, "Alta durabilidad con"), ("Replicación auto", "en"), ("Múltiples zonas", "previene"), ("Pérdida de datos", "ofrece"), ("Clases de acceso", "como"), ("Hot o Cold", "para"), ("Ahorrar dinero", "según"), ("Frecuencia uso", "incluye"), ("Cifrado en reposo", "para"), ("Seguridad", "y"), ("Versión de archivos", "para"), ("Deshacer cambios", "gestión de"), ("Ciclo de vida", "para"), ("Borrado automático", "o"), ("Archivado largo", "plazo"), ("Glacier", None)
                            ],
                        ],
                    },
                    {
                        "titulo": "4.3.2. Autentificación",
                        "conector": "Gestión de identidad",
                        "ramas": [
                            [
                                (None, "Controla acceso mediante"), ("Servicios IAM", "Identity Management"), ("Gestiona usuarios", "y"), ("Roles y grupos", "define"), ("Permisos finos", "quién"), ("Puede hacer qué", "sobre"), ("Qué recursos", "soporta"), ("MFA", "Multi-factor"), ("Para seguridad", "extra"), ("Evita robos", "de"), ("Cuentas", "integra"), ("Directorios activos", "para"), ("Empresas", "centralizando"), ("El login", "SSO"), ("Single Sign-On", None)
                            ],
                            [
                                (None, "Usa tokens"), ("como OAuth2", "y"), ("OIDC", "para"), ("Identidad federada", "permite"), ("Login social", "con"), ("Google o Facebook", "sin"), ("Crear cuentas", "nuevas"), ("Genera claves", "API Keys"), ("Para apps", "que"), ("Deben rotarse", "para"), ("Evitar fugas", "audita"), ("Intentos de acceso", "en"), ("Logs de seguridad", "detectando"), ("Intrusos", "o"), ("Actividad sospechosa", None)
                            ],
                        ],
                    },
                    {
                        "titulo": "4.3.3. Mensajería",
                        "conector": "Comunicación asíncrona",
                        "ramas": [
                            [
                                (None, "Desacopla apps mediante"), ("Colas (Queues)", "modelo"), ("Productor-Consumidor", "uno a uno"), ("Garantiza entrega", "procesamiento"), ("Asíncrono", "ideal para"), ("Tareas pesadas", "en background"), ("Topics (Temas)", "modelo"), ("Pub/Sub", "uno a muchos"), ("Notifica eventos", "a"), ("Múltiples apps", "como"), ("Email y Logs", "simultáneamente"), ("Sin bloquear", "al"), ("Emisor original", None)
                            ],
                            [
                                (None, "Mejora resiliencia si"), ("Consumidor falla", "el"), ("Mensaje persiste", "en"), ("La cola", "hasta"), ("Ser procesado", "amortigua"), ("Picos de tráfico", "actúa como"), ("Buffer", "evita"), ("Saturación", "del"), ("Backend", "permite"), ("Escalado libre", "de"), ("Productores", "y"), ("Consumidores", "integra"), ("Microservicios", "de forma"), ("Flexible", "y"), ("Robusta", None)
                            ],
                        ],
                    },
                ],
            },
            {
                "titulo": "4.4. Proyectos Cloud",
                "conector": "Desarrollo moderno",
                "ramas": [
                    [
                        (None, "Enfoque nativo"), ("usa Microservicios", "en vez de"), ("Monolitos", "para"), ("Escalar partes", "independientes"), ("Uso de contenedores", "como"), ("Docker", "orquestados por"), ("Kubernetes", "para"), ("Gestión automática", "adopta"), ("Cultura DevOps", "y"), ("CI/CD", "integración continua"), ("Despliegue continuo", "para"), ("Entregas rápidas", "y"), ("Frecuentes", "automatizando"), ("Pruebas unitarias", "y"), ("De integración", None)
                    ],
                    [
                        (None, "Infra como código"), ("IaC Usando Terraform", "o"), ("CloudFormation", "define"), ("Recursos en texto", "permite"), ("Versionar infra", "y"), ("Repetir entornos", "exactos"), ("Evita configuración", "manual"), ("Propensa a errores", "monitoreo con"), ("CloudWatch", "o"), ("Prometheus", "observabilidad"), ("Logs centralizados", "para"), ("Debugging", "distribuido"), ("Rastreo de errores", "en"), ("Tiempo real", None)
                    ],
                ],
            },
            {
                "titulo": "4.5. NoSQL",
                "conector": "Bases no relacionales",
                "ramas": [
                    {
                        "titulo": "4.5.1. Clave – valor",
                        "conector": "Modelo simple",
                        "ramas": [
                            [
                                (None, "Estructura básica mapa"), ("Hash distribuido", "guarda"), ("Dato binario", "contra"), ("Una llave única", "acceso"), ("Muy rápido", "O(1)"), ("Por llave", "no hay"), ("Esquema fijo", "es muy"), ("Flexible", "ideal para"), ("Caché de datos", "o"), ("Sesiones web", "y"), ("Carritos compra", "ejemplos"), ("Redis", "y"), ("DynamoDB", "ofrecen"), ("Baja latencia", "y"), ("Alto rendimiento", None)
                            ],
                            [
                                (None, "Operaciones base son"), ("Get, Put, Delete", "no tiene"), ("Queries complejos", "ni"), ("Joins SQL", "requiere"), ("Diseño previo", "de"), ("Claves de acceso", "para"), ("Recuperar datos", "su escalabilidad"), ("Es horizontal", "usando"), ("Sharding", "particiona datos"), ("Por rangos", "de claves"), ("Alta disponibilidad", "con"), ("Replicación", None)
                            ],
                        ],
                    },
                    {
                        "titulo": "4.5.2. Documentos",
                        "conector": "Datos semi-estructurados",
                        "ramas": [
                            [
                                (None, "Guarda documentos como"), ("JSON o BSON", "auto-contenidos"), ("Esquema dinámico", "cada doc"), ("Puede variar", "campos"), ("Permite anidar", "listas"), ("Y sub-objetos", "mapea"), ("Directo a objetos", "de"), ("Programación", "ejemplos"), ("MongoDB", "y"), ("Firestore", "flexible"), ("Para cambios", "rápidos"), ("En desarrollo", "ágil"), ("Sin migraciones", "pesadas"), ("De esquema", None)
                            ],
                            [
                                (None, "Consultas ricas sobre"), ("Cualquier campo", "incluso"), ("Anidados", "soporta"), ("Índices", "para"), ("Búsqueda rápida", "no tiene"), ("Joins nativos", "eficientes"), ("Suele desnormalizar", "datos"), ("Para evitar", "lecturas múltiples"), ("Atomicidad", "a nivel"), ("De documento", "consistencia"), ("Eventual", "común en"), ("Sistemas grandes distribuidos", None)
                            ],
                        ],
                    },
                    {
                        "titulo": "4.5.3. Grafos",
                        "conector": "Relaciones complejas",
                        "ramas": [
                            [
                                (None, "Prioriza relaciones" ), ("entre Entidades", "nodos"), ("Y aristas", "guardan"), ("Conexiones directas", "como"), ("Amigos de", "o"), ("Comprado por", "modelo"), ("Muy visual", "ideal"), ("Redes sociales", "y"), ("Motores recomendación", "ejemplos"), ("Neo4j", "y"), ("Amazon Neptune", "modelan"), ("El mundo real", "mejor que"), ("Tablas SQL", None)
                            ],
                            [
                                (None, "Recorrido rápido sin"), ("Índices costosos", "salta"), ("De nodo a nodo", "por"), ("Relaciones", "queries"), ("Tipo patrón", "encuentra"), ("Caminos cortos", "o"), ("Patrones fraude", "análisis"), ("De impacto", "difícil"), ("De escalar", "horizontalmente"), ("Comparado con", "otros NoSQL"), ("Requiere lenguaje", "propio como"), ("Cypher", "o"), ("Gremlin", None)
                            ],
                        ],
                    },
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
    "OUTPUT_FILE": os.path.join("Mapas", "Mapa_conceptua_GUEVARA.drawio"),
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
