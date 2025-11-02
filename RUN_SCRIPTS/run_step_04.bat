@echo off
cd ..
echo ========================================
echo  Executing Step 04: Fill Aligned Intensities
echo ========================================
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run the script
python scripts\04_fill_aligned_intensities.py

echo.
echo ========================================
echo  Script finished!
echo ========================================
echo.
pause
