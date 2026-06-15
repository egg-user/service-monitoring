import os
import paramiko

base_path = os.getcwd()
servers_path = os.path.join(base_path, "servers.txt")
services_path = os.path.join(base_path, "services.txt")

def read_servers_path():
    servers_ip = []
    with open(servers_path, "r") as file:
        next(file)
        for server in file:
            servers_ip.append(server.strip())
    return servers_ip

def read_services_path():
    services = []
    with open(services_path, "r") as file:
        next(file)
        for service in file:
            services.append(service.strip())
    return services

def check_service(servers_ip, services):
    try:
        services_status = []
        for ip in servers_ip:
            for service in services:
                username = "egg"
                host = ip
                password = "change"
                client = paramiko.client.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(host, username=username, password=password)
                stdin, stdout, stderr = client.exec_command(f"systemctl is-active {service}")
                service_server = stdout.read().decode().strip()
                services_status.append((
                    ip, service, service_server
                ))
        print(services_status)
    
    except:
        print("Host Unreachable")

        
servers_ip = read_servers_path()
services = read_services_path()
check_service(servers_ip, services)
