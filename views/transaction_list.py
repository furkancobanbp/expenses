from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                             QTableWidgetItem, QLabel, QComboBox, QHeaderView,
                             QSplitter, QAbstractItemView, QFrame)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QColor, QFont

import calendar
from datetime import datetime

class TransactionList(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.init_ui()
        
    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Filter section
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(15)
        
        # Period filter
        period_label = QLabel("Period:")
        period_label.setFixedWidth(50)
        self.period_combo = QComboBox()
        self.period_combo.addItem("Current Month", "current_month")
        self.period_combo.addItem("Previous Month", "previous_month")
        self.period_combo.addItem("Current Year", "current_year")
        self.period_combo.addItem("Previous Year", "previous_year")
        self.period_combo.addItem("All Time", "all_time")
        self.period_combo.setFixedWidth(150)
        self.period_combo.currentIndexChanged.connect(self.refresh_data)
        
        filter_layout.addWidget(period_label)
        filter_layout.addWidget(self.period_combo)
        filter_layout.addStretch()
        
        main_layout.addLayout(filter_layout)
        
        # Create a splitter for the two tables
        splitter = QSplitter(Qt.Vertical)
        
        # Income table section
        income_frame = QFrame()
        income_layout = QVBoxLayout(income_frame)
        income_layout.setContentsMargins(0, 0, 0, 0)
        
        income_header = QLabel("Income Transactions")
        income_header.setStyleSheet("font-size: 14px; font-weight: bold; color: #2e7d32;")
        income_layout.addWidget(income_header)
        
        self.income_table = QTableWidget()
        self.income_table.setAlternatingRowColors(True)
        self.income_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.income_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.income_table.setStyleSheet("""
            QTableView {
                background-color: #f8f9fa;
                alternate-background-color: #e8f5e9;
                selection-background-color: #81c784;
            }
            QHeaderView::section {
                background-color: #e8f5e9;
                color: #2e7d32;
                font-weight: bold;
                padding: 6px;
                border: none;
                border-bottom: 1px solid #81c784;
            }
        """)
        
        income_layout.addWidget(self.income_table)
        splitter.addWidget(income_frame)
        
        # Expense table section
        expense_frame = QFrame()
        expense_layout = QVBoxLayout(expense_frame)
        expense_layout.setContentsMargins(0, 0, 0, 0)
        
        expense_header = QLabel("Expense Transactions")
        expense_header.setStyleSheet("font-size: 14px; font-weight: bold; color: #c62828;")
        expense_layout.addWidget(expense_header)
        
        self.expense_table = QTableWidget()
        self.expense_table.setAlternatingRowColors(True)
        self.expense_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.expense_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.expense_table.setStyleSheet("""
            QTableView {
                background-color: #f8f9fa;
                alternate-background-color: #ffebee;
                selection-background-color: #e57373;
            }
            QHeaderView::section {
                background-color: #ffebee;
                color: #c62828;
                font-weight: bold;
                padding: 6px;
                border: none;
                border-bottom: 1px solid #e57373;
            }
        """)
        
        expense_layout.addWidget(self.expense_table)
        splitter.addWidget(expense_frame)
        
        # Set equal initial sizes for the splitter
        splitter.setSizes([300, 300])
        main_layout.addWidget(splitter)
        
        # Set up table headers
        self.setup_tables()
        
        # Initial data load
        self.refresh_data()
        
    def setup_tables(self):
        """Set up the table headers and columns"""
        headers = ["Date", "Name", "Category", "Amount (₺)"]  # Added Category column
        
        # Income table
        self.income_table.setColumnCount(len(headers))
        self.income_table.setHorizontalHeaderLabels(headers)
        
        # Set all columns to equal size
        for i in range(len(headers)):
            self.income_table.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
        
        # Expense table
        self.expense_table.setColumnCount(len(headers))
        self.expense_table.setHorizontalHeaderLabels(headers)
        
        # Set all columns to equal size
        for i in range(len(headers)):
            self.expense_table.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
        
    def refresh_data(self):
        """Refresh the table data based on selected period"""
        period = self.period_combo.currentData()
        transactions = self.get_transactions_by_period(period)
        
        # Split transactions by type
        income_transactions = [t for t in transactions if t.transaction_type.value == 'income']
        expense_transactions = [t for t in transactions if t.transaction_type.value == 'expense']
        
        # Sort transactions by date (newest first)
        income_transactions.sort(key=lambda x: x.date, reverse=True)
        expense_transactions.sort(key=lambda x: x.date, reverse=True)
        
        # Update income table
        self.update_table(self.income_table, income_transactions)
        
        # Update expense table
        self.update_table(self.expense_table, expense_transactions)
        
    def update_table(self, table, transactions):
        """Update table with transaction data"""
        table.setRowCount(0)  # Clear existing rows
        
        for transaction in transactions:
            row_position = table.rowCount()
            table.insertRow(row_position)
            
            # Date column
            date_item = QTableWidgetItem(transaction.date.strftime("%b %Y"))
            date_item.setTextAlignment(Qt.AlignCenter)
            table.setItem(row_position, 0, date_item)
            
            # Name column
            name_item = QTableWidgetItem(transaction.name)
            name_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            table.setItem(row_position, 1, name_item)
            
            # Category column
            category_text = transaction.category if transaction.category else "N/A"
            category_item = QTableWidgetItem(category_text)
            category_item.setTextAlignment(Qt.AlignCenter)
            
            # Style the category item
            font = QFont()
            font.setBold(True)
            category_item.setFont(font)
            
            # Colorize category based on transaction type
            if transaction.transaction_type.value == 'income':
                category_item.setForeground(QColor("#2e7d32"))  # Green for income
            else:
                category_item.setForeground(QColor("#c62828"))  # Red for expense
                
            table.setItem(row_position, 2, category_item)
            
            # Amount column
            amount_item = QTableWidgetItem(f"{transaction.amount:,.2f}")
            amount_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            
            # Set font to make amount bold
            amount_font = QFont()
            amount_font.setBold(True)
            amount_item.setFont(amount_font)
            
            # Colorize amount based on transaction type
            if transaction.transaction_type.value == 'income':
                amount_item.setForeground(QColor("#2e7d32"))  # Green for income
            else:
                amount_item.setForeground(QColor("#c62828"))  # Red for expense
                
            table.setItem(row_position, 3, amount_item)
            
        # Add summary row
        self.add_summary_row(table, transactions)
            
    def add_summary_row(self, table, transactions):
        """Add a summary row at the bottom of the table"""
        if not transactions:
            return
            
        row_position = table.rowCount()
        table.insertRow(row_position)
        
        # First cell - "TOTAL"
        total_label = QTableWidgetItem("TOTAL")
        total_label.setFont(QFont("", weight=QFont.Bold))
        total_label.setTextAlignment(Qt.AlignCenter)
        total_label.setBackground(QColor("#f0f0f0"))
        table.setItem(row_position, 0, total_label)
        
        # Second cell - empty with background
        empty_item = QTableWidgetItem("")
        empty_item.setBackground(QColor("#f0f0f0"))
        table.setItem(row_position, 1, empty_item)
        
        # Third cell (Category) - empty with background
        empty_category_item = QTableWidgetItem("")
        empty_category_item.setBackground(QColor("#f0f0f0"))
        table.setItem(row_position, 2, empty_category_item)
        
        # Fourth cell - total amount
        total_amount = sum(t.amount for t in transactions)
        total_item = QTableWidgetItem(f"{total_amount:,.2f}")
        total_item.setFont(QFont("", weight=QFont.Bold))
        total_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        total_item.setBackground(QColor("#f0f0f0"))
        
        # Set color based on transaction type
        if transactions and transactions[0].transaction_type.value == 'income':
            total_item.setForeground(QColor("#2e7d32"))  # Green for income
        else:
            total_item.setForeground(QColor("#c62828"))  # Red for expense
            
        table.setItem(row_position, 3, total_item)
        
    def get_transactions_by_period(self, period):
        """Get transactions filtered by the selected period"""
        all_transactions = self.controller.finance_manager.get_all_transactions()
        now = datetime.now()
        
        if period == "current_month":
            return [t for t in all_transactions 
                    if t.date.year == now.year and t.date.month == now.month]
        
        elif period == "previous_month":
            prev_month = now.month - 1
            year = now.year
            if prev_month == 0:
                prev_month = 12
                year -= 1
            return [t for t in all_transactions 
                    if t.date.year == year and t.date.month == prev_month]
        
        elif period == "current_year":
            return [t for t in all_transactions if t.date.year == now.year]
        
        elif period == "previous_year":
            return [t for t in all_transactions if t.date.year == now.year - 1]
        
        else:  # "all_time"
            return all_transactions