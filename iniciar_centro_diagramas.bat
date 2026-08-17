@echo off
setlocal EnableExtensions EnableDelayedExpansion

REM Inicia menu principal + backends + tunel ngrok.
cd /d "%~dp0"

set PORT=8000
if not "%~1"=="" set PORT=%~1

set "NGROK_AUTHTOKEN=3DbMc0Fr9z5qSLwSN404FVtMSMC_2THTp8Uv8dnuTTedKadFL"

set CONCEPT_PORT=8001
set MIND_PORT=8002
set SYNOPTIC_PORT=8003
if "%PORT%"=="8001" set CONCEPT_PORT=8101
if "%PORT%"=="8002" set MIND_PORT=8102
if "%PORT%"=="8003" set SYNOPTIC_PORT=8103

where ngrok >nul 2>nul
if errorlevel 1 (
  echo [ERROR] No se encontro "ngrok" en el PATH.
  echo Instala ngrok y vuelve a ejecutar este archivo.
  echo.
  pause
  exit /b 1
)

echo Configurando credenciales de ngrok...
ngrok config add-authtoken "%NGROK_AUTHTOKEN%" >nul 2>nul
if errorlevel 1 (
  echo [ERROR] No se pudo configurar el authtoken de ngrok.
  echo Verifica tu cuenta en https://dashboard.ngrok.com/
  echo.
  pause
  exit /b 1
)

echo Iniciando backend de mapa conceptual en puerto %CONCEPT_PORT%...
start "Backend Mapa conceptual" cmd /k "cd /d ""%~dp0\Mapa conceptual"" && (python servidor_mapa_conceptual.py --port %CONCEPT_PORT% || py servidor_mapa_conceptual.py --port %CONCEPT_PORT%)"

echo Iniciando backend de mapa mental en puerto %MIND_PORT%...
start "Backend Mapa mental" cmd /k "cd /d ""%~dp0\Mapa mental"" && (python servidor_mapa_mental.py --port %MIND_PORT% || py servidor_mapa_mental.py --port %MIND_PORT%)"

echo Iniciando backend de cuadro sinoptico en puerto %SYNOPTIC_PORT%...
start "Backend Cuadro sinoptico" cmd /k "cd /d ""%~dp0\Cuadro sinoptico"" && (python servidor_cuadro_sinoptico.py --port %SYNOPTIC_PORT% || py servidor_cuadro_sinoptico.py --port %SYNOPTIC_PORT%)"

timeout /t 2 >nul

echo Iniciando servidor central en puerto %PORT%...
start "Centro Diagramas" cmd /k "cd /d ""%~dp0"" && (python servidor_centro_diagramas.py --port %PORT% --concept-port %CONCEPT_PORT% --mind-port %MIND_PORT% || py servidor_centro_diagramas.py --port %PORT% --concept-port %CONCEPT_PORT% --mind-port %MIND_PORT%)"

timeout /t 2 >nul

echo Iniciando tunel ngrok para el puerto %PORT%...
start "Ngrok Centro Diagramas" cmd /k "ngrok http %PORT%"

echo Esperando URL publica de ngrok...
set NGROK_URL=
for /l %%I in (1,1,25) do (
  for /f "delims=" %%U in ('powershell -NoProfile -Command "try { $r=Invoke-RestMethod -Uri ""http://127.0.0.1:4040/api/tunnels""; $u=[string]::Empty; foreach($x in $r.tunnels){ if($x.proto -eq ""https"" -and $x.public_url){ $u=[string]$x.public_url; break } }; Write-Output $u } catch { Write-Output ([string]::Empty) }"') do (
    set CANDIDATE=%%U
    if /i "!CANDIDATE:~0,8!"=="https://" set NGROK_URL=!CANDIDATE!
    if /i "!CANDIDATE:~0,7!"=="http://" set NGROK_URL=!CANDIDATE!
  )
  if defined NGROK_URL goto :got_url
  timeout /t 1 >nul
)

echo.
echo [INFO] No se pudo leer la URL automaticamente.
echo Revisa la ventana de ngrok para copiarla.
echo.
echo Menu local:
echo   http://localhost:%PORT%/index.html
echo.
echo Para detener todo, cierra las 5 ventanas iniciadas.
echo.
pause
goto :eof

:got_url
if "!NGROK_URL:~-1!"=="/" set NGROK_URL=!NGROK_URL:~0,-1!

echo.
echo URL publica detectada:
echo   !NGROK_URL!
echo.
echo Abriendo menu principal...
start "" "!NGROK_URL!/index.html"
start "" "http://localhost:%PORT%/index.html"
echo.
echo Si no abre, usa:
echo   !NGROK_URL!/index.html
echo.
echo Para detener todo, cierra las 5 ventanas iniciadas.
echo.
pause
endlocal
