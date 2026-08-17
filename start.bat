@echo off
echo =======================================
echo Iniciando Centro de Diagramas
echo =======================================
echo.

:: Comprueba si uvicorn está instalado
python -c "import uvicorn" >nul 2>&1
if %errorlevel% neq 0 (
    echo Instalando dependencias desde requirements.txt...
    pip install -r requirements.txt
)

echo Iniciando servidor en http://localhost:8000
echo.
echo Presiona Ctrl+C para detener el servidor.
echo.

python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
pause
