import json
import psutil
import platform
from datetime import datetime

# System
uname = platform.uname()
boot_time_timestamp = psutil.boot_time()
bt = datetime.fromtimestamp(boot_time_timestamp)
boot_time_timestamp = psutil.boot_time()
# CPU
cpufreq = psutil.cpu_freq()
cpuCore = []
for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
    cpuCore.append(f"Core {i}: {percentage}%")
# Memory
def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor
svmem = psutil.virtual_memory()
swap = psutil.swap_memory()
# Network
networkInfo = {}
if_addrs = psutil.net_if_addrs()
for interface_name, interface_addresses in if_addrs.items():
    InterfaceName = (f"Interface: {interface_name}")
    for address in interface_addresses:
        networkInfo[InterfaceName] ={
            "NetworkInterfaceName": InterfaceName,
            "NetworkIP": (f"{str(address.family)}: {address.address}"),
            "NetworkBroadcast": (f"broadcast IP: {address.broadcast}"),
            "NetworkMAC":  (f"MAC Address: {address.address}"),
            "NetworkNetmask": (f"Netmask: {address.netmask}"),
            "NetworkBroadcastMAC": (f"Broadcast MAC: {address.broadcast}")
        }
net_io = psutil.net_io_counters()

Json_Info = {}
Json_Info["System"] = {
    "System": (f"System: {uname.system}"),
    "SystemNode": (f"Node Name: {uname.node}"),
    "SystemRelease": (f"Release: {uname.release}"),
    "SystemVersion": (f"Version: {uname.version}"),
    "SystemMachine": (f"Machine: {uname.machine}"),
    "SystemProcessor": (f"Processor: {uname.processor}"),
    "boot_time_timestamp": datetime.fromtimestamp(boot_time_timestamp).strftime('%Y-%m-%d %H:%M:%S'),
    "SystemBoot": (f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")
}
Json_Info["Cpu"] = {
    "CpuPhisicalCore": (f"Physical cores: {psutil.cpu_count(logical=False)}"),
    "CpuTotalCore": (f"Total cores: {psutil.cpu_count(logical=True)}"),
    "CpuMaxFrequency": (f"Max Frequency: {cpufreq.max:.2f}Mhz"),
    "CpuMinFrequency": (f"Min Frequency: {cpufreq.min:.2f}Mhz"),
    "CpuCurrentFrequency": (f"Current Frequency: {cpufreq.current:.2f}Mhz"),
    "CpuUsage": (f"Total CPU Usage: {psutil.cpu_percent()}"),
    "CpuCore": cpuCore
}
Json_Info["Memory"] = {
    "MemoryTotal": (f"Total: {get_size(svmem.total)}"),
    "MemoryAvailable": (f"Available: {get_size(svmem.available)}"),
    "MemoryUsed": (f"Used: {get_size(svmem.used)}"),
    "MemoryPercentage":  (f"Percentage: {svmem.percent}%"),
    "MemorySWAPTotal": (f"Total: {get_size(swap.total)}"),
    "MemorySWAPFree": (f"Free: {get_size(swap.free)}"),
    "MemorySWAPUsed": (f"Used: {get_size(swap.used)}"),
    "MemorySWAPPercentage": (f"Percentage: {swap.percent}%")
}
Json_Info["Network"] = {
    "IoByteSent": (f"Total Bytes Sent: {get_size(net_io.bytes_sent)}"),
    "IoByteRecived": (f"Total Bytes Received: {get_size(net_io.bytes_recv)}")
}
Json_Info["Network"].update(networkInfo)

# Serializing json
json_object = json.dumps(Json_Info, indent=4)
 
# Writing to sample.json
with open(".\mydata.json", "w") as outfile:
    outfile.write(json_object)