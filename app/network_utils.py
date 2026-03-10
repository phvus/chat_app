"""Network utilities for getting device IP addresses and connectivity information"""
import socket
import os
from typing import List, Dict, Tuple

def get_local_ip() -> str:
    """
    Get the local IPv4 address of this device on the LAN
    Returns the primary network interface IP
    """
    try:
        # Connect to an external address (doesn't actually send data)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        ip = sock.getsockname()[0]
        sock.close()
        return ip
    except Exception:
        try:
            # Fallback: use hostname resolution
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            return ip
        except Exception:
            return "127.0.0.1"

def get_all_local_ips() -> List[str]:
    """Get all local IP addresses for this device"""
    ips = []
    try:
        hostname = socket.gethostname()
        # Get all addresses associated with hostname
        addresses = socket.getaddrinfo(hostname, None)
        for addr_info in addresses:
            ip = addr_info[4][0]
            if ip not in ips and not ip.startswith("127."):
                ips.append(ip)
    except Exception:
        pass
    
    # Always include localhost
    if "127.0.0.1" not in ips:
        ips.append("127.0.0.1")
    
    return ips

def get_network_info(port: int = 5000, host: str = "0.0.0.0") -> Dict:
    """
    Get complete network connectivity information
    """
    local_ip = get_local_ip()
    all_ips = get_all_local_ips()
    
    info = {
        "primary_ip": local_ip,
        "all_ips": all_ips,
        "port": port,
        "localhost_url": f"http://localhost:{port}",
        "network_url": f"http://{local_ip}:{port}",
        "all_urls": [f"http://{ip}:{port}" for ip in all_ips],
        "device_name": socket.gethostname()
    }
    
    return info

def print_network_info(port: int = 5000, host: str = "0.0.0.0") -> None:
    """Print formatted network connectivity information to console"""
    info = get_network_info(port, host)
    
    print("\n" + "="*60)
    print("🚀 CHAT APPLICATION STARTED")
    print("="*60)
    print(f"\n📱 Device Name: {info['device_name']}")
    print(f"🔌 Primary LAN IP: {info['primary_ip']}")
    print(f"🌐 Port: {info['port']}\n")
    
    print("📍 Access URLs:")
    print(f"  • Local (this computer):    {info['localhost_url']}")
    print(f"  • LAN (other devices):      {info['network_url']}")
    
    if len(info['all_ips']) > 1:
        print(f"\n📡 Other available addresses:")
        for ip in info['all_ips']:
            if ip != "127.0.0.1":
                print(f"  • http://{ip}:{info['port']}")
    
    print("\n💡 Connection Guide:")
    print("  • From THIS device: Visit http://localhost:5000")
    print(f"  • From OTHER devices on same network: Visit http://{info['primary_ip']}:5000")
    print("  • Make sure both devices are on the same WiFi network!")
    print("\n🔐 Firewall Notice:")
    print("  • If you can't connect from another device, check your firewall settings")
    print(f"  • Allow port {port} through Windows Firewall (or your OS firewall)")
    
    print("\n⌨️  Press Ctrl+C to stop the server\n")
    print("="*60 + "\n")

def check_firewall_open(host: str = "0.0.0.0", port: int = 5000) -> bool:
    """Check if the specified port is accessible"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(("127.0.0.1", port))
        sock.close()
        return result == 0
    except Exception:
        return False
