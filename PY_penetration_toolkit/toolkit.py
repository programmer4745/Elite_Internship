from core.port_scanner import scan_ports
from core.brute_forcer import ssh_brute_force

def main():
    print("=== PyPentestToolkit ===")
    target = input("Target IP: ")
    print(f"Open Ports on {target}: {scan_ports(target)}")

    choice = input("Run brute force? (y/n): ")
    if choice.lower() == 'y':
        user = input("Username: ")
        with open("wordlists/common_passwords.txt") as f:
            passwords = f.readlines()
        ssh_brute_force(target, user, passwords)

if __name__ == "__main__":
    main()
