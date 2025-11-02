@echo off
cd ..
echo ========================================
echo  Executing Step 01: Remove Header Lines
echo ========================================
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run the script
python scripts\01_remove_header_lines.py

echo.
echo ========================================
echo  Script finished!
echo ========================================
echo.
pause
