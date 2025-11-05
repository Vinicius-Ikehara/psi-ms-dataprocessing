@echo off
cd ..
echo ========================================
echo  OPTIONAL: Apply Noise Threshold
echo ========================================
echo.
echo WARNING: This will modify 04_aligned_filled.csv
echo Run this AFTER Step 04 and BEFORE Step 05
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run the script
python scripts\noise_threshold.py

echo.
echo ========================================
echo  Script finished!
echo ========================================
echo.
pause
