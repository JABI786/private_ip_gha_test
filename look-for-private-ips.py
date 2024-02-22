#!/usr/bin/env python3

import yaml
import ipaddress
import os
import sys


def is_private_ip(ip):
    try:
        ip_obj = ipaddress.ip_address(ip)
        return ip_obj.is_private
    except ValueError:
        return False



def del_first_occurrence(ip_dels, ip_addr):
    index = ip_dels.index(ip_addr)
    del ip_dels[index]


changed_file = sys.argv[1]
changed_file_adds = changed_file + ".adds"
changed_file_dels = changed_file + ".dels"
actual_ip_adds = []
private_ips = []


with open(changed_file_adds, 'r') as file:
    ip_adds = file.read().splitlines()
with open(changed_file_dels,'r') as f:
    ip_dels = f.read().splitlines()


for ip in ip_adds:
    if ip in ip_dels:
        del_first_occurrence(ip_dels,ip)
    else:
        actual_ip_adds.append(ip)


for ipaddr in actual_ip_adds:
    if is_private_ip(ipaddr):
        private_ips.append(ipaddr)

if private_ips:
    print(f"The following Private IPs were detected in change for {changed_file}")
    for i in private_ips:
         print(i)
    sys.exit(1)
else:
    print(f"No Private IPs have been detected in change for {changed_file}")

