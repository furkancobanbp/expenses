from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, 
                             QLabel, QLineEdit, QComboBox, QPushButton, 
                             QDateEdit, QMessageBox, QGridLayout, QFrame,
                             QTableWidget, QTableWidgetItem, QHeaderView,
                             QAbstractItemView, QSplitter, QProgressBar,
                             QSpacerItem, QSizePolicy, QScrollArea)
from PyQt5.QtCore import Qt, pyqtSignal, QDate
from PyQt5.QtGui import QFont, QColor, QIcon

import calendar
from datetime import datetime
from models.financial_goal import GoalType

class GoalProgressWidget(QFrame):
    """Widget to display progress for a single goal"""
    def __init__(self, goal_data):
        super().__init__()
        self.goal_data = goal_data
        self.setObjectName("goalCard")
        self.setStyleSheet("""
            #goalCard {
                background-color: white;
                border-radius: 8px;
                padding: 10px;
                border: 1px solid rgba(0, 0, 0, 0.1);
            }
        """)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        goal = self.goal_data["goal"]
        
        # Goal title with type indicator
        title_layout = QHBoxLayout()
        
        # Icon/color indicator based on goal type
        type_indicator = QLabel()
        type_indicator.setFixedSize(16, 16)
        
        if goal.goal_type.value == "income":
            type_indicator.setStyleSheet("background-color: #2e7d32; border-radius: 8px;")
            color_style = "color: #2e7d32;"
        elif goal.goal_type.value == "expense":
            type_indicator.setStyleSheet("background-color: #c62828; border-radius: 8px;")
            color_style = "color: #c62828;"
        else:  # savings
            type_indicator.setStyleSheet("background-color: #1565c0; border-radius: 8px;")
            color_style = "color: #1565c0;"
        
        title_layout.addWidget(type_indicator)
        
        # Goal name
        goal_title = QLabel(goal.name)
        goal_title.setStyleSheet(f"font-size: 14px; font-weight: bold; {color_style}")
        title_layout.addWidget(goal_title)
        title_layout.addStretch()
        
        # Goal target amount
        goal_amount = QLabel(f"{goal.amount:,.2f} ₺")
        goal_amount.setStyleSheet(f"font-size: 14px; font-weight: bold; {color_style}")
        title_layout.addWidget(goal_amount)
        
        layout.addLayout(title_layout)
        
        # Description label
        description = ""
        if goal.goal_type.value == "income":
            description = f"Income goal for {calendar.month_name[goal.month]} {goal.year}"
        elif goal.goal_type.value == "expense":
            description = f"Expense budget for {calendar.month_name[goal.month]} {goal.year}"
        else:  # savings
            description = f"Savings target for {calendar.month_name[goal.month]} {goal.year}"
            
        desc_label = QLabel(description)
        desc_label.setStyleSheet("color: #6c757d; font-size: 12px;")
        layout.addWidget(desc_label)
        
        # Progress bar
        progress_bar = QProgressBar()
        progress_bar.setMinimum(0)
        progress_bar.setMaximum(100)
        progress_bar.setValue(int(self.goal_data["percentage"]))
        
        # Style progress bar based on type and progress
        if goal.goal_type.value == "income":
            progress_bar.setStyleSheet("""
                QProgressBar {
                    border: 1px solid #e0e0e0;
                    border-radius: 4px;
                    text-align: center;
                    height: 20px;
                    background-color: #f5f5f5;
                }
                QProgressBar::chunk {
                    background-color: #81c784;
                    border-radius: 3px;
                }
            """)
        elif goal.goal_type.value == "expense":
            # For expenses, we want to show warning as we approach the limit
            if self.goal_data["percentage"] < 75:
                bar_color = "#81c784"  # Green - good, under budget
            elif self.goal_data["percentage"] < 90:
                bar_color = "#ffb74d"  # Orange - warning, approaching budget
            else:
                bar_color = "#e57373"  # Red - danger, at or over budget
                
            progress_bar.setStyleSheet(f"""
                QProgressBar {{
                    border: 1px solid #e0e0e0;
                    border-radius: 4px;
                    text-align: center;
                    height: 20px;
                    background-color: #f5f5f5;
                }}
                QProgressBar::chunk {{
                    background-color: {bar_color};
                    border-radius: 3px;
                }}
            """)
        else:  # savings
            progress_bar.setStyleSheet("""
                QProgressBar {
                    border: 1px solid #e0e0e0;
                    border-radius: 4px;
                    text-align: center;
                    height: 20px;
                    background-color: #f5f5f5;
                }
                QProgressBar::chunk {
                    background-color: #64b5f6;
                    border-radius: 3px;
                }
            """)
            
        layout.addWidget(progress_bar)
        
        # Current amount and remaining
        amount_layout = QHBoxLayout()
        
        # Current amount
        current_label = QLabel(f"Current: {self.goal_data['current_amount']:,.2f} ₺")
        current_label.setStyleSheet("font-size: 12px;")
        amount_layout.addWidget(current_label)
        
        amount_layout.addStretch()
        
        # Remaining amount - with different wording for expense goals
        if goal.goal_type.value == "expense":
            if self.goal_data["remaining"] > 0:
                remaining_text = f"Remaining Budget: {self.goal_data['remaining']:,.2f} ₺"
            else:
                remaining_text = f"Over Budget: {-self.goal_data['remaining']:,.2f} ₺"
        else:
            remaining_text = f"To Goal: {self.goal_data['remaining']:,.2f} ₺"
            
        remaining_label = QLabel(remaining_text)
        remaining_label.setStyleSheet("font-size: 12px;")
        amount_layout.addWidget(remaining_label)
        
        layout.addLayout(amount_layout)


