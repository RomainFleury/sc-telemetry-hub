@echo off
setlocal EnableDelayedExpansion

::: Install / verify sc_telemetry editable package (daemon/)
::: Pattern follows libthirdspacevest-simhub check-python-packages.bat.

echo [CHECK] Checking Python package ^(sc-telemetry daemon^)...

if exist "%~dp0..\.env.bat" call "%~dp0..\.env.bat"

if not defined STH_PYTHON (
  call "%~dp0resolve-python.bat"
  if !ERRORLEVEL! neq 0 exit /b 1
)

set "PYTHON_CMD=%STH_PYTHON%"
if not defined PYTHON_CMD set "PYTHON_CMD=python"

if not exist "%~dp0..\..\daemon\pyproject.toml" (
  echo [FAIL] daemon\pyproject.toml not found. Clone the repo completely.
  exit /b 1
)

%PYTHON_CMD% -c "import sc_telemetry" >nul 2>&1
if !ERRORLEVEL! neq 0 (
  echo [INFO] sc_telemetry not importable; installing editable package...
  pushd "%~dp0..\..\daemon"
  %PYTHON_CMD% -m pip install -e . --quiet
  if !ERRORLEVEL! neq 0 (
    echo [FAIL] pip install -e . failed.
    echo Try manually: cd daemon ^&^& pip install -e .
    popd
    exit /b 1
  )
  popd
  echo [OK] Installed sc-telemetry package ^(editable^)
) else (
  echo [OK] sc_telemetry importable
)

%PYTHON_CMD% -m sc_telemetry.cli --help >nul 2>&1
if !ERRORLEVEL! neq 0 (
  echo [WARN] CLI --help failed ^(package partially broken?^)
) else (
  echo [OK] sc_telemetry CLI responds
)

exit /b 0
