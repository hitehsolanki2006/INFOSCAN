# network_info.py
import socket
import psutil
import requests

def get_network_info():
    info = {}

    # Hostname and IP
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    info["Hostname"] = hostname
    info["Local IP"] = local_ip

    # Public IP
    try:
        public_ip = requests.get('https://api.ipify.org').text
        info["Public IP"] = public_ip
    except Exception:
        info["Public IP"] = "Could not fetch"

    # Interfaces Info
    interfaces = {}
    addrs = psutil.net_if_addrs()
    stats = psutil.net_if_stats()
    for iface_name, iface_addresses in addrs.items():
        iface_info = {"Status": "Up" if stats[iface_name].isup else "Down"}
        for addr in iface_addresses:
            if str(addr.family) == 'AddressFamily.AF_INET':
                iface_info["IPv4"] = addr.address
            elif str(addr.family) == 'AddressFamily.AF_PACKET':
                iface_info["MAC"] = addr.address
        interfaces[iface_name] = iface_info
    info["Interfaces"] = interfaces

    # Gateway Info (simplified)
    gateway_summary = {}
    for iface, stat in stats.items():
        gateway_summary[iface] = {
            "Status": "Up" if stat.isup else "Down",
            "Speed": f"{stat.speed} Mbps",
            "MTU": stat.mtu
        }
    info["Gateway Info"] = gateway_summary

    # DNS Servers
    try:
        with open(r"C:\Windows\System32\drivers\etc\resolv.conf") as f:
            dns = [line.strip().split()[-1] for line in f if line.startswith("nameserver")]
    except:
        dns = []
    if not dns:
        dns = psutil.net_if_addrs().get("Wi-Fi", [])
    info["DNS Servers"] = socket.gethostbyname_ex(socket.gethostname())[2]

    return info
