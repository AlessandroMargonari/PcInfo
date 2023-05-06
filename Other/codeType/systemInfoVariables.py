import json
import os
import psutil
import platform
from datetime import datetime
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QGroupBox, QVBoxLayout, QGridLayout 

#System
uname = platform.uname()
System = (f"System: {uname.system}")
SystemNode = (f"Node Name: {uname.node}")
SystemRelease = (f"Release: {uname.release}")
SystemVersion = (f"Version: {uname.version}")
SystemMachine = (f"Machine: {uname.machine}")
SystemProcessor = (f"Processor: {uname.processor}")
boot_time_timestamp = psutil.boot_time()
bt = datetime.fromtimestamp(boot_time_timestamp)
SystemBoot = (f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")


#CPU
CpuPhisicalCore = (f"Physical cores: {psutil.cpu_count(logical=False)}")
CpuTotalCore = (f"Total cores: {psutil.cpu_count(logical=True)}")
cpufreq = psutil.cpu_freq()
CpuMaxFrequency = (f"Max Frequency: {cpufreq.max:.2f}Mhz")
CpuMinFrequency = (f"Min Frequency: {cpufreq.min:.2f}Mhz")
CpuCurrentFrequency = (f"Current Frequency: {cpufreq.current:.2f}Mhz")
CpuUsage = (f"Total CPU Usage: {psutil.cpu_percent()}")
for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
    CpuCore = (f"Core {i}: {percentage}%")

#Memory
def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

svmem = psutil.virtual_memory()
MemoryTotal = (f"Total: {get_size(svmem.total)}")
MemoryAvailable = (f"Available: {get_size(svmem.available)}")
MemoryUsed = (f"Used: {get_size(svmem.used)}")
MemoryPercentage = (f"Percentage: {svmem.percent}%")

swap = psutil.swap_memory()
MemorySWAPTotal = (f"Total: {get_size(swap.total)}")
MemorySWAPFree = (f"Free: {get_size(swap.free)}")
MemorySWAPUsed = (f"Used: {get_size(swap.used)}")
MemorySWAPPercentage = (f"Percentage: {swap.percent}%")

#Network
if_addrs = psutil.net_if_addrs()
for interface_name, interface_addresses in if_addrs.items():
    InterfaceName= (f"Interface: {interface_name}")
    for address in interface_addresses:
        NetworkIP= (f"{str(address.family)}: {address.address}")
        NetworkBroadcast = (f"broadcast IP: {address.broadcast}")
        NetworkMAC = (f"MAC Address: {address.address}")
        NetworkNetmask = (f"Netmask: {address.netmask}")
        NetworkBroadcastMAC = (f"Broadcast MAC: {address.broadcast}")

net_io = psutil.net_io_counters()
IoByteSent = (f"Total Bytes Sent: {get_size(net_io.bytes_sent)}")
IoByteRecived = (f"Total Bytes Received: {get_size(net_io.bytes_recv)}")