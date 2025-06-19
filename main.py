# main.py
import os
from datetime import datetime
from system_info import get_system_info
from network_info import get_network_info
from security_checks import get_security_info
from report import save_pdf_report 

from utils import install_missing_packages
install_missing_packages()


def print_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(r"""
    ██╗███╗   ██╗███████╗ ██████╗       ███████╗ ██████╗ █████╗ ███╗   ██╗
    ██║████╗  ██║██╔════╝██╔═══██╗      ██╔════╝██╔════╝██╔══██╗████╗  ██║
    ██║██╔██╗ ██║█████╗  ██║   ██║      ███████╗██║     ███████║██╔██╗ ██║
    ██║██║╚██╗██║██╔══╝  ██║   ██║      ╚════██║██║     ██╔══██║██║╚██╗██║
    ██║██║ ╚████║██║     ╚██████╔╝      ███████║╚██████╗██║  ██║██║ ╚████║
    ╚═╝╚═╝  ╚═══╝╚═╝      ╚═════╝       ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝
    """)
    print("                             🛡️  I N F O S C A N  🛡️\n")
    print("            🛡️  INFOSCAN - Cybersecurity System Audit Tool v1.0 🛡️")
    print("          Lightweight Python CLI scanner for system, network, and firewall\n")

def run_audit():
    data = {}

    while True:
        print_banner()
        print("Select an option:")
        print("1. System Info")
        print("2. Network Info")
        print("3. Security Info")
        print("4. Generate Full Report")
        print("5. Exit")

        choice = input("\nEnter your choice (1-5): ")

        if choice == "1":
            from system_info import get_system_info
            sys_info = get_system_info()
            data["System Info"] = sys_info
            print("\n--- System Info ---")
            for k, v in sys_info.items():
                print(f"{k}: {v}")
            input("\nPress Enter to continue...")

            
        elif choice == "2":
            net_info = get_network_info()
            data["Network Info"] = net_info

            print("\n--- Network Info ---")
            print(f"Hostname: {net_info.get('Hostname')}")
            print(f"Local IP: {net_info.get('Local IP')}")
            print(f"Public IP: {net_info.get('Public IP')}")

            print("\nInterfaces:")
            interfaces = net_info.get("Interfaces", {})
            for iface, details in interfaces.items():
                print(f"  {iface}:")
                for k, v in details.items():
                    print(f"    {k}: {v}")

            print("\nGateway Info:")
            gateways = net_info.get("Gateway Info", {})
            for iface, ginfo in gateways.items():
                    print(f"  {iface}:")
                    for k, v in ginfo.items():
                        print(f"    {k}: {v}")

            print("\nDNS Servers:")
            dns_servers = net_info.get("DNS Servers", [])
            if isinstance(dns_servers, list):
                for dns in dns_servers:
                    print(f"  {dns}")
            else:
                print(f"  {dns_servers}")

            input("\nPress Enter to continue...")


        elif choice == "3":
            from security_checks import get_security_info
            sec_info = get_security_info()
            data["Security Info"] = sec_info

            print("\n--- 🔒 Security Info ---")
            for key, value in sec_info.items():
                if isinstance(value, list):
                    print(f"{key}:")
                    for item in value:
                        print(f"  - {item}")
                elif isinstance(value, dict):
                    print(f"{key}:")
                    for k, v in value.items():
                        print(f"  {k}: {v}")
                else:
                    print(f"{key}: {value}")

            input("\nPress Enter to continue...")


        elif choice == "4":
            if not data:
                print("⚠️  No data collected yet. Run options 1–3 before generating report.")
            else:
                from report import save_pdf_report
                path = save_pdf_report(data)
                print(f"\n✅ Report saved to: {path}")
                print(f"\n✅ PDF Report saved successfully!")

                input("\nPress Enter to continue...")


        elif choice == "5":
            print("Exiting... Stay secure! 🛡️")
            break
        else:
            print("Invalid option. Try again.")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    print_banner()
    run_audit()
