# utils.py
import subprocess
import sys

required_packages = [
    "psutil",
    "requests",
    "fpdf",
    "shutil",
    "os",
    "datetime",
    "socket",
    "platform"
  
]

def install_missing_packages():
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            print(f"[🔧] Installing missing package: {package}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
