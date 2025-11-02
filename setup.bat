@echo off
REM Setup script for Windows

echo ========================================
echo Mass Spectrometry Data Processor Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed. Please install Python 3.7 or higher.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Display Python version
echo [OK] Python is installed
python --version
echo.

REM Create virtual environment
echo [1/3] Creating virtual environment...
python -m venv venv
echo [OK] Virtual environment created
echo.

REM Install dependencies
echo [2/3] Installing dependencies...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip >nul 2>&1
python -m pip install -r requirements.txt
echo [OK] Dependencies installed
echo.

REM Create directory structure if needed
echo [3/3] Setting up directory structure...
if not exist "input" mkdir input
if not exist "output" mkdir output
if not exist "scripts" mkdir scripts
if not exist "utils" mkdir utils
echo [OK] Directory structure ready
echo.

echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo To get started:
echo   1. Place your CSV file in the 'input' directory and rename it to 'data.csv'
echo   2. Activate the virtual environment: venv\Scripts\activate.bat
echo   3. Run a script: python scripts\01_remove_header_lines.py
echo.
pause
