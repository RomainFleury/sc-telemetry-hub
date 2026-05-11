@echo off
setlocal EnableDelayedExpansion

::: Install web/node_modules if missing
::: Pattern follows libthirdspacevest-simhub.

echo [CHECK] Checking web dependencies...

where node >nul 2>&1
if %ERRORLEVEL% neq 0 (
  echo [SKIP] Node.js not found
  exit /b 1
)

where yarn >nul 2>&1
if %ERRORLEVEL% neq 0 (
  echo [SKIP] Yarn not found
  exit /b 1
)

if not exist "%~dp0..\..\web" (
  echo [FAIL] web\ folder not found
  exit /b 1
)

if exist "%~dp0..\..\web\node_modules" (
  echo [OK] web\node_modules exists
) else (
  echo [INFO] Installing web dependencies...
  pushd "%~dp0..\..\web"
  call corepack enable >nul 2>&1
  call yarn install
  if !ERRORLEVEL! neq 0 (
    echo [FAIL] yarn install failed
    popd
    exit /b 1
  )
  popd
  echo [OK] web dependencies installed
)

exit /b 0
