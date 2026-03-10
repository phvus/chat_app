@echo off
echo Creating Virtual Environment...
python -m venv venv

echo.
echo Activating Virtual Environment...
call venv\Scripts\activate.bat

echo.
echo Installing Dependencies...
pip install -r requirements.txt

echo.
echo Setup Complete! Virtual environment is ready.
echo.
echo To activate the virtual environment in the future, run:
echo   venv\Scripts\activate.bat
echo.
echo To run the application:
echo   python run.py
echo.
pause
