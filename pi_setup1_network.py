import subprocess
import re
import time

# SOURCE
# https://www.elektronik-kompendium.de/sites/raspberry-pi/1912151.htm
# TODO Implement Question for Wifi setup
# https://www.elektronik-kompendium.de/sites/raspberry-pi/1912221.htm


# TODO Update def command_line to setup0 level

# Required variables
static_ip = ''
netmask = ''
gateway = ''
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

step0 = "sudo apt-get update && sudo apt-get upgrade --yes"

# Preparation steps/Deactivation of other services
step1 = "sudo update-rc.d networking remove"
step2 = "sudo systemctl stop dhcpcd"
step3 = "sudo systemctl disable dhcpcd"

# Installing
step4 = "sudo apt install systemd-resolved -y"
step5 = "sudo systemctl enable systemd-resolved"
step6 = "sudo systemctl start systemd-resolved"

# Link creation
step7 = "sudo ln -sf /run/systemd/resolve/resolv.conf /etc/resolv.conf"

# Creating network data file
step8 = f"sudo nano {file_location_eth}"

#
step9 = "sudo systemctl enable systemd-networkd"
step10 = "sudo systemctl start systemd-networkd"

# Installing VNC
step11 = "sudo apt install realvnc-vnc-server realvnc-vnc-viewer --yes"
step12 = "sudo reboot"


def command_line(step):
    try:
        # Use subprocess to run the Bash command
        result = subprocess.run(step, shell=True, text=True, capture_output=True)
        print(f"~ $ Commanding: {step}")
        if result.stdout != '':
            print("\n")
            print("Command Output:")
            print(result.stdout)
        else:
            print('\n')
        # Check the return code to see if the command was successful
        if result.returncode == 0:
            print("Command executed successfully.")
        else:
            print(f"Failed commanding: {step}")
            print(f"Command failed with return code {result.returncode}.")
            print("Error Output:")
            print(result.stderr)
    except Exception as ex:
        print(f"An error occurred: {ex}")


# Enable static or dynamic IP-address
print("Welcome to RaspberryPi network interface setup.")
setup_input = input("Starting setup? (Y/n): ")

if setup_input.lower() == 'yes' or setup_input.lower() == 'y':
    # Entering IP address
    while True:
        ip_input = str(input("Enter the required static IP address (e.g. 192.168.1.100): "))
        # Passing just if the re.match condition is fulfilled and required information is provided in the correct form
        # if not the question is looped...
        if not re.match(pattern, ip_input):
            print("The provided IP address is not correct, please enter valid IPv4 address.")
        else:
            print(f"Provided IP Address is: {ip_input}")
            break

    # Entering IP gateway
    while True:
        ip_gateway = str(input("Enter the corresponding gateway (e.g. 192.168.1.0): "))
        # Passing just if the re.match condition is fulfilled and required information is provided in the correct form
        # if not the question is looped...
        if not re.match(pattern, ip_gateway):
            print("The provided IP address is not correct, please enter valid gateway address.")
        else:
            print(f"Provided IP Address is: {ip_gateway}")
            break

    command_line(step1)
    command_line(step2)
    command_line(step3)
    command_line(step4)
    command_line(step5)
    command_line(step6)
    command_line(step7)

    # Writing IP address information to created file
    try:
        with open(file_location_eth, 'a') as settings_file:
            settings_file.write('[Match]\n'
                                'Name=eth0\n'
                                '[Network]\n'
                                f'Address={static_ip}/24\n'
                                f'Gateway={gateway}\n'
                                f'DNS={gateway}\n'
                                )
    except Exception as e:
        print(f"An error occurred: {e}")

    command_line(step8)
    command_line(step9)

    print("#################################################################\n")
    print("If no error occurred, setup completed. System will reboot in 10 s\n")
    print("#################################################################\n")
    time.sleep(10)

    command_line(step12)

else:
    print("Setup stopped")
