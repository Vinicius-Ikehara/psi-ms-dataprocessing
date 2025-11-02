@echo off
cd ..
echo ========================================
echo  Executing Step 03: Create Aligned List
echo ========================================
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run the script
python scripts\03_create_aligned.py

echo.
echo ========================================
echo  Script finished!
echo ========================================
echo.
pause
