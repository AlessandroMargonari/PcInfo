import os
import psutil
import platform
import sys
from datetime import datetime
import PyQt5
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
        app.setStyle('Fusion')

        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)

        #screen height
        desktop = QDesktopWidget()
        screenRect = desktop.screenGeometry()
        screenHeight = screenRect.height()

        #Scroll
        scrollArea = QScrollArea(self)
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scrollArea.setWidget(self.table_widget)
        self.setCentralWidget(scrollArea)
        self.setMinimumWidth(self.table_widget.width()+15)
        self.setMaximumWidth(self.table_widget.width()+15)
        self.setMaximumHeight(self.table_widget.height()+5)

        #geometry
        self.left = 80
        self.top = 80
        self.width = self.table_widget.width()+15
        self.height = int(screenHeight/2)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.show()
        
class MyTableWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        styleValues="""
            font-weight: bold;
            border: 1px solid #C0C0C0;
            border-radius: 4px;
            margin-top: 16px;
            padding: 1px;
        """

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
        labelSystem = QLabel(f"System: <span style='{styleValues}'>{uname.system}</span>")
        labelNode = QLabel(f"Node Name: <span style='{styleValues}'>{uname.node}</span>")
        labelRelease = QLabel(f"Release: <span style='{styleValues}'>{uname.release}</span>")
        labelVersion = QLabel(f"Version: <span style='{styleValues}'>{uname.version}</span>")
        labelMachine = QLabel(f"Machine: <span style='{styleValues}'>{uname.machine}</span>")
        labelProcessor = QLabel(f"Processor: <span style='{styleValues}'>{uname.processor}</span>")
        boot_time_timestamp = psutil.boot_time()
        bt = datetime.fromtimestamp(boot_time_timestamp)
        bootTime = QGroupBox('Boot Time:')
        labelBootDay = QLabel(f"Boot Day: <span style='{styleValues}'>{bt.year}/{bt.month}/{bt.day}</span>",bootTime)
        labelBootHour = QLabel(f"Boot Hour: <span style='{styleValues}'>{bt.hour}:{bt.minute}:{bt.second}</span>",bootTime)
        #labelUsers = QLabel(f"Users: <span style='{styleValues}'>{psutil.users()}</span>")
        #labelBattery = QLabel(f"Battery Status: <span style='{styleValues}'>{psutil.sensors_battery()}</span>")
        batteryStatus = QGroupBox('Battery Status:')

        layoutBootTime = QVBoxLayout()
        bootTime.setLayout(layoutBootTime)
        layoutBootTime.addWidget(labelBootDay)
        layoutBootTime.addWidget(labelBootHour)

        layoutBatteryStatus = QVBoxLayout()
        batteryStatus.setLayout(layoutBatteryStatus)
        battery_status = psutil.sensors_battery()
        if battery_status is not None:
            percent_label = QLabel(f'Percent: {battery_status[0]}%')
            layoutBatteryStatus.addWidget(percent_label)

            power_plugged_label = QLabel(f'Power Plugged In: {battery_status[1]}')
            layoutBatteryStatus.addWidget(power_plugged_label)

            seconds_left_label = QLabel(f'Time Left: {battery_status[2]// 60} minutes')
            layoutBatteryStatus.addWidget(seconds_left_label)
        else:
            battery_none = QLabel(f"<span style='{styleValues}'>No battery</span>")
            layoutBatteryStatus.addWidget(battery_none)

        self.tab1.layout.addWidget(labelSystem)
        self.tab1.layout.addWidget(labelNode)
        self.tab1.layout.addWidget(labelRelease)
        self.tab1.layout.addWidget(labelVersion)
        self.tab1.layout.addWidget(labelMachine)
        self.tab1.layout.addWidget(labelProcessor)
        self.tab1.layout.addWidget(bootTime)
        #self.tab1.layout.addWidget(labelUsers)
        self.tab1.layout.addWidget(batteryStatus)
        self.tab1.layout.addItem(spacer)

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
        MemoryDetails = QGroupBox('Memory Usage:')
        labelMemoryTotal = QLabel(f"Total: <span style='{styleValues}'>{get_size(svmem.total)} </span>", MemoryDetails)
        labelMemoryAvailable = QLabel(f"Available: {get_size(svmem.available)}", MemoryDetails)
        labelMemoryUsed = QLabel(f"Used: {get_size(svmem.used)}", MemoryDetails)
        labelMemoryPercentage = QLabel(f"Percentage: {svmem.percent}%", MemoryDetails)

        MemorySWAP = QGroupBox('Memory SWAP:')
        swap = psutil.swap_memory()
        labelMemorySWAPTotal = QLabel(f"Total: <span style='{styleValues}'>{get_size(swap.total)} </span>", MemorySWAP)
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
        self.tab2.layout.addItem(spacer)
        
        #third tab
        self.tab3.layout = QVBoxLayout(self)
        self.tab3.setLayout(self.tab3.layout)
        labelPhisicalCore = QLabel(f"Physical cores: <span style='{styleValues}'>{psutil.cpu_count(logical=False)}</style>")
        labelTotalCore = QLabel(f"Total cores: <span style='{styleValues}'>{psutil.cpu_count(logical=True)}</style>")
        cpufreq = psutil.cpu_freq()
        labelMaxFrequency = QLabel(f"Max Frequency: <span style='{styleValues}'>{cpufreq.max:.2f}Mhz</style>")
        labelMinFrequency = QLabel(f"Min Frequency: <span style='{styleValues}'>{cpufreq.min:.2f}Mhz</style>")
        labelCurrentFrequency = QLabel(f"Current Frequency: {cpufreq.current:.2f}Mhz")
        labelCPUUsage = QLabel(f"Total CPU Usage: {psutil.cpu_percent()}%")

        CPUUsage = QGroupBox('Core Usage:')
        layoutCPUUsage = QVBoxLayout()
        CPUUsage.setLayout(layoutCPUUsage)

        self.tab3.layout.addWidget(labelPhisicalCore)
        self.tab3.layout.addWidget(labelTotalCore)
        self.tab3.layout.addWidget(labelMaxFrequency)
        self.tab3.layout.addWidget(labelMinFrequency)
        self.tab3.layout.addWidget(labelCurrentFrequency)
        self.tab3.layout.addWidget(labelCPUUsage)
        self.tab3.layout.addWidget(CPUUsage)
        self.tab3.layout.addItem(spacer)

        labelCore =[]
        for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
            labelCore.append(QLabel(f"Core {i}: {percentage}%", CPUUsage))
        for x in labelCore:
            layoutCPUUsage.addWidget(x)

        #fourth tab
        self.tab4.layout = QVBoxLayout(self)
        self.tab4.setLayout(self.tab4.layout)

        IOInfo = QGroupBox('IO statistics: (Input/Output)')
        net_io = psutil.net_io_counters()
        labelByteSent = QLabel(f"Total Bytes Sent: {get_size(net_io.bytes_sent)}")
        labelByteRecived = QLabel(f"Total Bytes Received: {get_size(net_io.bytes_recv)}")

        layoutIOInfo = QVBoxLayout()
        IOInfo.setLayout(layoutIOInfo)
        layoutIOInfo.addWidget(labelByteSent)
        layoutIOInfo.addWidget(labelByteRecived)

        self.tab4.layout.addWidget(IOInfo)

        if_addrs = psutil.net_if_addrs()
        for interface_name, interface_addresses in if_addrs.items():
            networkInterface = QGroupBox(f"Interface: {interface_name}")
            layoutNetworkInterface = QVBoxLayout(networkInterface)
            for address in interface_addresses:
                networkAddress = QGroupBox(f"Adress: {address.address}")
                layoutNetworkAddress = QVBoxLayout(networkAddress)
                labelNetworkIP= QLabel(f"{str(address.family)}: <span style='{styleValues}'>{address.address}</span>")
                labelNetworkBroadcast = QLabel(f"broadcast IP: <span style='{styleValues}'>{address.broadcast}</span>")
                labelNetworkMAC = QLabel(f"MAC Address: <span style='{styleValues}'>{address.address}</span>")
                labelNetworkNetmask = QLabel(f"Netmask: <span style='{styleValues}'>{address.netmask}</span>")
                labelNetworkBroadcastMAC = QLabel(f"Broadcast MAC: <span style='{styleValues}'>{address.broadcast}</span>")
                layoutNetworkAddress.addWidget(labelNetworkIP)
                layoutNetworkAddress.addWidget(labelNetworkBroadcast)
                layoutNetworkAddress.addWidget(labelNetworkMAC)
                layoutNetworkAddress.addWidget(labelNetworkNetmask)
                layoutNetworkAddress.addWidget(labelNetworkBroadcastMAC)
                self.tab4.layout.addWidget(networkAddress)

        def update():
            svmem = psutil.virtual_memory()
            swap = psutil.swap_memory()
            #labelMemoryTotal.setText(f"Total: {get_size(svmem.total)}")
            labelMemoryAvailable.setText(f"Available: <span style='{styleValues}'>{get_size(svmem.available)}</span>")
            labelMemoryUsed.setText(f"Used: <span style='{styleValues}'>{get_size(svmem.used)}</span>")
            labelMemoryPercentage.setText(f"Percentage: <span style='{styleValues}'>{svmem.percent}%</span>")
            #labelMemorySWAPTotal.setText(f"Total: {get_size(swap.total)}")
            labelMemorySWAPFree.setText(f"Free: <span style='{styleValues}'>{get_size(swap.free)}</span>")
            labelMemorySWAPUsed.setText(f"Used: <span style='{styleValues}'>{get_size(swap.used)}</span>")
            labelMemorySWAPPercentage.setText(f"Percentage: <span style='{styleValues}'>{swap.percent}%</span>")

            labelCPUUsage.setText(f"Total CPU Usage: <span style='{styleValues}'>{psutil.cpu_percent()}%</span>")
            labelCurrentFrequency.setText(f"Current Frequency:  <span style='{styleValues}'>{cpufreq.current:.2f}Mhz</span>")
            
            for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
                labelCore[i]=(QLabel(f"Core {i}:  <span style='{styleValues}'>{percentage}%</span>", CPUUsage))

            while layoutCPUUsage.count():
                item = layoutCPUUsage.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)

            for x in labelCore:
                layoutCPUUsage.addWidget(x)

            labelByteSent.setText(f"Total Bytes Sent: <span style='{styleValues}'>{get_size(net_io.bytes_sent)}</span>")
            labelByteRecived.setText(f"Total Bytes Received: <span style='{styleValues}'>{get_size(net_io.bytes_recv)}</span>")
            QTimer.singleShot(1500, update)

        #more
        moreInfo = QGroupBox('')
        more = QGridLayout()
        moreInfo.setLayout(more)
        author = QLabel("By Alessandro Margonari")
        version = QLabel("Version: 2.2")
        version.setAlignment(QtCore.Qt.AlignCenter)
        author.setAlignment(QtCore.Qt.AlignCenter)
        more.addWidget(author, 0,0)
        more.addWidget(version, 0,1)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.layout.addWidget(moreInfo)
        self.setLayout(self.layout)

        #update data
        #update_memory()
        #update_cpu()
        #update_network()
        update()

        
    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())