import os
import psutil
import platform
import sys
from datetime import datetime
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget,QVBoxLayout
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QGroupBox, QVBoxLayout, QGridLayout, QScrollArea
from PyQt5.QtCore import QTimer, Qt, pyqtSlot
from PyQt5.QtGui import QIcon

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'System Information - Version 2.0'
        self.left = 0
        self.top = 0
        self.width = 400
        self.height = 300
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)
        
        self.show()
    
class Tab1(QWidget):
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
        
        #scroll
        scrollbar = QScrollArea(widgetResizable=True)
        scrollbar.setWidget(self.tab1)
        layout = QGridLayout(self)
          
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

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        
    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())