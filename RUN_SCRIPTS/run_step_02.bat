@echo off
cd ..
echo ========================================
echo  Executing Step 02: Round Mass Columns
echo ========================================
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run the script
python scripts\02_round_mass.py

echo.
echo ========================================
echo  Script finished!
echo ========================================
echo.
pause
