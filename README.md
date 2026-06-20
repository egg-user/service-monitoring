# Linux Service Monitoring Automation

## Overview

Python automation script that monitors Linux services across multiple servers through SSH connections. The script checks service availability, evaluates service health status, and generates a monitoring report for operational visibility.

## Features

* Read server inventory from file
* Read monitored services list from file
* SSH connectivity validation
* Service status monitoring using systemd
* Health evaluation based on service state
* Multi-server monitoring
* Unreachable host detection
* Automated report generation
* Monitoring summary statistics

## Technologies

* Python
* Paramiko
* Linux
* SSH
* Systemd

## Project Structure

```
service-monitoring/
│
├── main.py
├── servers.exaple.txt
├── services.txt
├── README.md
├── .gitignore
│
└── report/
    └── service_monitor_YYYYMMDD.txt
```

## Example Input

### servers.example.txt

```
IP_ADDRESS
192.168.1.138
192.168.1.178
```

### services.txt

```
SERVICE_NAME
sshd
docker
nginx
```

## Example Output

```
==================================================
SERVICE MONITORING REPORT
==================================================

Generated: 2026-06-20 18:30:00

--------------------------------------------------
Server : 192.168.1.138

Service         Status          Health Status
--------------------------------------------------
sshd            active          Healthy
docker          inactive        Warning
nginx           inactive        Warning

--------------------------------------------------
Server : 192.168.1.178

Service         Status          Health Status
--------------------------------------------------
sshd            Unreachable     Unreachable
docker          Unreachable     Unreachable
nginx           Unreachable     Unreachable

==================================================
Summary
==================================================

Total Server      : 2
Total Services    : 6
Healthy           : 1
Warning           : 2
Critical          : 0
Unreachable       : 3
```

## Health Evaluation Logic

| Service Status           | Health Status |
| ------------------------ | ------------- |
| active                   | Healthy       |
| inactive (sshd)          | Critical      |
| inactive (docker, nginx) | Warning       |
| SSH failed               | Unreachable   |
