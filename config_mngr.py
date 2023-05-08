import netmiko
import time
import os

def backup_configs(routers, username, password, backup_dir):
    backup_dir = "/home/py/nms/conf_mngr"

    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    for i, router in enumerate(routers):
        try:
            connection = netmiko.ConnectHandler(device_type="cisco_ios", ip=router, username=username, password=password)
            config = connection.send_command("show running-config")
            backup_filename = f"router{i}_config_{time.strftime('%Y%m%d-%H%M%S')}.txt"
            with open(f"{backup_dir}/{backup_filename}", "w") as backup_file:
                backup_file.write(config)
            print(f"Configuration backup for router{i} successful.")
        except Exception as e:
            print(f"Error backing up configuration for router{i}: {e}")
        finally:
            connection.disconnect()