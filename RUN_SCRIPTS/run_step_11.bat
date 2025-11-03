@echo off
cd ..
echo ========================================
echo  Executing Step 11: Remove QC Noise
echo ========================================
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run the script
python scripts\11_remove_qc_noise.py

echo.
echo ========================================
echo  Script finished!
echo ========================================
echo.
pause
