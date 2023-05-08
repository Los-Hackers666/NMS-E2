from netmiko import ConnectHandler

def check_security_compliance(router_ips, username, password):
    device_params = {
        'device_type': 'cisco_ios',
        'username': username,
        'password': password
    }   

    # Define SSH configuration commands
    ssh_config_cmds = [
        "ip domain-name hierritos.net",
        "crypto key generate rsa modulus 1024",
        "line vty 0 4",
        "transport input ssh",
        "login local",
        "exit",
    ]

    # Loop over routers
    for router_ip in router_ips:
        # Connect to router
        device_params["ip"] = router_ip
        with ConnectHandler(**device_params) as conn:
            # Check loopback interfaces
            output = conn.send_command("show ip int brief | include Loopback")
            for line in output.splitlines():
                if "Loopback0" in line:
                    continue
                fields = line.split()
                ifname = fields[0]
                ifstatus = fields[4]
                if ifstatus == "up":
                    print(f"Interface {ifname} on router {router_ip} is on. Turning it off...")
                    output = conn.send_command(f"show running-config interface {ifname}")
                    if "ip address" in output:
                        print(f"Interface {ifname} on router {router_ip} has an IP address configured. Removing it...")
                        conn.send_config_set([f"interface {ifname}", "no ip address", "shutdown"])
                else:
                    print(f"No Loopback interface found on {router_ip} turned on.")    
            
            # Check SSH configuration
            output = conn.send_command("show running-config | include ^line vty|^username")
            ssh_config_found = False
            for line in output.splitlines():
                if "line vty" in line:
                    ssh_config_found = True
                    break
            if not ssh_config_found:
                print(f"SSH configuration not found on router {router_ip}. Adding it...")
                config_cmds = ["enable", "configure terminal"] + ssh_config_cmds
                config_cmds.append(f"username {username} privilege 15 password {password}")
                conn.send_config_set(config_cmds)
            else:
                print(f"SSH configuration found on router {router_ip}. No action needed.")
            
            # Check username and password
            output = conn.send_command("show running-config | include ^username")
            user_found = False
            for line in output.splitlines():
                if f"username {username} privilege 15 password" in line:
                    user_found = True
                    break
            if not user_found:
                print(f"User {username} not found on router {router_ip}. Adding it...")
                conn.send_config_set([f"username {username} privilege 15 password {password}"])
            else:
                print(f"User {username} found on router {router_ip}. No action needed.")
