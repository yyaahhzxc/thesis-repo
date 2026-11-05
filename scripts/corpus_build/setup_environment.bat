@echo off
REM One-Click Environment Setup Launcher for Windows
REM Bypasses PowerShell ExecutionPolicy restrictions automatically
title Thesis Environment Setup
cd /d "%~dp0\.."
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0setup_environment.ps1"
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Setup encountered an issue. Review the output above.
)
pause
