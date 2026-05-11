@echo off
setlocal EnableDelayedExpansion

::: Star Citizen Telemetry Hub - prerequisite check
::: Layout mirrors libthirdspacevest-simhub\windows\check-setup.bat
::: (orchestrator + windows\setup\*.bat). USB / bettercam checks omitted.

echo.
echo ========================================
echo Star Citizen Telemetry Hub - Setup Check
echo ========================================
echo.

set "CHECKS_PASSED=0"
set "CHECKS_FAILED=0"
set "CHECKS_WARNED=0"

call "%~dp0setup\check-python.bat"
if !ERRORLEVEL! equ 0 (
  set /a CHECKS_PASSED+=1
) else (
  set /a CHECKS_FAILED+=1
  echo.
  echo Python is required. Fix the issue above, then re-run check-setup.bat
  goto :summary
)
echo.

call "%~dp0setup\check-node.bat"
if !ERRORLEVEL! equ 0 (
  set /a CHECKS_PASSED+=1
) else (
  set /a CHECKS_FAILED+=1
)
echo.

call "%~dp0setup\check-yarn.bat"
if !ERRORLEVEL! equ 0 (
  set /a CHECKS_PASSED+=1
) else (
  set /a CHECKS_FAILED+=1
)
echo.

call "%~dp0setup\check-python-packages.bat"
if !ERRORLEVEL! equ 0 (
  set /a CHECKS_PASSED+=1
) else (
  set /a CHECKS_FAILED+=1
)
echo.

call "%~dp0setup\check-web-dependencies.bat"
if !ERRORLEVEL! equ 0 (
  set /a CHECKS_PASSED+=1
) else (
  set /a CHECKS_FAILED+=1
)
echo.

echo Useful files:
echo   windows\.env.bat          - optional Python override ^(not committed^)
echo   windows\.env.bat.example  - template
echo   windows\SETUP.md          - Windows walkthrough
echo.

:summary
echo ========================================
echo Summary
echo ========================================
echo.
echo Passed: !CHECKS_PASSED!
echo Failed: !CHECKS_FAILED!
echo Warnings: !CHECKS_WARNED!
echo.

if !CHECKS_FAILED! equ 0 (
  echo [OK] All required checks passed.
  echo.
  echo Next: run start-all.bat   ^(daemon + UI^)
  echo    or: start-daemon.bat and start-ui.bat in two windows
  echo.
) else (
  echo [ERROR] Some checks failed. Fix the errors above and run again.
  echo.
)

exit /b %CHECKS_FAILED%
