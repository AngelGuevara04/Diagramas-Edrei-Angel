"""
Configuracion y datos para el generador de mapas conceptuales.
Edita este archivo para cambiar el contenido (concept_map) y los parametros de dibujo.
"""
import os
import sys

concept_map = [
    {
        "titulo_principal": "Unidad 4. Persistencia de Datos",
        "subtitulos": [
            {
                "titulo": "4.1. Ficheros",
                "conector": "Usada para",
                "ramas": [
                    [
                        (None, "Son una"), ("Colección de datos", "organizada en"), ("Discos duros", "utiliza"), ("Archivos de texto", "o"), ("Binarios", "para"), ("Guardar información", "el acceso puede ser"), ("Secuencial", "o"), ("Directo", "dependiendo del"), ("Tipo de fichero", "la operación requiere"), ("Abrir el fichero", "luego"), ("Leer y escribir", "y finalmente"), ("Cerrar el fichero", "para asegurar"), ("Integridad de datos", "son útiles para"), ("Configuración local", "o"), ("Registro de eventos", "y tienen"), ("Baja complejidad", "y también"), ("Alto rendimiento", "en operaciones"), ("Sencillas", "pero requieren"), ("Gestión de rutas", "para"), ("Evitar colisiones", "y"), ("Estandarizar nombres", "admiten"), ("Metadatos de sistema", "como"), ("Fechas y permisos", "lo que"), ("Facilita auditoría", "permiten"), ("Compresión opcional", "para"), ("Reducir espacio", "aunque"), ("Incrementa CPU", "se combinan con"), ("Herramientas CLI", "para"), ("Automatizar tareas", "y permiten"), ("Procesamiento por lotes", "en"), ("Jobs programados", "requieren"), ("Respaldos periódicos", "para"), ("Recuperación rápida", "y a veces"), ("Cifrado en reposo", "para"), ("Proteger datos", "soportan"), ("Firmas de integridad", "que"), ("Detectan corrupción", "además"), ("Sistemas de versionado", "para"), ("Rastrear cambios", "y"), ("Políticas de retención", "para"), ("Cumplir normativas", "finalmente"), ("Monitoreo de espacio", "para"), ("Evitar saturación", "y"), ("Alertas tempranas", "que"), ("Previenen caídas", "al mantener"), ("Higiene operativa", None)
                    ],
                    [
                        (None, "El manejo implica"), ("Streams de datos", "para"), ("Transferencia de bytes", "es necesario controlar"), ("Permisos de acceso", "como"), ("Lectura y escritura", "y la codificación"), ("ASCII o UTF-8", "es crucial para"), ("Manejo de texto", "la gestión requiere"), ("Manejo de errores", "por posibles"), ("Fallas de I/O", "se usa para guardar"), ("Información simple", "o"), ("Datos no estructurados", "y es el método"), ("Más básico de", "persistencia", "pero exige"), ("Control de buffer", "para"), ("Reducir latencia", "además"), ("Detección de encoding", "para"), ("Evitar caracteres rotos", "requiere"), ("Limpieza de recursos", "cerrando"), ("Handles y descriptores", "se puede aplicar"), ("Compresión de flujo", "para"), ("Transmisión eficiente", "incorpora"), ("Chequear espacio libre", "antes de"), ("Escribir archivos grandes", "se usan"), ("Pruebas unitarias", "para"), ("Validar operaciones", "y"), ("Métricas de throughput", "para"), ("Ajustar tamaños de bloque", "incluye"), ("Limitación de velocidad", "a fin de"), ("No saturar discos", "y también"), ("Logs detallados", "para"), ("Auditar accesos", "culmina con"), ("Alertas proactivas", "cuando hay"), ("Errores repetitivos", None)
                    ],
                    [
                        (None, "El diseño incluye"), ("Buffers de entrada", "y"), ("Buffers de salida", "para"), ("Optimizar lectura", "o"), ("Escritura", "según"), ("Tamaño de bloque", "se vigila el"), ("Manejo de punteros", "para"), ("Moverse por el archivo", "y se aplican"), ("Bloqueos (locks)", "para"), ("Evitar condiciones de carrera", "en entornos"), ("Multihilo o multiusuario", "requiere"), ("Flush controlado", "para"), ("Garantizar datos en disco", "y puede usar"), ("Buffers circulares", "para"), ("Evitar sobreescrituras", "además de"), ("Prefetch de datos", "para"), ("Minimizar esperas", "considera"), ("Alineación con disco", "para"), ("Reducir movimientos", "implica"), ("Reintentos con backoff", "cuando hay"), ("Errores temporales", "usa"), ("Trazas de rendimiento", "para"), ("Detectar cuellos de botella", "y habilita"), ("IO asíncrono", "para"), ("Procesar en paralelo", "se suma"), ("Pooling de descriptores", "para"), ("Reutilizar recursos", "requiere"), ("Limitar tamaño máximo", "evitando"), ("Out of memory", "además"), ("Afinidad a CPU/NUMA", "para"), ("Disminuir latencia", "y aplica"), ("Checksum de bloques", "para"), ("Detectar corrupción", "culmina con"), ("Notificación de errores", "para"), ("Recuperación automática", None)
                    ],
                ],
            },
            {
                "titulo": "4.2. Transferencia de estado representacional (Rest)",
                "conector": "Se implementa con",
                "ramas": [
                    {
                        "titulo": "4.2.1. JSON",
                        "conector": "Un formato común",
                        "ramas": [
                            [
                                (None, "Es un"), ("Estilo de arquitectura", "para"), ("Sistemas distribuidos", "utiliza el protocolo"), ("HTTP", "se basa en"), ("Recursos", "identificados por"), ("URIs", "las operaciones son"), ("CRUD", "usando métodos"), ("GET, POST, PUT, DELETE", "es un diseño"), ("Sin estado (Stateless)", "que garantiza"), ("Escalabilidad", "y promueve el uso"), ("Uniforme de interfaces", "los mensajes usan"), ("Representaciones ligeras", "como"), ("JSON o XML", "lo que facilita"), ("Comunicación cliente-servidor", "es la base de"), ("Servicios web modernos", "impulsa"), ("Hipermedios HATEOAS", "para"), ("Descubrir acciones", "requiere"), ("Códigos HTTP coherentes", "que dan"), ("Claridad semántica", "fomenta"), ("Cacheo con ETags", "para"), ("Reducir tráfico", "se apoya en"), ("Seguridad TLS", "para"), ("Proteger datos", "usa"), ("Versionado de recursos", "evitando"), ("Ruptura de clientes", "necesita"), ("Paginación y filtros", "para"), ("Respuestas controladas", "y"), ("Rate limiting", "para"), ("Prevenir abuso", "incluye"), ("Idempotencia en PUT/DELETE", "para"), ("Operaciones seguras", "además de"), ("Monitoreo y trazas", "para"), ("Observabilidad completa", None)
                            ],
                            [
                                (None, "Requiere diseno de"), ("Contratos claros", "con"), ("Esquemas JSON Schema", "que permiten"), ("Validacion temprana", "ademas de"), ("Versionar campos", "usando"), ("Deprecaciones controladas", "y"), ("Estrategias de compatibilidad", "se debe cuidar"), ("Paginado cursor", "para"), ("Escalar listados", "incorpora"), ("Filtros por query params", "para"), ("Flexibilidad sin romper", "incluye"), ("Pruebas de carga", "para"), ("Dimensionar recursos", "y"), ("Seguridad con CORS", "que"), ("Restringe origenes", "agrega"), ("Rate limits adaptativos", "para"), ("Mitigar abuso", "y"), ("Uso de cache inversa", "para"), ("Acelerar respuestas", "agrega"), ("Observabilidad en cliente", "que"), ("Propaga trace IDs", "requiere"), ("Validar headers", "para"), ("Evitar injection", "usa"), ("Linting de contratos", "que"), ("Detecta campos huérfanos", "incluye"), ("Mock servers", "para"), ("Probar integraciones", "añade"), ("Estrategias de paginado", "con"), ("Limites y offsets", "para"), ("Evitar timeouts", "considera"), ("Idempotent keys", "para"), ("Reintentos seguros", "y"), ("Caching en borde", "para"), ("Reducir latencia", "requiere"), ("Políticas de expiracion", "que"), ("Sincronizan clientes", "suma"), ("TLS mutual", "para"), ("Endurecer canales", "y"), ("Secretos rotados", "que"), ("Evitan fugas", "finaliza con"), ("Tableros de SLA", "para"), ("Seguir salud del API", None)
                            ],
                        ],
                    },
                    {
                        "titulo": "4.2.2. XML",
                        "conector": "Otro formato estructurado",
                        "ramas": [
                            [
                                (None, "Utiliza"), ("Etiquetas jerárquicas", "para"), ("Estructurar datos", "es"), ("Autodescriptivo", "y soporta"), ("Validación con XSD", "o"), ("DTD", "permite"), ("Namespaces", "para evitar"), ("Conflictos de nombres", "se usa en"), ("Servicios SOAP", "y"), ("Integraciones empresariales", "ofrece"), ("Extensibilidad", "aunque suele ser"), ("Más pesado", "que JSON", "requiere"), ("Espacios en blanco cuidados", "para"), ("Evitar ambigüedad", "habilita"), ("CDATA para texto crudo", "cuando"), ("Se requiere preservar formato", "soporta"), ("Procesamiento SAX y DOM", "según"), ("Necesidades de memoria", "incluye"), ("Comentarios inline", "útiles para"), ("Metadatos de lectura", "se integra con"), ("Firmas XMLDSig", "para"), ("Verificación robusta", "y usa"), ("XPath y XQuery", "para"), ("Consultas estructuradas", "necesita"), ("Versionado de esquemas", "que"), ("Resguarda compatibilidad", None)
                            ],
                            [
                                (None, "Requiere"), ("Normalizar indentación", "y"), ("Escape de caracteres", "para"), ("Evitar errores de parseo", "se beneficia de"), ("Transformaciones XSLT", "para"), ("Generar vistas", "y permite"), ("Firmas digitales", "para asegurar"), ("Integridad y origen", "manteniendo"), ("Compatibilidad retroactiva", "en"), ("Sistemas legados", "incluye"), ("Validación estricta", "mediante"), ("Esquemas versionados", "que permiten"), ("Evolucionar contratos", "sin"), ("Romper clientes", "se apoya en"), ("Herramientas de linting", "para"), ("Detectar inconsistencias", "y requiere"), ("Politicas de serialización", "para asegurar"), ("Coherencia entre servicios", "además requiere"), ("Orden de atributos", "para"), ("Predecir hashes", "favorece"), ("Uso de entidades externas", "con"), ("Controles de seguridad", "evita"), ("XXE y ataques de inyección", "mediante"), ("Validación de entrada", "añade"), ("Logging estructurado", "para"), ("Rastrear transformaciones", "y usa"), ("Namespaces bien definidos", "para"), ("Evitar choques futuros", "se suma"), ("Estrategia de nombres", "alineada a"), ("Dominios de negocio", "finalmente"), ("Pruebas de contrato", "para"), ("Proteger integraciones", None)
                            ],
                        ],
                    },
                    {
                        "titulo": "4.2.3. Buenas prácticas REST",
                        "conector": "Mejoran la",
                        "ramas": [
                            [
                                (None, "Incluyen"), ("Versionado de APIs", "mediante"), ("Encabezados o rutas", "garantizando"), ("Compatibilidad", "se recomienda"), ("Documentación clara", "usando"), ("OpenAPI/Swagger", "y"), ("Pruebas automatizadas", "para"), ("Validar contratos", "además de"), ("Manejo de errores", "con"), ("Códigos HTTP coherentes", "y"), ("Mensajes descriptivos", "se suman"), ("Políticas de caché", "con"), ("ETags o Cache-Control", "y"), ("Paginación consistente", "para"), ("Respuestas predecibles", "requiere"), ("Autenticación y authZ", "con"), ("OAuth2/JWT", "para"), ("Asegurar recursos", "usa"), ("Circuit breakers", "que"), ("Previenen cascadas", "incluye"), ("Tracing distribuido", "para"), ("Diagnóstico rápido", "y"), ("Correlación de peticiones", "favorece"), ("Headers idempotentes", "para"), ("Reintentos seguros", "añade"), ("Límites de tamaño", "evitando"), ("Payloads excesivos", "se complementa con"), ("Observabilidad", "usando"), ("Métricas y logs", "para"), ("Detectar anomalías", "además"), ("Revisiones de seguridad", "con"), ("OWASP API Top 10", "para"), ("Mitigar riesgos", "y finalmente"), ("Despliegue blue/green", "para"), ("Liberar cambios sin corte", None)
                            ],
                            [
                                (None, "Implica monitoreo"), ("de SLAs", "para"), ("Cumplir contratos", "requiere"), ("Testing de resiliencia", "que"), ("Valida fallas controladas", "incluye"), ("Documentar errores", "con"), ("Respuestas estandar", "y"), ("Politicas de versionado", "para"), ("Migraciones suaves", "agrega"), ("Analisis de seguridad", "contra"), ("Inyecciones y cors", "usa"), ("Tolerancia a fallos", "mediante"), ("Circuit breaker y retries", "añade"), ("Dashboards de latencia", "para"), ("Detectar cuellos", "incluye"), ("Alertas por percentiles", "que"), ("Reflejan picos", "requiere"), ("Chaos days", "para"), ("Entrenar equipos", "se complementa con"), ("Feature toggles", "que"), ("Permiten rollback rapido", "usa"), ("Sandbox de contratos", "para"), ("Validar cambios", "agrega"), ("Rehearsals de incidentes", "que"), ("Reducen MTTR", "añade"), ("Analisis de causa", "para"), ("Mejora continua", "y"), ("Tableros de error budgets", "para"), ("Gestionar riesgo", "incorpora"), ("Backpressure controlado", "para"), ("Evitar cascadas", "y"), ("Simulacion de picos", "para"), ("Planificar capacidad", "finaliza con"), ("Evidencias de auditoria", "que"), ("Demuestran cumplimiento", None)
                            ],
                        ],
                    },
                    
                ],
            },
            {
                "titulo": "4.3. Servicios en la nube",
                "conector": "Permiten usar",
                "ramas": [
                    {
                        "titulo": "4.3.1. Almacenamiento",
                        "conector": "Incluye el servicio de",
                        "ramas": [
                            [
                                (None, "Ofrece servicios como"), ("Bases de datos", "y"), ("Almacenamiento de objetos", "proporciona"), ("Alta disponibilidad", "y"), ("Durabilidad de datos", "el acceso es vía"), ("APIs web", "o"), ("Interfaces gráficas", "se diferencia en"), ("Bloques, archivos, objetos", "para distintas"), ("Necesidades de datos", "permite"), ("Escalabilidad automática", "y gestiona"), ("Backups y redundancia", "lo que reduce"), ("Carga operativa local", "incluye"), ("Versionado de objetos", "para"), ("Recuperar historiales", "usa"), ("Políticas de ciclo de vida", "que"), ("Mueven datos a frío", "habilita"), ("Cifrado gestionado", "para"), ("Cumplir normativas", "añade"), ("Control de acceso granular", "basado en"), ("Roles y etiquetas", "ofrece"), ("Replicación entre regiones", "para"), ("Resiliencia geográfica", "y"), ("Notificaciones por eventos", "que"), ("Disparan flujos serverless", "requiere"), ("Cost allocation tags", "para"), ("Optimizar gasto", "además de"), ("Pruebas de restauración", "para"), ("Verificar backups", "y"), ("Monitoreo de capacidad", "con"), ("Alertas tempranas", None)
                            ],
                            [
                                (None, "Agrega edge caching"), ("para" ,"Distribuir contenido"), ("y acelerar descargas", "requiere"), ("Politicas de lifecycle", "que"), ("Mueven a glacier", "usa"), ("Bloqueo WORM", "para"), ("Evidencia legal", "incluye"), ("Inventario de objetos", "que"), ("Verifica estado", "y"), ("Replicacion asincrona", "para"), ("Bajar latencia regional", "añade"), ("Cross-region copy", "para"), ("Resiliencia extra", "usa"), ("Policies de retencion", "que"), ("Expiran versiones", "incluye"), ("Etiquetas obligatorias", "para"), ("Trazar costos", "se suma"), ("Notificaciones S3 events", "para"), ("Disparar pipelines", "agrega"), ("Objetos inmutables", "que"), ("Protegen backups", "incorpora"), ("Checksum automatico", "para"), ("Detectar corrupcion", "requiere"), ("Inventario cifrado", "que"), ("Evita datos en claro", "incluye"), ("Access Analyzer", "para"), ("Detectar exposiciones", "usa"), ("Bloqueo de acceso publico", "que"), ("Previene fugas", "añade"), ("Replication time control", "para"), ("SLAs de copia", "y"), ("Policies de borrado legal", "para"), ("Cumplir normativas", None)
                            ],
                        ],
                    },
                    {
                        "titulo": "4.3.2. Autentificación",
                        "conector": "Se encarga de",
                        "ramas": [
                            [
                                (None, "Gestiona la"), ("Identidad de usuarios", "utiliza protocolos como"), ("OAuth o SAML", "para asegurar"), ("Acceso seguro", "proporciona"), ("Manejo de tokens", "para"), ("Autorización de recursos", "el servicio integra"), ("Directorios de usuarios", "y ofrece"), ("Autenticación multifactor", "lo que protege"), ("Cuentas y sistemas", "además de proveer"), ("APIs sencillas", "para integrar"), ("Login en aplicaciones", "incluye"), ("Rotación de claves", "para"), ("Reducir riesgos", "y añade"), ("Auditoría centralizada", "que registra"), ("Accesos y anomalías", "requiere"), ("Políticas de contraseñas", "para"), ("Fortalecer credenciales", "usa"), ("SSO empresarial", "que"), ("Simplifica experiencia", "ofrece"), ("Federación de identidades", "para"), ("Colaboradores externos", "incorpora"), ("Detección de anomalías", "que"), ("Evalúa riesgo", "hace"), ("Revocación inmediata", "ante"), ("Dispositivos comprometidos", "habilita"), ("Scopes granulares", "para"), ("Limitar privilegios", "incluye"), ("Logs firmados", "para"), ("Evidencia forense", "se suma"), ("Cumplimiento normativo", "GDPR/ISO"), ("para"), ("Auditorías exitosas", None)
                            ],
                        ],
                    },
                    {
                        "titulo": "4.3.3. Mensajería",
                        "conector": "Facilita la",
                        "ramas": [
                            [
                                (None, "Permite comunicación"), ("Asíncrona", "entre"), ("Componentes de sistemas", "utiliza"), ("Colas de mensajes", "o"), ("Temas (topics)", "para enviar"), ("Notificaciones o datos", "garantiza la entrega"), ("Fiable de mensajes", "y desacopla el"), ("Emisor del receptor", "esto ayuda a construir"), ("Microservicios resilientes", "y procesar"), ("Tareas en segundo plano", "añade"), ("Dead-letter queues", "para"), ("Mensajes fallidos", "y maneja"), ("Reintentos con backoff", "asegurando"), ("Orden o FIFO", "cuando el"), ("Negocio lo requiere", "habilita"), ("Time-to-live", "para"), ("Expirar mensajes viejos", "integra"), ("Encriptado en tránsito", "para"), ("Cumplir seguridad", "usa"), ("Idempotency keys", "que"), ("Evitan duplicados", "ofrece"), ("Metrics de cola", "para"), ("Dimensionar consumidores", "incluye"), ("Batching y prefetch", "para"), ("Optimizar throughput", "requiere"), ("Aislamiento por tenants", "para"), ("Separar clientes", "y proporciona"), ("Esquemas con Avro/JSON", "que"), ("Validan payloads", "además"), ("DLQ monitoring", "para"), ("Ajustar reintentos", "culmina con"), ("Topology as code", "que"), ("Documenta flujos", None)
                            ],
                            [
                                (None, "Incorpora filtros"), ("por headers", "para"), ("Rutas dinamicas", "requiere"), ("DLQ analizada", "para"), ("Evitar loops", "incluye"), ("Mensajes programados", "para"), ("Retrasos controlados", "agrega"), ("Outbox pattern", "para"), ("Evitar perdidas", "usa"), ("Metrics y alertas", "que"), ("Detectan backlog", "añade"), ("DLQ replay seguro", "para"), ("Reprocesar con control", "incluye"), ("Schemas versionados", "que"), ("Validan compatibilidad", "requiere"), ("Encryption at rest", "para"), ("Cumplir normativas", "usa"), ("Tracing distribuido", "que"), ("Propaga correlation IDs", "agrega"), ("Poison message handling", "para"), ("Aislar problematicos", "incorpora"), ("Idempotent consumers", "que"), ("Evitan duplicados", "añade"), ("Metrics de lag", "para"), ("Escalar consumidores", "y"), ("Alertas de throughput", "para"), ("Dimensionar colas", None)
                            ],
                        ],
                    },
                    {
                        "titulo": "4.3.4. Cómputo",
                        "conector": "Proporciona recursos de",
                        "ramas": [
                            [
                                (None, "Incluye"), ("Máquinas virtuales", "o"), ("Contenedores orquestados", "para"), ("Desplegar aplicaciones", "brinda"), ("Escalado automático", "basado en"), ("Métricas de carga", "y soporta"), ("Funciones serverless", "para"), ("Ejecución bajo demanda", "pagando solo por"), ("Tiempo de ejecución", "incluye"), ("Imágenes base endurecidas", "para"), ("Estandarizar despliegues", "y incorpora"), ("Auto-healing", "que reinicia"), ("Instancias fallidas", "además de"), ("Optimizar costos", "mediante"), ("Apagado programado", "agrega"), ("Auto-scaling policies", "que"), ("Ajustan replicas", "integra"), ("Rolling updates", "para"), ("Despliegues sin corte", "ofrece"), ("Observabilidad nativa", "con"), ("Logs y métricas", "usa"), ("Probes de salud", "para"), ("Detectar caídas", "habilita"), ("Plantillas IaC", "para"), ("Reproducir entornos", "incluye"), ("Gestión de secretos", "para"), ("Variables sensibles", "soporta"), ("Imágenes inmutables", "que"), ("Simplifican rollbacks", "añade"), ("Spot/Preemptibles", "para"), ("Reducir costos", "y"), ("Programación elástica", "para"), ("Cargas batch", None)
                            ],
                            [
                                (None, "Incluye GPU a demanda"), ("para", "Procesar IA"), ("y streaming" ,"requiere"), ("Auto escalado vertical", "para"), ("Picos breves", "usa"), ("Node pools dedicados", "que"), ("Separan cargas", "incluye"), ("Grupos de spot", "para"), ("Reducir costo", "y"), ("Politicas de afinidad", "para"), ("Mejorar cache", "añade"), ("Auto scaler bin packing", "que"), ("Optimiza recursos", "usa"), ("Imagenes con drivers", "para"), ("Compatibilidad CUDA", "incluye"), ("Taints y tolerations", "para"), ("Aislar workloads", "agrega"), ("GPUs compartidas", "que"), ("Reducen desperdicio", "requiere"), ("Monitor de temperatura", "para"), ("Prevenir thermal throttling", "usa"), ("Scheduler aware", "que"), ("Prioriza colas", "añade"), ("Cotas de GPU", "para"), ("Evitar acaparamiento", "y"), ("Snapshots de nodos", "para"), ("Recuperar configs rapido", None)
                            ],
                        ],
                    },
                    {
                        "titulo": "4.3.5. Redes",
                        "conector": "Aíslan y exponen",
                        "ramas": [
                            [
                                (None, "Permiten"), ("VPCs o VNets", "para"), ("Segmentar tráfico", "configuran"), ("Subredes y firewalls", "que"), ("Restringen acceso", "y ofrecen"), ("Balanceadores de carga", "para"), ("Distribuir peticiones", "además de"), ("VPNs", "para"), ("Conectar on-premise", "con"), ("Infraestructura en nube", "también integran"), ("WAFs y DNS gestionado", "para"), ("Proteger apps públicas", "e implementan"), ("Peering o private links", "que"), ("Reducen latencia", "incorporan"), ("Listas de control de acceso", "para"), ("Reglas detalladas", "habilitan"), ("Seguridad de capa 7", "con"), ("Inspección profunda", "ofrecen"), ("NAT gateways", "para"), ("Salida controlada", "y"), ("Políticas de ruteo", "que"), ("Definen caminos", "incluyen"), ("IPs elásticas", "para"), ("Alta disponibilidad", "implementan"), ("Registros de flujo", "para"), ("Auditar tráfico", "agregan"), ("QoS y shaping", "para"), ("Priorizar servicios críticos", "y"), ("Segmentación zero-trust", "para"), ("Minimizar superficie", None)
                            ],
                            [
                                (None, "Incluyen service mesh"), ("para", "Observabilidad de trafico"), ("y mTLS" ,"requiere"), ("Redundancia multi AZ", "para"), ("Disponibilidad alta", "usa"), ("Zonas privadas", "que"), ("Ocultan datos", "agrega"), ("Rutas dinamicas", "para"), ("Failover rapido", "añade"), ("Sidecars livianos", "para"), ("Gestionar politicas", "usa"), ("Rate limiting por servicio", "que"), ("Protege backends", "incluye"), ("Circuit breakers", "para"), ("Contener fallas", "agrega"), ("Mirroring de trafico", "que"), ("Prueba versiones", "requiere"), ("mTLS mutuo", "para"), ("Identidad fuerte", "usa"), ("RBAC de red", "que"), ("Restringe flujos", "suma"), ("Tracing distribuido", "para"), ("Correlacion completa", "y"), ("Metricas por salto", "que"), ("Facilitan tuning", None)
                            ],
                        ],
                    },
                ],
            },
            {
                "titulo": "4.4. Desarrollo de un proyecto con servicios en la nube",
                "conector": "Se centra en",
                "ramas": [
                    [
                        (None, "La fase inicial es"), ("Planificación de arquitectura", "donde se elige"), ("Proveedores de nube", "se define la"), ("Estructura de la aplicación", "y se considera"), ("Seguridad y costes", "luego sigue la"), ("Implementación de código", "utilizando las"), ("APIs de la nube", "se configura el"), ("Almacenamiento y BBDD", "y se implementa"), ("Lógica de negocio", "el siguiente paso es"), ("Despliegue (deployment)", "usando herramientas de"), ("Integración continua", "para automatizar el"), ("Lanzamiento de versiones", "se añade"), ("Pruebas automatizadas", "para"), ("Validar cada build", "requiere"), ("Branching strategy", "que"), ("Coordina equipos", "usa"), ("Revisiones de código", "para"), ("Elevar calidad", "incluye"), ("Gestión de secretos", "con"), ("Vaults centralizados", "considera"), ("Feature flags", "para"), ("Lanzar gradualmente", "y"), ("Observabilidad inicial", "para"), ("Medir impacto", "finaliza con"), ("Checklist de release", "que"), ("Garantiza cumplimiento", None)
                    ],
                    [
                        (None, "Implica también"), ("Monitoreo constante", "para vigilar"), ("Rendimiento y errores", "se usan servicios de"), ("Logging y métricas", "para identificar"), ("Puntos de mejora", "es crucial asegurar"), ("Escalabilidad", "para manejar"), ("Cargas variables de tráfico", "y mantener"), ("Alta disponibilidad", "mediante"), ("Balanceadores de carga", "la gestión requiere"), ("Cultura DevOps", "para integrar"), ("Desarrollo y operaciones", "requiere"), ("SLO/SLA definidos", "para"), ("Priorizar alertas", "y habilitar"), ("Optimización de costes", "mediante"), ("Rightsizing y reservas", "añade"), ("Capacidad de rollback", "para"), ("Recuperar versiones", "usa"), ("Runbooks y playbooks", "que"), ("Estandarizan respuesta", "incluye"), ("Chaos engineering", "para"), ("Validar resiliencia", "y"), ("Gestión de incidencias", "con"), ("Postmortems claros", "requiere"), ("Capas de caché", "para"), ("Reducir latencia", "y"), ("Autoscaling tests", "para"), ("Ajustar umbrales", "además"), ("Guardrails de seguridad", "para"), ("Accesos mínimos", None)
                    ],
                    [
                        (None, "Incluye"), ("Pruebas de carga", "para"), ("Validar resiliencia", "y"), ("Revisiones de seguridad", "con"), ("Escaneos automatizados", "además de"), ("IaC (Terraform, ARM)", "para"), ("Versionar infraestructura", "esto facilita"), ("Reproducibilidad", "y"), ("Recuperación ante desastres", "mediante"), ("Ambientes replicables", "requiere"), ("Documentación viva", "para"), ("Onboarding rápido", "y"), ("Ejercicios de incidente", "para"), ("Mejorar respuesta", "considera"), ("Gestión de artefactos", "con"), ("Repositorios binarios", "integra"), ("Canary releases", "para"), ("Probar en producción", "usa"), ("Monitoreo sintético", "para"), ("Validar rutas críticas", "añade"), ("Backup como código", "para"), ("Restauraciones repetibles", "incluye"), ("Mapeo de dependencias", "para"), ("Entender acoplamientos", "y"), ("Control de cambios", "mediante"), ("Change advisory boards", "cuando"), ("El riesgo es alto", None)
                    ],
                ],
            },
            {
                "titulo": "4.5. NoSQL",
                "conector": "Incluye el modelo",
                "ramas": [
                    {
                        "titulo": "4.5.1. Clave – valor",
                        "conector": "Se enfoca en",
                        "ramas": [
                            [
                                (None, "Ofrece un modelo"), ("Simple de datos", "cada ítem es"), ("Una clave única", "asociada a un"), ("Valor (Value)", "el valor puede ser"), ("Cualquier tipo de", "dato", "proporciona"), ("Lectura y escritura", "de forma"), ("Extremadamente rápida", "es ideal para"), ("Caché de datos", "o"), ("Sesiones de usuario", "la escalabilidad es"), ("Horizontal", "y maneja"), ("Grandes volúmenes", "de tráfico con"), ("Baja latencia", "incluye"), ("TTL por clave", "para"), ("Expirar sesiones", "usa"), ("Sharding automático", "que"), ("Distribuye carga", "añade"), ("Replicación en memoria", "para"), ("Alta disponibilidad", "ofrece"), ("Operaciones atómicas", "como"), ("Increments o sets", "permite"), ("Persistencia opcional", "mediante"), ("Snapshots o AOF", "y"), ("Pub/Sub ligero", "para"), ("Notificaciones rápidas", "requiere"), ("Monitoreo de memoria", "para"), ("Evitar evicciones inesperadas", None)
                            ],
                        ],
                    },
                    {
                        "titulo": "4.5.2. Documentos",
                        "conector": "Se almacena como",
                        "ramas": [
                            [
                                (None, "Los datos se guardan"), ("En formato JSON", "o"), ("BSON", "cada documento es"), ("Independiente", "y tiene su propio"), ("Esquema flexible", "esto permite"), ("Rápida iteración", "y adaptación a"), ("Cambios de datos", "son ideales para"), ("Catálogos de productos", "o"), ("Contenido web", "las consultas pueden ser"), ("Complejas y dinámicas", "y permiten"), ("Indexación por campos", "para mejorar"), ("Velocidad de búsqueda", "se suman"), ("Índices compuestos", "para"), ("Consultas multi campo", "incluye"), ("Proyecciones parciales", "que"), ("Reducen payloads", "habilita"), ("Sharding por clave", "para"), ("Balancear datos", "usa"), ("Agregaciones pipeline", "para"), ("Analítica embebida", "admite"), ("Validadores de esquema", "para"), ("Governance de datos", "y"), ("Triggers/Change streams", "que"), ("Reaccionan en tiempo real", "requiere"), ("Tuning de TTL e históricos", "para"), ("Controlar retención", None)
                            ],
                        ],
                    },
                    {
                        "titulo": "4.5.3. Grafos",
                        "conector": "Se basa en",
                        "ramas": [
                            [
                                (None, "Los datos se modelan"), ("Como nodos (vértices)", "y"), ("Relaciones (edges)", "entre ellos"), ("Cada nodo tiene"), ("Propiedades (properties)", "y las relaciones tienen"), ("Tipos y dirección", "son óptimas para"), ("Modelar conexiones", "o"), ("Redes sociales", "la consulta de relaciones"), ("Es muy eficiente", "usando lenguajes como"), ("Cypher o Gremlin", "y son esenciales para"), ("Análisis de impacto", "o"), ("Sistemas de recomendación", "permiten"), ("Caminos más cortos", "para"), ("Analizar rutas", "soportan"), ("Algoritmos de centralidad", "para"), ("Detectar influencias", "incluyen"), ("Etiquetas en nodos", "que"), ("Segmentan comunidades", "habilitan"), ("Versionado de grafos", "para"), ("Comparar estados", "usan"), ("Indices de relaciones", "para"), ("Consultas rápidas", "y"), ("APIs traversal streaming", "que"), ("Evitan cargas totales", "requiere"), ("Gestión de cardinalidad", "para"), ("Evitar explosión de nodos", None)
                            ],
                        ],
                    },
                    {
                        "titulo": "4.5.4. Columnas",
                        "conector": "Enfocado en",
                        "ramas": [
                            [
                                (None, "Almacena datos por"), ("Column families", "que agrupan"), ("Filas relacionadas", "optimiza"), ("Consultas analíticas", "al leer"), ("Conjuntos parciales", "es ideal para"), ("Series temporales", "o"), ("Aplicaciones de telemetría", "permite"), ("Compresión eficiente", "y"), ("Distribución horizontal", "usando"), ("Particionamiento y replicación", "requiere"), ("Monitorear compaction", "para"), ("Mantener rendimiento", "y demanda"), ("Modelar consultas", "en torno a"), ("Claves de partición", "agrega"), ("Bloom filters", "para"), ("Reducir lecturas", "incluye"), ("TTL granular", "que"), ("Limpia datos viejos", "usa"), ("Wide rows", "para"), ("Agrupar series", "requiere"), ("Tuning de consistency", "balanceando"), ("Disponibilidad y latencia", "ofrece"), ("Batch de escrituras", "para"), ("Mayor throughput", "añade"), ("Secondary indexes limitados", "que"), ("Necesitan diseño cuidadoso", "y"), ("Backups incremental", "para"), ("Proteger información", None)
                            ],
                        ],
                    },
                    {
                        "titulo": "4.5.5. Series de tiempo",
                        "conector": "Optimiza",
                        "ramas": [
                            [
                                (None, "Datos ordenados"), ("por timestamp", "para"), ("Metricas y logs", "requiere"), ("Retention policies", "que"), ("Depuran historicos", "usa"), ("Downsampling", "para"), ("Reducir costo", "incluye"), ("Etiquetas", "para"), ("Agrupar dimensiones", "agrega"), ("Indices por tiempo", "que"), ("Aceleran rangos", "incorpora"), ("Lectura append-only", "para"), ("Ingesta rapida", "añade"), ("Compresion por bloques", "que"), ("Reduce espacio", "usa"), ("Window functions", "para"), ("Calcular agregados", "incluye"), ("Cardinalidad controlada", "para"), ("Evitar explosion", "agrega"), ("Shard por tiempo", "que"), ("Balancea escritura", "requiere"), ("Clock sync", "para"), ("Evitar skew", "usa"), ("Batch ingest", "que"), ("Optimiza IO", "incluye"), ("Downsampling jerarquico", "para"), ("Vistas de largo plazo", "finaliza con"), ("Alertas por umbral", "que"), ("Detectan anomalías", "y"), ("Gap filling", "para"), ("Series incompletas", None)
                            ],
                        ],
                    },
                ],
            },
        ],
    }
]

