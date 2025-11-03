@echo off
cd ..
echo ========================================
echo  Executing Step 08: Subtract BFF
echo ========================================
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run the script
python scripts\08_subtract_bff.py

echo.
echo ========================================
echo  Script finished!
echo ========================================
echo.
pause
