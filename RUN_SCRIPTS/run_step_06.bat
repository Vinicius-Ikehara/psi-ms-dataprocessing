@echo off
cd ..
echo ========================================
echo  Executing Step 06: Remove Zero Rows
echo ========================================
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run the script
python scripts\06_remove_zero_rows.py

echo.
echo ========================================
echo  Script finished!
echo ========================================
echo.
pause
