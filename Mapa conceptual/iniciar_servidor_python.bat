@echo off
setlocal

REM Inicia un servidor HTTP en la carpeta donde esta este archivo.
cd /d "%~dp0"

set PORT=8000
if not "%~1"=="" set PORT=%~1

echo Iniciando servidor en:
echo   http://localhost:%PORT%/
echo.
echo Presiona Ctrl+C para detenerlo.
echo.

python servidor_mapa_conceptual.py --port %PORT%
if errorlevel 1 (
  echo.
  echo No se pudo ejecutar "python". Intentando con "py"...
  py servidor_mapa_conceptual.py --port %PORT%
)

endlocal
