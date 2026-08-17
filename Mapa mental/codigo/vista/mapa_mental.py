"""
Configuracion y datos para el generador de mapas mentales.
Edita este archivo para cambiar el contenido (mapa_ejemplo) y los parametros de dibujo.
"""
import os
import sys
from pathlib import Path

mapa_ejemplo = {
    "Big Data: Universo de Información Digital": {
        
        # ---------------------------------------------------------
        # RAMA 1: DIMENSIÓN FÍSICA (Infraestructura y Escala)
        # ---------------------------------------------------------
        "Dimensión Física: Escala e Infraestructura": {
            
            # SUB-RAMA 1.A: EL VOLUMEN (Bifurcaciones en Nivel 4 y 8)
            "Volumen: Crecimiento Exponencial de Datos": { # Nivel 2
                "De Terabytes a Zettabytes Globales": { # Nivel 3
                    # Bifurcación Temprana (Nivel 4)
                    "Almacenamiento Distribuido Masivo": { 
                        "Sistemas de Archivos Hadoop HDFS": { # Nivel 5 (Rama A1)
                            "Replicación de Datos en Nodos": { # Nivel 6
                                "Tolerancia a Fallos de Hardware": { # Nivel 7
                                    "Clusters de Servidores Commodity": { # Nivel 8
                                        # Bifurcación Profunda A1
                                        "Escalabilidad Horizontal": { 
                                            "Añadir Nodos al Cluster": { "Costo Efectivo": {} },
                                            "Procesamiento Paralelo MapReduce": { "Divide y Vencerás": {} }
                                        }
                                    }
                                }
                            }
                        },
                        "Data Lakes en la Nube": { # Nivel 5 (Rama A2)
                            "Flexibilidad de Amazon S3 y Azure": { # Nivel 6
                                "Costos por Uso y Demanda": { # Nivel 7
                                    # Bifurcación Profunda A2
                                    "Tipos de Almacenamiento": { 
                                        "Hot Storage": { "Acceso Frecuente y Rápido": {} },
                                        "Cold Storage": { "Archivado a Largo Plazo": {} }
                                    }
                                }
                            }
                        }
                    }
                }
            },

            # SUB-RAMA 1.B: LA VELOCIDAD (Bifurcaciones en Nivel 4 y 9)
            "Velocidad: Análisis en Tiempo Real": { # Nivel 2
                "Ingesta de Datos sin Latencia": { # Nivel 3
                    # Bifurcación Temprana (Nivel 4)
                    "Arquitecturas de Streaming": {
                        "Apache Kafka como Bus de Mensajes": { # Nivel 5 (Rama B1)
                            "Desacoplamiento de Productores y Consumidores": { # Nivel 6
                                "Persistencia Temporal de Eventos": { # Nivel 7
                                    "Alta Tasa de Transferencia": { # Nivel 8
                                        "Millones de Mensajes por Segundo": { # Nivel 9
                                            # Bifurcación Profunda B1
                                            "Usos Críticos": { 
                                                "Monitorización de Servidores": { "Alertas Instantáneas": {} },
                                                "Tracking de Usuarios Web": { "Personalización en Vivo": {} }
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "Motores de Procesamiento Complejo": { # Nivel 5 (Rama B2)
                            "Apache Spark y Flink": { # Nivel 6
                                "Ventanas de Tiempo Deslizantes": { # Nivel 7
                                    "Agregación de Datos en Movimiento": { # Nivel 8
                                        # Bifurcación Profunda B2
                                        "Detección de Patrones": { 
                                            "Fraude Bancario Instantáneo": { "Bloqueo de Transacción": {} },
                                            "Anomalías en IoT": { "Mantenimiento Predictivo": {} }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },

            # SUB-RAMA 1.C: HARDWARE (Antes lineal, ahora compleja)
            "Hardware: Potencia de Cómputo": { # Nivel 2
                "Evolución de Procesadores y Memoria": { # Nivel 3
                    # Bifurcación Temprana (Nivel 4)
                    "Paradigmas de Computación": {
                        "Computación en Memoria (In-Memory)": { # Nivel 5
                            "Velocidad Superior al Disco": { # Nivel 6
                                "SAP HANA y Redis": { # Nivel 7
                                    "Análisis en Milisegundos": { # Nivel 8
                                        "Costos Elevados de RAM": {}
                                    }
                                }
                            }
                        },
                        "Aceleración por Hardware Especializado": { # Nivel 5
                            "Uso de GPUs para Cálculos": { # Nivel 6
                                "Paralelismo Masivo de Núcleos": { # Nivel 7
                                    # Bifurcación Profunda C2
                                    "Aplicaciones IA": { 
                                        "Entrenamiento Deep Learning": { "Redes Neuronales": {} },
                                        "Renderizado de Datos": { "Visualización 3D": {} }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },

        # ---------------------------------------------------------
        # RAMA 2: DIMENSIÓN DE CAOS (Variedad y Calidad)
        # ---------------------------------------------------------
        "Dimensión Caos: Gestión de la Complejidad": {
            
            # SUB-RAMA 2.A: VARIEDAD (Múltiples formatos)
            "Variedad: Multiplicidad de Fuentes": { # Nivel 2
                "Integración de Datos Heterogéneos": { # Nivel 3
                    # Bifurcación Temprana (Nivel 4)
                    "Categorías de Formatos": {
                        "Datos No Estructurados Humanos": { # Nivel 5
                            "Texto Libre y Multimedia": { # Nivel 6
                                "Desafío de Interpretación Semántica": { # Nivel 7
                                    "Procesamiento Lenguaje Natural (NLP)": { # Nivel 8
                                        # Bifurcación Profunda
                                        "Fuentes Sociales": {
                                            "Twitter y Redes": { "Análisis Sentimiento": {} },
                                            "Correos Electrónicos": { "Clasificación Spam": {} }
                                        }
                                    }
                                }
                            }
                        },
                        "Datos Semiestructurados Máquina": { # Nivel 5
                            "Logs y Archivos JSON/XML": { # Nivel 6
                                "Jerarquías Flexibles sin Esquema": { # Nivel 7
                                    "Intercambio de Datos Web": { # Nivel 8
                                        # Bifurcación Profunda
                                        "APIs Modernas": {
                                            "Respuestas RESTful": { "Integración Apps": {} },
                                            "Configuraciones Sistema": { "Despliegue Automático": {} }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },

            # SUB-RAMA 2.B: VERACIDAD (Confianza)
            "Veracidad: Confianza en el Dato": { # Nivel 2
                "Higiene y Limpieza de Datos": { # Nivel 3
                    "Eliminación de Ruido y Error": { # Nivel 4
                        # Bifurcación Media
                        "Problemas Comunes de Calidad": {
                            "Datos Incompletos o Nulos": { # Nivel 5
                                "Técnicas de Imputación Estadística": { # Nivel 6
                                    "Rellenar con Medias/Medianas": { # Nivel 7
                                        "Riesgo de Sesgo Inducido": {}
                                    }
                                }
                            },
                            "Duplicidad e Inconsistencia": { # Nivel 5
                                "Procesos de Deduplicación": { # Nivel 6
                                    "Reglas de Negocio Unificadas": { # Nivel 7
                                        # Bifurcación Profunda
                                        "Impacto Negativo": {
                                            "Pérdida de Clientes": { "Comunicaciones Erróneas": {} },
                                            "Multas Regulatorias": { "Reportes Falsos": {} }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },

            # SUB-RAMA 2.C: GOBERNANZA (Nueva rama compleja)
            "Gobernanza: Control y Seguridad": { # Nivel 2
                "Políticas de Gestión de Datos": { # Nivel 3
                    # Bifurcación Temprana
                    "Pilares de la Gobernanza": {
                        "Seguridad y Acceso": { # Nivel 5
                            "Encriptación en Reposo y Tránsito": { # Nivel 6
                                "Gestión de Identidades (IAM)": { # Nivel 7
                                    "Auditoría de Accesos": {}
                                }
                            }
                        },
                        "Cumplimiento Normativo Legal": { # Nivel 5
                            "Regulaciones GDPR y CCPA": { # Nivel 6
                                "Derecho al Olvido Digital": { # Nivel 7
                                    # Bifurcación Profunda
                                    "Acciones Requeridas": {
                                        "Anonimización Datos": { "Proteger Identidad": {} },
                                        "Consentimiento Usuario": { "Cookies y Tracking": {} }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },

        # ---------------------------------------------------------
        # RAMA 3: DIMENSIÓN ESTRATÉGICA (Valor y Futuro)
        # ---------------------------------------------------------
        "Dimensión Estratégica: Valor y Futuro": {
            
            # SUB-RAMA 3.A: VALOR (El "Por qué")
            "Valor: Transformación en Conocimiento": { # Nivel 2
                "Monetización de los Datos": { # Nivel 3
                    # Bifurcación Temprana
                    "Estrategias de Negocio": {
                        "Optimización Operativa Interna": { # Nivel 5
                            "Reducción de Costos Logísticos": { # Nivel 6
                                "Cadena de Suministro Eficiente": { # Nivel 7
                                    "Just-in-Time Inventory": { # Nivel 8
                                        "Menor Desperdicio": {}
                                    }
                                }
                            }
                        },
                        "Nuevos Productos y Servicios": { # Nivel 5
                            "Innovación Basada en Datos": { # Nivel 6
                                "Modelos de Suscripción": { # Nivel 7
                                    # Bifurcación Profunda
                                    "Ejemplos Disruptivos": {
                                        "Uber/Transporte": { "Tarifas Dinámicas": {} },
                                        "Spotify/Música": { "Discover Weekly": {} }
                                    }
                                }
                            }
                        }
                    }
                }
            },

            # SUB-RAMA 3.B: INTELIGENCIA ARTIFICIAL (Simbiosis)
            "IA: El Motor de Análisis": { # Nivel 2
                "Machine Learning sobre Big Data": { # Nivel 3
                    "Entrenamiento con Gran Volumen": { # Nivel 4
                        # Bifurcación Media
                        "Tipos de Aprendizaje": {
                            "Aprendizaje Supervisado": { # Nivel 5
                                "Datos Etiquetados Previamente": { # Nivel 6
                                    "Predicción de Ventas Futuras": { # Nivel 7
                                        "Regresión Lineal Simple": {}
                                    }
                                }
                            },
                            "Aprendizaje No Supervisado": { # Nivel 5
                                "Descubrimiento de Patrones Ocultos": { # Nivel 6
                                    "Segmentación de Clientes (Clustering)": { # Nivel 7
                                        # Bifurcación Profunda
                                        "Aplicaciones Marketing": {
                                            "Grupos de Comportamiento": { "Campañas Dirigidas": {} },
                                            "Detección Anomalías": { "Ciberseguridad": {} }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },

            # SUB-RAMA 3.C: VISUALIZACIÓN (Nueva rama compleja)
            "Visualización: Contar la Historia": { # Nivel 2
                "Comunicación Efectiva de Insights": { # Nivel 3
                    # Bifurcación Temprana
                    "Herramientas y Técnicas": {
                        "Dashboards Interactivos BI": { # Nivel 5
                            "Tableau y PowerBI": { # Nivel 6
                                "KPIs en Tiempo Real": { # Nivel 7
                                    "Toma Decisiones Gerencial": {}
                                }
                            }
                        },
                        "Narrativa de Datos (Storytelling)": { # Nivel 5
                            "Contexto para no Expertos": { # Nivel 6
                                "Simplificación de lo Complejo": { # Nivel 7
                                    # Bifurcación Profunda
                                    "Elementos Clave": {
                                        "Gráficos Intuitivos": { "Evitar Confusión": {} },
                                        "Flujo Lógico": { "Conclusión Clara": {} }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}


# CONFIG = {
#     "CENTER_X": 800,
#     "CENTER_Y": 600,
#     "R_STEP": 360,
#     # Ajusta el crecimiento radial en los primeros niveles (factor 1.05 = +5%)
#     "R_STEP_BOOST": {"levels": 5, "factor": 1.05},
#     "CURVED_EDGES": False,
#     "EDGE_CONNECTOR_STYLE": "curved_block",  # default | curved_block
#     "EDGE_CURVE_FACTOR": 0.09, # Factor de curvatura de las aristas
#     "IMAGE_DIR": Path("ImagenesMapaMental"),
#     "IMAGE_RADIUS_OFFSET": 200, # Offset radial para las imágenes respecto al centro del mapa (px). Positivo = más lejos del centro.
#     "IMAGE_WIDTH": 250,
#     "IMAGE_WIDTH_NOISE": 0.2,  # 0.0 = sin ruido, 0.1 = +/-10% del ancho
#     "IMAGE_TEXT_PADDING": 24,  # Distancia minima de imagen vs cuadros de texto.
#     "IMAGE_EDGE_PADDING": 12,  # Distancia minima de imagen vs lineas conectoras.
#     "IMAGE_HEIGHT": None,
#     "TEXT_FONT_SIZE": 14, # Tamaño de la fuente del texto
#     "TEXT_FONT_FAMILY": "Helvetica",
#     "TEXT_FONT_COLOR": "#000000", # Color del texto
#     "TEXT_FONT_BORDER_COLOR": "none", # Color del borde del texto
#     "TEXT_BG_COLOR": "none", # Color de fondo del texto
#     "TEXT_STROKE_COLOR": "#000000", # Color del contorno del cuadro de texto
#     "TEXT_STROKE_WIDTH": 2, # Ancho del contorno del cuadro de texto
#     "TEXT_FILL_COLOR": "none", # Color de relleno del cuadro de texto
#     "TEXT_ROUNDED": True,  # Permite ajustar el redondeado de los cuadros de texto
#     "TEXT_ARC_SIZE": 50,   # Tamaño de las esquinas redondeadas (0 para esquinas rectas)
#     "TEXT_BOLD": True, # Negrita
#     "TEXT_ITALIC": False, # Cursiva
#     "TEXT_UNDERLINE": False, # Subrayado
#     "TEXT_WRAP": True, # Ajuste de texto dentro de cuadros de texto
#     "NODE_WIDTH": 120,  # Ancho del nodo
#     "NODE_HEIGHT": 40, # Alto del nodo
#     "POSITION_NOISE": 300, # Ruido aleatorio en la posición de los nodos
#     "RANDOM_SEED": 42, # Semilla para reproducibilidad
#     "EDGE_STROKE_WIDTH": 2, # Ancho de las aristas
#     "EDGE_COLOR": "#000000", # Color de las aristas
#     # Flechas en ambos extremos de la linea: "none", "block", "classic", etc.
#     "EDGE_LEFT_ARROW": "none",
#     "EDGE_RIGHT_ARROW": "block",
#     # Paleta opcional: cada subtema principal hereda colores de su entrada.
#     # Formato dict: {"fill": "...", "edge": "...", "text": "...", "label_bg": "...", "label_border": "...", "outline": "..."}
#     #  - fill: relleno del cuadro de texto
#     #  - outline: contorno del cuadro de texto (stroke)
#     #  - edge: color de línea que conecta nodos (si no se define usa stroke, luego EDGE_COLOR)
#     # Formato tupla: (fill, stroke, edge, text, label_bg, label_border, outline) (elementos posteriores son opcionales)
#     "PALETTE": [
#         {"fill": "#fff3c4", "edge": "#d97706", "text": "#111827", "outline": "#b45309"},
#         {"fill": "#d8ffe5", "edge": "#15803d", "text": "#0f5132", "outline": "#0f5132"},
#         {"fill": "#e0eeff", "edge": "#1d4ed8", "text": "#0f172a", "outline": "#1d4ed8"},
#         {"fill": "#ffe4e6", "edge": "#be185d", "text": "#831843", "outline": "#be185d"},
#     ],
#     "USE_PALETTE": True,
#     "OUTPUT_FILE": os.path.join("Mapas", "mapa_mental.drawio"),
# }

CONFIG = {
    "CENTER_X": 800,
    "CENTER_Y": 600,
    "R_STEP": 360,
    # Ajusta el crecimiento radial en los primeros niveles (factor 1.05 = +5%)
    "R_STEP_BOOST": {"levels": 5, "factor": 1.05},
    "CURVED_EDGES": False,
    "EDGE_CONNECTOR_STYLE": "default",  # default | curved_block
    "EDGE_CURVE_FACTOR": 0.09, # Factor de curvatura de las aristas
    "IMAGE_DIR": Path("ImagenesMapaMental"),
    "IMAGE_RADIUS_OFFSET": 0, # Offset radial para las imágenes respecto al centro del mapa (px). Positivo = más lejos del centro.
    "IMAGE_WIDTH": 300,
    "IMAGE_WIDTH_NOISE": 0.2,  # 0.0 = sin ruido, 0.1 = +/-10% del ancho
    "IMAGE_TEXT_PADDING": 24,  # Distancia minima de imagen vs cuadros de texto.
    "IMAGE_EDGE_PADDING": 12,  # Distancia minima de imagen vs lineas conectoras.
    "IMAGE_HEIGHT": None,
    "TEXT_FONT_SIZE": 12, # Tamaño de la fuente del texto
    "TEXT_FONT_FAMILY": "Times New Roman", # Familia de la fuente del texto
    "TEXT_FONT_COLOR": "#000000", # Color del texto
    "TEXT_FONT_BORDER_COLOR": "#1E6921", # Color del borde del texto
    "TEXT_BG_COLOR": "#A1E9A3", # Color de fondo del texto
    "TEXT_STROKE_COLOR": "none", # Color del contorno del cuadro de texto
    "TEXT_STROKE_WIDTH": 2, # Ancho del contorno del cuadro de texto
    "TEXT_FILL_COLOR": "none", # Color de relleno del cuadro de texto
    "TEXT_ROUNDED": True,  # Permite ajustar el redondeado de los cuadros de texto
    "TEXT_ARC_SIZE": 50,   # Tamaño de las esquinas redondeadas (0 para esquinas rectas)
    "TEXT_BOLD": False, # Negrita
    "TEXT_ITALIC": True, # Cursiva
    "TEXT_UNDERLINE": False, # Subrayado
    "TEXT_WRAP": False, # Ajuste de texto dentro de cuadros de texto
    "NODE_WIDTH": 120,  # Ancho del nodo
    "NODE_HEIGHT": 40, # Alto del nodo
    "POSITION_NOISE": 200, # Ruido aleatorio en la posición de los nodos
    "RANDOM_SEED": 42, # Semilla para reproducibilidad
    "EDGE_STROKE_WIDTH": 2, # Ancho de las aristas
    "EDGE_COLOR": "#1E6921", # Color de las aristas
    # Flechas en ambos extremos de la linea: "none", "block", "classic", etc.
    "EDGE_LEFT_ARROW": "none",
    "EDGE_RIGHT_ARROW": "block",
    # Paleta opcional: cada subtema principal hereda colores de su entrada.
    # Formato dict: {"fill": "...", "edge": "...", "text": "...", "label_bg": "...", "label_border": "...", "outline": "..."}
    #  - fill: relleno del cuadro de texto
    #  - outline: contorno del cuadro de texto (stroke)
    #  - edge: color de línea que conecta nodos (si no se define usa stroke, luego EDGE_COLOR)
    # Formato tupla: (fill, stroke, edge, text, label_bg, label_border, outline) (elementos posteriores son opcionales)
    "PALETTE": [
        {"fill": "#fff3c4", "edge": "#d97706", "text": "#111827", "outline": "#b45309"},
        {"fill": "#d8ffe5", "edge": "#15803d", "text": "#0f5132", "outline": "#0f5132"},
        {"fill": "#e0eeff", "edge": "#1d4ed8", "text": "#0f172a", "outline": "#1d4ed8"},
        {"fill": "#ffe4e6", "edge": "#be185d", "text": "#831843", "outline": "#be185d"},
    ],
    
    "USE_PALETTE": False,
    "OUTPUT_FILE": os.path.join("Mapas", "mapa_mental.drawio"),
}



def run():
    """Permite ejecutar el generador directamente desde este archivo."""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    scripts_dir = os.path.join(base_dir, "Scripts")
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)

    from Mapas_mentales import generar_mapa_mental

    out_path = generar_mapa_mental(mapa_ejemplo, CONFIG)
    print(f"Mapa mental generado en: {out_path}")


if __name__ == "__main__":
    run()
