# Aws-infos
Simplify the management of your Amazon AWS EC2 instances with this command-line Python utility. Generate hosts.ini files for Ansible, SSH connection strings for each EC2 instance, and configure Microsoft's SSH extension for VSCode. 🚀

markdown

# An EC2 SSH File Generator

![License](https://img.shields.io/badge/license-GNU%20GPL%20v3-blue)

## Description

This Python script, **EC2 SSH File Generator**, simplifies the process of managing SSH configurations for Amazon EC2 instances. It automates the generation of SSH files and configuration for EC2 instances, making it easy to retrieve their IP addresses and connect to them, especially after instance restarts when IP addresses are reset.

### Do I need it?

Managing SSH configurations for EC2 instances can be cumbersome, especially when instances are frequently restarted, leading to changing IP addresses. This script aims to solve this problem by automatically generating SSH configuration files, allowing you to seamlessly connect to your EC2 instances, whether they have PublicDnsNames, PrivateDnsNames, or neither.

## Features

- Automatically generates SSH configuration files: `hosts.ini`, `connection_helper`, `ssh_config`.
- Handles instances with PublicDnsNames, PrivateDnsNames, or no names.
- Logs machine status with color-coded output for easy visualization.
- Supports configuration through a YAML file.
- Cross-platform compatibility (Linux, macOS, Windows).

## Installation

1. Install the required dependencies:

   ```bash
   python install_dependencies.py

2. Run the main script:
    ```bash
    python main.py

## Configuration

You can customize the script's behavior by editing the config/config.yml file. Here are all the key configurations you can modify:
    ```yaml
    key_path: Specify the path to your SSH key (default: .ssh/aws.pem).
    region_name: Set your preferred AWS region (default: eu-west-3).
    log_file: Path to the log file (default: logs/main_log.log).
    instance_status_log: Path to the instance status log file (default: logs/instance_status.log).
    hosts_ini_file: Path to the hosts.ini file (default: files/hosts.ini).
    connection_helper_file: Path to the connection_helper file (default: files/connection_helper).


## License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.
Acknowledgments

    Special thanks to the Free Software Foundation for their work on the GNU General Public License.
    This script was created by method($man).

For more details and usage instructions, please refer to the complete source code documentation.