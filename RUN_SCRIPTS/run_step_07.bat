@echo off
cd ..
echo ========================================
echo  Executing Step 07: Calculate BFF
echo ========================================
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run the script
python scripts\07_calculate_bff.py

echo.
echo ========================================
echo  Script finished!
echo ========================================
echo.
pause
