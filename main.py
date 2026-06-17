import os
import paramiko
import getpass
import datetime

current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
current_date = datetime.datetime.now().date()


base_path = os.getcwd()
servers_path = os.path.join(base_path, "servers.txt")
services_path = os.path.join(base_path, "services.txt")
report_path = os.path.join(base_path, "report", f"service_monitor_{current_date}.txt")

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
    username = input("Input Your Username: ")
    password = getpass.getpass("Input Your Password: ")
    services_status = []
    for ip in servers_ip:
        try:
            host = ip

            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(host, username=username, password=password, timeout=5)
            for service in services:
                stdin, stdout, stderr = client.exec_command(f"systemctl is-active {service}")
                service_server = stdout.read().decode().strip()
                services_status.append((
                    ip, service, service_server
                ))
        except:
            for service in services:
                services_status.append((
                    ip, service, "Unreachable"
                ))
            print(f"Host {ip} Unreachable")
    
    return services_status

def evaluate_service_status(services_status):
    services_status_evaluate = []
    for ip, service, service_server in services_status:
        if service_server == "inactive":
            if service == "sshd":
                services_status_evaluate.append((
                    ip, service, service_server, "Critical"
                ))
            elif service == "docker" or service == "nginx":
                services_status_evaluate.append((
                    ip, service, service_server, "Warning"
                ))
        elif service_server == "active":
            services_status_evaluate.append((
                ip, service, service_server, "Healthy"
            ))
        else:
            services_status_evaluate.append((
                ip, service, service_server, "Unreachable"
            ))
    return services_status_evaluate

def generate_report(services_status_evaluate):
    previous_ip = ""
    servers_count = []
    healthy_count = []
    warning_count = []
    uncreachable_count = []
    with open(report_path, "w") as file:
        file.write(
            "==================================================\n"
            "SERVICE MONITORING REPORT\n"
            "==================================================\n\n"
            f"Generated: {current_time}\n\n"
        )
        for ip, service, service_status, health_status in services_status_evaluate:
            if ip != previous_ip:
                file.write(
                    "--------------------------------------------------\n"
                    f"Server : {ip}\n\n"
                )
                previous_ip = ip
            else:
                file.write(
                    f"{service}     {service_status}    {health_status}\n"
                )


                

        
servers_ip = read_servers_path()
services = read_services_path()
services_status = check_service(servers_ip, services)
services_status_evaluate = evaluate_service_status(services_status)
generate_report(services_status_evaluate)