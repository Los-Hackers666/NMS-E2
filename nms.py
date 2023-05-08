import sys
import argparse
from ipam import extract_ip_addresses
from config_mngr import backup_configs
from change_mngr import send_config_commands
from log_analyzer import get_last_5_syslog_messages
from sec_compliance import check_security_compliance
from config_comparison import config_comparison

parser = argparse.ArgumentParser(description="Network Management System")

subparsers = parser.add_subparsers(dest="command", help="NMS commands")

# IPAM command
ipam_parser = subparsers.add_parser("ipam", help="IP Address Management")
ipam_parser.add_argument("router_ips", nargs="+", help="List of router IP addresses")
ipam_parser.add_argument("-u", "--username", default="netadmin", help="Username for device access")
ipam_parser.add_argument("-p", "--password", default="ola", help="Password for device access")

# Configuration Management command
conf_parser = subparsers.add_parser("backup", help="Configuration Management")
conf_parser.add_argument("router_ips", nargs="+", help="List of router IP addresses")
conf_parser.add_argument("-u", "--username", default="netadmin", help="Username for device access")
conf_parser.add_argument("-p", "--password", default="ola", help="Password for device access")
conf_parser.add_argument("-d", "--dir", default="/home/py/nms/conf_mngr", help="Directory to save configuration backups")

# Change Management command
change_parser = subparsers.add_parser("config", help="Change Management")
change_parser.add_argument("router_ips", nargs="+", help="List of router IP addresses")
change_parser.add_argument("-u", "--username", default="netadmin", help="Username for device access")
change_parser.add_argument("-p", "--password", default="ola", help="Password for device access")
change_parser.add_argument("-c", "--commands", nargs="+", help="List of configuration commands to send to routers")

# Log Analyzer command
log_parser = subparsers.add_parser("log", help="Log Analyzer")
log_parser.add_argument("router_ips", nargs="+", help="List of router IP addresses")

# Compliance/Security Management command
sec_parser = subparsers.add_parser("security", help="Compliance/Security Management")
sec_parser.add_argument("router_ips", nargs="+", help="List of router IP addresses")
sec_parser.add_argument("-u", "--username", default="netadmin", help="Username for device access")
sec_parser.add_argument("-p", "--password", default="ola", help="Password for device access")

# Configuration Comparison command
cmp_parser = subparsers.add_parser("compare", help="Configuration Comparison")
cmp_parser.add_argument("router_ips", nargs=2, help="List of 2 router IP addresses for comparison")
cmp_parser.add_argument("-u", "--username", default="netadmin", help="Username for device access")
cmp_parser.add_argument("-p", "--password", default="ola", help="Password for device access")

if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    sys.exit(1)

args = parser.parse_args()

# Call the appropriate function based on the command provided
if args.command == "ipam":
    extract_ip_addresses(args.router_ips, args.username, args.password)

elif args.command == "backup":
    backup_configs(args.router_ips, args.username, args.password, args.dir)

elif args.command == "config":
    send_config_commands(args.router_ips, args.username, args.password, args.commands)

elif args.command == "log":
    get_last_5_syslog_messages(args.router_ips)

elif args.command == "security":
    check_security_compliance(args.router_ips, args.username, args.password)

elif args.command == "compare":
    router1_ip, router2_ip = args.router_ips
    router1_username, router2_username = args.username, args.username
    router1_password, router2_password = args.password, args.password
    config_comparison(router1_ip, router1_username, router1_password, router2_ip, router2_username, router2_password)