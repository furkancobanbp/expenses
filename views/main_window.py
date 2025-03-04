from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                          QTabWidget, QLabel, QPushButton)
from PyQt5.QtCore import Qt

from .dashboard import Dashboard
from .entry_form import EntryForm

class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Personal Finance Manager")
        self.setMinimumSize(800, 600)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create header
        header = QLabel("Personal Finance Manager")
        header.setObjectName("header")
        header.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header)
        
        # Create tab widget
        tab_widget = QTabWidget()
        
        # Create dashboard tab
        self.dashboard = Dashboard(self.controller)
        tab_widget.addTab(self.dashboard, "Dashboard")
        
        # Create entry form tab
        self.entry_form = EntryForm(self.controller)
        tab_widget.addTab(self.entry_form, "Add Transaction")
        
        main_layout.addWidget(tab_widget)
        
        # Connect signals
        self.entry_form.transaction_added.connect(self.on_transaction_added)
        
    def on_transaction_added(self):
        # Refresh dashboard when a transaction is added
        self.dashboard.refresh_charts()