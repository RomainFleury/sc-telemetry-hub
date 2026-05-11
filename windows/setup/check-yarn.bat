@echo off
setlocal EnableDelayedExpansion

::: Star Citizen Telemetry Hub - Yarn via Corepack
::: Pattern follows libthirdspacevest-simhub.

echo [CHECK] Checking Yarn ^(Corepack^)...

for /f "tokens=*" %%i in ('yarn --version 2^>nul') do set "YARN_VERSION=%%i"
if not defined YARN_VERSION (
  echo [INFO] Yarn not found; enabling Corepack...
  call corepack enable >nul 2>&1
  if !ERRORLEVEL! neq 0 (
    echo [FAIL] corepack enable failed. Run from an elevated prompt once: corepack enable
    exit /b 1
  )
  for /f "tokens=*" %%i in ('yarn --version 2^>nul') do set "YARN_VERSION=%%i"
  if not defined YARN_VERSION (
    echo [FAIL] Yarn still unavailable. Try: corepack enable
    exit /b 1
  )
)

set "REQUIRED_VERSION=4.11.0"
set "VERSION_CLEAN=%YARN_VERSION%"
if "!VERSION_CLEAN:~0,1!"=="v" set "VERSION_CLEAN=!VERSION_CLEAN:~1!"

if not "!VERSION_CLEAN!"=="%REQUIRED_VERSION%" (
  echo [WARN] Yarn version is !YARN_VERSION!; package.json pins %REQUIRED_VERSION%.
  echo If installs fail, run: corepack enable
  echo.
)

echo [OK] Yarn !YARN_VERSION!
exit /b 0