class AddGoalWidget(QFrame):
    """Widget for adding a new financial goal"""
    goal_added = pyqtSignal()
    
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setObjectName("addGoalCard")
        self.setStyleSheet("""
            #addGoalCard {
                background-color: white;
                border-radius: 8px;
                padding: 10px;
                border: 1px solid rgba(0, 0, 0, 0.1);
            }
        """)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Title
        title = QLabel("Create New Goal")
        title.setStyleSheet("font-size: 14px; font-weight: bold; color: #3a4f9b;")
        layout.addWidget(title)
        
        # Form layout
        form_layout = QFormLayout()
        form_layout.setVerticalSpacing(10)
        form_layout.setHorizontalSpacing(15)
        
        # Goal name
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("e.g., Monthly Salary Target, Grocery Budget")
        form_layout.addRow("Goal Name:", self.name_edit)
        
        # Goal amount
        self.amount_edit = QLineEdit()
        self.amount_edit.setPlaceholderText("Target amount in ₺")
        form_layout.addRow("Target Amount:", self.amount_edit)
        
        # Goal type
        self.type_combo = QComboBox()
        self.type_combo.addItem("Income Goal", GoalType.INCOME)
        self.type_combo.addItem("Expense Budget", GoalType.EXPENSE)
        self.type_combo.addItem("Savings Target", GoalType.SAVINGS)
        form_layout.addRow("Goal Type:", self.type_combo)
        
        # Month and year
        date_layout = QHBoxLayout()
        
        self.month_combo = QComboBox()
        for i in range(1, 13):
            self.month_combo.addItem(calendar.month_name[i], i)
        
        current_date = datetime.now()
        current_month_idx = self.month_combo.findData(current_date.month)
        if current_month_idx >= 0:
            self.month_combo.setCurrentIndex(current_month_idx)
            
        date_layout.addWidget(self.month_combo)
        
        self.year_combo = QComboBox()
        current_year = current_date.year
        for year in range(current_year - 1, current_year + 3):
            self.year_combo.addItem(str(year), year)
        
        current_year_idx = self.year_combo.findData(current_year)
        if current_year_idx >= 0:
            self.year_combo.setCurrentIndex(current_year_idx)
            
        date_layout.addWidget(self.year_combo)
        
        form_layout.addRow("Period:", date_layout)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_form)
        button_layout.addWidget(self.clear_btn)
        
        self.add_btn = QPushButton("Add Goal")
        self.add_btn.setObjectName("primaryButton")
        self.add_btn.clicked.connect(self.add_goal)
        button_layout.addWidget(self.add_btn)
        
        layout.addLayout(button_layout)
        
    def clear_form(self):
        """Clear all form fields"""
        self.name_edit.clear()
        self.amount_edit.clear()
        self.type_combo.setCurrentIndex(0)
        
        # Reset to current month/year
        current_date = datetime.now()
        current_month_idx = self.month_combo.findData(current_date.month)
        if current_month_idx >= 0:
            self.month_combo.setCurrentIndex(current_month_idx)
            
        current_year_idx = self.year_combo.findData(current_date.year)
        if current_year_idx >= 0:
            self.year_combo.setCurrentIndex(current_year_idx)
            
    def add_goal(self):
        """Add a new financial goal"""
        # Validate input
        name = self.name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "Input Error", "Please enter a goal name.")
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
        
        # Get goal type, month and year
        goal_type = self.type_combo.currentData()
        month = self.month_combo.currentData()
        year = self.year_combo.currentData()
        
        # Add goal
        try:
            self.controller.add_goal(name, amount, goal_type, year, month)
            
            # Show success message
            QMessageBox.information(self, "Success", "Financial goal added successfully!")
            
            # Clear form
            self.clear_form()
            
            # Emit signal
            self.goal_added.emit()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add goal: {str(e)}")


