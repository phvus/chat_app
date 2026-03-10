@echo off
REM This script opens port 5000 in Windows Firewall
REM Run as administrator!

echo.
echo ================================================
echo Opening Windows Firewall for Port 5000...
echo ================================================
echo.

REM Check if running as admin
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: This script must be run as Administrator!
    echo.
    echo Steps:
    echo 1. Right-click on this file (open_firewall.bat)
    echo 2. Select "Run as administrator"
    echo 3. Click "Yes" when prompted
    echo.
    pause
    exit /b 1
)

echo Adding firewall rule for port 5000...
netsh advfirewall firewall add rule name="Python Chat App Port 5000" dir=in action=allow protocol=tcp localport=5000 description="Allow Flask chat app to accept connections from LAN devices"

if %errorlevel% equ 0 (
    echo.
    echo ✓ SUCCESS! Firewall rule added!
    echo.
    echo You can now:
    echo 1. Try to access the website from Device B
    echo 2. Use: http://[YOUR_IP_FROM_DEVICE_A]:5000
    echo.
    echo If it still doesn't work, try:
    echo - Restart the Flask server (Ctrl+C and python run.py again)
    echo - Check if both devices are on the same WiFi network
    echo.
) else (
    echo.
    echo ✗ FAILED to add firewall rule!
    echo Please check Windows Firewall settings manually.
    echo.
)

echo ================================================
pause
