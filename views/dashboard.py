import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QComboBox, 
                           QLabel, QSizePolicy, QGroupBox, QFrame)
from PyQt5.QtCore import Qt, pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import calendar

class MplCanvas(FigureCanvas):
    def __init__(self, width=5, height=4, dpi=100):
        # Create figure with modern styling
        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor='#ffffff')
        self.fig.subplots_adjust(left=0.1, right=0.95, top=0.9, bottom=0.13)
        
        # Add subplot with grid
        self.axes = self.fig.add_subplot(111)
        self.axes.grid(True, linestyle='--', alpha=0.3, color='#cccccc')
        
        # Style improvements
        self.axes.spines['top'].set_visible(False)
        self.axes.spines['right'].set_visible(False)
        self.axes.spines['left'].set_alpha(0.3)
        self.axes.spines['bottom'].set_alpha(0.3)
        
        # Font styling
        self.axes.xaxis.label.set_color('#495057')
        self.axes.yaxis.label.set_color('#495057')
        self.axes.title.set_color('#212529')
        
        # Tick styling
        self.axes.tick_params(colors='#6c757d', direction='out', length=5, width=1, grid_alpha=0.3)
        
        super(MplCanvas, self).__init__(self.fig)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.updateGeometry()

class Dashboard(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.init_ui()
        
    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Summary section
        summary_group = QGroupBox("Monthly Summary")
        summary_layout = QVBoxLayout(summary_group)
        
        # Month and year selector
        selector_layout = QHBoxLayout()
        
        year_label = QLabel("Year:")
        self.year_combo = QComboBox()
        self.update_year_combo()
        
        month_label = QLabel("Month:")
        self.month_combo = QComboBox()
        for i in range(1, 13):
            self.month_combo.addItem(calendar.month_name[i], i)
        
        # Default to current month/year
        current_date = datetime.now()
        current_month_idx = self.month_combo.findData(current_date.month)
        if current_month_idx >= 0:
            self.month_combo.setCurrentIndex(current_month_idx)
        
        selector_layout.addWidget(year_label)
        selector_layout.addWidget(self.year_combo)
        selector_layout.addWidget(month_label)
        selector_layout.addWidget(self.month_combo)
        selector_layout.addStretch()
        
        summary_layout.addLayout(selector_layout)
        
        # Summary values - using modern card-like design
        summary_values_layout = QHBoxLayout()
        summary_values_layout.setSpacing(15)
        
        # Income card
        income_frame = QFrame()
        income_frame.setObjectName("card")
        income_frame.setStyleSheet("""
            #card {
                background-color: #e8f5e9;
                border-radius: 10px;
                padding: 15px;
                border: 1px solid rgba(0, 0, 0, 0.05);
            }
        """)
        income_layout = QVBoxLayout(income_frame)
        income_layout.setContentsMargins(15, 15, 15, 15)
        
        income_label = QLabel("Total Income")
        income_label.setStyleSheet("font-size: 16px; font-weight: 500; color: #2e7d32;")
        self.income_value = QLabel("$0.00")
        self.income_value.setObjectName("valueLabel")
        self.income_value.setStyleSheet("font-size: 22px; font-weight: bold; color: #2e7d32;")
        self.income_value.setAlignment(Qt.AlignCenter)
        
        income_layout.addWidget(income_label, alignment=Qt.AlignCenter)
        income_layout.addWidget(self.income_value, alignment=Qt.AlignCenter)
        
        # Expenses card
        expenses_frame = QFrame()
        expenses_frame.setObjectName("card")
        expenses_frame.setStyleSheet("""
            #card {
                background-color: #ffebee;
                border-radius: 10px;
                padding: 15px;
                border: 1px solid rgba(0, 0, 0, 0.05);
            }
        """)
        expenses_layout = QVBoxLayout(expenses_frame)
        expenses_layout.setContentsMargins(15, 15, 15, 15)
        
        expenses_label = QLabel("Total Expenses")
        expenses_label.setStyleSheet("font-size: 16px; font-weight: 500; color: #c62828;")
        self.expenses_value = QLabel("$0.00")
        self.expenses_value.setObjectName("valueLabel")
        self.expenses_value.setStyleSheet("font-size: 22px; font-weight: bold; color: #c62828;")
        self.expenses_value.setAlignment(Qt.AlignCenter)
        
        expenses_layout.addWidget(expenses_label, alignment=Qt.AlignCenter)
        expenses_layout.addWidget(self.expenses_value, alignment=Qt.AlignCenter)
        
        # Net Worth card
        net_frame = QFrame()
        net_frame.setObjectName("card")
        net_frame.setStyleSheet("""
            #card {
                background-color: #e3f2fd;
                border-radius: 10px;
                padding: 15px;
                border: 1px solid rgba(0, 0, 0, 0.05);
            }
        """)
        net_layout = QVBoxLayout(net_frame)
        net_layout.setContentsMargins(15, 15, 15, 15)
        
        net_label = QLabel("Net Worth")
        net_label.setStyleSheet("font-size: 16px; font-weight: 500; color: #1565c0;")
        self.net_value = QLabel("$0.00")
        self.net_value.setObjectName("valueLabel")
        self.net_value.setStyleSheet("font-size: 22px; font-weight: bold; color: #1565c0;")
        self.net_value.setAlignment(Qt.AlignCenter)
        
        net_layout.addWidget(net_label, alignment=Qt.AlignCenter)
        net_layout.addWidget(self.net_value, alignment=Qt.AlignCenter)
        
        summary_values_layout.addLayout(income_layout)
        summary_values_layout.addLayout(expenses_layout)
        summary_values_layout.addLayout(net_layout)
        
        summary_layout.addLayout(summary_values_layout)
        main_layout.addWidget(summary_group)
        
        # Charts section
        charts_layout = QHBoxLayout()
        
        # Monthly chart
        monthly_group = QGroupBox("Monthly Breakdown")
        monthly_layout = QVBoxLayout(monthly_group)
        self.monthly_canvas = MplCanvas(width=5, height=4, dpi=100)
        monthly_layout.addWidget(self.monthly_canvas)
        charts_layout.addWidget(monthly_group)
        
        # Cumulative chart
        cumulative_group = QGroupBox("Cumulative Overview")
        cumulative_layout = QVBoxLayout(cumulative_group)
        self.cumulative_canvas = MplCanvas(width=5, height=4, dpi=100)
        cumulative_layout.addWidget(self.cumulative_canvas)
        charts_layout.addWidget(cumulative_group)
        
        main_layout.addLayout(charts_layout)
        
        # Connect signals
        self.year_combo.currentIndexChanged.connect(self.on_date_changed)
        self.month_combo.currentIndexChanged.connect(self.on_date_changed)
        
        # Initial refresh
        self.refresh_charts()
        
    def update_year_combo(self):
        """Update the years in the combo box based on transaction history"""
        self.year_combo.clear()
        years = self.controller.get_unique_years()
        
        for year in years:
            self.year_combo.addItem(str(year), year)
            
        # Set current year
        current_year = datetime.now().year
        current_year_idx = self.year_combo.findData(current_year)
        if current_year_idx >= 0:
            self.year_combo.setCurrentIndex(current_year_idx)
        else:
            # If current year not in list, select the most recent
            self.year_combo.setCurrentIndex(self.year_combo.count() - 1)
        
    def on_date_changed(self):
        """Handle date selection change"""
        self.refresh_charts()
        
    def refresh_charts(self):
        """Refresh all charts and summary data"""
        # Get selected year and month
        year = self.year_combo.currentData()
        month = self.month_combo.currentData()
        
        if year is None or month is None:
            return
            
        # Update summary values
        summary = self.controller.get_monthly_summary(year, month)
        self.income_value.setText(f"${summary['total_income']:.2f}")
        self.expenses_value.setText(f"${summary['total_expenses']:.2f}")
        
        # Set color based on positive or negative net worth
        net_worth = summary['net_worth']
        if net_worth >= 0:
            self.net_value.setStyleSheet("font-size: 22px; font-weight: bold; color: #2e7d32;")
        else:
            self.net_value.setStyleSheet("font-size: 22px; font-weight: bold; color: #c62828;")
        self.net_value.setText(f"${net_worth:.2f}")
        
        # Update monthly chart
        self.update_monthly_chart(year)
        
        # Update cumulative chart
        self.update_cumulative_chart()
        
    def update_monthly_chart(self, year):
        """Update the monthly breakdown chart"""
        monthly_data = self.controller.get_monthly_data_for_year(year)
        
        # Clear previous plot
        self.monthly_canvas.axes.clear()
        
        months = list(range(1, 13))
        income_values = [monthly_data[m]['total_income'] for m in months]
        expense_values = [monthly_data[m]['total_expenses'] for m in months]
        
        # Create bar chart with modern colors
        x = range(len(months))
        width = 0.35
        
        self.monthly_canvas.axes.bar([i - width/2 for i in x], income_values, width, 
                                     label='Income', color='#2e7d32', alpha=0.85,
                                     edgecolor='white', linewidth=0.7)
        self.monthly_canvas.axes.bar([i + width/2 for i in x], expense_values, width, 
                                     label='Expenses', color='#c62828', alpha=0.85,
                                     edgecolor='white', linewidth=0.7)
        
        # Add labels and formatting with improved styling
        self.monthly_canvas.axes.set_title(f'Monthly Income vs Expenses ({year})', 
                                          fontsize=14, fontweight='bold', pad=15)
        self.monthly_canvas.axes.set_xlabel('Month', fontsize=12, labelpad=10)
        self.monthly_canvas.axes.set_ylabel('Amount ($)', fontsize=12, labelpad=10)
        self.monthly_canvas.axes.set_xticks(x)
        self.monthly_canvas.axes.set_xticklabels([calendar.month_abbr[m] for m in months])
        
        # Improved legend
        legend = self.monthly_canvas.axes.legend(loc='upper right', frameon=True, 
                                               fancybox=True, framealpha=0.9, 
                                               shadow=True, fontsize=10)
        legend.get_frame().set_edgecolor('#cccccc')
        
        self.monthly_canvas.fig.tight_layout()
        self.monthly_canvas.draw()
        
    def update_cumulative_chart(self):
        """Update the cumulative overview chart"""
        cumulative_data = self.controller.get_cumulative_data()
        
        if not cumulative_data:
            # No data to display
            self.cumulative_canvas.axes.clear()
            self.cumulative_canvas.axes.text(0.5, 0.5, 'No transaction data available',
                                           horizontalalignment='center',
                                           verticalalignment='center',
                                           transform=self.cumulative_canvas.axes.transAxes)
            self.cumulative_canvas.draw()
            return
        
        # Extract data for plotting
        dates = [d['date'] for d in cumulative_data]
        income = [d['cumulative_income'] for d in cumulative_data]
        expenses = [d['cumulative_expenses'] for d in cumulative_data]
        net = [d['cumulative_net'] for d in cumulative_data]
        
        # Clear previous plot
        self.cumulative_canvas.axes.clear()
        
        # Create line chart with modern colors and styling
        self.cumulative_canvas.axes.plot(dates, income, '-', label='Income', 
                                        color='#2e7d32', linewidth=2.5, marker='o', 
                                        markersize=5, markerfacecolor='white')
        self.cumulative_canvas.axes.plot(dates, expenses, '-', label='Expenses', 
                                        color='#c62828', linewidth=2.5, marker='o', 
                                        markersize=5, markerfacecolor='white')
        self.cumulative_canvas.axes.plot(dates, net, '-', label='Net Worth', 
                                        color='#1565c0', linewidth=3, marker='o', 
                                        markersize=6, markerfacecolor='white')
        
        # Add labels and formatting with improved styling
        self.cumulative_canvas.axes.set_title('Cumulative Financial Overview', 
                                              fontsize=14, fontweight='bold', pad=15)
        self.cumulative_canvas.axes.set_xlabel('Date', fontsize=12, labelpad=10)
        self.cumulative_canvas.axes.set_ylabel('Amount ($)', fontsize=12, labelpad=10)
        
        # Format the dates on x-axis
        self.cumulative_canvas.axes.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        self.cumulative_canvas.axes.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
        
        # Improved legend
        legend = self.cumulative_canvas.axes.legend(loc='upper left', frameon=True, 
                                                  fancybox=True, framealpha=0.9, 
                                                  shadow=True, fontsize=10)
        legend.get_frame().set_edgecolor('#cccccc')
        
        # Rotate date labels for better readability
        plt.setp(self.cumulative_canvas.axes.get_xticklabels(), rotation=45, ha='right')
        
        self.cumulative_canvas.fig.tight_layout()
        self.cumulative_canvas.draw()