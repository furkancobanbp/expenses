from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, 
                             QLabel, QLineEdit, QComboBox, QPushButton, 
                             QMessageBox, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QAbstractItemView, QFrame)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor, QFont

from models.transaction import TransactionType

class CategoryManagerView(QWidget):
    """Widget for managing transaction categories"""
    
    # Signal emitted when categories are changed
    categories_changed = pyqtSignal()
    
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.editing_category = None  # Track which category is being edited
        self.init_ui()
        
    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
        
        # Header
        header_label = QLabel("Transaction Categories")
        header_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #3a4f9b;")
        header_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header_label)
        
        # Split into two sections: table on left, form on right
        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)
        
        # Left side: Table of categories
        table_frame = QFrame()
        table_layout = QVBoxLayout(table_frame)
        table_layout.setContentsMargins(0, 0, 0, 0)
        
        table_label = QLabel("Existing Categories")
        table_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #3a4f9b;")
        table_layout.addWidget(table_label)
        
        self.category_table = QTableWidget()
        self.category_table.setColumnCount(2)
        self.category_table.setHorizontalHeaderLabels(["Category Name", "Type"])
        self.category_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.category_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.category_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.category_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.category_table.setAlternatingRowColors(True)
        self.category_table.verticalHeader().setVisible(False)
        
        # Style the table
        self.category_table.setStyleSheet("""
            QTableView {
                background-color: #f8f9fa;
                alternate-background-color: #e9ecef;
                selection-background-color: #4b6cb7;
                selection-color: white;
            }
            QHeaderView::section {
                background-color: #edf2f7;
                color: #3a4f9b;
                font-weight: bold;
                padding: 6px;
                border: none;
                border-bottom: 1px solid #c5d0e6;
            }
        """)
        
        table_layout.addWidget(self.category_table)
        
        # Buttons for table actions
        table_buttons_layout = QHBoxLayout()
        
        self.edit_btn = QPushButton("Edit Selected")
        self.edit_btn.clicked.connect(self.edit_selected)
        
        self.delete_btn = QPushButton("Delete Selected")
        self.delete_btn.clicked.connect(self.delete_selected)
        
        table_buttons_layout.addWidget(self.edit_btn)
        table_buttons_layout.addWidget(self.delete_btn)
        
        table_layout.addLayout(table_buttons_layout)
        
        # Right side: Add/edit category form
        form_frame = QFrame()
        form_frame.setObjectName("formFrame")
        form_frame.setStyleSheet("""
            #formFrame {
                background-color: white;
                border-radius: 8px;
                border: 1px solid rgba(0, 0, 0, 0.1);
                padding: 10px;
            }
        """)
        
        form_layout = QVBoxLayout(form_frame)
        form_layout.setContentsMargins(15, 15, 15, 15)
        form_layout.setSpacing(15)
        
        # Form title
        self.form_title = QLabel("Add New Category")
        self.form_title.setStyleSheet("font-size: 14px; font-weight: bold; color: #3a4f9b;")
        form_layout.addWidget(self.form_title)
        
        # Form fields
        fields_layout = QFormLayout()
        fields_layout.setVerticalSpacing(15)
        
        # Category name
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Enter category name")
        fields_layout.addRow("Category Name:", self.name_edit)
        
        # Category type
        self.type_combo = QComboBox()
        self.type_combo.addItem("Income", TransactionType.INCOME)
        self.type_combo.addItem("Expense", TransactionType.EXPENSE)
        fields_layout.addRow("Category Type:", self.type_combo)
        
        form_layout.addLayout(fields_layout)
        
        # Form buttons
        buttons_layout = QHBoxLayout()
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.cancel_edit)
        
        self.save_btn = QPushButton("Add Category")
        self.save_btn.setObjectName("primaryButton")
        self.save_btn.clicked.connect(self.save_category)
        
        buttons_layout.addWidget(self.cancel_btn)
        buttons_layout.addWidget(self.save_btn)
        
        form_layout.addLayout(buttons_layout)
        form_layout.addStretch()
        
        # Add frames to content layout
        content_layout.addWidget(table_frame, 2)  # 2/3 of space
        content_layout.addWidget(form_frame, 1)   # 1/3 of space
        
        main_layout.addLayout(content_layout)
        
        # Initial refresh
        self.refresh_categories()
        self.reset_form()
        
    def refresh_categories(self):
        """Refresh the category table"""
        # Clear the table
        self.category_table.setRowCount(0)
        
        # Get all categories
        categories = self.controller.get_all_categories()
        
        # Add rows for each category
        for category in categories:
            row_position = self.category_table.rowCount()
            self.category_table.insertRow(row_position)
            
            # Category name
            name_item = QTableWidgetItem(category["name"])
            self.category_table.setItem(row_position, 0, name_item)
            
            # Category type
            type_item = QTableWidgetItem(category["type"].capitalize())
            
            # Style based on type
            if category["type"] == "income":
                type_item.setForeground(QColor("#2e7d32"))  # Green for income
            else:
                type_item.setForeground(QColor("#c62828"))  # Red for expense
            
            self.category_table.setItem(row_position, 1, type_item)
    
    def edit_selected(self):
        """Load the selected category for editing"""
        selected_rows = self.category_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "No Selection", "Please select a category to edit.")
            return
        
        # Get the first selected row
        row = selected_rows[0].row()
        
        # Get category name and type
        category_name = self.category_table.item(row, 0).text()
        category_type_text = self.category_table.item(row, 1).text().lower()
        
        # Set form values
        self.name_edit.setText(category_name)

        # Set type combo
        type_index = 0 if category_type_text == "income" else 1
        self.type_combo.setCurrentIndex(type_index)
        
        # Update form state
        self.form_title.setText("Edit Category")
        self.save_btn.setText("Update Category")
        
        # Store original name for updating
        self.editing_category = category_name
    
    def delete_selected(self):
        """Delete the selected category"""
        selected_rows = self.category_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "No Selection", "Please select a category to delete.")
            return
        
        # Get the first selected row
        row = selected_rows[0].row()
        category_name = self.category_table.item(row, 0).text()
        
        # Ask for confirmation
        reply = QMessageBox.question(
            self, 
            "Confirm Deletion",
            f"Are you sure you want to delete the category '{category_name}'?\n\n"
            "This will not affect existing transactions with this category.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Delete the category
            success = self.controller.remove_category(category_name)
            
            if success:
                QMessageBox.information(self, "Success", f"Category '{category_name}' has been deleted.")
                self.refresh_categories()
                self.categories_changed.emit()
            else:
                QMessageBox.critical(self, "Error", f"Failed to delete category '{category_name}'.")
    
    def cancel_edit(self):
        """Cancel editing and reset the form"""
        self.reset_form()
    
    def reset_form(self):
        """Reset the form to add new category state"""
        self.name_edit.clear()
        self.type_combo.setCurrentIndex(0)
        self.form_title.setText("Add New Category")
        self.save_btn.setText("Add Category")
        self.editing_category = None
    
    def save_category(self):
        """Save or update a category"""
        # Validate input
        name = self.name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "Input Error", "Please enter a category name.")
            return
        
        # Get selected type
        transaction_type = self.type_combo.currentData()
        
        # Check if we're editing or adding
        if self.editing_category:
            # Update existing category
            success = self.controller.update_category(self.editing_category, name, transaction_type)
            message = f"Category '{self.editing_category}' has been updated to '{name}'."
        else:
            # Add new category
            success = self.controller.add_category(name, transaction_type)
            message = f"New category '{name}' has been added."
        
        if success:
            QMessageBox.information(self, "Success", message)
            self.refresh_categories()
            self.reset_form()
            self.categories_changed.emit()
        else:
            QMessageBox.critical(
                self, 
                "Error", 
                f"Failed to {'update' if self.editing_category else 'add'} category. "
                "A category with this name may already exist."
            )