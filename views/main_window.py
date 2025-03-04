from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QTabWidget, QLabel)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from .dashboard import Dashboard
from .entry_form import EntryForm
from .transaction_list import TransactionList
from .goals import GoalsTab

class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Personal Finance Manager")
        self.setMinimumSize(800, 600)
        
        # Create central widget and single layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(5)
        
        # Create compact header
        header = QLabel("Personal Finance Manager")
        header.setObjectName("header")
        header.setAlignment(Qt.AlignCenter)
        header.setMaximumHeight(30)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        header.setFont(font)
        main_layout.addWidget(header)
        
        # Create tab widget that takes all available space
        tab_widget = QTabWidget()
        tab_widget.setDocumentMode(True)
        
        # Adjust tab size to fit content
        tab_widget.setStyleSheet("""
            QTabBar::tab {
                min-width: 120px;
                padding: 8px 12px;
            }
        """)
        
        # Create dashboard tab
        self.dashboard = Dashboard(self.controller)
        tab_widget.addTab(self.dashboard, "Dashboard")
        
        # Create transactions list tab
        self.transaction_list = TransactionList(self.controller)
        tab_widget.addTab(self.transaction_list, "Transactions")
        
        # Create goals tab
        self.goals_tab = GoalsTab(self.controller)
        tab_widget.addTab(self.goals_tab, "Financial Goals")
        
        # Create entry form tab
        self.entry_form = EntryForm(self.controller)
        tab_widget.addTab(self.entry_form, "Add Transaction")
        
        # Add tab widget with stretch priority
        main_layout.addWidget(tab_widget, 1)
        
        # Connect signals
        self.entry_form.transaction_added.connect(self.on_transaction_added)
        
    def on_transaction_added(self):
        # Refresh views when a transaction is added
        self.dashboard.refresh_charts()
        self.transaction_list.refresh_data()
        self.goals_tab.refresh_goals()