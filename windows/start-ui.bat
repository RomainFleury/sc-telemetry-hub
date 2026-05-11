@echo off

::: Start Electron + Vite dev ^(pattern: libthirdspacevest-simhub\windows\start-ui.bat^)

echo.
echo ========================================
echo Star Citizen Telemetry Hub - UI
echo ========================================
echo.

if exist "%~dp0.env.bat" call "%~dp0.env.bat"

where node >nul 2>&1
if errorlevel 1 (
  echo [ERROR] Node.js is not installed. See windows\SETUP.md
  pause
  exit /b 1
)

call "%~dp0setup\resolve-python.bat" >nul 2>&1
if not errorlevel 1 (
  echo [INFO] STH_PYTHON=%STH_PYTHON%
  echo ^(Reserved for future Electron / daemon auto-start parity^)
  echo.
)

cd /d "%~dp0..\web"
if not exist "node_modules" (
  echo [WARN] node_modules missing; running yarn install...
  call corepack enable >nul 2>&1
  call yarn install
)

echo [OK] Starting dev ^(Vite + Electron^) ...
echo.

call yarn dev

echo.
echo UI stopped.
pause
