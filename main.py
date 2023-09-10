#!/usr/bin/env python3
"""! @brief Script for generating SSH files and configuration for EC2 instances.

@file generate_ssh_files.py
@brief Script for generating SSH files and configuration for EC2 instances.
@mainpage Generating SSH files and configuration for EC2 instances
@section description_main Description
This Python script uses Boto3 to retrieve information about EC2 instances and generate SSH configuration files, including hosts.ini, connection_helper, ssh_config, and config.yml. It handles cases where an instance has a PublicDnsName, a PrivateDnsName, or neither.

@section libraries_main Libraries/Modules
- [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [os](https://docs.python.org/3/library/os.html)
- [yaml](https://pyyaml.org/)
- [datetime](https://docs.python.org/3/library/datetime.html)
- [re](https://docs.python.org/3/library/re.html) (Regular expressions for string matching)
- [colorama](https://pypi.org/project/colorama/) (Styling and coloring terminal text)

@section author_doxygen_example Auteur
- Réalisé par method($man).

@see For more information, refer to the complete source code documentation.
"""

# Import Python standards modules
import os
from datetime import datetime

# Import third-party modules
import boto3
import yaml
import re
from colorama import Fore, Style

# File paths
LOG_FILE = 'logs/main_log.log'
MACHINE_STATUS_LOG = 'logs/machine_status.log'
HOSTS_INI_FILE = 'files/hosts.ini'
CONNECTION_HELPER_FILE = 'files/connection_helper'
CONFIG_FILE = 'config/config.yml'

# Default configuration
DEFAULT_SSH_KEY_PATH = '.ssh/aws.pem'
AWS_REGION = 'eu-west-3'


def log(message, file='logs/main_log.log'):
    """
     @brief Creates a timestamp and the username in the log file.
     @param message The message to be recorded should be a string.
     @param file The file to write to.
    """
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    username = os.getlogin()
    log_entry = f"[{timestamp}] {username}: {message}\n"
    with open(file, 'a', encoding='utf-8') as log_file:
        log_file.write(log_entry)

# Function to open and read a file
def open_file(filename, mode, content=None):
    """
     @brief Open and read a file. This function is used to read or write file content.
     @param filename name of the file to open
     @param mode file mode (r t t)
     @param content The file content (optional) defaults to None
     @return file content (rỡw) or None if there is an error (unset mode)
    """
    try:
        if mode == 'r':
            with open(filename, 'r') as file:
                return file.read()
        elif mode == 'w':
            with open(filename, 'w') as file:
                file.write(content)
        else:
            print(f"Error: Unsupported access mode: {mode}")
    except Exception as e:
        print(f"Error: {e}")
 
def get_all_regions():
    ec2 = boto3.client('ec2', region_name='eu-west-3')  # Use any region for this
    response = ec2.describe_regions()
    regions = [region['RegionName'] for region in response['Regions']]
    return regions

def get_instance_data(region):
    """
    @brief Get data on EC2 instances for a specific region.
    """
    ec2 = boto3.client('ec2', region_name=region)
    instances = ec2.describe_instances()
    instance_data = []

    # Logging the queried region
    log(f"Querying region: {region}")

    # This function will save the state of all instances in the reservation.
    for reservation in instances['Reservations']:
        # This function will save the state of all instances in the reservation.
        for instance in reservation['Instances']:
            instance_name = instance.get('Tags', [{'Key': 'Name', 'Value': 'Unnamed'}])[0]['Value']
            instance_ip = instance.get('PublicDnsName', '')
            private_ip = instance.get('PrivateDnsName', '')
            instance_status = instance['State']['Name']

            # Machine and region status logging
            log_machine_status(instance_name, instance_status, region)

            # Create a new instance data structure.
            if instance_ip:
                instance_data.append({'Name': instance_name, 'PublicDns': instance_ip, 'Status': instance_status, 'Region': region})
            elif private_ip:
                instance_data.append({'Name': instance_name, 'PrivateDns': private_ip, 'Status': 'NoPublicDns', 'Region': region})

    return instance_data

def remove_ansi_styles(input_string):
    # Define a regular expression to search for ANSI escape codes
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')

    # Use sub de re function to remove ANSI escape codes
    plain_string = ansi_escape.sub('', input_string)
    return plain_string

