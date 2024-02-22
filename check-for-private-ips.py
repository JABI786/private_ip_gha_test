#!/usr/bin/env python3

import yaml
import ipaddress
import os
import sys

def is_valid_yaml(line):
    try:
        yaml.safe_load(line)
        return True
    except yaml.YAMLError:
        return False

def remove_invalid_yaml_lines(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            if is_valid_yaml(line):
                outfile.write(line)


def is_private_ip(ip):
    try:
        ip_obj = ipaddress.ip_address(ip)
        return ip_obj.is_private
    except ValueError:
        return False

def analyze_yaml(yaml_data):
    private_ips_summary = {}
    def analyze_data(data, path=''):
        nonlocal private_ips_summary
        if isinstance(data, dict):
            for key, value in data.items():
                new_path = f"{path}/{key}" if path else key
                analyze_data(value, new_path)
        
        elif isinstance(data, list):
            for idx, item in enumerate(data):
                new_path = f"{path}[{idx}]"
                analyze_data(item, new_path)

        elif isinstance(data, str):
            if is_private_ip(data):
                    private_ips_summary[path] = data
    analyze_data(yaml_data)
    return private_ips_summary



def analyze_yaml_pr(yaml_data, priv_ip_details_previous):
    private_ips_summary_pr = {}
    private_ip_count = 0
    def analyze_data_pr(data, path=''):
        nonlocal private_ips_summary_pr
        nonlocal private_ip_count
        if isinstance(data, dict):
            for key, value in data.items():
                new_path = f"{path}/{key}" if path else key
                analyze_data_pr(value, new_path)

        elif isinstance(data, list):
            for idx, item in enumerate(data):
                new_path = f"{path}[{idx}]"
                analyze_data_pr(item, new_path)

        elif isinstance(data, str):
            if is_private_ip(data):
                if path not in priv_ip_details_previous:
                    private_ips_summary_pr[path] = data
                    private_ip_count += 1 
    analyze_data_pr(yaml_data)
    return (private_ips_summary_pr, private_ip_count)

changed_file = sys.argv[1]
changed_file_previous = changed_file + ".previous"
new_changed_file = changed_file + "-updated"
new_changed_file_previous = changed_file_previous + "-updated"
remove_invalid_yaml_lines(changed_file_previous, new_changed_file_previous)
with open(new_changed_file_previous,'r') as f:
    yaml_data_previous = yaml.safe_load(f)
os.remove(new_changed_file_previous)
priv_ip_details_previous = analyze_yaml(yaml_data_previous)
print(priv_ip_details_previous)
remove_invalid_yaml_lines(changed_file, new_changed_file)
with open(new_changed_file,'r') as file:
    yaml_data_pr = yaml.safe_load(file)
os.remove(new_changed_file)
private_ip_details_pr = analyze_yaml_pr(yaml_data_pr, priv_ip_details_previous)
if private_ip_details_pr and private_ip_details_pr[1] != 0:
    private_ip_found = True
    print(f"Private IP addresses found in {changed_file}:")
    print(f"Printing Summary ...\nTotal number of private IP addresses found: {private_ip_details_pr[1]}")
    for path, ip in private_ip_details_pr[0].items():
        print(f"-Private IP {ip} found at {path}")
    sys.exit(1)
else:
    print(f"No private IP addresses found in {changed_file}\n")
