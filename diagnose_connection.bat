@echo off
REM Diagnostic script to identify firewall and connection issues

setlocal enabledelayedexpansion

cls
echo.
echo ================================================
echo Connection Diagnostic Tool
echo ================================================
echo.

REM Get Device IP
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /i "IPv4"') do (
    set "IP=%%a"
    goto :found_ip
)

:found_ip
set "IP=%IP: =%"

echo Device A Information:
echo =====================
echo IP Address: %IP%
echo.

REM Check if server is running
echo Checking if Flask server is running on port 5000...
netstat -ano | findstr ":5000" > nul
if %errorlevel% equ 0 (
    echo [OK] Server appears to be RUNNING on port 5000
    echo.
) else (
    echo [ERROR] Server is NOT running on port 5000!
    echo Please start it with: python run.py
    echo.
)

REM Check firewall rule
echo Checking Windows Firewall...
echo ============================
netsh advfirewall firewall show rule name="Python Chat App Port 5000" > nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Firewall rule EXISTS for port 5000
) else (
    echo [WARNING] No firewall rule found!
    echo You need to run: open_firewall.bat (as administrator)
)

echo.
echo Firewall Status:
echo ================
netsh advfirewall show allprofiles | findstr /i "state"

echo.
echo Open Ports (listening):
echo ========================
netstat -ano | findstr "LISTENING" | findstr ":50"

echo.
echo Next Steps:
echo ===========
echo.
echo If server is running and firewall is open:
echo 1. On Device B, try: http://%IP%:5000
echo 2. If that fails, try testing connection:
echo    - From Device B Command Prompt: ping %IP%
echo    - From Device B Command Prompt: telnet %IP% 5000
echo.
echo If server is NOT running:
echo 1. Open Command Prompt
echo 2. Navigate to: cd "e:\Web scraping\chat_app"
echo 3. Run: python run.py
echo.
echo If firewall rule is missing:
echo 1. Right-click: open_firewall.bat
echo 2. Select: "Run as administrator"
echo 3. Click: "Yes" when prompted
echo.
pause
