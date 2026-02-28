@echo off
title Building NHL Trade Analyzer
echo ============================================
echo   Building NHL Trade Analyzer Executable
echo ============================================
echo.

cd /d "%~dp0"

echo Installing PyInstaller if needed...
pip install pyinstaller

echo.
echo Building executable (this may take a few minutes)...
echo.

pyinstaller --name "NHL Trade Analyzer" --onefile --windowed --add-data "src;src" --hidden-import customtkinter --hidden-import openai --hidden-import PIL --collect-all customtkinter main.py

echo.
echo ============================================
if exist "dist\NHL Trade Analyzer.exe" (
    echo   BUILD SUCCESSFUL!
    echo   Your .exe is at: dist\NHL Trade Analyzer.exe
    echo.
    echo   You can copy that file anywhere and run it.
) else (
    echo   BUILD FAILED - check the output above for errors
)
echo ============================================
echo.
pause
