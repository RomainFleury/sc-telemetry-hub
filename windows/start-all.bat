@echo off

::: Start daemon + Electron dev UI ^(pattern: libthirdspacevest-simhub\windows\start-all.bat^)

echo.
echo ========================================
echo Star Citizen Telemetry Hub - Full start
echo ========================================
echo.

if exist "%~dp0.env.bat" call "%~dp0.env.bat"

where node >nul 2>&1
if errorlevel 1 (
  echo [ERROR] Node.js is not installed. See windows\SETUP.md
  pause
  exit /b 1
)

call "%~dp0setup\resolve-python.bat"
if errorlevel 1 (
  echo [ERROR] Python could not be resolved.
  pause
  exit /b 1
)

echo [OK] Node.js and Python found
echo [INFO] Python: %STH_PYTHON%
echo.

set "DAEMON_SCRIPT=%TEMP%\start-sc-telemetry-daemon.bat"
echo @echo off> "%DAEMON_SCRIPT%"
echo cd /d "%~dp0..\daemon">> "%DAEMON_SCRIPT%"
echo %STH_PYTHON% -m sc_telemetry.cli daemon start>> "%DAEMON_SCRIPT%"
echo pause>> "%DAEMON_SCRIPT%"

echo [..] Starting Python daemon in a new window...
start "SC Telemetry Hub Daemon" cmd /k ""%DAEMON_SCRIPT%""

echo [..] Waiting for daemon to listen...
timeout /t 3 /nobreak >nul

cd /d "%~dp0..\web"
if not exist "node_modules" (
  echo [WARN] Installing web dependencies...
  call corepack enable >nul 2>&1
  call yarn install
)

echo.
echo [OK] Starting UI ^(close Electron to exit; then close the daemon window^)
echo.

cd /d "%~dp0..\web"
call yarn dev

echo.
echo UI stopped. You can close the daemon window.
pause
