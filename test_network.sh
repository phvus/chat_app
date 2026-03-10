#!/bin/bash

# Script to test network connectivity and display network information

clear

echo ""
echo "================================================"
echo "Network Connectivity Test"
echo "================================================"
echo ""

# Get the local IP
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -n1)
else
    # Linux
    IP=$(hostname -I | awk '{print $1}')
fi

echo "Your Device IP Address: $IP"
echo ""
echo "Testing connectivity..."
echo ""

# Test if server is running
if lsof -i :5000 > /dev/null 2>&1 || netstat -tuln 2>/dev/null | grep -q ":5000 "; then
    echo "✓ Server appears to be running on port 5000"
    echo ""
    echo "You can access the chat from another device at:"
    echo "  http://$IP:5000"
    echo ""
    echo "Make sure to use this IP address in your browser"
    echo "from another device on the same network."
else
    echo "✗ Server is NOT running on port 5000"
    echo ""
    echo "Please start the server first:"
    echo "  python run.py"
fi

echo ""
echo "================================================"
echo "Network Interface Information"
echo "================================================"
echo ""

if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    ifconfig
else
    # Linux
    ip addr
fi

echo ""
read -p "Press Enter to close..."
