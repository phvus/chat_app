@echo off
setlocal enabledelayedexpansion

REM Check if Python is installed
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo Python found. Creating Virtual Environment...
python -m venv venv

REM Check if venv was created successfully
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Failed to create virtual environment!
    echo Please ensure you have enough disk space and proper permissions.
    pause
    exit /b 1
)

echo.
echo Activating Virtual Environment...
call venv\Scripts\activate.bat

REM Check if activation worked
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment!
    pause
    exit /b 1
)

echo.
echo Installing Dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: Failed to install dependencies!
    pause
    exit /b 1
)

echo.
echo ============================================
echo Setup Complete! Virtual environment is ready.
echo ============================================
echo.
echo To activate the virtual environment in the future, run:
echo   venv\Scripts\activate.bat
echo.
echo To run the application:
echo   python run.py
echo.
pause
endlocal
