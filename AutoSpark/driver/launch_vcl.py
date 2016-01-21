import os
import socket
import subprocess
import sys
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
vcl_LAUNCHER_DIR = BASE_DIR + "/../connector/vcl/"
ANSIBLE_DIR = BASE_DIR + "/../Ansible/playbooks/"


def install_packages(filename):

    with open(filename) as req_file:
        for package in req_file.readlines():
            if package != "\n":
                cmd = 'sudo pip install {0}'
                cmd_fmt = cmd.format(package)
                subprocess.call(cmd_fmt, shell=True)


def execute(command):
    print("Executing Command" + command)
    subprocess.call(command, shell=True)


def launch(args):
    # Moving to the vcl Launcher dir
    os.chdir(vcl_LAUNCHER_DIR)

    # Getting the IP Address of machine
    ip_addr = socket.gethostbyname(socket.gethostname())
    print("IP Address: " + ip_addr)

    # Setting key name to ipaddress & location

    key_name = ip_addr
    name = args[0]
    count = args[1]

    # Running python command
    cmd_format = "python ec2_connector.py --name {0} --count {1} --key_name {2}"
    command = cmd_format.format(name, count, key_name)

    execute(command)
    # subprocess.call(command, shell=True)

    # Wait for instance to be ssh ready
    print("Waiting for ec2 instances to be ready for ssh")
    time.sleep(250)
    
    # Move to ansible directory
    os.chdir(ANSIBLE_DIR)

    # Setting the shell to ignore ssh check
    # subprocess.call("export ANSIBLE_HOST_KEY_CHECKING=False", shell=True)

    print("Executing master.sh")
    cmd = "sudo ./master.sh"
    execute(cmd)
    # subprocess.call("sudo ./master.sh", shell=True)

    print("Executing slave.sh")
    cmd = "sudo ./slave.sh"
    execute(cmd)
    # subprocess.call("sudo ./slave.sh", shell=True)'''

if __name__ == '__main__':
    sys.exit(launch(sys.argv[1:]))
