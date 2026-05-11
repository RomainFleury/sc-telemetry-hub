@echo off
setlocal EnableDelayedExpansion

::: Start Python daemon only ^(pattern: libthirdspacevest-simhub\windows\start-daemon.bat^)

echo.
echo ========================================
echo Star Citizen Telemetry Hub - Daemon
echo ========================================
echo.

if exist "%~dp0.env.bat" call "%~dp0.env.bat"

call "%~dp0setup\resolve-python.bat"
if !ERRORLEVEL! neq 0 (
  pause
  exit /b 1
)

for /f "tokens=*" %%i in ('%STH_PYTHON% --version 2^>^&1') do echo [OK] %%i
echo [INFO] Using: %STH_PYTHON%
echo.

cd /d "%~dp0..\daemon"
if !ERRORLEVEL! neq 0 (
  echo [ERROR] Could not cd to daemon\
  pause
  exit /b 1
)

echo [..] Starting daemon ^(Ctrl+C to stop^) ...
echo.
%STH_PYTHON% -m sc_telemetry.cli daemon start

echo.
echo Daemon stopped.
pause
