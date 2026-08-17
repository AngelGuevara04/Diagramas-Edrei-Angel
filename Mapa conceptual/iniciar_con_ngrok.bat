@echo off
setlocal EnableExtensions EnableDelayedExpansion

cd /d "%~dp0"

set "PORT=8000"
if not "%~1"=="" set "PORT=%~1"

where ngrok >nul 2>nul
if errorlevel 1 (
  echo [ERROR] No se encontro "ngrok" en el PATH.
  echo Instala ngrok y vuelve a ejecutar este archivo.
  echo.
  pause
  exit /b 1
)

echo Iniciando servidor local en puerto %PORT%...
start "Servidor Mapa conceptual" cmd /k "cd /d ""%~dp0"" && (python servidor_mapa_conceptual.py --port %PORT% || py servidor_mapa_conceptual.py --port %PORT%)"

timeout /t 2 >nul

echo Iniciando tunel ngrok...
start "Ngrok Mapa conceptual" cmd /k "ngrok http %PORT%"

echo Esperando URL publica de ngrok...
set "NGROK_URL="
for /l %%I in (1,1,20) do (
  for /f "delims=" %%U in ('powershell -NoProfile -Command "try { $r=Invoke-RestMethod -Uri ""http://127.0.0.1:4040/api/tunnels""; $u=[string]::Empty; foreach($x in $r.tunnels){ if($x.proto -eq ""https"" -and $x.public_url){ $u=[string]$x.public_url; break } }; Write-Output $u } catch { Write-Output ([string]::Empty) }"') do (
    set "CANDIDATE=%%U"
    if /i "!CANDIDATE:~0,8!"=="https://" set "NGROK_URL=!CANDIDATE!"
    if /i "!CANDIDATE:~0,7!"=="http://" set "NGROK_URL=!CANDIDATE!"
  )
  if defined NGROK_URL goto :got_url
  timeout /t 1 >nul
)

echo.
echo [INFO] No se pudo leer la URL automaticamente.
echo Revisa la ventana de ngrok para copiar la URL publica.
echo Luego abre: URL_PUBLICA/visor/editor_mapa_conceptual.html
echo.
goto :done

:got_url
if not defined NGROK_URL goto :done
if /i not "!NGROK_URL:~0,8!"=="https://" if /i not "!NGROK_URL:~0,7!"=="http://" goto :done

if "!NGROK_URL:~-1!"=="/" set "NGROK_URL=!NGROK_URL:~0,-1!"

echo.
echo URL publica detectada:
echo   !NGROK_URL!
echo.
echo Abriendo editor...
start "" "!NGROK_URL!/visor/editor_mapa_conceptual.html"
echo.
echo Si no abre, copia manualmente:
echo   !NGROK_URL!/visor/editor_mapa_conceptual.html
echo.

:done
echo Ventanas iniciadas:
echo - Servidor local
echo - Ngrok
echo.
echo Para detener todo, cierra ambas ventanas.
echo.
pause
endlocal
