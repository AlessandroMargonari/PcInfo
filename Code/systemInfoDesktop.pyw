import os
import psutil
import platform
import sys
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QGroupBox, QVBoxLayout, QGridLayout, QScrollArea
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(600, 100, 1000, 900)
        self.setWindowTitle('System Information - Version 1.0')
        # - - - - - - - - - System - - - - - - - - - 
        self.systemInfo = QGroupBox('System Information', self)
        uname = platform.uname()
        labelSystem = QLabel(f"System: {uname.system}", self.systemInfo)
        labelNode = QLabel(f"Node Name: {uname.node}", self.systemInfo)
        labelRelease = QLabel(f"Release: {uname.release}", self.systemInfo)
        labelVersion = QLabel(f"Version: {uname.version}", self.systemInfo)
        labelMachine = QLabel(f"Machine: {uname.machine}", self.systemInfo)
        labelProcessor = QLabel(f"Processor: {uname.processor}", self.systemInfo)
        boot_time_timestamp = psutil.boot_time()
        bt = datetime.fromtimestamp(boot_time_timestamp)
        labelBoot = QLabel(f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}", self.systemInfo)
        labelUsers = QLabel(f"Users: {psutil.users()}", self.systemInfo)
        labelBattery = QLabel(f"Battery Status: {psutil.sensors_battery()}", self.systemInfo)

        layoutSystem = QVBoxLayout()
        self.systemInfo.setLayout(layoutSystem)
        layoutSystem.addWidget(labelSystem)
        layoutSystem.addWidget(labelNode)
        layoutSystem.addWidget(labelRelease)
        layoutSystem.addWidget(labelVersion)
        layoutSystem.addWidget(labelMachine)
        layoutSystem.addWidget(labelProcessor)
        layoutSystem.addWidget(labelBoot)
        layoutSystem.addWidget(labelUsers)
        layoutSystem.addWidget(labelBattery)


        # - - - - - - - - - CPU - - - - - - - - - 
        self.CPUInfo = QGroupBox('CPU Information', self)
        labelPhisicalCore = QLabel(f"Physical cores: {psutil.cpu_count(logical=False)}", self.CPUInfo)
        labelTotalCore = QLabel(f"Total cores: {psutil.cpu_count(logical=True)}", self.CPUInfo)
        cpufreq = psutil.cpu_freq()
        labelMaxFrequency = QLabel(f"Max Frequency: {cpufreq.max:.2f}Mhz", self.CPUInfo)
        labelMinFrequency = QLabel(f"Min Frequency: {cpufreq.min:.2f}Mhz", self.CPUInfo)
        labelCurrentFrequency = QLabel(f"Current Frequency: {cpufreq.current:.2f}Mhz", self.CPUInfo)
        labelCPUUsage = QLabel(f"Total CPU Usage: {psutil.cpu_percent()}%", self.CPUInfo)

        CPUUsage = QGroupBox('Core Usage')


        layoutCPU = QVBoxLayout()
        self.CPUInfo.setLayout(layoutCPU)
        layoutCPUUsage = QVBoxLayout()
        CPUUsage.setLayout(layoutCPUUsage)
        layoutCPU.addWidget(labelPhisicalCore)
        layoutCPU.addWidget(labelTotalCore)
        layoutCPU.addWidget(labelMaxFrequency)
        layoutCPU.addWidget(labelMinFrequency)
        layoutCPU.addWidget(labelCurrentFrequency)
        layoutCPU.addWidget(labelCPUUsage)
        layoutCPU.addWidget(CPUUsage)

        for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
            labelCore = QLabel(f"Core {i}: {percentage}%", CPUUsage)
            layoutCPUUsage.addWidget(labelCore)

        def updateCore():
            print("test")
            for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
                # Get the corresponding QLabel object using its index in the layout
                labelCore = layoutCPUUsage.itemAt(i).widget()
                # Update the text of the QLabel
                labelCore.setText(f"Core {i}: {percentage}%")
                print
                
        timer = QTimer()
        timer.timeout.connect(updateCore)
        timer.start(5000)
        #app.exec_()

        # - - - - - - - - - Memory - - - - - - - - - 
        self.MemoryInfo = QGroupBox('Memory Information', self)
        def get_size(bytes, suffix="B"):
            factor = 1024
            for unit in ["", "K", "M", "G", "T", "P"]:
                if bytes < factor:
                    return f"{bytes:.2f}{unit}{suffix}"
                bytes /= factor
        svmem = psutil.virtual_memory()
        MemoryDetails = QGroupBox('Memory Usage')
        labelMemoryTotal = QLabel(f"Total: {get_size(svmem.total)}", MemoryDetails)
        labelMemoryAvailable = QLabel(f"Available: {get_size(svmem.available)}", MemoryDetails)
        labelMemoryUsed = QLabel(f"Used: {get_size(svmem.used)}", MemoryDetails)
        labelMemoryPercentage = QLabel(f"Percentage: {svmem.percent}%", MemoryDetails)

        MemorySWAP = QGroupBox('Memory SWAP')
        swap = psutil.swap_memory()
        labelMemorySWAPTotal = QLabel(f"Total: {get_size(swap.total)}", MemorySWAP)
        labelMemorySWAPFree = QLabel(f"Free: {get_size(swap.free)}", MemorySWAP)
        labelMemorySWAPUsed = QLabel(f"Used: {get_size(swap.used)}", MemorySWAP)
        labelMemorySWAPPercentage = QLabel(f"Percentage: {swap.percent}%", MemorySWAP)

        layoutMemoryInfo = QVBoxLayout()
        self.MemoryInfo.setLayout(layoutMemoryInfo)
        layoutMemoryInfo.addWidget(MemoryDetails)
        layoutMemoryInfo.addWidget(MemorySWAP)

        layoutMemory = QVBoxLayout()
        MemoryDetails.setLayout(layoutMemory)
        layoutMemory.addWidget(labelMemoryTotal)
        layoutMemory.addWidget(labelMemoryAvailable)
        layoutMemory.addWidget(labelMemoryUsed)
        layoutMemory.addWidget(labelMemoryPercentage)

        layoutMemorySWAP = QVBoxLayout()
        MemorySWAP.setLayout(layoutMemorySWAP)
        layoutMemorySWAP.addWidget(labelMemorySWAPTotal)
        layoutMemorySWAP.addWidget(labelMemorySWAPFree)
        layoutMemorySWAP.addWidget(labelMemorySWAPUsed)
        layoutMemorySWAP.addWidget(labelMemorySWAPPercentage)

        # - - - - - - - - - Network - - - - - - - - - 
        self.NetworkInfo = QGroupBox('Network Information', self)
        layoutNetwork = QVBoxLayout()
        self.NetworkInfo.setLayout(layoutNetwork)

        if_addrs = psutil.net_if_addrs()
        for interface_name, interface_addresses in if_addrs.items():
            networkInterface = QGroupBox(f"Interface: {interface_name}")
            layoutNetworkInterface = QVBoxLayout(networkInterface)
            for address in interface_addresses:
                networkAddress = QGroupBox(f"Adress: {address.address}")
                layoutNetworkAddress = QVBoxLayout(networkAddress)
                labelNetworkIP= QLabel(f"{str(address.family)}: {address.address}")
                labelNetworkBroadcast = QLabel(f"broadcast IP: {address.broadcast}")
                labelNetworkMAC = QLabel(f"MAC Address: {address.address}")
                labelNetworkNetmask = QLabel(f"Netmask: {address.netmask}")
                labelNetworkBroadcastMAC = QLabel(f"Broadcast MAC: {address.broadcast}")
                layoutNetworkAddress.addWidget(labelNetworkIP)
                layoutNetworkAddress.addWidget(labelNetworkBroadcast)
                layoutNetworkAddress.addWidget(labelNetworkMAC)
                layoutNetworkAddress.addWidget(labelNetworkNetmask)
                layoutNetworkAddress.addWidget(labelNetworkBroadcastMAC)
                layoutNetworkInterface.addWidget(networkAddress)
            layoutNetwork.addWidget(networkInterface)

        IOInfo = QGroupBox('IO statistics')
        net_io = psutil.net_io_counters()
        labelByteSent = QLabel(f"Total Bytes Sent: {get_size(net_io.bytes_sent)}")
        labelByteRecived = QLabel(f"Total Bytes Received: {get_size(net_io.bytes_recv)}")

        #layoutNetwork = QVBoxLayout()
        #self.NetworkInfo.setLayout(layoutNetwork)
        layoutIOInfo = QVBoxLayout()
        IOInfo.setLayout(layoutIOInfo)

        layoutIOInfo.addWidget(labelByteSent)
        layoutIOInfo.addWidget(labelByteRecived)

        # Add the widgets to the main window layout
        layout = QGridLayout()
        layout.addWidget(self.systemInfo, 0, 0)
        layout.addWidget(self.MemoryInfo, 0, 1)
        layout.addWidget(self.CPUInfo, 1, 0)
        layout.addWidget(self.NetworkInfo, 1, 1)
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

        self.scroll = QScrollArea()
        self.widget = QWidget()

        #Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        #self.scroll.setWidgetResizable(True)
        #self.scroll.setWidget(centralWidget)
        #self.setCentralWidget(centralWidget)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())


