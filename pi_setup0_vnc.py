import subprocess
import time

step0 = "sudo apt-get update && sudo apt-get upgrade --yes"

# Installing VNC
step1 = "sudo apt install realvnc-vnc-server realvnc-vnc-viewer --yes"
step2 = "sudo reboot"


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


# Setup Start
print("Welcome to RaspberryPi VNC setup.")
setup_input = input("Starting setup? (Y/n): ")

if setup_input.lower() == 'yes' or setup_input.lower() == 'y':
    # Running updates
    command_line(step0)

    # Install VNC Server connection
    command_line(step1)
    print("#################################################################\n")
    print("If no error occurred, setup completed. System will reboot in 10 s\n")
    print("#################################################################\n")
    time.sleep(10)
    command_line(step2)

else:
    print("Setup stopped")
