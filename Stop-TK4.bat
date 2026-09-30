@echo off
echo ============================================
echo   MVS 3.8J TK4- Environment Stopper
echo ============================================
echo.
powershell.exe -ExecutionPolicy Bypass -File "%~dp0Stop-TK4.ps1"
echo.
pause
