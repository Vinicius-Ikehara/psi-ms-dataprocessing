@echo off
cd ..
echo ========================================
echo  Executing Step 09: Zero Negatives
echo ========================================
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run the script
python scripts\09_zero_negatives.py

echo.
echo ========================================
echo  Script finished!
echo ========================================
echo.
pause
