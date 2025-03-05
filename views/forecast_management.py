from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, 
                           QLabel, QLineEdit, QComboBox, QPushButton, 
                           QDateEdit, QMessageBox, QGridLayout, QTabWidget,
                           QTableWidget, QTableWidgetItem, QHeaderView,
                           QAbstractItemView, QTextEdit, QSplitter,
                           QFrame, QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal, QDate
from PyQt5.QtGui import QColor, QFont

import calendar
from datetime import datetime
from models.transaction import TransactionType

class ForecastEntryForm(QWidget):
    """Form for entering new forecast transactions"""
    forecast_added = pyqtSignal()
    
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.init_ui()
        
    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)
        
        # Header
        header_label = QLabel("Enter Forecast Transaction Details")
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
        self.name_edit.setPlaceholderText("e.g., Expected Salary, Planned Rent Payment")
        self.name_edit.setFixedHeight(30)
        
        form_grid.addWidget(name_label, 0, 0)
        form_grid.addWidget(self.name_edit, 0, 1)
        
        # Amount
        amount_label = QLabel("Amount (₺):")
        amount_label.setStyleSheet("font-weight: 500;")
        self.amount_edit = QLineEdit()
        self.amount_edit.setPlaceholderText("Forecast amount in Turkish Lira")
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
        
        # Notes
        notes_label = QLabel("Notes:")
        notes_label.setStyleSheet("font-weight: 500;")
        self.notes_edit = QTextEdit()
        self.notes_edit.setPlaceholderText("Add notes or assumptions about this forecast")
        self.notes_edit.setMaximumHeight(80)
        
        form_grid.addWidget(notes_label, 4, 0, Qt.AlignTop)
        form_grid.addWidget(self.notes_edit, 4, 1)
        
        # Add form grid to main layout
        main_layout.addLayout(form_grid)
        
        # Add spacer for better appearance
        main_layout.addSpacing(20)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_form)
        self.clear_btn.setFixedHeight(35)
        
        self.add_btn = QPushButton("Add Forecast")
        self.add_btn.setObjectName("primaryButton")
        self.add_btn.clicked.connect(self.add_forecast)
        self.add_btn.setFixedHeight(35)
        
        buttons_layout.addWidget(self.clear_btn)
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
        self.notes_edit.clear()
    
    def add_forecast(self):
        """Add a new forecast transaction based on form data"""
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
        
        # Get notes
        notes = self.notes_edit.toPlainText()
        
        # Add forecast
        try:
            # The updated controller method signature only accepts name, amount, category_name, date
            # and handles notes separately
            self.controller.add_forecast(name, amount, category_name, date)
            
            # Show success message
            QMessageBox.information(self, "Success", "Forecast transaction added successfully!")
            
            # Clear form
            self.clear_form()
            
            # Emit signal
            self.forecast_added.emit()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add forecast: {str(e)}")


