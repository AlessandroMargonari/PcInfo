import os
import psutil
import platform
import sys
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer, Qt, pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        #title
        self.title = 'System Information'
        self.setWindowTitle(self.title)

        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)

        #Scroll
        scrollArea = QScrollArea(self)
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scrollArea.setWidget(self.table_widget)
        self.setCentralWidget(scrollArea)
        self.setMinimumWidth(self.table_widget.width()+15)
        self.setMaximumWidth(self.table_widget.width()+15)
        self.setMaximumHeight(self.table_widget.height()+5)

        #geometry
        self.left = 0
        self.top = 0
        self.width = self.table_widget.width()+15
        self.height = self.table_widget.height()+5
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.show()
        
class MyTableWidget(QWidget):
    
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tabs.resize(300,200)
        
        # Add tabs
        self.tabs.addTab(self.tab1,"System Info")
        self.tabs.addTab(self.tab2,"Memory")
        self.tabs.addTab(self.tab3,"CPU")
        self.tabs.addTab(self.tab4,"Network")
          
        #first tab
        self.tab1.layout = QVBoxLayout(self)
        self.tab1.setLayout(self.tab1.layout)
        uname = platform.uname()
        labelSystem = QLabel(f"System: {uname.system}")
        labelNode = QLabel(f"Node Name: {uname.node}")
        labelRelease = QLabel(f"Release: {uname.release}")
        labelVersion = QLabel(f"Version: {uname.version}")
        labelMachine = QLabel(f"Machine: {uname.machine}")
        labelProcessor = QLabel(f"Processor: {uname.processor}")
        boot_time_timestamp = psutil.boot_time()
        bt = datetime.fromtimestamp(boot_time_timestamp)
        labelBoot = QLabel(f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")
        labelUsers = QLabel(f"Users: {psutil.users()}")
        labelBattery = QLabel(f"Battery Status: {psutil.sensors_battery()}")

        self.tab1.layout.addWidget(labelSystem)
        self.tab1.layout.addWidget(labelNode)
        self.tab1.layout.addWidget(labelRelease)
        self.tab1.layout.addWidget(labelVersion)
        self.tab1.layout.addWidget(labelMachine)
        self.tab1.layout.addWidget(labelProcessor)
        self.tab1.layout.addWidget(labelBoot)
        self.tab1.layout.addWidget(labelUsers)
        self.tab1.layout.addWidget(labelBattery)

        #second tab
        self.tab2.layout = QVBoxLayout(self)
        self.tab2.setLayout(self.tab2.layout)
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

        self.tab2.layout.addWidget(MemoryDetails)
        self.tab2.layout.addWidget(MemorySWAP)

        def update_memory():
            svmem = psutil.virtual_memory()
            swap = psutil.swap_memory()
            labelMemoryTotal.setText(f"Total: {get_size(svmem.total)}")
            labelMemoryAvailable.setText(f"Available: {get_size(svmem.available)}")
            labelMemoryUsed.setText(f"Used: {get_size(svmem.used)}")
            labelMemoryPercentage.setText(f"Percentage: {svmem.percent}%")
            labelMemorySWAPTotal.setText(f"Total: {get_size(swap.total)}")
            labelMemorySWAPFree.setText(f"Free: {get_size(swap.free)}")
            labelMemorySWAPUsed.setText(f"Used: {get_size(swap.used)}")
            labelMemorySWAPPercentage.setText(f"Percentage: {swap.percent}%")
            QTimer.singleShot(5000, update_memory)
        
        #third tab
        self.tab3.layout = QVBoxLayout(self)
        self.tab3.setLayout(self.tab3.layout)
        labelPhisicalCore = QLabel(f"Physical cores: {psutil.cpu_count(logical=False)}")
        labelTotalCore = QLabel(f"Total cores: {psutil.cpu_count(logical=True)}")
        cpufreq = psutil.cpu_freq()
        labelMaxFrequency = QLabel(f"Max Frequency: {cpufreq.max:.2f}Mhz")
        labelMinFrequency = QLabel(f"Min Frequency: {cpufreq.min:.2f}Mhz")
        labelCurrentFrequency = QLabel(f"Current Frequency: {cpufreq.current:.2f}Mhz")
        labelCPUUsage = QLabel(f"Total CPU Usage: {psutil.cpu_percent()}%")

        CPUUsage = QGroupBox('Core Usage')
        layoutCPUUsage = QVBoxLayout()
        CPUUsage.setLayout(layoutCPUUsage)

        self.tab3.layout.addWidget(labelPhisicalCore)
        self.tab3.layout.addWidget(labelTotalCore)
        self.tab3.layout.addWidget(labelMaxFrequency)
        self.tab3.layout.addWidget(labelMinFrequency)
        self.tab3.layout.addWidget(labelCurrentFrequency)
        self.tab3.layout.addWidget(labelCPUUsage)
        self.tab3.layout.addWidget(CPUUsage)

        labelCore =[]
        for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
            labelCore.append(QLabel(f"Core {i}: {percentage}%", CPUUsage))
        for x in labelCore:
            layoutCPUUsage.addWidget(x)

        def update_cpu():
            labelCPUUsage.setText(f"Total CPU Usage: {psutil.cpu_percent()}%")
            labelCurrentFrequency.setText(f"Current Frequency: {cpufreq.current:.2f}Mhz")
            
            for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
                labelCore[i]=(QLabel(f"Core {i}: {percentage}%", CPUUsage))

            while layoutCPUUsage.count():
                item = layoutCPUUsage.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)

            for x in labelCore:
                layoutCPUUsage.addWidget(x)
            QTimer.singleShot(5100, update_cpu)

        #fourth tab
        self.tab4.layout = QVBoxLayout(self)
        self.tab4.setLayout(self.tab4.layout)

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
                self.tab4.layout.addWidget(networkAddress)

        IOInfo = QGroupBox('IO statistics')
        net_io = psutil.net_io_counters()
        labelByteSent = QLabel(f"Total Bytes Sent: {get_size(net_io.bytes_sent)}")
        labelByteRecived = QLabel(f"Total Bytes Received: {get_size(net_io.bytes_recv)}")

        layoutIOInfo = QVBoxLayout()
        IOInfo.setLayout(layoutIOInfo)
        layoutIOInfo.addWidget(labelByteSent)
        layoutIOInfo.addWidget(labelByteRecived)

        self.tab4.layout.addWidget(IOInfo)

        def update_network():
            labelByteSent.setText(f"Total Bytes Sent: {get_size(net_io.bytes_sent)}")
            labelByteRecived.setText(f"Total Bytes Received: {get_size(net_io.bytes_recv)}")
            QTimer.singleShot(5200, update_network)

        #more
        moreInfo = QGroupBox('')
        more = QGridLayout()
        moreInfo.setLayout(more)
        author = QLabel("By Alessandro Margonari")
        version = QLabel("Version: 2.1")
        version.setAlignment(QtCore.Qt.AlignCenter)
        author.setAlignment(QtCore.Qt.AlignCenter)
        more.addWidget(author, 0,0)
        more.addWidget(version, 0,1)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.layout.addWidget(moreInfo)
        self.setLayout(self.layout)

        #update data
        update_memory()
        update_cpu()
        update_network()

        
    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())