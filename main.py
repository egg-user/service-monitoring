import os
import paramiko
import getpass
import datetime

current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
current_date = datetime.datetime.now().strftime("%Y%m%d")


base_path = os.getcwd()
servers_path = os.path.join(base_path, "servers.example.txt")
services_path = os.path.join(base_path, "services.txt")
report_path = os.path.join(base_path, "report", f"service_monitor_{current_date}.txt")

def read_servers_path():
    """
    Read server IP addresses from servers.txt.

    Returns:
        list: Server IP addresses.
    """
    servers_ip = []
    with open(servers_path, "r") as file:
        next(file)
        for server in file:
            servers_ip.append(server.strip())
    return servers_ip

def read_services_path():
    """
    Read service names from services.txt.

    Returns:
        list: Service names.
    """
    services = []
    with open(services_path, "r") as file:
        next(file)
        for service in file:
            services.append(service.strip())
    return services

def check_service(servers_ip, services):
    """
    Connect to servers via SSH and check service status.

    Args:
        servers_ip (list): List of server IP addresses.
        services (list): List of services to monitor.

    Returns:
        list: Service monitoring results.
    """
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
        except Exception as e:
            for service in services:
                services_status.append((
                    ip, service, "Unreachable"
                ))
            print(f"Host {ip} Unreachable: {e}")
        finally:
            if client:
                client.close()
    
    return services_status

def evaluate_service_status(services_status):
    """
    Evaluate service health based on service status.

    Args:
        services_status (list): Raw service monitoring results.

    Returns:
        list: Service monitoring results with health status.
    """
    services_status_evaluate = []
    for ip, service, service_server in services_status:
        if service_server == "inactive":
            if service == "sshd":
                services_status_evaluate.append((
                    ip, service, service_server, "Critical"
                ))
            elif service in ["docker", "nginx"]:
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
    """
    Generate monitoring report and summary.

    Args:
        services_status_evaluate (list): Evaluated monitoring results.

    Returns:
        None
    """
    previous_ip = ""
    healthy_count = 0
    warning_count = 0
    critical_count = 0
    unreachable_count = 0
    servers_count = len(servers_ip)
    total_services_count = len(services_status_evaluate)
    with open(report_path, "w") as file:
        file.write(
            "==================================================\n"
            "SERVICE MONITORING REPORT\n"
            "==================================================\n\n"
            f"Generated: {current_time}\n\n"
        )
        for ip, service, service_status, health_status in services_status_evaluate:
            if ip != previous_ip:
                if previous_ip:
                    file.write("\n")
                file.write(
                    "--------------------------------------------------\n"
                    f"Server : {ip}\n\n"
                    f"{'Service':<15} {'Status':<15} {'Health Status'}\n"
                    "--------------------------------------------------\n"
                )
                previous_ip = ip

            file.write(
                f"{service:<15} {service_status:<15} {health_status}\n"
            )
                
            if health_status == "Healthy":
                healthy_count += 1
            elif health_status == "Warning":
                warning_count += 1
            elif health_status == "Critical":
                critical_count += 1
            elif health_status == "Unreachable":
                unreachable_count += 1
        file.write(
                "\n==================================================\n"
                "Summary\n"
                "==================================================\n\n"
                )
        file.write(
            f"Total Server      : {servers_count}\n"
            f"Total Services    : {total_services_count}\n"
            f"Healthy           : {healthy_count}\n"
            f"Warning           : {warning_count}\n"
            f"Critical          : {critical_count}\n"
            f"Unreachable       : {unreachable_count}\n"
        )



if __name__ == "__main__":
    """
    Main workflow.

    1. Read server list
    2. Read service list
    3. Check service status via SSH
    4. Evaluate service health
    5. Generate monitoring report
    """
    servers_ip = read_servers_path()
    services = read_services_path()

    services_status = check_service(
        servers_ip,
        services
    )

    services_status_evaluate = evaluate_service_status(
        services_status
    )

    generate_report(
        services_status_evaluate,
    )

    print("\nReport generated successfully:")
    print(report_path)