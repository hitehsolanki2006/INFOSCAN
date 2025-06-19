# system_info.py
import platform
import psutil
import shutil

def get_size(bytes, suffix="B"):
    # Format bytes to human-readable
    factor = 1024
    for unit in ["", "K", "M", "G", "T"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def get_system_info():
    info = {}

    # OS info
    info["OS"] = platform.system()
    info["OS Version"] = platform.version()
    info["Architecture"] = platform.machine()

    # CPU info
    info["Processor"] = platform.processor()
    info["CPU Cores (Logical)"] = psutil.cpu_count()
    info["CPU Cores (Physical)"] = psutil.cpu_count(logical=False)
    info["CPU Usage"] = f"{psutil.cpu_percent(interval=1)}%"

    # RAM info
    ram = psutil.virtual_memory()
    info["Total RAM"] = get_size(ram.total)
    info["Available RAM"] = get_size(ram.available)
    info["Used RAM"] = get_size(ram.used)
    info["RAM Usage"] = f"{ram.percent}%"

    # Disk info
    total, used, free = shutil.disk_usage("/")
    info["Disk Total"] = get_size(total)
    info["Disk Used"] = get_size(used)
    info["Disk Free"] = get_size(free)

    return info
