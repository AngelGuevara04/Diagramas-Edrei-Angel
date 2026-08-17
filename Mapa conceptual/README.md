# Mapa conceptual

Estructura organizada de los archivos relacionados con el mapa conceptual.

## Estructura
- `visor/editor_mapa_conceptual.html`: interfaz web para editar y exportar.
- `servidor_mapa_conceptual.py`: servidor local (archivos + API Gemini).
- `codigo/vista/mapa_conceptual.py`: datos (`concept_map`) y configuración (`CONFIG`).
- `codigo/Scripts/Mapas_conceptuales.py`: generador de archivos `.drawio`.
- `codigo/utilidades/ajuste_mapa_conceptual.py`: normalización opcional de tuplas.
- `codigo/herramientas/recrear_config_mapa_conceptual.py`: script de recreación de configuraciones.
- `historico/`: versiones anteriores relacionadas con mapas conceptuales.
- `salidas/`: carpeta sugerida para exportaciones.

## Nota rápida
El visor (`visor/editor_mapa_conceptual.html`) ya fue ajustado para cargar archivos desde `codigo/`.

## Arranque recomendado
1. Define tu API key de Gemini:
   - Variable de entorno `GEMINI_API_KEY`, o
   - Copia `Mapa conceptual/.env.example` a `Mapa conceptual/.env` y completa:
     - `GEMINI_API_KEY=TU_API_KEY`
2. Ejecuta `iniciar_servidor_python.bat`.
3. Abre `http://localhost:8000/visor/editor_mapa_conceptual.html`.

## Arranque con ngrok (automatizado)
1. Instala `ngrok` y asegúrate de que esté en el `PATH`.
2. Ejecuta `iniciar_con_ngrok.bat` (opcional: `iniciar_con_ngrok.bat 8000` para otro puerto).
3. El script abre:
   - una ventana del servidor local
   - una ventana de ngrok
   - y el editor en la URL pública, cuando la detecta.
