import subprocess

def get_last_5_syslog_messages(router_ips):

    # Create a dictionary to hold the last 5 syslog messages for each router
    last_5_syslog_messages = {}

    # Loop through each router
    for router_ip in router_ips:
        # Use grep to extract the last 5 syslog messages for the router from the syslog file
        command = f"grep {router_ip} /var/log/syslog | tail -n 5"
        output = subprocess.check_output(command, shell=True, universal_newlines=True)

        # Add the last 5 syslog messages to the dictionary for this router
        last_5_syslog_messages[router_ip] = output.strip().splitlines()

    # Print the last 5 syslog messages for each router
    for router_ip, syslog_messages in last_5_syslog_messages.items():
        print(f"Last 5 syslog messages for router {router_ip}:")
        for message in syslog_messages:
            print(f"\t{message}")