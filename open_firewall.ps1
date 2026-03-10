# PowerShell script to open port 5000 in Windows Firewall
# Run as administrator!

# Check if running as admin
$isAdmin = [Security.Principal.WindowsIdentity]::GetCurrent().Groups -contains 'S-1-5-32-544'
if (-not $isAdmin) {
    Write-Host "❌ ERROR: This script must be run as Administrator!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Steps to run as administrator:" -ForegroundColor Yellow
    Write-Host "1. Right-click PowerShell"
    Write-Host "2. Select 'Run as administrator'"
    Write-Host "3. Run: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser"
    Write-Host "4. Then run this script again"
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "Opening Windows Firewall for Port 5000..." -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""

# Remove existing rule if it exists
Write-Host "Checking for existing firewall rules..."
$existingRule = Get-NetFirewallRule -DisplayName "Python Chat App Port 5000" -ErrorAction SilentlyContinue
if ($existingRule) {
    Write-Host "Removing existing rule..."
    Remove-NetFirewallRule -DisplayName "Python Chat App Port 5000" -ErrorAction SilentlyContinue
}

# Add new firewall rule
Write-Host "Adding new firewall rule for port 5000..."
try {
    New-NetFirewallRule `
        -DisplayName "Python Chat App Port 5000" `
        -Direction Inbound `
        -Action Allow `
        -Protocol TCP `
        -LocalPort 5000 `
        -Description "Allow Flask chat app to accept connections from LAN devices" `
        -ErrorAction Stop | Out-Null
    
    Write-Host ""
    Write-Host "✓ SUCCESS! Firewall rule created!" -ForegroundColor Green
    Write-Host ""
    Write-Host "You can now:" -ForegroundColor Yellow
    Write-Host "1. Try to access the website from Device B"
    Write-Host "2. Use: http://[YOUR_IP_FROM_DEVICE_A]:5000"
    Write-Host ""
    Write-Host "If it still doesn't work, try:" -ForegroundColor Yellow
    Write-Host "- Restart the Flask server (Ctrl+C and python run.py again)"
    Write-Host "- Check if both devices are on the same WiFi network"
    Write-Host ""
} catch {
    Write-Host ""
    Write-Host "❌ FAILED to add firewall rule!" -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please check Windows Firewall settings manually." -ForegroundColor Yellow
}

Write-Host "================================================" -ForegroundColor Green
Read-Host "Press Enter to close"
