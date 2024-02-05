import subprocess
import re
import time

# Required variables
pattern = re.compile(r"""
                    ^                       # Start of the string
                    (25[0-5]|               # Match 250-255
                    2[0-4][0-9]|            # Match 200-249
                    [01]?[0-9][0-9]?)       # Match 0-199
                    \.                      # Dot separator
                    (25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.
                    (25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.
                    (25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?) 
                    $                       # End of the string
                    """, re.VERBOSE)

file_location_eth = '/etc/systemd/network/eth0.network'
file_location_wifi = '/etc/systemd/network/wlan0.network'

# Preparation steps/Deactivation of other services
setup_steps = [
    "sudo update-rc.d networking remove",
    "sudo systemctl stop dhcpcd",
    "sudo systemctl disable dhcpcd",
    "sudo apt install systemd-resolved -y",
    "sudo systemctl enable systemd-resolved",
    "sudo systemctl start systemd-resolved",
    "sudo ln -sf /run/systemd/resolve/resolv.conf /etc/resolv.conf",
    "sudo systemctl enable systemd-networkd"
]


# Function to execute command line
def execute_command(step):
    try:
        result = subprocess.run(step, shell=True, text=True, capture_output=True)
        if result.stdout != '':
            print(f"~ $ Commanding: {step}")
            print("\n")
            print("Command Output:")
            print(result.stdout)
        else:
            print('\n')
        if result.returncode == 0:
            print("Command executed successfully.")
        else:
            print(f"Failed commanding: {step}")
            print(f"Command failed with return code {result.returncode}.")
            print("Error Output:")
            print(result.stderr)
    except Exception as ex:
        print(f"An error occurred: {ex}")


# Function to validate and input IP address
def get_valid_ip(prompt):
    while True:
        ip_input = input(prompt)
        if not re.match(pattern, ip_input):
            print("The provided IP address is not correct, please enter a valid IPv4 address.")
        else:
            print(f"Provided IP Address is: {ip_input}")
            return ip_input


# Function to setup WiFi configuration
def setup_wifi():
    # Prompt user for WiFi SSID and password
    wifi_ssid = input("Enter WiFi SSID: ")
    wifi_password = input("Enter WiFi password: ")
    # Write WiFi configuration file
    try:
        with open(file_location_wifi, 'w') as wifi_file:
            wifi_file.write(
                f'[Match]\nName=wlan0\n[Network]\nDHCP=yes\n[WiFi]\nSSID={wifi_ssid}\nPassword={wifi_password}\n')
    except Exception as e:
        print(f"An error occurred while writing WiFi configuration file: {e}")


# Enable static or dynamic IP-address
print("Welcome to Raspberry Pi network interface setup.")
setup_input = input("Start setup? (Y/n): ")

if setup_input.lower() == 'yes' or setup_input.lower() == 'y':
    # Get static IP address and gateway for Ethernet
    eth_static_ip = get_valid_ip("Enter the required static IP address for Ethernet (e.g. 192.168.1.100): ")
    eth_gateway_ip = get_valid_ip("Enter the corresponding gateway for Ethernet (e.g. 192.168.1.1): ")

    # Execute setup steps
    for step in setup_steps:
        execute_command(step)

    # Write Ethernet IP address information to the network configuration file
    try:
        with open(file_location_eth, 'w') as settings_file:
            settings_file.write('[Match]\n'
                                'Name=eth0\n'
                                '[Network]\n'
                                f'Address={eth_static_ip}/24\n'
                                f'Gateway={eth_gateway_ip}\n'
                                f'DNS={eth_gateway_ip}\n'
                                )
    except Exception as ex:
        print(f"An error occurred while writing to the network configuration file: \n {ex}")

    # Start systemd-networkd
    execute_command("sudo systemctl start systemd-networkd")

    print("#################################################################\n")
    print("If no error occurred, Ethernet setup completed.\n")
    print("#################################################################\n")
    time.sleep(5)

    # Check if WiFi setup is needed
    wifi_setup_input = input("WiFi configuration setup needed? (Y/n): ")
    if wifi_setup_input.lower() == 'yes' or wifi_setup_input.lower() == 'y':
        # Get static IP address and gateway for WiFi
        wifi_static_ip = get_valid_ip("Enter the required static IP address for WiFi (e.g. 192.168.2.100): ")
        wifi_gateway_ip = get_valid_ip("Enter the corresponding gateway for WiFi (e.g. 192.168.2.1): ")
        setup_wifi()
        execute_command("sudo systemctl restart systemd-networkd")

    print("#################################################################\n")
    print("Setup completed. System will reboot in 10 seconds.\n")
    print("#################################################################\n")
    time.sleep(10)

    # Reboot the system
    execute_command("sudo reboot")

else:
    print("Setup stopped.")
