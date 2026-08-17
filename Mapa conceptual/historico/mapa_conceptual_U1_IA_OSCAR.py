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
        "titulo_principal": "Unidad 1. Desarrollo Móvil",
        "subtitulos": [
            {
                "titulo": "1.1. Dispositivos Móviles",
                "conector": "Computación portátil",
                "ramas": [
                    [
                        (None, "Definición"), ("Aparato pequeño", "con"), ("Capacidad proceso", "para"), ("Correr software", "que necesita"),
                        {
                            "texto": "Sistemas Operativos",
                            "conector": "principales",
                            "bifurcaciones": [
                                [
                                    (None, "Plataforma"), ("Google Android", "basado"), ("En Kernel", "de"), ("Linux", "es"), ("Código abierto", "AOSP"), ("Lo que permite", "alta"), ("Personalización", "por"), ("Los fabricantes", "tiene"), ("Gran cuota", "de"), ("Mercado mundial", "y usa"), ("Google Play", "como"), ("Tienda principal", "su"), ("Entorno desarrollo", "es"), ("Android Studio", None)
                                ],
                                [
                                    (None, "Plataforma"), ("Apple iOS", "basado"), ("En Unix", "es"), ("Código cerrado", "y"), ("Altamente optimizado", "para"), ("Su hardware", "específico"), ("Ofrece alta", "seguridad"), ("Mediante sandboxing", "y"), ("Estricta revisión", "de"), ("Apps", "en"), ("La App Store", "su"), ("Interfaz gráfica", "sigue"), ("Guías HIG", "de"), ("Diseño", "muy"), ("Consistentes", None)
                                ],
                                [
                                    (None, "Plataforma"), ("Otros", "como"), ("KaiOS", "para"), ("Teléfonos básicos", "con"), ("Funciones smart", "y"), ("HarmonyOS", "de"), ("Huawei", "enfocado"), ("En ecosistema", "de"), ("Dispositivos IoT", "busca"), ("Ser una", "alternativa"), ("A los", "dos"), ("Grandes dominadores", "del"), ("Mercado actual", "pero"), ("Con menor", "cuota"), ("De mercado", None)
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
                        (None, "Componentes"), ("SoC", "fabricado por"),
                        {
                            "texto": "Fabricantes SoC",
                            "conector": "líderes",
                            "bifurcaciones": [
                                [
                                    (None, "Marca"), ("Qualcomm", "domina"), ("Gama alta", "con"), ("Su serie", "Snapdragon"), ("Que integra", "CPU"), ("Kryo custom", "y"), ("GPU Adreno", "para"), ("Excelente rendimiento", "en"), ("Juegos 3D", "son"), ("Líderes en", "módems"), ("5G", "y"), ("Procesamiento", "de"), ("Inteligencia Artificial", "en"), ("Teléfonos Android", None)
                                ],
                                [
                                    (None, "Marca"), ("Apple", "diseña"), ("Sus propios", "chips"), ("Serie A", "para"), ("iPhone", "y"), ("Serie M", "para"), ("IPad/Mac", "logrando"), ("Integración vertical", "y"), ("Máxima eficiencia", "energética"), ("Su enfoque", "es"), ("Rendimiento", "por"), ("Vatio", "y"), ("Potentes núcleos", "de"), ("CPU y GPU", "que son"), ("propios", None)
                                ],
                                [
                                    (None, "Marca"), ("MediaTek", "fuerte"), ("En gamas", "media"), ("Y de entrada", "con"), ("Su familia", "Dimensity"), ("Y Helio", "compite"), ("Fuertemente", "con"), ("Qualcomm", "ofreciendo"), ("Soluciones 5G", "más"), ("Asequibles", "han"), ("Mejorado mucho", "en"), ("Rendimiento", "y"), ("Eficiencia", "en"), ("Los últimos años", None)
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
                        (None, "Concepto"), ("Programa informático", "diseñado"), ("Específicamente", "para"), ("Sistemas operativos", "móviles"), ("Que satisface", "necesidades"),
                        {
                            "texto": "Categorías Populares",
                            "conector": "ejemplos",
                            "bifurcaciones": [
                                [
                                    (None, "Tipo"), ("Redes Sociales", "permiten"), ("Crear perfiles", "y"), ("Compartir contenido", "como"), ("Fotos y videos", "conectan"), ("Amigos", "y"), ("Familiares", "forman"), ("Comunidades", "con"), ("Intereses comunes", "se"), ("Monetizan", "con"), ("Publicidad dirigida", "y"), ("Recopilación", "de"), ("Datos de usuario", None)
                                ],
                                [
                                    (None, "Tipo"), ("Juegos", "son"), ("Fuente principal", "de"), ("Entretenimiento", "hay"), ("Desde casuales", "hasta"), ("Títulos complejos", "con"), ("Gráficos avanzados", "utilizan"), ("Modelos", "de"), ("Monetización", "como"), ("Compras in-app", "para"), ("Obtener ventajas", "o"), ("Cosméticos", "son"), ("Muy populares", "en"), ("Todas las edades", None)
                                ],
                                [
                                    (None, "Tipo"), ("Productividad", "ayudan"), ("A organizar", "el"), ("Trabajo diario", "incluyen"), ("Agendas", "y"), ("Calendarios", "también"), ("Gestores", "de"), ("Tareas", "y"), ("Proyectos", "permiten"), ("Tomar notas", "y"), ("Editar documentos", "desde"), ("Cualquier lugar", "aumentando"), ("La eficiencia", "personal y"), ("Profesional", None)
                                ]
                            ]
                        }
                    ],
                    {
                        "titulo": "1.2.1. Clasificación Apps",
                        "conector": "Tipos desarrollo",
                        "ramas": [
                            [
                                (None, "Nativas"), ("Desarrollo específico", "para"), ("Cada plataforma", "usando"),
                                {
                                    "texto": "Lenguajes Nativos",
                                    "conector": "usados en",
                                    "bifurcaciones": [
                                        [
                                            (None, "OS"), ("Android", "usa"), ("Kotlin", "como"), ("Lenguaje principal", "respaldado"), ("Por Google", "es"), ("Interoperable", "con"), ("Java", "el"), ("Lenguaje anterior", "se"), ("Ejecuta sobre", "la"), ("Máquina virtual", "ART"), ("Y usa", "Gradle como"), ("Sistema", "de"), ("Construcción", None)
                                        ],
                                        [
                                            (None, "OS"), ("iOS", "usa"), ("Swift", "un"), ("Lenguaje moderno", "y"), ("Seguro", "creado"), ("Por Apple", "es"), ("Más rápido", "que"), ("Su predecesor", "Objective-C"), ("Se compila", "directamente"), ("A código", "máquina"), ("Sin VM", "y"), ("Usa Xcode", "como"), ("Entorno", "de"), ("Desarrollo", None)
                                        ]
                                    ]
                                }
                            ],
                            [
                                (None, "Web Apps"), ("Corren sobre", "un"), ("Navegador web", "sin"), ("Necesidad de", "instalación"), ("Se adaptan", "a"), ("Cualquier dispositivo", "son"), ("Multiplataforma", "por"), ("Definición", "utilizan"), ("Tecnologías estándar", "HTML5"), ("CSS3", "y"), ("JavaScript", "pueden"), ("Ser PWAs", "para"), ("Funcionar offline", "y"), ("Enviar notificaciones", "pero"), ("Tienen acceso", "limitado"), ("Al hardware", None)
                            ],
                            [
                                (None, "Híbridas"), ("Combinan nativo", "y"), ("Web", "usando"),
                                {
                                    "texto": "Frameworks Híbridos",
                                    "conector": "populares",
                                    "bifurcaciones": [
                                        [
                                            (None, "Framework"), ("React Native", "creado"), ("Por Facebook", "usa"), ("JavaScript", "y"), ("React", "para"), ("Controlar componentes", "nativos"), ("Traduce la", "lógica"), ("A través", "de"), ("Un puente", "asíncrono"), ("Logrando", "buen"), ("Rendimiento", "y"), ("Apariencia nativa", None)
                                        ],
                                        [
                                            (None, "Framework"), ("Flutter", "desarrollado"), ("Por Google", "usa"), ("El lenguaje", "Dart"), ("No usa", "componentes"), ("Nativos", "sino"), ("Que renderiza", "su"), ("Propia interfaz", "con"), ("El motor", "Skia"), ("Logrando control", "total"), ("Del pixel", "y"), ("Alto rendimiento", "en"), ("Multiplataforma", None)
                                        ],
                                        [
                                            (None, "Framework"), ("Ionic", "usa"), ("Tecnologías web", "HTML"), ("CSS", "y"), ("JavaScript", "para"), ("Construir la", "UI"), ("La envuelve", "en"), ("Un contenedor", "nativo"), ("Mediante Capacitor", "o"), ("Cordova", "para"), ("Acceder", "al"), ("Hardware", "del"), ("Dispositivo", None)
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
                        (None, "Ciclo Vida"), ("Inicia con", "fase"), ("De idea", "y"), ("Planificación", "luego"), ("Diseño UX/UI", "y"), ("Codificación", "usando"),
                        {
                            "texto": "Metodologías",
                            "conector": "desarrollo",
                            "bifurcaciones": [
                                [
                                    (None, "Modelo"), ("Cascada", "es"), ("Un enfoque", "secuencial"), ("Y lineal", "donde"), ("Cada fase", "debe"), ("Completarse", "antes"), ("De iniciar", "la"), ("Siguiente", "es"), ("Poco flexible", "a"), ("Cambios", "pero"), ("Fácil", "de"), ("Gestionar", "y"), ("Planificar", None)
                                ],
                                [
                                    (None, "Modelo"), ("Ágil", "se"), ("Basa en", "ciclos"), ("Cortos e", "iterativos"), ("Llamados sprints", "fomenta"), ("La colaboración", "constante"), ("Con el", "cliente"), ("Y la", "adaptación"), ("A cambios", "durante"), ("El proceso", "prioriza"), ("Entregar valor", "rápido"), ("Y de", "forma"), ("Continua", None)
                                ],
                                [
                                    (None, "Modelo"), ("DevOps", "es"), ("Una cultura", "que"), ("Une desarrollo", "Dev"), ("Y operaciones", "Ops"), ("Busca automatizar", "y"), ("Monitorear", "todo"), ("El ciclo", "de"), ("Vida del", "software"), ("Desde la", "integración"), ("Hasta la", "entrega"), ("Y el", "despliegue"), ("Continuo", None)
                                ]
                            ]
                        }
                    ]
                ],
            },
            {
                "titulo": "1.3. Ventajas y Desventajas",
                "conector": "Impacto tecnológico",
                "ramas": [
                    [
                        (None, "Ventajas"), ("Ubicuidad", "permite"), ("Acceso constante", "generando"),
                        {
                            "texto": "Impacto Positivo",
                            "conector": "en áreas",
                            "bifurcaciones": [
                                [
                                    (None, "Sector"), ("Educación", "facilita"), ("El aprendizaje", "móvil"), ("M-learning", "con"), ("Acceso a", "plataformas"), ("Como Coursera", "o"), ("Khan Academy", "permite"), ("Consultar material", "y"), ("Realizar evaluaciones", "desde"), ("Cualquier lugar", "rompiendo"), ("Barreras", "de"), ("Tiempo", "y"), ("Espacio", None)
                                ],
                                [
                                    (None, "Sector"), ("Salud", "impulsa"), ("La m-Health", "o"), ("Salud móvil", "con"), ("Apps que", "monitorean"), ("Signos vitales", "o"), ("Niveles glucosa", "facilita"), ("La telemedicina", "consultas"), ("A distancia", "y"), ("El seguimiento", "de"), ("Pacientes crónicos", "mejorando"), ("La adherencia", "a"), ("Tratamientos", None)
                                ],
                                [
                                    (None, "Sector"), ("Comercio", "transformado"), ("Por el", "m-commerce"), ("Permite comprar", "y"), ("Vender productos", "o"), ("Servicios", "desde"), ("El móvil", "facilitando"), ("Pagos digitales", "con"), ("NFC", "o"), ("Códigos QR", "las"), ("Apps de", "delivery"), ("Como Uber", "Eats"), ("Son un", "claro"), ("Ejemplo", None)
                                ]
                            ]
                        }
                    ],
                    [
                        (None, "Desventajas"), ("Existen riesgos", "de"), ("Privacidad", "y"), ("Seguridad", "por"),
                        {
                            "texto": "Amenazas Comunes",
                            "conector": "seguridad",
                            "bifurcaciones": [
                                [
                                    (None, "Ataque"), ("Phishing", "busca"), ("Engañar al", "usuario"), ("Mediante correos", "o"), ("Mensajes falsos", "que"), ("Suplantan", "la"), ("Identidad de", "entidades"), ("Legítimas", "para"), ("Robar credenciales", "o"), ("Datos bancarios", "es"), ("Una amenaza", "muy"), ("Frecuente", None)
                                ],
                                [
                                    (None, "Ataque"), ("Malware", "es"), ("Software malicioso", "que"), ("Se instala", "sin"), ("Consentimiento", "puede"), ("Robar información", "mostrar"), ("Publicidad", "o"), ("Secuestrar", "el"), ("Dispositivo", "ransomware"), ("Se propaga", "a"), ("Través de", "apps"), ("No oficiales", "o"), ("Descargas ", None)
                                ],
                                [
                                    (None, "Ataque"), ("Smishing", "es"), ("Una variante", "de"), ("Phishing", "que"), ("Utiliza SMS", "o"), ("Mensajería instantánea", "como"), ("Vector de", "ataque"), ("Los mensajes", "suelen"), ("Incluir", "un"), ("Enlace malicioso", "que"), ("Invita a", "descargar"), ("Malware", "o"), ("Introducir", "datos"), ("Sensibles", None)
                                ]
                            ]
                        }
                    ],
                    [
                        (None, "Beneficios"), ("Acceso inmediato", "a"), ("Volúmenes masivos", "de"), ("Información", "lo"), ("Que democratiza", "el"), ("Conocimiento", "y"), ("Facilita", "la"), ("Toma de", "decisiones"), ("Informadas", "permite"), ("Comparar precios", "al"), ("Instante", "o"), ("Aprender algo", "nuevo"), ("En cualquier", "momento"), ("Y lugar", "potenciando"), ("Autodidactismo", None)
                    ],
                    [
                        (None, "Riesgos"), ("Distracciones constantes", "a"), ("Través de", "notificaciones"), ("Redes sociales", "y"), ("Juegos", "lo"), ("Que puede", "afectar"), ("La concentración", "y"), ("El rendimiento", "laboral"), ("O académico", "puede"), ("Generar dependencia", "o"), ("Adicción", "con"), ("Efectos negativos", "en"), ("Salud mental", "y"), ("Relaciones interpersonales", "cara"), ("A cara", None)
                    ],
                    [
                        (None, "Impacto Social"), ("Transforma", "la"), ("Interacción humana", "facilitando"), ("Comunicación", "a"), ("Larga distancia", "pero"), ("Pudiendo mermar", "el"), ("Contacto físico", "ha"), ("Impulsado", "nuevos"), ("Movimientos sociales", "y"), ("Formas de", "activismo"), ("También ha", "creado"), ("Nuevas economías", "como"), ("La Gig Economy", "con"), ("Sus propias", "controversias"), ("Laborales", None)
                    ]
                ],
            },
            {
                "titulo": "1.4. Tecnologías Inalámbricas",
                "conector": "Redes sin cables",
                "ramas": [
                    [
                        (None, "Corto alcance"), ("WPAN", "red"), ("Personal", "usa"), ("Bluetooth", "para"), ("Periféricos", "y"), ("NFC", "para"), ("Pagos sin", "contacto"), ("Zigbee", "automatiza"), ("Iluminación", "del hogar"), ("Infrarrojo", "controla"), ("Televisores", "y"), ("BLE beacons", "emiten"), ("Microlocalización", "en"), ("Tiendas", "y"), ("Museos", None),
                        {
                            "texto": "Bluetooth Evolución",
                            "conector": "versiones",
                            "bifurcaciones": [
                                [
                                    (None, "BLE"), ("Diseñado", "para"), ("Bajo consumo", "ideal"), ("Sensores IoT", "y"), ("Beacons", "que"), ("Operan con", "batería más"), ("Duradera", "usa"), ("Publicidad", "para"), ("Broadcast liviano", "soporta"), ("Perfiles GATT", "que"), ("Estandarizan", "servicios"), ("Como salud", "fitness", None)
                                ],
                                [
                                    (None, "5.2/5.3"), ("Introduce LE Audio", "para"), ("Audio compartido", "y"), ("Multipunto", "mejora"), ("Latencia", "y"), ("Seguridad", "en"), ("Emparejamientos", "añade"), ("Isochronous Channels", "para"), ("Sincronizar audio", "multi-device"), ("Optimize", "consumo"), ("En audífonos", None)
                                ],
                                [
                                    (None, "BLE Mesh"), ("Crea topologías", "malladas"), ("Amplía cobertura", "sin"), ("Consumir mucha", "energía"), ("Útil en", "domótica"), ("Y sensores", "industriales"), ("Permite", "mensajería"), ("Store-and-forward", "y"), ("Escalabilidad", "a"), ("Miles de nodos", "manteniendo"), ("Bajo costo", None)
                                ],
                                [
                                    (None, "Thread"), ("Protocolo IP", "para"), ("Hogar inteligente", "con"), ("Bajo consumo", "y"), ("Latencia reducida", "permite"), ("Automatizaciones", "fiables"), ("Integra Matter", "para"), ("Interoperabilidad", "usa"), ("Border Routers", "que"), ("Conectan", "a Internet"), ("Aislando", "la red", None)
                                ]
                            ]
                        }
                    ],
                    [
                        (None, "Largo alcance"), ("WLAN", "red"), ("Local", "Wi-Fi"), ("Alta velocidad", "y"), ("WWAN", "celular"), ("GSM/LTE", "masivo"), ("5G SA", "despliegue"), ("Backhaul", "para"), ("IoT masivo", "en"), ("Ciudades", "y"), ("WMAN", "WiMAX"), ("Cobertura", "metropolitana"), ("Satcom GEO", "sigue"), ("Conectando", "zonas remotas"),
                        {
                            "texto": "Estándares y tendencias",
                            "conector": "rendimiento",
                            "bifurcaciones": [
                                [
                                    (None, "Wi-Fi 6/6E"), ("Usa OFDMA", "y"), ("MU-MIMO", "para"), ("Más capacidad", "opera"), ("En 6 GHz", "con"), ("Menos interferencia", "añade"), ("TWT", "para"), ("Ahorrar batería", "en"), ("Dispositivos IoT", "mejora"), ("Eficiencia espectral", None)
                                ],
                                [
                                    (None, "Wi-Fi 7"), ("Aún mayor", "ancho"), ("De canal", "320 MHz"), ("Permite latencia", "ultra baja"), ("Velocidades multi-gigabit", "incluye"), ("MLO", "para"), ("Multi-link", "y"), ("Coordinación", "multi-AP"), ("Reduce interferencia", "y"), ("Mejora roaming", None)
                                ],
                                [
                                    (None, "5G"), ("Bandas Sub6", "y"), ("mmWave", "logran"), ("Gigabit", "baja"), ("Latencia", "habilita"), ("Vehículos conectados", "y"), ("Realidad aumentada", "apoya"), ("Network Slicing", "para"), ("SLAs", "dedicados"), ("y URLLC", "industrial", None)
                                ],
                                [
                                    (None, "IoT masivo"), ("NB-IoT", "y"), ("LTE-M", "para"), ("Dispositivos", "de"), ("Bajo consumo", "y"), ("Cobertura amplia", "en"), ("Ciudades inteligentes", "permiten"), ("Sensores", "de bajo"), ("Costo", "con"), ("Larga batería", "y"), ("Cobertura indoor", None)
                                ],
                                [
                                    (None, "Roaming"), ("Asegura conectividad", "en"), ("Viajes", "requiere"), ("Acuerdos entre", "operadores"), ("Y autenticación", "segura"), ("Para itinerancia", "usa"), ("eSIM/GSMA", "para"), ("Provisionar perfiles", "remotos"), ("y evitar", "cambios SIM", None)
                                ],
                                [
                                    (None, "Hotspots públicos"), ("Usan portales", "cautivos"), ("Con políticas", "de uso"), ("Filtrado de", "contenidos"), ("Y ancho de banda", "limitado"), ("Captive bypass", "requiere"), ("MAC random", "y"), ("Compatibilidad", "con WPA3", "transition", None)
                                ],
                                [
                                    (None, "Satcom LEO"), ("Órbitas bajas", "ofrecen"), ("Cobertura remota", "para"), ("Zonas rurales", "y"), ("Enlaces", "de respaldo"), ("Baja latencia", "comparada"), ("Con GEO", "viabiliza"), ("Backhaul 5G", "en"), ("Emergencias", None)
                                ]
                            ]
                        }
                    ],
                    [
                        (None, "Seguridad"), ("Cifrado WPA3", "reemplaza"), ("WPA2", "mitigando"), ("Ataques diccionario", "y"), ("Filtrado MAC", "no"), ("Es suficiente", "requiere"), ("Autenticación fuerte", "y"), ("Monitoreo", "constante"), ("Segmentación", "por"), ("VLAN/SSID", "para"), ("Aislar IoT", "del"), ("Tráfico crítico", None),
                        {
                            "texto": "Protecciones",
                            "conector": "buenas prácticas",
                            "bifurcaciones": [
                                [
                                    (None, "OWE"), ("Protege redes", "abiertas"), ("Autenticación", "sin contraseña"), ("Mitiga escuchas", "en"), ("Entornos públicos", "requiere"), ("Clientes compatibles", "para"), ("Evitar downgrade", None)
                                ],
                                [
                                    (None, "Rotación claves"), ("Uso de SAE", "evita"), ("Reutilización", "de contraseñas"), ("Recomendado", "en empresas"), ("Revoca credenciales", "cuando"), ("Hay bajas", "de"), ("Personal", None)
                                ],
                                [
                                    (None, "WIPS"), ("Detecta rogues", "y"), ("Ataques de", "desautenticación"), ("Genera alertas", "para"), ("Respuesta rápida", "incluye"), ("WIDS", "para"), ("Monitoreo pasivo", None)
                                ],
                                [
                                    (None, "802.1X"), ("EAP-TLS", "para"), ("Autenticación fuerte", "con"), ("Certificados", "y"), ("Trazabilidad", "de usuarios"), ("Permite VLAN", "dinámicas"), ("Y control", "por rol", None)
                                ],
                                [
                                    (None, "Segmentación"), ("Separar IoT", "de"), ("Red corporativa", "reduce"), ("Superficie de ataque", "y"), ("Limita movimientos", "implementa"), ("Firewalls internos", "y"), ("ACLs", "para"), ("Tráfico mínimo", None)
                                ]
                            ]
                        }
                    ]
                ],
            },
            {
                "titulo": "1.5. Streaming Móvil",
                "conector": "Transmisión continua",
                "ramas": [
                    [
                        (None, "Funcionamiento"), ("Descarga progresiva", "en"), ("Buffer", "reproduce"), ("Mientras baja", "sin"), ("Guardar archivo", "depende"), ("De red", "estable"), ("Codificación", "con"), ("Codecs eficientes", "reduce"), ("Bitrate", "adaptado"), ("Al dispositivo", "y"), ("Condiciones", "de red"),
                        {
                            "texto": "Componentes streaming",
                            "conector": "claves",
                            "bifurcaciones": [
                                [
                                    (None, "Modalidades"), ("Bajo demanda", "VOD"), ("Netflix/YouTube", "elige"), ("Qué ver", "y"), ("Cuándo", "usa"), ("Catálogo amplio", "con"), ("Licencias", "y"), ("CDN globales", "para"), ("Entrega confiable", None)
                                ],
                                [
                                    (None, "Modalidades"), ("En vivo", "Live"), ("Twitch/TV", "tiempo"), ("Real", "y"), ("Eventos", "usa"), ("Ingest", "a"), ("CDN", "con"), ("RTMP/SRT", "y"), ("Segmentación LL", "para"), ("Latencia baja", None)
                                ],
                                [
                                    (None, "Protocolos"), ("HLS/DASH", "segmentan"), ("Video", "en"), ("Pequeños chunks", "permiten"), ("ABR", "que adapta"), ("Calidad a", "ancho de banda"), ("Del usuario", "soportan"), ("CMAF", "para"), ("Low Latency", "y"), ("Segmentos parciales", None)
                                ],
                                [
                                    (None, "Codecs"), ("H.264/AVC", "compatibilidad"), ("Universal", "mientras"), ("H.265/HEVC", "y"), ("AV1", "reducen"), ("Bitrate", "manteniendo"), ("Calidad", "códecs AV1"), ("Son eficientes", "pero"), ("Requieren soporte", "en"), ("Hardware nuevo", None)
                                ],
                                [
                                    (None, "Infraestructura"), ("CDN", "replica"), ("Contenido cerca", "disminuye"), ("Latencia", "y"), ("Picos", "de"), ("Carga en origen", "usa"), ("Edge caching", "y"), ("TLS", "para"), ("Seguridad", None)
                                ],
                                [
                                    (None, "DRM"), ("Widevine/FairPlay", "protegen"), ("Licencias", "evitan"), ("Piratería", "y"), ("Controlan", "descargas offline"), ("Aplican", "políticas"), ("De expiración", "y"), ("Límites de", "dispositivos", None)
                                ],
                                [
                                    (None, "Control congestión"), ("Algoritmos ABR", "evitan"), ("Saturación", "monitorea"), ("RTT y pérdida", "para"), ("Ajustar bitrate", "reduce"), ("Latencia", "con"), ("Segmentos cortos", "mejora"), ("Start-up time", "y"), ("QoE", "percibida"), ("Mitiga bufferbloat", "y"), ("Congestión celular", None)
                                ]
                            ]
                        }
                    ],
                    [
                        (None, "Calidad de experiencia"), ("Algoritmos ABR", "evitan"), ("Rebuffering", "seleccionando"), ("Bitrate correcto", "considera"), ("CPU/GPU", "del"), ("Móvil", "y"), ("Estado red", "dinámico"), ("Start-up time", "impacta"), ("Retención", "mide"), ("Errores de", "playback"), ("QoE", "se mejora"), ("Con subtítulos", "y"), ("Audio adaptable", "para"), ("Usuarios", "conectividad variable"),
                        {
                            "texto": "Optimiza datos",
                            "conector": "en movilidad",
                            "bifurcaciones": [
                                [
                                    (None, "Prefetch"), ("Descarga previa", "en"), ("Wi-Fi", "para"), ("Reducir consumo", "celular"), ("Cortes", "y"), ("Descarga parcial", "para"), ("Transiciones", "entre"), ("Redes", None)
                                ],
                                [
                                    (None, "Low Latency"), ("HLS LL", "y"), ("CMAF", "reducen"), ("Retraso", "para"), ("Eventos interactivos", "como"), ("Apuestas o live shopping", None)
                                ],
                                [
                                    (None, "KPIs"), ("Métricas MOS", "y"), ("Play Delay", "miden"), ("Vistas retenidas", "y"), ("Tasa abandono", "para"), ("Ajustar CDN", "y"), ("Planificar horas", "pico"), ("Se vigila", "rebuffering"), ("Errores HTTP", "y"), ("TTFF", "para"), ("Alertar fallas", None)
                                ],
                                [
                                    (None, "Ahorro datos"), ("Detección Wi-Fi", "activa"), ("Prefetch inteligente", "reduce"), ("Consumo de", "datos móviles"), ("Prepara segmentos", "cuando"), ("Hay red", "disponible"), ("Descarga resoluciones", "bajas"), ("Si el plan", "es"), ("Limitado", None)
                                ]
                            ]
                        }
                    ]
                ],
            },
            {
                "titulo": "1.6. Sistema Operativo",
                "conector": "Gestor recursos",
                "ramas": [
                    [
                        (None, "Funciones"), ("Interfaz usuario", "GUI"), ("Táctil", "gestiona"), ("Memoria y CPU", "y"), ("Batería", "optimiza"), ("Multitarea", "con"), ("Gestor procesos", "y"), ("Colas de", "sistema"), ("Drivers", "para"), ("Sensores", "coordinan"),
                        {
                            "texto": "Plataformas y arquitectura",
                            "conector": "capas y mercado",
                            "bifurcaciones": [
                                [
                                    (None, "Android"), ("Google", "basado"), ("En Linux", "código"), ("Abierto", "y"), ("Mayoría", "usa"), ("Servicios Google", "o"), ("AOSP forks", "para"), ("Mercados", "regionales"), ("Con Play", "Protect", None)
                                ],
                                [
                                    (None, "iOS"), ("Apple", "basado"), ("En Unix", "código"), ("Cerrado", "y"), ("Exclusivo", "integra"), ("Metal", "para"), ("Gráficos", "y"), ("Neural Engine", "para"), ("ML en dispositivo", None)
                                ],
                                [
                                    (None, "HarmonyOS"), ("Huawei", "alternativa"), ("Enfocada", "a"), ("IoT", "usa"), ("Microkernel", "y"), ("Distribución", "de servicios"), ("Entre dispositivos", None)
                                ],
                                [
                                    (None, "Kernel"), ("Planifica procesos", "gestiona"), ("Drivers", "para"), ("CPU y GPU", "y"), ("Sensores", "implementa"), ("Mecanismos IPC", "maneja"), ("Memoria virtual", "y"), ("Seguridad", "LSM/SE", None)
                                ],
                                [
                                    (None, "Frameworks"), ("APIs UI", "como"), ("UIKit/Jetpack", "y"), ("Servicios", "de"), ("Notificaciones", "ubicación"), ("Telephony", "componen"), ("Experiencia", "incluye"), ("APIs ML", "y"), ("Health/Payments", "para"), ("Ecosistema", None)
                                ],
                                [
                                    (None, "Gestión energía"), ("Doze/App Nap", "extiende"), ("Autonomía", "con"), ("Planificadores", "que"), ("Priorizan UX", "según"), ("Uso y contexto", "limitan"), ("WakeLocks", "y"), ("Jobs en", "segundo plano", None)
                                ]
                            ]
                        }
                    ],
                    [
                        (None, "Seguridad"), ("Sandboxing", "aísla"), ("Apps", "usa"), ("Permisos granulares", "para"), ("GPS/cámara", "y"), ("Micro", "controla"), ("Accesos a", "archivos"), ("Políticas", "de"), ("Play Store", "o"), ("App Store", "revisan"), ("Runtime", "pide"), ("Consentimiento", "al usuario"),
                        {
                            "texto": "Actualizaciones",
                            "conector": "entrega",
                            "bifurcaciones": [
                                [
                                    (None, "OTA"), ("Parches mensuales", "corrigen"), ("Vulnerabilidades", "y"), ("Añaden", "funciones"), ("Sin", "perder datos")
                                ],
                                [
                                    (None, "Fragmentación"), ("Android", "depende"), ("Del fabricante", "para"), ("Liberar updates", "mientras"), ("iOS", "controla"), ("Desde Apple", "logrando"), ("Adopción rápida", None)
                                ],
                                [
                                    (None, "Protección núcleo"), ("Code signing", "y"), ("Verificación boot", "evita"), ("Malware", "aplica"), ("SELinux/App Sandbox", "para"), ("Políticas", "y"), ("Encriptación disco", "protege"), ("Datos en reposo", "con"), ("Enclave seguro", "para"), ("Llaves y biometría", "implementa"), ("ASLR", "y"), ("Protección", "de memoria", None)
                                ]
                            ]
                        }
                    ]
                ],
            },
            {
                "titulo": "1.7. Desarrollo Móvil",
                "conector": "Herramientas creación",
                "ramas": [
                    [
                        (None, "Entornos (IDE)"), ("Android Studio", "oficial"), ("Google", "y"), ("Xcode", "oficial"), ("Apple", "y"), ("VS Code", "ligero"), ("Extensiones", "para"), ("Depurar", "y"), ("Emuladores", "multidispositivo"),
                        {
                            "texto": "Herramientas apoyo",
                            "conector": "productividad",
                            "bifurcaciones": [
                                [
                                    (None, "Control versiones"), ("Git", "con"), ("Workflows", "GitFlow"), ("Pull Requests", "y"), ("CI", "para"), ("Revisar código", None)
                                ],
                                [
                                    (None, "Prototipado"), ("Figma", "o"), ("Sketch", "permiten"), ("Diseñar", "interfaces"), ("Y handoff", "a"), ("Desarrollo", None)
                                ],
                                [
                                    (None, "Perf tools"), ("Profiler/Layout", "Inspector"), ("Optimiza UI", "y"), ("Systrace/Instruments", "miden"), ("Rendimiento", "en"), ("CPU/GPU", None)
                                ]
                            ]
                        }
                    ],
                    [
                        (None, "Lenguajes"), ("Java/Kotlin", "nativos"), ("Android", "y"), ("Swift/Obj-C", "nativos"), ("iOS", "y"), ("JavaScript", "para"), ("Apps híbridas", "Dart"), ("Para Flutter", "y"), ("C#", "para"), ("Xamarin/Unity", "además"),
                        {
                            "texto": "Buenas prácticas",
                            "conector": "código limpio",
                            "bifurcaciones": [
                                [
                                    (None, "Arquitecturas"), ("MVC", "MVVM"), ("MVI", "para"), ("Separar UI", "de"), ("Lógica negocio", "y"), ("Facilitar pruebas", "usa"), ("Capas dominio", "datos"), ("Presentación", "con"), ("Repositorios", "y"), ("Use Cases", None)
                                ],
                                [
                                    (None, "Dependencias"), ("Inyección", "con"), ("Hilt/Dagger", "o"), ("Koin", "evita"), ("Acoplamiento", "y"), ("Mejora escalabilidad", "usa"), ("Scopes", "para"), ("Ciclos de", "vida"), ("Reduce boilerplate", "y"), ("Facilita testing", None)
                                ],
                                [
                                    (None, "Stack ampliado"), ("JavaScript", "para"), ("Híbridos", "y"), ("Dart", "para"), ("Flutter", "C# para"), ("Xamarin/Unity", "Python/Kivy"), ("SQL/Room", "para"), ("Persistencia local", "GraphQL"), ("Para APIs", "y"), ("KMP/Swift", "para"), ("Compartir lógica", None)
                                ],
                                [
                                    (None, "Módulos nativos"), ("Rust con", "UniFFI"), ("Para seguridad", "y"), ("Rendimiento", "integrado"), ("C/C++", "para"), ("Bindings", "de"), ("Bajo nivel", "cuando"), ("Se necesitan", "drivers"), ("O codecs", None)
                                ]
                            ]
                        }
                    ],
                    [
                        (None, "Frameworks"), ("React Native", "usa"), ("Componentes nativos", "con"), ("Lógica JS", "y"), ("Flutter", "renderiza"), ("Skia", "para"), ("Pixel perfect", "Ionic"), ("Envuelve web", "para"), ("Mobile", "rápido"),
                        {
                            "texto": "Ciclo de entrega",
                            "conector": "DevOps móvil",
                            "bifurcaciones": [
                                [
                                    (None, "CI/CD"), ("Github Actions", "o"), ("Bitrise", "automatizan"), ("Builds y tests", "y"), ("Firmado", "de"), ("Apps", None)
                                ],
                                [
                                    (None, "Distribución"), ("TestFlight", "Play Console"), ("Rollout gradual", "monitorea"), ("Crashes", "con"), ("Firebase Crashlytics", "y"), ("Observabilidad", "con"), ("Analytics", None)
                                ],
                                [
                                    (None, "Alternativas"), ("Flutter", "renderiza"), ("Skia", "para"), ("Pixel perfect", "Ionic"), ("Usa HTML/CSS", "NativeScript"), ("Angular/Vue", "Qt/QML"), ("Apunta industria", None)
                                ]
                            ]
                        }
                    ],
                    [
                        (None, "Pruebas"), ("Unitarias", "validan"), ("Lógica", "instrumentadas"), ("Verifican UI", "con"), ("Espresso", "y"), ("XCUITest", "cubren"), ("UI nativa", "tests"), ("De snapshot", "ayudan"),
                        {
                            "texto": "Calidad continua",
                            "conector": "métricas",
                            "bifurcaciones": [
                                [
                                    (None, "Performance"), ("Perfetto", "Systrace"), ("y Xcode Instruments", "miden"), ("CPU y memoria", "y"), ("Jank", "para"), ("Optimizar UX", None)
                                ],
                                [
                                    (None, "Accesibilidad"), ("VoiceOver/TalkBack", "pruebas"), ("Contrast Checker", "y"), ("Etiquetas ARIA", "cumplen"), ("Buenas prácticas", None)
                                ],
                                [
                                    (None, "Cobertura"), ("Smoke tests", "garantizan"), ("Builds sanos", "mocking"), ("Aísla dependencias", "y"), ("Pruebas carga", "miden"), ("Backend móvil", "para"), ("Escalabilidad", None)
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
    "OUTPUT_FILE": os.path.join("Mapas", "Mapa_conceptual_U1_IA_OSCAR.drawio"),
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
