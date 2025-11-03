@echo off
cd ..
echo ========================================
echo  Executing Step 10: Add QC Totals
echo ========================================
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run the script
python scripts\10_add_qc_totals.py

echo.
echo ========================================
echo  Script finished!
echo ========================================
echo.
pause
