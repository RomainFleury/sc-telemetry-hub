@echo off
setlocal EnableDelayedExpansion

::: Install Python package ^(editable^) and web/node_modules
::: Same dependency targets as check-setup.bat (without full diagnostics).

echo.
echo ========================================
echo Telemetry Hub - Install dependencies
echo ========================================
echo.

call "%~dp0setup\resolve-python.bat"
if !ERRORLEVEL! neq 0 exit /b 1

echo [..] pip install -e daemon ...
pushd "%~dp0..\daemon"
%STH_PYTHON% -m pip install -e .
if !ERRORLEVEL! neq 0 (
  echo [FAIL] pip install -e .
  popd
  exit /b 1
)
popd

where node >nul 2>&1
if !ERRORLEVEL! neq 0 (
  echo [WARN] Node.js not found; skipping web install.
  exit /b 0
)

call corepack enable >nul 2>&1
pushd "%~dp0..\web"
echo [..] yarn install ...
call yarn install
if !ERRORLEVEL! neq 0 (
  echo [FAIL] yarn install
  popd
  exit /b 1
)
popd

echo.
echo [OK] Dependencies installed.
exit /b 0
