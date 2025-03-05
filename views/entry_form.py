from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, 
                           QLabel, QLineEdit, QComboBox, QPushButton, 
                           QDateEdit, QMessageBox, QGridLayout)
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
        # Single main layout with everything properly sized
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)
        
        # Header
        header_label = QLabel("Enter Transaction Details")
        header_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #3a4f9b;")
        header_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header_label)
        
        # Form layout in a grid for better organization
        form_grid = QGridLayout()
        form_grid.setVerticalSpacing(10)
        form_grid.setHorizontalSpacing(15)
        
        # Transaction name
        name_label = QLabel("Transaction Name:")
        name_label.setStyleSheet("font-weight: 500;")
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("e.g., Monthly Salary, Rent Payment")
        self.name_edit.setFixedHeight(30)
        
        form_grid.addWidget(name_label, 0, 0)
        form_grid.addWidget(self.name_edit, 0, 1)
        
        # Amount
        amount_label = QLabel("Amount (₺):")
        amount_label.setStyleSheet("font-weight: 500;")
        self.amount_edit = QLineEdit()
        self.amount_edit.setPlaceholderText("Amount in Turkish Lira")
        self.amount_edit.setFixedHeight(30)
        
        form_grid.addWidget(amount_label, 1, 0)
        form_grid.addWidget(self.amount_edit, 1, 1)
        
        # Transaction category
        category_label = QLabel("Category:")
        category_label.setStyleSheet("font-weight: 500;")
        self.category_combo = QComboBox()
        self.category_combo.setFixedHeight(30)
        
        # Load categories from controller
        self.refresh_categories()
        
        # Set background color based on whether category is income or expense
        self.category_combo.currentIndexChanged.connect(self.update_category_style)
        
        form_grid.addWidget(category_label, 2, 0)
        form_grid.addWidget(self.category_combo, 2, 1)
        
        # Date (month and year)
        date_label = QLabel("Date:")
        date_label.setStyleSheet("font-weight: 500;")
        self.date_edit = QDateEdit()
        self.date_edit.setDisplayFormat("MMMM yyyy")
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setFixedHeight(30)
        
        form_grid.addWidget(date_label, 3, 0)
        form_grid.addWidget(self.date_edit, 3, 1)
        
        # Add form grid to main layout
        main_layout.addLayout(form_grid)
        
        # Add spacer for better appearance
        main_layout.addSpacing(20)
        
        # Buttons - side by side
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_form)
        self.clear_btn.setFixedHeight(35)
        
        self.add_btn = QPushButton("Add Transaction")
        self.add_btn.setObjectName("primaryButton")
        self.add_btn.clicked.connect(self.add_transaction)
        self.add_btn.setFixedHeight(35)
        
        # Add Manage Categories button
        self.manage_categories_btn = QPushButton("Manage Categories")
        self.manage_categories_btn.clicked.connect(self.show_category_manager)
        self.manage_categories_btn.setFixedHeight(35)
        
        buttons_layout.addWidget(self.clear_btn)
        buttons_layout.addWidget(self.manage_categories_btn)
        buttons_layout.addWidget(self.add_btn)
        
        main_layout.addLayout(buttons_layout)
        
        # Add stretch to push all content to the top
        main_layout.addStretch(1)
        
        # Initial styling update
        self.update_category_style()
        
    def refresh_categories(self):
        """Refresh the categories in the combobox"""
        # Save the current selection if any
        current_category = self.category_combo.currentText() if self.category_combo.count() > 0 else None
        
        # Clear the combobox
        self.category_combo.clear()
        
        # Get all categories from controller
        categories = self.controller.get_all_categories()
        
        # Sort categories by type (income first, then expense)
        sorted_categories = sorted(categories, key=lambda c: c["type"])
        
        # Add to combobox with type indication
        for category in sorted_categories:
            display_text = f"{category['name']} ({category['type'].capitalize()})"
            self.category_combo.addItem(display_text, category["name"])
        
        # Restore the previous selection if possible
        if current_category:
            index = self.category_combo.findText(current_category, Qt.MatchStartsWith)
            if index >= 0:
                self.category_combo.setCurrentIndex(index)
        
    def update_category_style(self):
        """Update background color based on whether selected category is income or expense"""
        if self.category_combo.count() == 0:
            return
            
        # Get the category name
        current_index = self.category_combo.currentIndex()
        if current_index < 0:
            return
            
        # Get the display text which includes the type
        display_text = self.category_combo.currentText()
        
        # Check if it's income or expense
        if "(Income)" in display_text:
            # Green for income
            self.category_combo.setStyleSheet("""
                background-color: #e8f5e9;
                border: 1px solid #81c784;
                border-radius: 4px;
                padding: 5px;
            """)
        else:
            # Red for expense
            self.category_combo.setStyleSheet("""
                background-color: #ffebee;
                border: 1px solid #e57373;
                border-radius: 4px;
                padding: 5px;
            """)
        
    def clear_form(self):
        """Clear all form fields"""
        self.name_edit.clear()
        self.amount_edit.clear()
        if self.category_combo.count() > 0:
            self.category_combo.setCurrentIndex(0)
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
        
        # Validate category selection
        if self.category_combo.count() == 0:
            QMessageBox.warning(self, "Input Error", "No categories available. Please add categories first.")
            return
            
        # Get category name (stored as user data)
        category_name = self.category_combo.currentData()
        
        # Get date
        qdate = self.date_edit.date()
        date = datetime(qdate.year(), qdate.month(), 1)  # Set day to 1
        
        # Add transaction
        try:
            self.controller.add_transaction(name, amount, category_name, date)
            
            # Show success message
            QMessageBox.information(self, "Success", "Transaction added successfully!")
            
            # Clear form
            self.clear_form()
            
            # Emit signal
            self.transaction_added.emit()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add transaction: {str(e)}")
            
    def show_category_manager(self):
        """Show the category manager dialog"""
        # This will be implemented in the main window to show the category manager tab
        # We'll emit a signal that the main window will connect to
        self.transaction_added.emit()  # Reuse the same signal to trigger UI updates