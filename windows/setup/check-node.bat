@echo off
setlocal EnableDelayedExpansion

::: Star Citizen Telemetry Hub - Node.js check
::: Pattern follows libthirdspacevest-simhub.

echo [CHECK] Checking Node.js installation...

for /f "tokens=*" %%i in ('node --version 2^>nul') do set "NODE_VERSION=%%i"
if not defined NODE_VERSION (
  echo [FAIL] Node.js is not installed.
  echo Install Node.js 18+ LTS from https://nodejs.org/
  exit /b 1
)

set "NODE_MAJOR=%NODE_VERSION:~1%"
for /f "tokens=1 delims=." %%i in ("%NODE_MAJOR%") do set "NODE_MAJOR=%%i"

if %NODE_MAJOR% LSS 18 (
  echo [WARN] Node.js %NODE_VERSION% found; v18+ LTS recommended.
) else (
  echo [OK] Node.js %NODE_VERSION%
)

exit /b 0
