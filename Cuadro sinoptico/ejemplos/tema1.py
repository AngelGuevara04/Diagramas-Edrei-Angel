{
    "Unidad 2. Framework multiplataforma:\nFlutter": {
        "2.1. Descripción, características,\nventajas y desventajas": {
            "Descripción y fundamentos": {
                "Flutter es un SDK de Google para crear aplicaciones desde una sola base de código.": {
                    "Puede compilar interfaces para Android, iOS, web, Windows, macOS y Linux desde el mismo proyecto.": {
                        "Su enfoque declarativo organiza la interfaz en widgets reutilizables, facilitando mantenimiento, consistencia visual y evolución del producto.": [
                            "El framework separa claramente presentación, estado y navegación, lo que ayuda a estructurar proyectos medianos y grandes."
                        ]
                    }
                },
                "Dart es el lenguaje principal de Flutter y fue diseñado para productividad y rendimiento predecible.": {
                    "Incluye compilación JIT para desarrollo rápido y compilación AOT para distribuir aplicaciones optimizadas en producción.": {
                        "Sound Null Safety reduce errores por referencias nulas y hace más explícitas las intenciones del programador.": [
                            "La sintaxis de Dart resulta familiar para quienes ya conocen Java, JavaScript, C# o lenguajes orientados a objetos."
                        ]
                    }
                },
                "Flutter también destaca por su enfoque declarativo, donde la interfaz se describe como resultado del estado actual.": {
                    "Este modelo facilita razonar sobre cambios visuales, porque cada reconstrucción expresa claramente lo que debe verse.": [
                        "Cuando el estado se organiza bien, el código suele ser más predecible, mantenible y sencillo de probar."
                    ]
                },
                "La autenticación no sustituye reglas del backend; ambas capas deben trabajar juntas para proteger información.": [
                    "Confiar solo en la interfaz del cliente es un error común y técnicamente peligroso."
                ]
            },
            "Características clave": {
                "Hot Reload aplica cambios de código casi inmediatamente sin reiniciar por completo la aplicación en ejecución.": {
                    "Esto acelera pruebas visuales, correcciones menores y ajustes de diseño durante sesiones normales de desarrollo.": [
                        "No reemplaza una compilación completa, pero sí reduce tiempos muertos cuando se modifican widgets, estilos o textos."
                    ]
                },
                "Flutter renderiza la interfaz con su propio motor gráfico en lugar de depender de widgets nativos.": {
                    "Ese control directo favorece una apariencia uniforme entre dispositivos, densidades de pantalla y versiones del sistema operativo.": {
                        "La composición por widgets permite personalizar desde botones sencillos hasta interfaces complejas con animaciones fluidas.": [
                            "En plataformas modernas, Flutter también impulsa mejoras de rendimiento mediante el renderizador Impeller en contextos compatibles."
                        ]
                    }
                },
                "El ecosistema oficial incluye DevTools para inspección, depuración, análisis de memoria y rendimiento.": {
                    "Estas herramientas ayudan a detectar reconstrucciones innecesarias, cuellos de botella y problemas de consumo de recursos.": [
                        "Usarlas desde etapas tempranas mejora la calidad técnica y reduce problemas difíciles de rastrear en producción."
                    ]
                },
                "Flutter ofrece un sistema de animaciones amplio que permite crear transiciones suaves y experiencias interactivas elaboradas.": {
                    "Las animaciones implícitas simplifican tareas comunes, mientras las explícitas ofrecen mayor control temporal y visual.": [
                        "Esto resulta útil en interfaces modernas donde movimiento y jerarquía visual comunican estado y prioridad."
                    ]
                },
                "Firestore cobra según operaciones y almacenamiento, por lo que el modelo de datos debe planearse cuidadosamente.": [
                    "Un mal diseño puede escalar costos y degradar rendimiento cuando la cantidad de usuarios aumenta."
                ]
            },
            "Arquitectura interna": {
                "La arquitectura de Flutter suele dividirse en framework, motor gráfico y adaptadores de plataforma.": {
                    "El framework incluye widgets, gestos, layout y animaciones escritos principalmente en lenguaje Dart.": {
                        "El motor se encarga de renderizado, texto, composición y comunicación con recursos gráficos subyacentes.": [
                            "Los adaptadores conectan Flutter con ventanas, entrada táctil y servicios del sistema operativo correspondiente."
                        ]
                    }
                },
                "Comprender la diferencia entre widgets, elements y render objects ayuda a entender rendimiento y reconstrucciones.": {
                    "Los widgets describen configuración, los elements administran montaje y los render objects realizan layout y dibujo.": [
                        "Este modelo explica por qué Flutter puede actualizar secciones específicas sin redibujar todo innecesariamente."
                    ]
                }
            },
            "Ventajas principales": {
                "Una sola base de código reduce duplicación de lógica y simplifica mantenimiento entre varias plataformas objetivo.": {
                    "Los equipos pueden compartir validaciones, navegación, modelos de datos y parte importante de las pruebas automatizadas.": [
                        "Eso acorta tiempos de entrega y facilita liberar versiones con funciones equivalentes en distintos sistemas."
                    ]
                },
                "La biblioteca de widgets es amplia y permite construir interfaces consistentes sin depender de demasiados componentes externos.": {
                    "Material y Cupertino cubren patrones comunes de Android e iOS con comportamiento visual ya preparado.": {
                        "Además, pub.dev ofrece paquetes para mapas, autenticación, almacenamiento local, gráficos y acceso a servicios externos.": [
                            "La documentación oficial incluye ejemplos, recetas y guías arquitectónicas que reducen la curva de adopción inicial."
                        ]
                    }
                },
                "Flutter facilita crear interfaces altamente personalizadas cuando una identidad visual diferenciada es prioridad del proyecto.": {
                    "Ese nivel de control es útil en productos educativos, comerciales o corporativos con requisitos gráficos específicos.": [
                        "También favorece experiencias consistentes cuando la marca necesita verse prácticamente igual en varias plataformas."
                    ]
                },
                "La experiencia de desarrollo es especialmente fuerte en prototipado rápido, validación temprana y productos iterativos.": {
                    "Esto permite mostrar avances funcionales pronto y ajustar detalles conforme aparecen necesidades reales del proyecto.": [
                        "Esa velocidad beneficia tanto a equipos pequeños como a contextos académicos y demostraciones técnicas."
                    ]
                }
            },
            "Desventajas y limitaciones": {
                "El tamaño inicial de algunas aplicaciones puede ser mayor que alternativas nativas extremadamente simples.": {
                    "Esto ocurre porque la distribución incluye componentes del framework y del motor necesarios para ejecutarse correctamente.": [
                        "En contextos con almacenamiento restringido o descargas muy limitadas, ese aspecto puede influir en decisiones técnicas."
                    ]
                },
                "Dart es accesible, pero su mercado laboral sigue siendo menor que el de JavaScript o Java.": {
                    "Algunas organizaciones necesitan capacitar internamente al equipo antes de adoptar Flutter en proyectos estratégicos.": {
                        "También conviene evaluar disponibilidad local de talento, soporte empresarial y experiencia previa en arquitectura reactiva.": [
                            "La gestión avanzada de estado, navegación y rendimiento requiere disciplina técnica para evitar aplicaciones difíciles de escalar."
                        ]
                    }
                },
                "Ciertas integraciones muy específicas dependen de plugins o de escribir código nativo adicional.": {
                    "Eso puede aumentar complejidad cuando se usan funciones poco comunes del dispositivo o SDK empresariales cerrados.": [
                        "Antes de adoptar Flutter, es prudente validar las dependencias críticas que el proyecto realmente necesita."
                    ]
                },
                "En la plataforma web, Flutter puede no ser la mejor elección si el proyecto depende mucho de SEO.": {
                    "Tampoco siempre es ideal cuando se requieren tiempos mínimos de carga o manipulación DOM muy especializada.": [
                        "La decisión técnica debe tomarse según objetivos concretos del producto y no solo por preferencia general."
                    ]
                },
                "En proyectos más grandes puede existir una carpeta integration_test para flujos completos de validación.": [
                    "Separar esas pruebas ayuda a distinguir comportamiento interno, interfaz y recorridos reales del usuario."
                ]
            },
            "Configuración de entornos": {
                "Es frecuente manejar variantes para desarrollo, pruebas y producción con servicios o credenciales distintas.": {
                    "Esto puede resolverse con archivos separados, variables de entorno o parámetros de compilación definidos.": [
                        "Separar entornos correctamente reduce errores costosos al desplegar y simplifica pruebas controladas."
                    ]
                }
            }
        },
        "2.2. Entorno de trabajo": {
            "Instalación y configuración del SDK": {
                "La instalación oficial comienza descargando Flutter SDK desde docs.flutter.dev según el sistema operativo utilizado.": {
                    "Después debe configurarse la variable PATH para ejecutar comandos como flutter, dart y flutter doctor.": {
                        "El comando flutter doctor resume dependencias faltantes, licencias pendientes y herramientas no configuradas correctamente.": [
                            "Revisarlo tras cada instalación importante evita errores de entorno antes de empezar a desarrollar."
                        ]
                    }
                },
                "Git es necesario porque Flutter usa repositorios versionados para actualizaciones y administración del SDK.": [
                    "El comando flutter upgrade permite obtener versiones estables recientes cuando el proyecto decide actualizarse."
                ],
                "También conviene aceptar licencias del SDK de Android y revisar avisos de flutter doctor periódicamente.": [
                    "Resolver esos pendientes desde el inicio evita errores de compilación que suelen aparecer más adelante."
                ]
            },
            "Entornos de desarrollo": {
                "Visual Studio Code es popular por su rapidez, extensiones oficiales y flujo simple para proyectos Flutter.": {
                    "Las extensiones de Flutter y Dart añaden autocompletado, depuración, snippets y ejecución directa desde el editor.": [
                        "Es una opción eficiente para equipos que prefieren herramientas ligeras y configuración rápida."
                    ]
                },
                "Android Studio integra emuladores, profiler, administración del SDK de Android y herramientas visuales robustas.": {
                    "Suele ser conveniente cuando el proyecto necesita diagnosticar rendimiento o revisar configuraciones nativas en detalle.": [
                        "Su asistente inicial también ayuda a instalar componentes obligatorios para compilar aplicaciones Android."
                    ]
                },
                "En sistemas Apple, Xcode es indispensable para firmar, compilar y probar aplicaciones dirigidas a iOS.": [
                    "Sin esa herramienta no puede completarse el flujo oficial de desarrollo ni publicación para dispositivos Apple."
                ]
            },
            "Dispositivos y emulación": {
                "Los emuladores permiten validar interfaz, navegación y compatibilidad básica sin requerir un teléfono físico siempre disponible.": {
                    "Sin embargo, consumen memoria, CPU y almacenamiento, por lo que exigen hardware razonablemente potente.": [
                        "Activar virtualización por hardware mejora notablemente fluidez, tiempos de arranque y experiencia de prueba."
                    ]
                },
                "Las pruebas en dispositivos reales siguen siendo necesarias para evaluar sensores, batería y rendimiento auténtico.": {
                    "En Android se habilita depuración USB; en iOS se requiere configuración adicional con Xcode y certificados.": [
                        "Probar en hardware real ayuda a detectar diferencias que un emulador no siempre reproduce fielmente."
                    ]
                },
                "Conviene probar en distintos tamaños de pantalla, versiones del sistema y gamas de hardware cuando sea posible.": [
                    "Eso mejora la detección de errores de compatibilidad que podrían afectar a usuarios finales."
                ]
            },
            "Herramientas de línea de comandos": {
                "La terminal permite crear proyectos, ejecutar pruebas, compilar versiones y administrar dependencias con precisión.": {
                    "Comandos como flutter create, flutter run, flutter test y flutter pub get forman parte del flujo diario.": [
                        "Dominar esta capa facilita automatización, integración continua y resolución más rápida de incidencias técnicas."
                    ]
                },
                "flutter analyze ayuda a detectar errores estáticos y malas prácticas antes de ejecutar la aplicación.": {
                    "Su uso continuo mejora calidad del código y complementa pruebas unitarias o revisiones manuales.": [
                        "Integrarlo en pipelines de integración continua reduce defectos triviales antes de publicar cambios."
                    ]
                }
            },
            "Dependencias y canales": {
                "Flutter ofrece canales como stable, beta y main, aunque la mayoría de proyectos productivos usa stable.": {
                    "Elegir un canal incorrecto puede introducir cambios experimentales o inestabilidad innecesaria en el equipo.": [
                        "Por ello suele ser importante fijar versión y documentar claramente el entorno esperado."
                    ]
                },
                "Las dependencias deben evaluarse con criterio, porque demasiados paquetes aumentan mantenimiento y riesgo técnico.": [
                    "Revisar soporte, actividad reciente y compatibilidad evita depender de bibliotecas abandonadas o inestables."
                ]
            }
        },
        "2.3. Estructura de un proyecto": {
            "Configuración y metadatos": {
                "El archivo pubspec.yaml define dependencias, versiones, recursos estáticos y metadatos básicos del proyecto Flutter.": {
                    "También registra imágenes, fuentes, paquetes internos y restricciones mínimas del SDK necesarias para compilar.": [
                        "Una configuración ordenada en pubspec evita errores de carga y facilita reproducir el entorno del proyecto."
                    ]
                },
                "La versión declarada del proyecto también influye en publicación, seguimiento de cambios y distribución oficial.": [
                    "Mantenerla correctamente ayuda a controlar lanzamientos y a cumplir requisitos de las tiendas."
                ]
            },
            "Directorios por plataforma": {
                "Las carpetas android, ios, web, windows, linux y macos contienen ajustes específicos de cada plataforma.": {
                    "Ahí se declaran permisos, íconos, identificadores de aplicación y configuraciones nativas indispensables para publicar.": [
                        "Cuando un plugin lo requiere, estos directorios también alojan código nativo complementario en Kotlin, Swift o C++."
                    ]
                }
            },
            "Código fuente en lib": {
                "La carpeta lib concentra la lógica principal escrita en Dart y la mayor parte de la interfaz.": {
                    "El archivo main.dart actúa como punto de entrada y normalmente inicializa widgets raíz, rutas y servicios.": [
                        "Separar pantallas, modelos, servicios y estado en subcarpetas mejora legibilidad, pruebas y crecimiento sostenible."
                    ]
                },
                "Muchos equipos organizan la carpeta lib por funcionalidades para acercar vistas, lógica y modelos relacionados.": {
                    "Ese enfoque reduce dispersión del código y facilita entender cada parte del sistema con más rapidez.": [
                        "La convención elegida debe mantenerse de forma constante para evitar crecimiento desordenado del proyecto."
                    ]
                }
            },
            "Pruebas y recursos adicionales": {
                "La carpeta test se utiliza para pruebas unitarias y de widgets que verifican comportamiento esperado.": [
                    "Automatizar estas comprobaciones ayuda a detectar regresiones antes de distribuir nuevas versiones a usuarios."
                ],
                "Los recursos como imágenes, tipografías y archivos JSON deben declararse manualmente en pubspec.yaml.": {
                    "Si un recurso no se registra correctamente, Flutter no lo empaqueta y la aplicación fallará al cargarlo.": [
                        "Mantener nombres consistentes y rutas claras simplifica trabajo colaborativo y mantenimiento posterior."
                    ]
                }
            }
        },
        "2.4. Controles y componentes": {
            "Widgets fundamentales": {
                "Los StatelessWidget representan partes de la interfaz que no dependen de cambios internos persistentes.": {
                    "Se usan para textos, íconos, contenedores decorativos o composiciones que solo reciben datos externos.": [
                        "Su simplicidad reduce complejidad conceptual y favorece interfaces más previsibles y fáciles de probar."
                    ]
                },
                "Los StatefulWidget manejan información cambiante durante la vida útil visible del componente en pantalla.": {
                    "Su objeto State conserva datos temporales como selección, progreso, validación o respuestas de interacción.": [
                        "Se utilizan en formularios, animaciones, listas dinámicas y vistas conectadas a eventos del usuario."
                    ]
                },
                "BuildContext es una referencia clave para acceder a navegación, tema y widgets ancestros.": [
                    "Comprender su alcance evita errores frecuentes relacionados con rutas o dependencias visuales."
                ]
            },
            "Widgets de estructura y layout": {
                "Row, Column, Stack, Expanded y Container forman parte del núcleo para organizar elementos visuales.": {
                    "Con ellos pueden construirse diseños adaptables combinando alineación, espaciado, flexibilidad y superposición controlada.": [
                        "Comprender bien estas piezas evita interfaces rígidas y mejora adaptación a pantallas distintas."
                    ]
                },
                "ListView y GridView permiten mostrar conjuntos extensos de información con desplazamiento eficiente.": [
                    "Son esenciales en catálogos, menús, historiales, galerías y pantallas que renderizan muchos elementos."
                ],
                "Padding, Align, SizedBox y SingleChildScrollView ayudan a controlar espaciado, posición y desbordamientos.": [
                    "Usarlos correctamente mejora legibilidad y hace más consistente la interfaz en diferentes pantallas."
                ]
            },
            "Bibliotecas de diseño visual": {
                "Material Design ofrece componentes alineados con las guías visuales promovidas por Google para aplicaciones modernas.": {
                    "Incluye barras de aplicación, botones, tarjetas, menús, diálogos y navegación lista para personalizar.": [
                        "Es especialmente útil cuando se busca coherencia con patrones familiares para usuarios de Android."
                    ]
                },
                "Cupertino proporciona widgets inspirados en el estilo visual y comportamiento de aplicaciones iOS.": [
                    "Esto ayuda a presentar una experiencia más natural para usuarios acostumbrados al ecosistema Apple."
                ],
                "ThemeData centraliza colores, tipografías y estilos para conservar una identidad visual uniforme.": [
                    "Definir un tema claro desde el inicio simplifica cambios globales y reduce inconsistencias."
                ]
            },
            "Interacción y entrada de datos": {
                "TextField, Form, Checkbox, Switch y botones capturan información y acciones del usuario de forma controlada.": {
                    "Flutter permite validar formularios, escuchar eventos y responder gestos mediante clases y widgets especializados.": [
                        "GestureDetector reconoce toques, arrastres y pulsaciones prolongadas sobre prácticamente cualquier componente visible."
                    ]
                },
                "Controladores como TextEditingController y FocusNode permiten manejar texto, foco y validaciones complejas.": [
                    "Son útiles cuando se necesita limpiar campos, reaccionar a cambios o mover el foco manualmente."
                ]
            },
            "Gestión de estado": {
                "Toda aplicación mediana necesita una estrategia para manejar estado local, compartido y asincronía correctamente.": {
                    "Flutter permite usar setState en casos simples o patrones más estructurados en aplicaciones grandes.": {
                        "Entre las opciones populares destacan Provider, Riverpod, Bloc, Cubit y ChangeNotifier según el contexto.": [
                            "La mejor alternativa depende del equipo, complejidad del dominio y experiencia técnica disponible."
                        ]
                    }
                },
                "Una mala gestión de estado puede dispersar la lógica y dificultar pruebas, mantenimiento y escalabilidad.": [
                    "Por eso conviene acordar convenciones tempranas y no mezclar patrones sin una razón sólida."
                ]
            },
            "Accesibilidad y adaptación": {
                "Flutter incluye soporte para accesibilidad mediante semántica, contraste adecuado y escalado de texto.": {
                    "Diseñar pensando en accesibilidad mejora inclusión y facilita uso por personas con necesidades diversas.": [
                        "Además, muchas buenas prácticas accesibles también mejoran claridad general de la experiencia."
                    ]
                },
                "MediaQuery y LayoutBuilder ayudan a adaptar interfaces a tamaños, orientaciones y densidades distintas.": [
                    "Esto es esencial para crear experiencias consistentes en teléfonos, tabletas y escritorios."
                ]
            }
        },
        "2.5. Desarrollo de un proyecto\ncon servicios en la nube": {
            "Backend as a Service": {
                "Los servicios BaaS permiten delegar infraestructura común para concentrarse en lógica y experiencia del usuario.": {
                    "En Flutter, Firebase es una opción frecuente por su integración oficial mediante FlutterFire y documentación amplia.": {
                        "Este enfoque reduce tiempo de arranque técnico cuando el proyecto necesita autenticación, base de datos y almacenamiento.": [
                            "Aun así, conviene evaluar costos, límites y dependencia del proveedor antes de escalar el sistema."
                        ]
                    }
                }
            },
            "Autenticación": {
                "Firebase Authentication admite inicio de sesión con correo, Google, Apple y otros proveedores compatibles.": {
                    "Ese servicio simplifica registro, recuperación de acceso y administración básica de identidad para aplicaciones móviles.": {
                        "También maneja sesiones y credenciales comunes, aunque la aplicación debe definir reglas adecuadas de seguridad.": [
                            "Una autenticación bien diseñada protege datos sensibles y mejora confianza del usuario final."
                        ]
                    }
                }
            },
            "Base de datos en la nube": {
                "Cloud Firestore es una base de datos NoSQL orientada a documentos con sincronización entre clientes.": {
                    "Permite escuchar cambios en tiempo real y trabajar con persistencia local cuando hay conectividad intermitente.": {
                        "Ese modelo resulta útil en chats, paneles colaborativos, catálogos dinámicos y aplicaciones distribuidas.": [
                            "Diseñar correctamente colecciones, índices y reglas evita consultas costosas o accesos inseguros."
                        ]
                    }
                }
            },
            "Archivos y notificaciones": {
                "Firebase Storage permite guardar imágenes, videos y documentos con escalabilidad administrada por Google Cloud.": {
                    "Suele combinarse con Firestore para registrar metadatos, rutas de acceso y permisos lógicos.": [
                        "Es apropiado cuando la aplicación necesita manejar contenido subido por usuarios de manera segura."
                    ]
                },
                "Firebase Cloud Messaging envía notificaciones y mensajes de datos a dispositivos registrados.": {
                    "Estas alertas sirven para recordatorios, novedades, eventos del sistema o reactivación de usuarios inactivos.": [
                        "Su uso debe planearse cuidadosamente para evitar saturación, desinstalaciones o pérdida de confianza."
                    ]
                },
                "Las notificaciones funcionan mejor cuando aportan valor claro y se segmentan según contexto del usuario.": [
                    "Enviar mensajes irrelevantes con demasiada frecuencia reduce retención y deteriora percepción del producto."
                ]
            },
            "Seguridad y buenas prácticas": {
                "Las reglas de seguridad en Firestore y Storage son críticas para limitar lectura y escritura de datos.": {
                    "Definirlas correctamente evita accesos no autorizados o modificaciones indebidas sobre información sensible.": [
                        "Estas reglas deben probarse igual que cualquier otra parte importante del sistema."
                    ]
                },
                "También es recomendable no incrustar secretos sensibles dentro del cliente móvil o del repositorio compartido.": [
                    "Las claves y configuraciones delicadas deben gestionarse con mecanismos apropiados para cada entorno."
                ]
            },
            "Compilación y publicación": {
                "Antes de publicar, la aplicación debe compilarse en modo release para obtener mejor rendimiento final.": {
                    "En Android suele generarse APK o AAB; en Apple se preparan archivos firmados para App Store.": [
                        "La firma digital, las versiones y los metadatos son requisitos indispensables para distribuir oficialmente."
                    ]
                },
                "Publicar también implica revisar permisos, política de privacidad, capturas e información exigida por tiendas.": [
                    "Ese trabajo no es solo técnico; también influye en aprobación, confianza y éxito del producto."
                ]
            }
        }
    }
}
