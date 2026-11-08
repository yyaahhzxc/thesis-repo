@echo off
title Ex-Ante Davao City Semantic Conflict Detection Prototype
echo ====================================================================
echo Starting Ex-Ante Semantic Conflict Detection System Prototype...
echo ====================================================================

if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" run_demo.py %*
) else if exist "D:\Documents\davao_ocr_thesis\venv\Scripts\python.exe" (
    "D:\Documents\davao_ocr_thesis\venv\Scripts\python.exe" run_demo.py %*
) else (
    python run_demo.py %*
)

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [!] Server exited with an error.
    pause
)
