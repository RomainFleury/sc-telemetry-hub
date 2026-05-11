@echo off
setlocal EnableDelayedExpansion

::: Resolve Python for Star Citizen Telemetry Hub (no prompts).
::: Optional: windows\.env.bat may set STH_PYTHON (see .env.bat.example).
::: Exports STH_PYTHON and PYTHON_CMD to the caller environment.

if exist "%~dp0..\.env.bat" call "%~dp0..\.env.bat"

set "DETECTED_PYTHON="
if defined STH_PYTHON (
  set "DETECTED_PYTHON=!STH_PYTHON!"
  goto :verify_python
)

where py >nul 2>&1
if !ERRORLEVEL! equ 0 (
  for %%P in (14 13 12 11 10) do (
    py -3.%%P -c "import sys" >nul 2>&1
    if !ERRORLEVEL! equ 0 (
      set "DETECTED_PYTHON=py -3.%%P"
      goto :verify_python
    )
  )
)

where python >nul 2>&1
if !ERRORLEVEL! equ 0 (
  set "DETECTED_PYTHON=python"
  goto :verify_python
)

where python3 >nul 2>&1
if !ERRORLEVEL! equ 0 (
  set "DETECTED_PYTHON=python3"
  goto :verify_python
)

echo [ERROR] Python is not installed or not on PATH.
echo Install Python 3.10+ from https://www.python.org/downloads/ ^(enable "Add to PATH"^).
exit /b 1

:verify_python
%DETECTED_PYTHON% -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)" >nul 2>&1
if !ERRORLEVEL! neq 0 (
  echo [ERROR] Python 3.10+ is required. The selected interpreter is too old.
  exit /b 1
)

set "EXPORT_PYTHON=!DETECTED_PYTHON!"
endlocal & set "STH_PYTHON=%EXPORT_PYTHON%" & set "PYTHON_CMD=%EXPORT_PYTHON%"
exit /b 0
