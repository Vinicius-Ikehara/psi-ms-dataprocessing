@echo off
cd ..
echo ========================================
echo  Executing Step 05: Clean Aligned
echo ========================================
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run the script
python scripts\05_clean_aligned.py

echo.
echo ========================================
echo  Script finished!
echo ========================================
echo.
pause