class ForecastList(QWidget):
    """Widget to display forecast transactions"""
    forecast_updated = pyqtSignal()
    
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
        
        self.month_combo = QComboBox()
        for i in range(1, 13):
            self.month_combo.addItem(calendar.month_name[i], i)
        
        current_date = datetime.now()
        current_month_idx = self.month_combo.findData(current_date.month)
        if current_month_idx >= 0:
            self.month_combo.setCurrentIndex(current_month_idx)
        
        self.year_combo = QComboBox()
        
        # Get unique years and add future years
        years = self.controller.get_unique_years()
        for year in range(min(years), max(years) + 3):
            self.year_combo.addItem(str(year), year)
        
        current_year_idx = self.year_combo.findData(current_date.year)
        if current_year_idx >= 0:
            self.year_combo.setCurrentIndex(current_year_idx)
        
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.refresh_data)
        
        filter_layout.addWidget(period_label)
        filter_layout.addWidget(self.month_combo)
        filter_layout.addWidget(self.year_combo)
        filter_layout.addWidget(self.refresh_btn)
        filter_layout.addStretch()
        
        main_layout.addLayout(filter_layout)
        
        # Create a splitter for the two tables
        splitter = QSplitter(Qt.Vertical)
        
        # Income forecasts table section
        income_frame = QFrame()
        income_layout = QVBoxLayout(income_frame)
        income_layout.setContentsMargins(0, 0, 0, 0)
        
        income_header = QLabel("Income Forecasts")
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
        
        # Income table buttons
        income_buttons = QHBoxLayout()
        self.edit_income_btn = QPushButton("Edit Selected")
        self.edit_income_btn.clicked.connect(lambda: self.edit_forecast(self.income_table))
        
        self.delete_income_btn = QPushButton("Delete Selected")
        self.delete_income_btn.clicked.connect(lambda: self.delete_forecast(self.income_table))
        
        income_buttons.addWidget(self.edit_income_btn)
        income_buttons.addWidget(self.delete_income_btn)
        income_buttons.addStretch()
        
        income_layout.addLayout(income_buttons)
        splitter.addWidget(income_frame)
        
        # Expense forecasts table section
        expense_frame = QFrame()
        expense_layout = QVBoxLayout(expense_frame)
        expense_layout.setContentsMargins(0, 0, 0, 0)
        
        expense_header = QLabel("Expense Forecasts")
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
        
        # Expense table buttons
        expense_buttons = QHBoxLayout()
        self.edit_expense_btn = QPushButton("Edit Selected")
        self.edit_expense_btn.clicked.connect(lambda: self.edit_forecast(self.expense_table))
        
        self.delete_expense_btn = QPushButton("Delete Selected")
        self.delete_expense_btn.clicked.connect(lambda: self.delete_forecast(self.expense_table))
        
        expense_buttons.addWidget(self.edit_expense_btn)
        expense_buttons.addWidget(self.delete_expense_btn)
        expense_buttons.addStretch()
        
        expense_layout.addLayout(expense_buttons)
        splitter.addWidget(expense_frame)
        
        # Set equal initial sizes for the splitter
        splitter.setSizes([300, 300])
        main_layout.addWidget(splitter)
        
        # Set up table headers
        self.setup_tables()
        
        # Connect signals
        self.month_combo.currentIndexChanged.connect(self.refresh_data)
        self.year_combo.currentIndexChanged.connect(self.refresh_data)
        
        # Initial data load
        self.refresh_data()
    
    def setup_tables(self):
        """Set up the table headers and columns"""
        headers = ["ID", "Date", "Name", "Category", "Amount (₺)", "Notes"]
        
        # Income table
        self.income_table.setColumnCount(len(headers))
        self.income_table.setHorizontalHeaderLabels(headers)
        
        # Hide ID column
        self.income_table.setColumnHidden(0, True)
        
        # Set column widths
        self.income_table.setColumnWidth(1, 100)  # Date
        self.income_table.setColumnWidth(2, 200)  # Name
        self.income_table.setColumnWidth(3, 150)  # Category
        self.income_table.setColumnWidth(4, 100)  # Amount
        self.income_table.setColumnWidth(5, 300)  # Notes
        
        # Expense table
        self.expense_table.setColumnCount(len(headers))
        self.expense_table.setHorizontalHeaderLabels(headers)
        
        # Hide ID column
        self.expense_table.setColumnHidden(0, True)
        
        # Set column widths
        self.expense_table.setColumnWidth(1, 100)  # Date
        self.expense_table.setColumnWidth(2, 200)  # Name
        self.expense_table.setColumnWidth(3, 150)  # Category
        self.expense_table.setColumnWidth(4, 100)  # Amount
        self.expense_table.setColumnWidth(5, 300)  # Notes
    
    def refresh_data(self):
        """Refresh the forecast data for the selected period"""
        year = self.year_combo.currentData()
        month = self.month_combo.currentData()
        
        if year is None or month is None:
            return
        
        # Get forecasts for the selected month
        forecasts = self.controller.get_forecasts_by_month(year, month)
        
        # Split by type
        income_forecasts = [f for f in forecasts if f.transaction_type.value == 'income']
        expense_forecasts = [f for f in forecasts if f.transaction_type.value == 'expense']
        
        # Update tables
        self.update_table(self.income_table, income_forecasts)
        self.update_table(self.expense_table, expense_forecasts)
    
    def update_table(self, table, forecasts):
        """Update the table with forecast data"""
        table.setRowCount(0)  # Clear existing rows
        
        for forecast in forecasts:
            row_position = table.rowCount()
            table.insertRow(row_position)
            
            # ID column (hidden)
            id_item = QTableWidgetItem(forecast.id)
            table.setItem(row_position, 0, id_item)
            
            # Date column
            date_item = QTableWidgetItem(forecast.date.strftime("%b %Y"))
            date_item.setTextAlignment(Qt.AlignCenter)
            table.setItem(row_position, 1, date_item)
            
            # Name column
            name_item = QTableWidgetItem(forecast.name)
            name_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            table.setItem(row_position, 2, name_item)
            
            # Category column
            category_text = forecast.category if forecast.category else "N/A"
            category_item = QTableWidgetItem(category_text)
            category_item.setTextAlignment(Qt.AlignCenter)
            
            # Style the category
            font = QFont()
            font.setBold(True)
            category_item.setFont(font)
            
            # Colorize category based on transaction type
            if forecast.transaction_type.value == 'income':
                category_item.setForeground(QColor("#2e7d32"))  # Green for income
            else:
                category_item.setForeground(QColor("#c62828"))  # Red for expense
                
            table.setItem(row_position, 3, category_item)
            
            # Amount column
            amount_item = QTableWidgetItem(f"{forecast.amount:,.2f}")
            amount_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            
            # Make amount bold
            amount_item.setFont(font)
            
            # Colorize amount
            if forecast.transaction_type.value == 'income':
                amount_item.setForeground(QColor("#2e7d32"))  # Green for income
            else:
                amount_item.setForeground(QColor("#c62828"))  # Red for expense
                
            table.setItem(row_position, 4, amount_item)
            
            # Notes column
            notes_text = getattr(forecast, "notes", "")
            notes_item = QTableWidgetItem(notes_text)
            notes_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            table.setItem(row_position, 5, notes_item)
        
        # Add summary row
        self.add_summary_row(table, forecasts)
    
    def add_summary_row(self, table, forecasts):
        """Add a summary row at the bottom of the table"""
        if not forecasts:
            return
        
        row_position = table.rowCount()
        table.insertRow(row_position)
        
        # First cell - "TOTAL"
        total_label = QTableWidgetItem("TOTAL")
        total_label.setFont(QFont("", weight=QFont.Bold))
        total_label.setTextAlignment(Qt.AlignCenter)
        total_label.setBackground(QColor("#f0f0f0"))
        table.setItem(row_position, 1, total_label)
        
        # Empty cells with background
        for col in [2, 3, 5]:
            empty_item = QTableWidgetItem("")
            empty_item.setBackground(QColor("#f0f0f0"))
            table.setItem(row_position, col, empty_item)
        
        # Total amount
        total_amount = sum(f.amount for f in forecasts)
        total_item = QTableWidgetItem(f"{total_amount:,.2f}")
        total_item.setFont(QFont("", weight=QFont.Bold))
        total_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        total_item.setBackground(QColor("#f0f0f0"))
        
        # Set color based on transaction type
        if forecasts and forecasts[0].transaction_type.value == 'income':
            total_item.setForeground(QColor("#2e7d32"))  # Green for income
        else:
            total_item.setForeground(QColor("#c62828"))  # Red for expense
            
        table.setItem(row_position, 4, total_item)
    
    def edit_forecast(self, table):
        """Edit the selected forecast transaction"""
        selected_rows = table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "No Selection", "Please select a forecast to edit.")
            return
        
        # Get the ID from the first column (hidden)
        row = selected_rows[0].row()
        
        # Don't allow editing the summary row
        if row == table.rowCount() - 1 and table.item(row, 0) is None:
            QMessageBox.warning(self, "Invalid Selection", "Cannot edit the summary row.")
            return
        
        forecast_id = table.item(row, 0).text()
        forecast_name = table.item(row, 2).text()
        
        # Implement the edit dialog (similar to the entry form but pre-filled)
        # For simplicity, we'll just show a message for now
        QMessageBox.information(self, "Edit Forecast", 
                              f"Editing forecast: {forecast_name}\nID: {forecast_id}\n\n"
                              "This feature will be implemented in a future update.")
        
        # TODO: Implement a proper edit dialog
    
    def delete_forecast(self, table):
        """Delete the selected forecast transaction"""
        selected_rows = table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "No Selection", "Please select a forecast to delete.")
            return
        
        # Get the ID from the first column (hidden)
        row = selected_rows[0].row()
        
        # Don't allow deleting the summary row
        if row == table.rowCount() - 1 and table.item(row, 0) is None:
            QMessageBox.warning(self, "Invalid Selection", "Cannot delete the summary row.")
            return
        
        forecast_id = table.item(row, 0).text()
        forecast_name = table.item(row, 2).text()
        
        # Ask for confirmation
        reply = QMessageBox.question(self, "Confirm Deletion", 
                                   f"Are you sure you want to delete the forecast '{forecast_name}'?",
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # Delete the forecast
            if self.controller.remove_forecast(forecast_id):
                QMessageBox.information(self, "Success", f"Forecast '{forecast_name}' has been deleted.")
                self.refresh_data()
                self.forecast_updated.emit()
            else:
                QMessageBox.critical(self, "Error", f"Failed to delete forecast '{forecast_name}'.")


class ForecastComparison(QWidget):
    """Widget to compare forecast with actual financial data"""
    
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.init_ui()
        
    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Period selection
        period_layout = QHBoxLayout()
        
        period_label = QLabel("Select Period for Comparison:")
        period_label.setStyleSheet("font-weight: bold;")
        
        self.month_combo = QComboBox()
        for i in range(1, 13):
            self.month_combo.addItem(calendar.month_name[i], i)
        
        current_date = datetime.now()
        # Default to previous month for comparison
        prev_month = current_date.month - 1
        if prev_month == 0:
            prev_month = 12
        prev_month_idx = self.month_combo.findData(prev_month)
        if prev_month_idx >= 0:
            self.month_combo.setCurrentIndex(prev_month_idx)
        
        self.year_combo = QComboBox()
        
        # Get unique years
        years = self.controller.get_unique_years()
        for year in years:
            self.year_combo.addItem(str(year), year)
        
        # If previous month is December, default to previous year
        prev_year = current_date.year
        if prev_month == 12:
            prev_year -= 1
        
        prev_year_idx = self.year_combo.findData(prev_year)
        if prev_year_idx >= 0:
            self.year_combo.setCurrentIndex(prev_year_idx)
        
        self.compare_btn = QPushButton("Compare")
        self.compare_btn.clicked.connect(self.perform_comparison)
        self.compare_btn.setObjectName("primaryButton")
        
        period_layout.addWidget(period_label)
        period_layout.addWidget(self.month_combo)
        period_layout.addWidget(self.year_combo)
        period_layout.addWidget(self.compare_btn)
        period_layout.addStretch()
        
        main_layout.addLayout(period_layout)
        
        # Results area - we'll use a simple grid layout for now
        # In a real implementation, this would display charts and tables
        self.results_frame = QFrame()
        self.results_frame.setFrameShape(QFrame.StyledPanel)
        self.results_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                border: 1px solid rgba(0, 0, 0, 0.1);
                padding: 10px;
            }
        """)
        
        self.results_layout = QVBoxLayout(self.results_frame)
        
        # Welcome/instruction message
        self.welcome_label = QLabel(
            "Select a month and year, then click 'Compare' to view the comparison between\n"
            "forecast and actual financial data for that period."
        )
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.welcome_label.setStyleSheet("font-size: 13px; color: #666;")
        
        self.results_layout.addWidget(self.welcome_label)
        
        main_layout.addWidget(self.results_frame)
        
    def perform_comparison(self):
        """Compare forecast with actual data for the selected period"""
        year = self.year_combo.currentData()
        month = self.month_combo.currentData()
        
        if year is None or month is None:
            return
        
        # Clear previous results
        self.clear_results()
        
        # Get comparison data
        comparison_data = self.controller.compare_forecast_vs_actual(year, month)
        
        # Display results
        self.display_comparison_results(comparison_data, year, month)
        
    def clear_results(self):
        """Clear the results area"""
        # Remove all widgets from the results layout
        while self.results_layout.count():
            child = self.results_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
    
    def display_comparison_results(self, comparison_data, year, month):
        """Display the comparison results"""
        # Title
        title_label = QLabel(f"Forecast vs. Actual - {calendar.month_name[month]} {year}")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #3a4f9b;")
        title_label.setAlignment(Qt.AlignCenter)
        self.results_layout.addWidget(title_label)
        
        # Overall summary
        summary_frame = QFrame()
        summary_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-radius: 8px;
                border: 1px solid rgba(0, 0, 0, 0.1);
                padding: 5px;
            }
        """)
        
        summary_layout = QGridLayout(summary_frame)
        summary_layout.setColumnStretch(0, 1)  # Label column
        summary_layout.setColumnStretch(1, 1)  # Forecast column
        summary_layout.setColumnStretch(2, 1)  # Actual column
        summary_layout.setColumnStretch(3, 1)  # Variance column
        
        # Headers
        summary_layout.addWidget(QLabel(""), 0, 0)
        
        forecast_header = QLabel("Forecast")
        forecast_header.setAlignment(Qt.AlignCenter)
        forecast_header.setStyleSheet("font-weight: bold; color: #555;")
        summary_layout.addWidget(forecast_header, 0, 1)
        
        actual_header = QLabel("Actual")
        actual_header.setAlignment(Qt.AlignCenter)
        actual_header.setStyleSheet("font-weight: bold; color: #555;")
        summary_layout.addWidget(actual_header, 0, 2)
        
        variance_header = QLabel("Variance")
        variance_header.setAlignment(Qt.AlignCenter)
        variance_header.setStyleSheet("font-weight: bold; color: #555;")
        summary_layout.addWidget(variance_header, 0, 3)
        
        # Row labels
        income_label = QLabel("Income")
        income_label.setStyleSheet("font-weight: bold; color: #2e7d32;")
        summary_layout.addWidget(income_label, 1, 0)
        
        expenses_label = QLabel("Expenses")
        expenses_label.setStyleSheet("font-weight: bold; color: #c62828;")
        summary_layout.addWidget(expenses_label, 2, 0)
        
        net_label = QLabel("Net")
        net_label.setStyleSheet("font-weight: bold; color: #1565c0;")
        summary_layout.addWidget(net_label, 3, 0)
        
        # Income row
        income_forecast = QLabel(f"{comparison_data['summary']['income']['forecast']:,.2f} ₺")
        income_forecast.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        income_forecast.setStyleSheet("color: #2e7d32;")
        summary_layout.addWidget(income_forecast, 1, 1)
        
        income_actual = QLabel(f"{comparison_data['summary']['income']['actual']:,.2f} ₺")
        income_actual.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        income_actual.setStyleSheet("color: #2e7d32;")
        summary_layout.addWidget(income_actual, 1, 2)
        
        income_variance = QLabel(f"{comparison_data['summary']['income']['variance']:+,.2f} ₺ ({comparison_data['summary']['income']['variance_pct']:+.1f}%)")
        income_variance.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        if comparison_data['summary']['income']['variance'] >= 0:
            income_variance.setStyleSheet("color: #2e7d32; font-weight: bold;")
        else:
            income_variance.setStyleSheet("color: #c62828; font-weight: bold;")
        summary_layout.addWidget(income_variance, 1, 3)
        
        # Expenses row
        expenses_forecast = QLabel(f"{comparison_data['summary']['expenses']['forecast']:,.2f} ₺")
        expenses_forecast.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        expenses_forecast.setStyleSheet("color: #c62828;")
        summary_layout.addWidget(expenses_forecast, 2, 1)
        
        expenses_actual = QLabel(f"{comparison_data['summary']['expenses']['actual']:,.2f} ₺")
        expenses_actual.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        expenses_actual.setStyleSheet("color: #c62828;")
        summary_layout.addWidget(expenses_actual, 2, 2)
        
        expenses_variance = QLabel(f"{comparison_data['summary']['expenses']['variance']:+,.2f} ₺ ({comparison_data['summary']['expenses']['variance_pct']:+.1f}%)")
        expenses_variance.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        if comparison_data['summary']['expenses']['variance'] <= 0:
            expenses_variance.setStyleSheet("color: #2e7d32; font-weight: bold;")
        else:
            expenses_variance.setStyleSheet("color: #c62828; font-weight: bold;")
        summary_layout.addWidget(expenses_variance, 2, 3)
        
        # Net row
        net_forecast = QLabel(f"{comparison_data['summary']['net_worth']['forecast']:,.2f} ₺")
        net_forecast.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        net_forecast.setStyleSheet("color: #1565c0;")
        summary_layout.addWidget(net_forecast, 3, 1)
        
        net_actual = QLabel(f"{comparison_data['summary']['net_worth']['actual']:,.2f} ₺")
        net_actual.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        net_actual.setStyleSheet("color: #1565c0;")
        summary_layout.addWidget(net_actual, 3, 2)
        
        net_variance = QLabel(f"{comparison_data['summary']['net_worth']['variance']:+,.2f} ₺ ({comparison_data['summary']['net_worth']['variance_pct']:+.1f}%)")
        net_variance.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        if comparison_data['summary']['net_worth']['variance'] >= 0:
            net_variance.setStyleSheet("color: #2e7d32; font-weight: bold;")
        else:
            net_variance.setStyleSheet("color: #c62828; font-weight: bold;")
        summary_layout.addWidget(net_variance, 3, 3)
        
        self.results_layout.addWidget(summary_frame)
        
        # Category breakdown headers
        self.results_layout.addSpacing(15)
        
        income_cat_label = QLabel("Income Categories")
        income_cat_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #2e7d32;")
        self.results_layout.addWidget(income_cat_label)
        
        # Income categories table
        income_table = QTableWidget()
        income_table.setColumnCount(4)
        income_table.setHorizontalHeaderLabels(["Category", "Forecast", "Actual", "Variance"])
        income_table.setAlternatingRowColors(True)
        income_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        income_table.setStyleSheet("""
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
        
        # Add income category rows
        income_categories = comparison_data['income_categories']
        income_table.setRowCount(len(income_categories))
        
        for i, (category, data) in enumerate(income_categories.items()):
            # Category name
            cat_item = QTableWidgetItem(category)
            cat_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            income_table.setItem(i, 0, cat_item)
            
            # Forecast amount
            forecast_item = QTableWidgetItem(f"{data['forecast']:,.2f} ₺")
            forecast_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            income_table.setItem(i, 1, forecast_item)
            
            # Actual amount
            actual_item = QTableWidgetItem(f"{data['actual']:,.2f} ₺")
            actual_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            income_table.setItem(i, 2, actual_item)
            
            # Variance
            variance_item = QTableWidgetItem(f"{data['variance']:+,.2f} ₺ ({data['variance_pct']:+.1f}%)")
            variance_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            
            if data['variance'] >= 0:
                variance_item.setForeground(QColor("#2e7d32"))  # Green for positive variance
            else:
                variance_item.setForeground(QColor("#c62828"))  # Red for negative variance
                
            income_table.setItem(i, 3, variance_item)
        
        income_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        income_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        income_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        income_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        
        income_table.setMaximumHeight(150)
        self.results_layout.addWidget(income_table)
        
        # Expense categories
        self.results_layout.addSpacing(15)
        
        expense_cat_label = QLabel("Expense Categories")
        expense_cat_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #c62828;")
        self.results_layout.addWidget(expense_cat_label)
        
        # Expense categories table
        expense_table = QTableWidget()
        expense_table.setColumnCount(4)
        expense_table.setHorizontalHeaderLabels(["Category", "Forecast", "Actual", "Variance"])
        expense_table.setAlternatingRowColors(True)
        expense_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        expense_table.setStyleSheet("""
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
        
        # Add expense category rows
        expense_categories = comparison_data['expense_categories']
        expense_table.setRowCount(len(expense_categories))
        
        for i, (category, data) in enumerate(expense_categories.items()):
            # Category name
            cat_item = QTableWidgetItem(category)
            cat_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            expense_table.setItem(i, 0, cat_item)
            
            # Forecast amount
            forecast_item = QTableWidgetItem(f"{data['forecast']:,.2f} ₺")
            forecast_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            expense_table.setItem(i, 1, forecast_item)
            
            # Actual amount
            actual_item = QTableWidgetItem(f"{data['actual']:,.2f} ₺")
            actual_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            expense_table.setItem(i, 2, actual_item)
            
            # Variance
            variance_item = QTableWidgetItem(f"{data['variance']:+,.2f} ₺ ({data['variance_pct']:+.1f}%)")
            variance_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            
            # For expenses, negative variance is good (spent less than forecast)
            if data['variance'] <= 0:
                variance_item.setForeground(QColor("#2e7d32"))  # Green for positive (under budget)
            else:
                variance_item.setForeground(QColor("#c62828"))  # Red for negative (over budget)
                
            expense_table.setItem(i, 3, variance_item)
        
        expense_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        expense_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        expense_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        expense_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        
        expense_table.setMaximumHeight(150)
        self.results_layout.addWidget(expense_table)
        
        # Add explanation text
        self.results_layout.addSpacing(15)
        
        explanation = QLabel(
            "Note: Positive variances for income indicate actual income exceeded forecasts.\n"
            "Negative variances for expenses indicate actual expenses were lower than forecasts."
        )
        explanation.setAlignment(Qt.AlignCenter)
        explanation.setStyleSheet("font-style: italic; color: #666;")
        
        self.results_layout.addWidget(explanation)


class ForecastManagement(QWidget):
    """Main widget for forecast management tab"""
    
    forecast_changed = pyqtSignal()
    
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.init_ui()
        
    def init_ui(self):
        # Main layout with tabs
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Create tab widget
        tab_widget = QTabWidget()
        tab_widget.setDocumentMode(True)
        
        # Create forecast tabs
        self.forecast_entry = ForecastEntryForm(self.controller)
        self.forecast_entry.forecast_added.connect(self.on_forecast_changed)
        
        self.forecast_list = ForecastList(self.controller)
        self.forecast_list.forecast_updated.connect(self.on_forecast_changed)
        
        self.comparison = ForecastComparison(self.controller)
        
        # Add tabs to widget
        tab_widget.addTab(self.forecast_entry, "Add Forecast")
        tab_widget.addTab(self.forecast_list, "View Forecasts")
        tab_widget.addTab(self.comparison, "Compare with Actual")
        
        main_layout.addWidget(tab_widget)
    
    def on_forecast_changed(self):
        """Handle forecast add/update/delete events"""
        self.forecast_changed.emit()