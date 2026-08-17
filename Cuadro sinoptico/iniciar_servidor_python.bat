@echo off
setlocal

cd /d "%~dp0"

set PORT=8003
if not "%~1"=="" set PORT=%~1

echo Iniciando servidor de cuadro sinoptico en:
echo   http://localhost:%PORT%/
echo.
echo Presiona Ctrl+C para detenerlo.
echo.

python servidor_cuadro_sinoptico.py --port %PORT%
if errorlevel 1 (
  echo.
  echo No se pudo ejecutar "python". Intentando con "py"...
  py servidor_cuadro_sinoptico.py --port %PORT%
)

endlocal
