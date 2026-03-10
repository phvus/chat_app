@echo off
REM Script to test network connectivity and display network information

setlocal enabledelayedexpansion

cls
echo.
echo ================================================
echo Network Connectivity Test
echo ================================================
echo.

REM Get the local IP
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /i "IPv4"') do (
    set "IP=%%a"
    goto :found_ip
)

:found_ip
set "IP=%IP: =%"

echo Your Device IP Address: %IP%
echo.
echo Testing connectivity...
echo.

REM Test if server is running
netstat -ano | findstr ":5000" >nul
if %errorlevel% equ 0 (
    echo ✓ Server appears to be running on port 5000
    echo.
    echo You can access the chat from another device at:
    echo   http://%IP%:5000
    echo.
    echo Make sure to use this IP address in your browser
    echo from another device on the same network.
) else (
    echo ✗ Server is NOT running on port 5000
    echo.
    echo Please start the server first:
    echo   python run.py
)

echo.
echo ================================================
echo Network Diagnostic Info
echo ================================================
echo.
ipconfig
echo.
pause