def log_machine_status(instance_name, status, region):
    """
    @brief Groups machine status with colors.
    @param instance_name Name of the running instance
    @param status The machine status as defined in the command.
    @param region The region to which the machine belongs
    """
    # Set ANSI color codes for each state
    if status == 'running':
        status_color = Fore.GREEN
    elif status == 'stopped':
        status_color = Fore.RED
    else:
        status_color = ''

    # Format the message with colors
    message = f"{Style.BRIGHT}{Fore.YELLOW}Machine {Style.RESET_ALL}:'{Style.BRIGHT}{Fore.LIGHTRED_EX}{instance_name}{Style.RESET_ALL}' - {Style.BRIGHT}{Fore.YELLOW}Status: {Style.RESET_ALL}{Style.DIM}{status_color}{status}{Style.RESET_ALL} - {Style.BRIGHT}{Fore.YELLOW}Region{Style.RESET_ALL}: {Style.DIM}{Fore.BLUE}{region}{Style.RESET_ALL}"
    print_and_log(message, 'logs/machine_status.log')

def generate_files(instance_data, ssh_key):
    """
     @brief Generate files for use with SSH. This is a helper function to generate the files.
     @param instance_data A list of dictionaries containing information on instances
     @param ssh_key The SSH key for
    """
    hosts_ini_content = ''
    connection_helper_content = ''
    ssh_config_content = ''

    # Return the path to the ssh configuration file.
    if os.name == 'posix':  
        ssh_config_path = os.path.expanduser('~/.ssh/config')
    elif os.name == 'nt': 
        ssh_config_path = os.path.expanduser(os.path.join('~', '.ssh', 'config'))

    # Generates the content of instance data
    for data in instance_data:
        name = data['Name']
        public_dns = data.get('PublicDns', '')
        private_dns = data.get('PrivateDns', '')

        hosts_ini_content += f"{name} ansible_host={public_dns} ansible_ssh_private_key_file={ssh_key}\n"
        connection_helper_content += f'ssh -i "{ssh_key}" ec2-user@{public_dns}\n'

        # Generate ssh configuration content for ssh_config file
        if public_dns:
            ssh_config_content += f'\nHost {name}\n'
            ssh_config_content += f'  HostName {public_dns}\n'
            ssh_config_content += f'  User ec2-user\n'
            ssh_config_content += f'  IdentityFile {ssh_key}\n'

        elif private_dns:
            ssh_config_content += f'\nHost {name}\n'
            ssh_config_content += f'  HostName {private_dns}\n'
            ssh_config_content += f'  User ec2-user\n'
            ssh_config_content += f'  IdentityFile {ssh_key}\n'

    open_file('files/hosts.ini', 'w', hosts_ini_content)
    open_file('files/connection_helper', 'w', connection_helper_content)

    # Open the ssh_config_content file if the ssh_config_content content n
    if ssh_config_content:
        open_file(ssh_config_path, 'w', ssh_config_content)

def read_config(yaml_file_path):
    """
     @brief Read a YAML file and return its content as a dictionary.
     @param yaml_file_path The path to the YAML file to read.
     @return The YAML file content as a dictionary.
    """
    try:
        with open(yaml_file_path, 'r') as yaml_file:
            yaml_content = yaml.safe_load(yaml_file)
            return yaml_content
    except Exception as e:
        print(f"Error reading YAML file: {e}")
        return {}

def print_and_log(message, file='logs/main_log.log'):
    print(message)
    log(remove_ansi_styles(message), file)

# Main function
def check_and_generate_files():
    try:
        # Get the list of all AWS Regions
        all_regions = get_all_regions()

        # Collect instance data for all regions
        all_instance_data = []
        for region in all_regions:
            instance_data = get_instance_data(region)
            all_instance_data.extend(instance_data)

        # Filter running instances
        running_instances = [instance for instance in all_instance_data if instance['Status'] == 'running']

        if not running_instances:
            print_and_log("No running instances found. Files will not be generated.")
            return

        config_yaml = read_config(CONFIG_FILE)
        ssh_key_path = config_yaml.get('key_path', DEFAULT_SSH_KEY_PATH)

        generate_files(running_instances, ssh_key_path)
        print_and_log("The hosts.ini, connection_helper, ssh_config files have been successfully generated.")

    except Exception as e:
        log(f"Error: {str(e)}")

if __name__ == "__main__":
    check_and_generate_files()