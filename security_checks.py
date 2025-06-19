# security_checks.py
import platform
import socket
import subprocess
import psutil

def check_firewall_status():
    if platform.system() == "Windows":
        try:
            result = subprocess.run(
                ["netsh", "advfirewall", "show", "allprofiles"],
                capture_output=True, text=True
            )
            return result.stdout
        except Exception as e:
            return f"Firewall check failed: {e}"
    else:
        return "Firewall check: Not supported on this OS"

def scan_ports(host='127.0.0.1', ports=[21, 22, 23, 80, 443, 3306]):
    open_ports = []
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((host, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    return open_ports

def get_security_info():
    info = {}

    # Firewall
    info["Firewall Status"] = check_firewall_status()

    # Open Ports
    open_ports = scan_ports()
    info["Open Ports (localhost)"] = open_ports if open_ports else "No common ports open"

    return info