class GoalsTab(QWidget):
    """Main widget for the Goals tab"""
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.init_ui()
        
    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(15)
        
        # Split into two sections - left for goals list, right for adding new goals
        splitter = QSplitter(Qt.Horizontal)
        
        # Left side - Goals List
        goals_widget = QWidget()
        goals_layout = QVBoxLayout(goals_widget)
        goals_layout.setContentsMargins(0, 0, 0, 0)
        goals_layout.setSpacing(10)
        
        # Filter section
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(15)
        
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
        
        # Get unique years from the controller
        years = self.controller.get_unique_years()
        for year in years:
            self.year_combo.addItem(str(year), year)
            
        # Add the next year as well
        next_year = max(years) + 1 if years else current_date.year + 1
        self.year_combo.addItem(str(next_year), next_year)
        
        # Set to current year
        current_year_idx = self.year_combo.findData(current_date.year)
        if current_year_idx >= 0:
            self.year_combo.setCurrentIndex(current_year_idx)
            
        filter_layout.addWidget(period_label)
        filter_layout.addWidget(self.month_combo)
        filter_layout.addWidget(self.year_combo)
        filter_layout.addStretch()
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh_goals)
        filter_layout.addWidget(refresh_btn)
        
        goals_layout.addLayout(filter_layout)
        
        # Scrollable area for goals
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        
        # Container widget for goal cards
        self.goals_container = QWidget()
        self.goals_container_layout = QVBoxLayout(self.goals_container)
        self.goals_container_layout.setContentsMargins(0, 0, 0, 0)
        self.goals_container_layout.setSpacing(10)
        self.goals_container_layout.addStretch()
        
        scroll_area.setWidget(self.goals_container)
        goals_layout.addWidget(scroll_area)
        
        # Right side - Add new goal
        self.add_goal_widget = AddGoalWidget(self.controller)
        self.add_goal_widget.goal_added.connect(self.refresh_goals)
        
        # Add widgets to splitter
        splitter.addWidget(goals_widget)
        splitter.addWidget(self.add_goal_widget)
        
        # Set initial sizes (left side larger)
        splitter.setSizes([700, 300])
        
        main_layout.addWidget(splitter)
        
        # Connect signals
        self.month_combo.currentIndexChanged.connect(self.refresh_goals)
        self.year_combo.currentIndexChanged.connect(self.refresh_goals)
        
        # Initial refresh
        self.refresh_goals()
        
    def refresh_goals(self):
        """Refresh the list of goals"""
        # Clear existing goals
        while self.goals_container_layout.count() > 1:
            item = self.goals_container_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
                
        # Get selected month and year
        month = self.month_combo.currentData()
        year = self.year_combo.currentData()
        
        if not month or not year:
            return
            
        # Get goals for the selected period
        goals = self.controller.get_goals_by_month(year, month)
        
        if not goals:
            # No goals message
            no_goals_label = QLabel("No goals set for this period. Create a new goal to get started!")
            no_goals_label.setStyleSheet("font-size: 13px; color: #6c757d; font-style: italic;")
            no_goals_label.setAlignment(Qt.AlignCenter)
            self.goals_container_layout.insertWidget(0, no_goals_label)
            return
            
        # Add goals in reverse order (newest first)
        for goal in reversed(goals):
            # Get progress data
            progress_data = self.controller.get_goal_progress(goal.id)
            
            # Create and add goal widget
            goal_widget = GoalProgressWidget(progress_data)
            self.goals_container_layout.insertWidget(0, goal_widget)