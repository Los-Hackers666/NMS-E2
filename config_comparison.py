from netmiko import ConnectHandler
from difflib import ndiff

def config_comparison(router1_ip, router1_username, router1_password, router2_ip, router2_username, router2_password):
    # Define the device parameters for Netmiko
    device1 = {
        'device_type': 'cisco_ios',
        'ip': router1_ip,
        'username': router1_username,
        'password': router1_password
    }

    device2 = {
        'device_type': 'cisco_ios',
        'ip': router2_ip,
        'username': router2_username,
        'password': router2_password
    }

    # Connect to the routers and get the running configuration
    with ConnectHandler(**device1) as net_connect1, ConnectHandler(**device2) as net_connect2:
        config1 = net_connect1.send_command('show running-config')
        config2 = net_connect2.send_command('show running-config')

    # Compare the configurations using ndiff
    diff = ndiff(config1.splitlines(), config2.splitlines())
    print('\n'.join(diff))

