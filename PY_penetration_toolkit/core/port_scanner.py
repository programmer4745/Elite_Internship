import socket

def scan_ports(target, ports=[21, 22, 80, 443, 8080]):
    open_ports = []
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            if s.connect_ex((target, port)) == 0:
                open_ports.append(port)
    return open_ports
