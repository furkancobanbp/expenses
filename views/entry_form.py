from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, 
                           QLabel, QLineEdit, QComboBox, QPushButton, 
                           QDateEdit, QMessageBox, QGroupBox)
from PyQt5.QtCore import Qt, pyqtSignal, QDate

from datetime import datetime
from models.transaction import TransactionType

class EntryForm(QWidget):
    # Signal emitted when a transaction is added
    transaction_added = pyqtSignal()
    
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.init_ui()
        
    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Form group with enhanced styling
        form_group = QGroupBox("Add New Transaction")
        form_layout = QFormLayout(form_group)
        form_layout.setSpacing(15)
        form_layout.setContentsMargins(25, 35, 25, 25)
        
        # Add heading
        heading = QLabel("Enter Transaction Details")
        heading.setStyleSheet("font-size: 18px; font-weight: bold; color: #3a4f9b; margin-bottom: 15px;")
        heading.setAlignment(Qt.AlignCenter)
        form_layout.addRow(heading)
        
        # Add separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: #e9ecef; margin: 10px 0 20px 0;")
        separator.setFixedHeight(1)
        form_layout.addRow(separator)
        
        # Transaction name
        name_label = QLabel("Transaction Name:")
        name_label.setStyleSheet("font-weight: 500;")
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("e.g., Salary, Rent, Groceries")
        self.name_edit.setMinimumHeight(40)
        form_layout.addRow(name_label, self.name_edit)
        
        # Amount
        amount_label = QLabel("Amount ($):")
        amount_label.setStyleSheet("font-weight: 500;")
        self.amount_edit = QLineEdit()
        self.amount_edit.setPlaceholderText("Amount in dollars")
        self.amount_edit.setMinimumHeight(40)
        form_layout.addRow(amount_label, self.amount_edit)
        
        # Transaction type
        type_label = QLabel("Type:")
        type_label.setStyleSheet("font-weight: 500;")
        self.type_combo = QComboBox()
        self.type_combo.addItem(TransactionType.INCOME.value, TransactionType.INCOME)
        self.type_combo.addItem(TransactionType.EXPENSE.value, TransactionType.EXPENSE)
        self.type_combo.setMinimumHeight(40)
        form_layout.addRow(type_label, self.type_combo)
        
        # Date (month and year)
        date_label = QLabel("Date:")
        date_label.setStyleSheet("font-weight: 500;")
        self.date_edit = QDateEdit()
        self.date_edit.setDisplayFormat("MMMM yyyy")
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setMinimumHeight(40)
        form_layout.addRow(date_label, self.date_edit)
        
        # Add some space before buttons
        form_layout.addItem(QSpacerItem(20, 20))
        
        main_layout.addWidget(form_group)
        
        # Buttons with modern styling
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_form)
        self.clear_btn.setMinimumHeight(45)
        
        self.add_btn = QPushButton("Add Transaction")
        self.add_btn.setObjectName("primaryButton")
        self.add_btn.clicked.connect(self.add_transaction)
        self.add_btn.setMinimumHeight(45)
        
        buttons_layout.addWidget(self.clear_btn)
        buttons_layout.addWidget(self.add_btn)
        
        main_layout.addLayout(buttons_layout)
        main_layout.addStretch()
        
    def clear_form(self):
        """Clear all form fields"""
        self.name_edit.clear()
        self.amount_edit.clear()
        self.type_combo.setCurrentIndex(0)
        self.date_edit.setDate(QDate.currentDate())
        
    def add_transaction(self):
        """Add a new transaction based on form data"""
        # Validate input
        name = self.name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "Input Error", "Please enter a transaction name.")
            return
        
        # Validate amount
        amount_text = self.amount_edit.text().strip()
        try:
            amount = float(amount_text)
            if amount <= 0:
                raise ValueError("Amount must be positive")
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter a valid positive amount.")
            return
        
        # Get transaction type
        transaction_type = self.type_combo.currentData()
        
        # Get date
        qdate = self.date_edit.date()
        date = datetime(qdate.year(), qdate.month(), 1)  # Set day to 1
        
        # Add transaction
        try:
            self.controller.add_transaction(name, amount, transaction_type, date)
            
            # Show success message
            QMessageBox.information(self, "Success", "Transaction added successfully!")
            
            # Clear form
            self.clear_form()
            
            # Emit signal
            self.transaction_added.emit()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add transaction: {str(e)}")