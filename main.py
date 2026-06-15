import os

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

        
servers_ip = read_servers_path()
services = read_services_path()
print(services)