# Todos los valores son opcionales; solo sobreescribe los que necesites.
CONFIG = {
    # Tipografia
    "FONT_FAMILY": "Courier New",
    "FONT_SIZE": 12,
    "FONT_COLOR": "#1f2937",
    # Bordes y conectores
    "STROKE_W": 1.2,
    "EDGE_COLOR": "#38579b",
    # Nodos
    "BOX_ARC_SIZE": 30,
    "BOX_SHADOW": True,
    # Colores de titulo y subtitulo
    "MAIN_FILL_COLOR": "#dbeafe",
    "MAIN_STROKE_COLOR": "#1d4ed8",
    "SUBTITLE_FILL_COLOR": "#e2e8f0",
    "SUBTITLE_STROKE_COLOR": "#475569",
    # Texto de conectores
    "CONNECTOR_FONT_FAMILY": "Verdana",
    "CONNECTOR_FONT_SIZE": 9,
    "CONNECTOR_FONT_COLOR": "#111827",
    "CONNECTOR_BG_COLOR": "#f8fafc",
    "CONNECTOR_BORDER_COLOR": "#cbd5e1",
    "CONNECTOR_SHADOW": False,
    "CONNECTOR_TEXT_SHADOW": True,
    # Tamaño de nodos
    "BOX_W": 100,
    "BOX_H": 70,
    # Separaciones basicas
    "X_STEP": 150,
    "Y_STEP": 110,
    # Separaciones jerarquicas
    "MAIN_TO_SUBTITLE": 130,
    "SUBTITLE_TO_BRANCH": 150,
    "SUBTITLE_GAP": 80,
    "GROUP_GAP": 200,
    # Paleta de ramas
    "PALETTE": [
        ("#fff3c4", "#d97706"),
        ("#d8ffe5", "#15803d"),
        ("#e0eeff", "#1d4ed8"),
        ("#ffead2", "#c2410c"),
    ],
    # Posicion inicial y salida
    "START_X": 120,
    "START_Y": 40,
    "OUTPUT_FILE": os.path.join("Mapas", "mapa_juan.drawio"),
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
