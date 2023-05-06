# https://www.thepythoncode.com/article/get-hardware-system-information-python#System_Information
# https://stackabuse.com/executing-shell-commands-with-python/

import json
import os
import psutil
import platform
from datetime import datetime
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QGroupBox, QVBoxLayout, QGridLayout 

#System
uname = platform.uname()
print("- - - System - - -")
print(f"System: {uname.system}")
print(f"Node Name: {uname.node}")
print(f"Release: {uname.release}")
print(f"Version: {uname.version}")
print(f"Machine: {uname.machine}")
print(f"Processor: {uname.processor}")
boot_time_timestamp = psutil.boot_time()
bt = datetime.fromtimestamp(boot_time_timestamp)
print(f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")


#CPU
print("- - - CPU - - -")
print(f"Physical cores: {psutil.cpu_count(logical=False)}")
print(f"Total cores: {psutil.cpu_count(logical=True)}")
cpufreq = psutil.cpu_freq()
print(f"Max Frequency: {cpufreq.max:.2f}Mhz")
print(f"Min Frequency: {cpufreq.min:.2f}Mhz")
print(f"Current Frequency: {cpufreq.current:.2f}Mhz")
print(f"Total CPU Usage: {psutil.cpu_percent()}")
for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
    print(f"Core {i}: {percentage}%")

#Memory
print("- - - Memory - - -")
def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

svmem = psutil.virtual_memory()
print(f"Total: {get_size(svmem.total)}")
print(f"Available: {get_size(svmem.available)}")
print(f"Used: {get_size(svmem.used)}")
print(f"Percentage: {svmem.percent}%")

swap = psutil.swap_memory()
print (f"Total: {get_size(swap.total)}")
print(f"Free: {get_size(swap.free)}")
print(f"Used: {get_size(swap.used)}")
print (f"Percentage: {swap.percent}%")

#Network
print("- - - Network - - -")
if_addrs = psutil.net_if_addrs()
for interface_name, interface_addresses in if_addrs.items():
    print(f"Interface: {interface_name}")
    for address in interface_addresses:
        print(f"{str(address.family)}: {address.address}")
        print(f"broadcast IP: {address.broadcast}")
        print(f"MAC Address: {address.address}")
        print(f"Netmask: {address.netmask}")
        print(f"Broadcast MAC: {address.broadcast}")

net_io = psutil.net_io_counters()
print(f"Total Bytes Sent: {get_size(net_io.bytes_sent)}")
print(f"Total Bytes Received: {get_size(net_io.bytes_recv)}")