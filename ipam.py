from netmiko import ConnectHandler

def extract_ip_addresses(router_ips, username, password):
    # Define the device parameters for Netmiko
    device_params = {
        'device_type': 'cisco_ios',
        'username': username,
        'password': password
    }
    
    # Loop over routers and extract IP addresses
    ip_addresses_by_router = {}
    for router_ip in router_ips:
        device_params['ip'] = router_ip
        with ConnectHandler(**device_params) as net_connect:
            config = net_connect.send_command('show running-config')
        ip_addresses = []
        for line in config.splitlines():
            if 'ip address ' in line:
                ip = line.split(' ')[-2]
                ip_addresses.append(ip)
        ip_addresses_by_router[router_ip] = ip_addresses
    
    # Return a dictionary with the IP addresses for each router
    for router_ip, ip_addresses in ip_addresses_by_router.items():
        print(f"IP addresses for router {router_ip}:")
        for ip in ip_addresses:
            print(ip)
        print()
