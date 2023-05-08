from netmiko import ConnectHandler

def send_config_commands(router_ips, username, password, commands):
    for i, router_ip in enumerate(router_ips):
        # Define the device parameters for Netmiko
        device = {
            'device_type': 'cisco_ios',
            'ip': router_ip,
            'username': username,
            'password': password
        }

        # Connect to the router and send configuration commands
        with ConnectHandler(**device) as net_connect:
            output = net_connect.send_config_set(commands)

        # Print the output of the configuration commands for each router
        print(f"Output for router router{i}:\n{output}\n")

