import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QComboBox, 
                           QLabel, QSizePolicy, QFrame, QGridLayout, QTabWidget)
from PyQt5.QtCore import Qt, pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import calendar
from collections import defaultdict
import numpy as np

class MplCanvas(FigureCanvas):
    def __init__(self, width=5, height=3, dpi=100):
        # Create figure with modern styling
        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor='#ffffff')
        self.fig.subplots_adjust(left=0.1, right=0.95, top=0.9, bottom=0.15)
        
        # Add subplot with grid
        self.axes = self.fig.add_subplot(111)
        self.axes.grid(True, linestyle='--', alpha=0.3, color='#cccccc')
        
        # Style improvements
        self.axes.spines['top'].set_visible(False)
        self.axes.spines['right'].set_visible(False)
        self.axes.spines['left'].set_alpha(0.3)
        self.axes.spines['bottom'].set_alpha(0.3)
        
        # Font styling
        self.axes.tick_params(labelsize=8)
        self.axes.xaxis.label.set_color('#495057')
        self.axes.xaxis.label.set_fontsize(10)
        self.axes.yaxis.label.set_color('#495057')
        self.axes.yaxis.label.set_fontsize(10)
        self.axes.title.set_color('#212529')
        self.axes.title.set_fontsize(12)
        
        # Tick styling
        self.axes.tick_params(colors='#6c757d', direction='out', length=4, width=1, grid_alpha=0.3)
        
        super(MplCanvas, self).__init__(self.fig)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.updateGeometry()

class Dashboard(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.init_ui()
        
    def init_ui(self):
        # Single main layout with all content
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(5)
        
        # Top section with year/month selector
        top_layout = QHBoxLayout()
        
        year_label = QLabel("Year:")
        year_label.setFixedWidth(30)
        self.year_combo = QComboBox()
        self.year_combo.setFixedWidth(70)
        self.update_year_combo()
        
        month_label = QLabel("Month:")
        month_label.setFixedWidth(40)
        self.month_combo = QComboBox()
        self.month_combo.setFixedWidth(100)
        for i in range(1, 13):
            self.month_combo.addItem(calendar.month_name[i], i)
        
        # Default to current month/year
        current_date = datetime.now()
        current_month_idx = self.month_combo.findData(current_date.month)
        if current_month_idx >= 0:
            self.month_combo.setCurrentIndex(current_month_idx)
        
        top_layout.addWidget(year_label)
        top_layout.addWidget(self.year_combo)
        top_layout.addWidget(month_label)
        top_layout.addWidget(self.month_combo)
        top_layout.addStretch()
        
        main_layout.addLayout(top_layout)
        
        # Summary values - three cards in one row
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(10)
        
        # Income card
        income_frame = QFrame()
        income_frame.setObjectName("card")
        income_frame.setStyleSheet("""
            #card {
                background-color: #e8f5e9;
                border-radius: 8px;
                padding: 5px;
                border: 1px solid rgba(0, 0, 0, 0.05);
            }
        """)
        income_layout = QVBoxLayout(income_frame)
        income_layout.setContentsMargins(5, 5, 5, 5)
        income_layout.setSpacing(2)
        
        income_label = QLabel("Total Income")
        income_label.setStyleSheet("font-size: 13px; font-weight: 500; color: #2e7d32;")
        income_label.setAlignment(Qt.AlignCenter)
        self.income_value = QLabel("0.00 ₺")
        self.income_value.setObjectName("valueLabel")
        self.income_value.setStyleSheet("font-size: 16px; font-weight: bold; color: #2e7d32;")
        self.income_value.setAlignment(Qt.AlignCenter)
        
        income_layout.addWidget(income_label)
        income_layout.addWidget(self.income_value)
        
        # Expenses card
        expenses_frame = QFrame()
        expenses_frame.setObjectName("card")
        expenses_frame.setStyleSheet("""
            #card {
                background-color: #ffebee;
                border-radius: 8px;
                padding: 5px;
                border: 1px solid rgba(0, 0, 0, 0.05);
            }
        """)
        expenses_layout = QVBoxLayout(expenses_frame)
        expenses_layout.setContentsMargins(5, 5, 5, 5)
        expenses_layout.setSpacing(2)
        
        expenses_label = QLabel("Total Expenses")
        expenses_label.setStyleSheet("font-size: 13px; font-weight: 500; color: #c62828;")
        expenses_label.setAlignment(Qt.AlignCenter)
        self.expenses_value = QLabel("0.00 ₺")
        self.expenses_value.setObjectName("valueLabel")
        self.expenses_value.setStyleSheet("font-size: 16px; font-weight: bold; color: #c62828;")
        self.expenses_value.setAlignment(Qt.AlignCenter)
        
        expenses_layout.addWidget(expenses_label)
        expenses_layout.addWidget(self.expenses_value)
        
        # Net Worth card
        net_frame = QFrame()
        net_frame.setObjectName("card")
        net_frame.setStyleSheet("""
            #card {
                background-color: #e3f2fd;
                border-radius: 8px;
                padding: 5px;
                border: 1px solid rgba(0, 0, 0, 0.05);
            }
        """)
        net_layout = QVBoxLayout(net_frame)
        net_layout.setContentsMargins(5, 5, 5, 5)
        net_layout.setSpacing(2)
        
        net_label = QLabel("Net Worth")
        net_label.setStyleSheet("font-size: 13px; font-weight: 500; color: #1565c0;")
        net_label.setAlignment(Qt.AlignCenter)
        self.net_value = QLabel("0.00 ₺")
        self.net_value.setObjectName("valueLabel")
        self.net_value.setStyleSheet("font-size: 16px; font-weight: bold; color: #1565c0;")
        self.net_value.setAlignment(Qt.AlignCenter)
        
        net_layout.addWidget(net_label)
        net_layout.addWidget(self.net_value)
        
        # Add all cards to layout
        cards_layout.addWidget(income_frame)
        cards_layout.addWidget(expenses_frame)
        cards_layout.addWidget(net_frame)
        
        main_layout.addLayout(cards_layout)
        
        # Create tab widget for charts
        charts_tab = QTabWidget()
        charts_tab.setDocumentMode(True)
        
        # Tab 1: Main Charts (Monthly and Cumulative)
        main_charts_widget = QWidget()
        main_charts_layout = QGridLayout(main_charts_widget)
        main_charts_layout.setContentsMargins(5, 5, 5, 5)
        main_charts_layout.setSpacing(10)
        
        # Monthly chart
        self.monthly_canvas = MplCanvas(width=5, height=3)
        main_charts_layout.addWidget(self.monthly_canvas, 0, 0)
        
        # Cumulative chart
        self.cumulative_canvas = MplCanvas(width=5, height=3)
        main_charts_layout.addWidget(self.cumulative_canvas, 0, 1)
        
        charts_tab.addTab(main_charts_widget, "Overview")
        
        # Tab 2: Additional Charts
        additional_charts_widget = QWidget()
        additional_charts_layout = QGridLayout(additional_charts_widget)
        additional_charts_layout.setContentsMargins(5, 5, 5, 5)
        additional_charts_layout.setSpacing(10)
        
        # Trend Chart
        self.trend_canvas = MplCanvas(width=5, height=3)
        additional_charts_layout.addWidget(self.trend_canvas, 0, 0)
        
        # Category Chart
        self.category_canvas = MplCanvas(width=5, height=3)
        additional_charts_layout.addWidget(self.category_canvas, 0, 1)
        
        charts_tab.addTab(additional_charts_widget, "Insights")

        # Tab 3: Monthly Comparison - NEW FEATURE
        comparison_widget = QWidget()
        comparison_layout = QGridLayout(comparison_widget)
        comparison_layout.setContentsMargins(5, 5, 5, 5)
        comparison_layout.setSpacing(10)
        
        # Monthly Comparison Chart
        self.comparison_canvas = MplCanvas(width=5, height=3)
        comparison_layout.addWidget(self.comparison_canvas, 0, 0)
        
        # Category Comparison Chart
        self.category_comparison_canvas = MplCanvas(width=5, height=3)
        comparison_layout.addWidget(self.category_comparison_canvas, 0, 1)
        
        charts_tab.addTab(comparison_widget, "Monthly Comparison")
        
        # Tab 4: Financial Forecast - NEW FEATURE
        forecast_widget = QWidget()
        forecast_layout = QGridLayout(forecast_widget)
        forecast_layout.setContentsMargins(5, 5, 5, 5)
        forecast_layout.setSpacing(10)
        
        # Forecast Chart
        self.forecast_canvas = MplCanvas(width=5, height=3)
        forecast_layout.addWidget(self.forecast_canvas, 0, 0)
        
        # Savings Forecast Chart
        self.savings_forecast_canvas = MplCanvas(width=5, height=3)
        forecast_layout.addWidget(self.savings_forecast_canvas, 0, 1)
        
        charts_tab.addTab(forecast_widget, "Financial Forecast")
        
        # Add charts tab to main layout with stretch
        main_layout.addWidget(charts_tab, 1)
        
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
        self.income_value.setText(f"{summary['total_income']:.2f} ₺")
        self.expenses_value.setText(f"{summary['total_expenses']:.2f} ₺")
        
        # Set color based on positive or negative net worth
        net_worth = summary['net_worth']
        if net_worth >= 0:
            self.net_value.setStyleSheet("font-size: 16px; font-weight: bold; color: #2e7d32;")
        else:
            self.net_value.setStyleSheet("font-size: 16px; font-weight: bold; color: #c62828;")
        self.net_value.setText(f"{net_worth:.2f} ₺")
        
        # Update all charts
        self.update_monthly_chart(year)
        self.update_cumulative_chart()
        self.update_trend_chart(year)
        self.update_category_chart(year, month)
        
        # Update new charts
        self.update_comparison_chart(year, month)
        self.update_category_comparison_chart(year, month)
        self.update_forecast_chart(year, month)
        self.update_savings_forecast_chart(year, month)
        
    def update_monthly_chart(self, year):
        """Update the monthly breakdown chart - IMPROVED VERSION"""
        monthly_data = self.controller.get_monthly_data_for_year(year)
        
        # Clear previous plot
        self.monthly_canvas.axes.clear()
        
        months = list(range(1, 13))
        income_values = [monthly_data[m]['total_income'] for m in months]
        expense_values = [monthly_data[m]['total_expenses'] for m in months]
        net_values = [monthly_data[m]['net_worth'] for m in months]
        
        # Set up X axis for months
        x = range(len(months))
        month_names = [calendar.month_abbr[m] for m in months]
        
        # Create stacked bar chart showing income and expenses
        # with net worth as a point on top
        
        # Income as positive values
        self.monthly_canvas.axes.bar(x, income_values, 
                                    color='#4CAF50', alpha=0.8, 
                                    label='Income',
                                    width=0.6,
                                    edgecolor='white', linewidth=0.5)
        
        # Expenses as negative values
        self.monthly_canvas.axes.bar(x, [-val for val in expense_values], 
                                    color='#F44336', alpha=0.8, 
                                    label='Expenses',
                                    width=0.6,
                                    edgecolor='white', linewidth=0.5)
        
        # Net worth as marker points
        self.monthly_canvas.axes.plot(x, net_values, 'o-', 
                                    color='#2196F3', linewidth=2, 
                                    markersize=6, label='Net Worth')
        
        # Add zero line
        self.monthly_canvas.axes.axhline(y=0, color='#888888', linestyle='-', alpha=0.3, linewidth=1)
        
        # Add labels
        self.monthly_canvas.axes.set_title(f'Financial Summary ({year})', 
                                          fontsize=11, fontweight='bold', pad=8)
        self.monthly_canvas.axes.set_xlabel('Month', fontsize=9, labelpad=5)
        self.monthly_canvas.axes.set_ylabel('Amount (₺)', fontsize=9, labelpad=5)
        
        # Set x-axis ticks and labels
        self.monthly_canvas.axes.set_xticks(x)
        self.monthly_canvas.axes.set_xticklabels(month_names)
        
        # Add a single-column legend at the top-right
        legend = self.monthly_canvas.axes.legend(loc='upper right', frameon=True, 
                                              fancybox=True, framealpha=0.9, 
                                              shadow=True, fontsize=8)
        legend.get_frame().set_edgecolor('#cccccc')
        
        # Add data labels for current month
        current_month = self.month_combo.currentData() - 1  # Adjust to 0-based index
        if current_month >= 0 and current_month < len(x):
            # Income label
            self.monthly_canvas.axes.annotate(
                f"{income_values[current_month]:,.0f} ₺",
                xy=(x[current_month], income_values[current_month]),
                xytext=(0, 5), textcoords="offset points",
                ha='center', va='bottom',
                fontsize=8, fontweight='bold', color='#2e7d32'
            )
            
            # Expense label
            self.monthly_canvas.axes.annotate(
                f"{expense_values[current_month]:,.0f} ₺",
                xy=(x[current_month], -expense_values[current_month]),
                xytext=(0, -12), textcoords="offset points",
                ha='center', va='top',
                fontsize=8, fontweight='bold', color='#c62828'
            )
            
            # Net worth label
            self.monthly_canvas.axes.annotate(
                f"{net_values[current_month]:,.0f} ₺",
                xy=(x[current_month], net_values[current_month]),
                xytext=(0, 10), textcoords="offset points",
                ha='center', va='bottom',
                fontsize=8, fontweight='bold', color='#1565c0'
            )
            
            # Highlight current month
            self.monthly_canvas.axes.axvline(x=x[current_month], color='#888888', 
                                         linestyle='--', alpha=0.3, linewidth=1)
        
        self.monthly_canvas.fig.tight_layout()
        self.monthly_canvas.draw()
        
    def update_cumulative_chart(self):
        """Update the cumulative overview chart - IMPROVED VERSION"""
        cumulative_data = self.controller.get_cumulative_data()
        
        if not cumulative_data:
            # No data to display
            self.cumulative_canvas.axes.clear()
            self.cumulative_canvas.axes.text(0.5, 0.5, 'No transaction data available',
                                           horizontalalignment='center',
                                           verticalalignment='center',
                                           fontsize=9,
                                           transform=self.cumulative_canvas.axes.transAxes)
            self.cumulative_canvas.draw()
            return
        
        # Extract data for plotting
        dates = [d['date'] for d in cumulative_data]
        income = [d['cumulative_income'] for d in cumulative_data]
        expenses = [d['cumulative_expenses'] for d in cumulative_data]
        net = [d['cumulative_net'] for d in cumulative_data]
        
        # Determine if we have enough data points for a sophisticated chart
        if len(dates) < 2:
            # Not enough data points, use simpler presentation
            self.cumulative_canvas.axes.clear()
            
            # Create a horizontal stacked bar chart
            labels = ['Current Status']
            width = 0.5
            
            # Calculate the current values
            current_income = income[-1] if income else 0
            current_expenses = expenses[-1] if expenses else 0
            current_net = net[-1] if net else 0
            
            # Create stacked bars
            self.cumulative_canvas.axes.barh(labels, [current_income], 
                                           color='#4CAF50', alpha=0.8, 
                                           height=width, edgecolor='white',
                                           label='Income')
            
            self.cumulative_canvas.axes.barh(labels, [-current_expenses], left=[current_income],
                                           color='#F44336', alpha=0.8, 
                                           height=width, edgecolor='white',
                                           label='Expenses')
            
            # Add labels for each value
            self.cumulative_canvas.axes.text(current_income/2, 0, f"{current_income:,.0f} ₺", 
                                           ha='center', va='center', color='white', 
                                           fontweight='bold', fontsize=9)
            
            self.cumulative_canvas.axes.text(current_income - current_expenses/2, 0, 
                                           f"{current_expenses:,.0f} ₺", 
                                           ha='center', va='center', color='white', 
                                           fontweight='bold', fontsize=9)
            
            # Add net worth indicator
            self.cumulative_canvas.axes.annotate(
                f"Net Worth: {current_net:,.0f} ₺",
                xy=(current_income - current_expenses, 0),
                xytext=(0, 20), textcoords="offset points",
                ha='center', va='bottom',
                fontsize=10, fontweight='bold', 
                color='#1565c0',
                bbox=dict(boxstyle="round,pad=0.3", fc="#e3f2fd", ec="#1565c0", alpha=0.8)
            )
            
            self.cumulative_canvas.axes.set_title('Current Financial Status', 
                                                fontsize=11, fontweight='bold', pad=8)
        else:
            # Clear previous plot
            self.cumulative_canvas.axes.clear()
            
            # Create area chart for income and expenses
            self.cumulative_canvas.axes.fill_between(dates, income, 
                                                 color='#4CAF50', alpha=0.3, 
                                                 label='Income')
            
            self.cumulative_canvas.axes.fill_between(dates, expenses, 
                                                 color='#F44336', alpha=0.3, 
                                                 label='Expenses')
            
            # Add line for net worth
            self.cumulative_canvas.axes.plot(dates, net, '-', 
                                         color='#1565c0', linewidth=2.5, 
                                         marker='o', markersize=5,
                                         label='Net Worth')
            
            # Add labels for final values
            final_date = dates[-1]
            final_income = income[-1]
            final_expenses = expenses[-1]
            final_net = net[-1]
            
            # Income label
            self.cumulative_canvas.axes.annotate(
                f"{final_income:,.0f} ₺",
                xy=(final_date, final_income),
                xytext=(5, 0), textcoords="offset points",
                ha='left', va='center',
                fontsize=8, fontweight='bold', color='#2e7d32'
            )
            
            # Expense label
            self.cumulative_canvas.axes.annotate(
                f"{final_expenses:,.0f} ₺",
                xy=(final_date, final_expenses),
                xytext=(5, 0), textcoords="offset points",
                ha='left', va='center',
                fontsize=8, fontweight='bold', color='#c62828'
            )
            
            # Net worth label
            self.cumulative_canvas.axes.annotate(
                f"{final_net:,.0f} ₺",
                xy=(final_date, final_net),
                xytext=(5, 0), textcoords="offset points",
                ha='left', va='center',
                fontsize=8, fontweight='bold', color='#1565c0'
            )
            
            self.cumulative_canvas.axes.set_title('Financial Growth Over Time', 
                                              fontsize=11, fontweight='bold', pad=8)
            self.cumulative_canvas.axes.set_xlabel('Date', fontsize=9, labelpad=5)
            self.cumulative_canvas.axes.set_ylabel('Amount (₺)', fontsize=9, labelpad=5)
            
            # Format the dates on x-axis
            self.cumulative_canvas.axes.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
            self.cumulative_canvas.axes.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
            
            # Rotate date labels for better readability
            plt.setp(self.cumulative_canvas.axes.get_xticklabels(), rotation=45, ha='right')
        
        # Add legend
        legend = self.cumulative_canvas.axes.legend(loc='upper left', frameon=True, 
                                                 fancybox=True, framealpha=0.9, 
                                                 shadow=True, fontsize=8)
        legend.get_frame().set_edgecolor('#cccccc')
        
        self.cumulative_canvas.fig.tight_layout()
        self.cumulative_canvas.draw()
        
    def update_trend_chart(self, year):
        """Update the income vs expense trend chart - IMPROVED VERSION"""
        monthly_data = self.controller.get_monthly_data_for_year(year)
        
        # Clear previous plot
        self.trend_canvas.axes.clear()
        
        months = list(range(1, 13))
        income_values = [monthly_data[m]['total_income'] for m in months]
        expense_values = [monthly_data[m]['total_expenses'] for m in months]
        net_values = [monthly_data[m]['net_worth'] for m in months]
        
        # Set up month positions
        x = np.arange(len(months))
        
        # Calculate ranges for shading
        max_value = max(max(income_values), max(expense_values)) * 1.1
        
        # Create area chart for positive and negative cash flow
        for i in range(len(months)):
            # Skip months with no data
            if income_values[i] == 0 and expense_values[i] == 0:
                continue
                
            # Green for positive cash flow
            if net_values[i] > 0:
                self.trend_canvas.axes.fill_between([x[i]-0.4, x[i]+0.4], [0, 0], [net_values[i], net_values[i]], 
                                                 color='#4CAF50', alpha=0.2)
            # Red for negative cash flow
            elif net_values[i] < 0:
                self.trend_canvas.axes.fill_between([x[i]-0.4, x[i]+0.4], [0, 0], [net_values[i], net_values[i]], 
                                                 color='#F44336', alpha=0.2)
        
        # Draw lines for income and expenses
        self.trend_canvas.axes.plot(x, income_values, '-o', color='#4CAF50', 
                                  linewidth=2, markersize=6, label='Income')
        self.trend_canvas.axes.plot(x, expense_values, '-o', color='#F44336', 
                                  linewidth=2, markersize=6, label='Expenses')
        
        # Highlight the balance point with a horizontal line
        self.trend_canvas.axes.axhline(y=0, color='#444444', linestyle='-', alpha=0.3)
        
        # Add savings/deficit markers at each point
        for i, (inc, exp, net) in enumerate(zip(income_values, expense_values, net_values)):
            # Skip months with no data
            if inc == 0 and exp == 0:
                continue
                
            # Add net value text
            if net > 0:
                color = '#4CAF50'  # Green for positive
                y_offset = 10
                va = 'bottom'
                prefix = '+'
            else:
                color = '#F44336'  # Red for negative
                y_offset = -10
                va = 'top'
                prefix = ''
            
            # Add text label for the net value
            self.trend_canvas.axes.annotate(
                f"{prefix}{net:,.0f} ₺",
                xy=(x[i], (inc + exp) / 2),
                xytext=(0, y_offset), textcoords="offset points",
                ha='center', va=va,
                fontsize=8, fontweight='bold', color=color
            )
        
        # Add labels and formatting
        self.trend_canvas.axes.set_title(f'Monthly Cash Flow ({year})', 
                                      fontsize=11, fontweight='bold', pad=8)
        self.trend_canvas.axes.set_xlabel('Month', fontsize=9, labelpad=5)
        self.trend_canvas.axes.set_ylabel('Amount (₺)', fontsize=9, labelpad=5)
        
        # Set x-axis ticks and labels
        self.trend_canvas.axes.set_xticks(x)
        self.trend_canvas.axes.set_xticklabels([calendar.month_abbr[m] for m in months])
        
        # Add a legend
        legend = self.trend_canvas.axes.legend(loc='upper right', fontsize=8)
        
        # Get the current month
        current_month = self.month_combo.currentData() - 1  # Adjust to 0-based index
        if current_month >= 0 and current_month < len(x):
            # Highlight current month
            self.trend_canvas.axes.axvline(x=x[current_month], color='#888888', 
                                        linestyle='--', alpha=0.5, linewidth=1)
        
        self.trend_canvas.fig.tight_layout()
        self.trend_canvas.draw()
        
    def update_category_chart(self, year, month):
        """Update the expense category breakdown pie chart using transaction categories"""
        # Get transactions for the selected month
        transactions = self.controller.finance_manager.get_transactions_by_month(year, month)
        
        # Clear previous plot
        self.category_canvas.axes.clear()
        
        if not transactions:
            self.category_canvas.axes.text(0.5, 0.5, 'No transactions for this month',
                                          horizontalalignment='center',
                                          verticalalignment='center',
                                          fontsize=9,
                                          transform=self.category_canvas.axes.transAxes)
            self.category_canvas.draw()
            return
        
        # Filter for expenses only
        expense_transactions = [t for t in transactions if t.transaction_type.value == 'expense']
        
        if not expense_transactions:
            self.category_canvas.axes.text(0.5, 0.5, 'No expense transactions for this month',
                                          horizontalalignment='center',
                                          verticalalignment='center',
                                          fontsize=9,
                                          transform=self.category_canvas.axes.transAxes)
            self.category_canvas.draw()
            return
        
        # Group transactions by category
        categories = defaultdict(float)
        
        for transaction in expense_transactions:
            # Use transaction category if available, otherwise use name as fallback
            category = transaction.category if transaction.category else transaction.name
            categories[category] += transaction.amount
        
        # Sort by amount and get top categories
        sorted_categories = dict(sorted(categories.items(), key=lambda x: x[1], reverse=True))
        
        # Limit to top 6 categories and group the rest as "Other"
        if len(sorted_categories) > 6:
            top_categories = dict(list(sorted_categories.items())[:5])
            other_amount = sum(list(sorted_categories.values())[5:])
            top_categories["Other"] = other_amount
            sorted_categories = top_categories
        
        # Prepare data for donut chart
        labels = list(sorted_categories.keys())
        sizes = list(sorted_categories.values())
        
        # Calculate percentages
        total = sum(sizes)
        percentages = [(size/total)*100 for size in sizes]
        
        # Set an aspect ratio for the pie chart
        self.category_canvas.axes.set_aspect('equal')
        
        # Create donut chart with custom colors
        colors = ['#42A5F5', '#66BB6A', '#FFA726', '#EF5350', '#AB47BC', '#7E57C2', '#78909C']
        
        # Create wedges with auto-pct text
        wedges, texts, autotexts = self.category_canvas.axes.pie(
            sizes, 
            labels=None,  # We'll add custom labels
            colors=colors[:len(labels)],
            autopct='%1.1f%%',
            pctdistance=0.85,
            wedgeprops={'width': 0.4, 'edgecolor': 'w', 'linewidth': 2},
            textprops={'fontsize': 9, 'color': '#333333'},
            startangle=90
        )
        
        # Style percentage texts
        for autotext in autotexts:
            autotext.set_fontsize(8)
            autotext.set_fontweight('bold')
        
        # Create center circle for donut chart
        circle = plt.Circle((0, 0), 0.4, fc='white')
        self.category_canvas.axes.add_artist(circle)
        
        # Display total amount in center
        self.category_canvas.axes.text(0, 0, f"{total:,.0f} ₺",
                                     ha='center', va='center',
                                     fontsize=11, fontweight='bold')
        
        self.category_canvas.axes.text(0, -0.15, "Total Expenses",
                                     ha='center', va='center',
                                     fontsize=8, color='#555555')
        
        # Create legend with categories and values
        legend_labels = [f"{label} ({value:,.0f} ₺)" for label, value in zip(labels, sizes)]
        self.category_canvas.axes.legend(wedges, legend_labels,
                                       loc="center left",
                                       bbox_to_anchor=(1, 0.5),
                                       fontsize=8)
        
        # Add title
        self.category_canvas.axes.set_title(f'Expense Breakdown by Category - {calendar.month_name[month]} {year}', 
                                          fontsize=11, fontweight='bold', pad=8)
        
        self.category_canvas.fig.tight_layout()
        self.category_canvas.draw()
        
    def update_comparison_chart(self, year, month):
        """NEW FEATURE: Monthly Comparison Chart that compares expenses with previous and next month"""
        # Clear previous plot
        self.comparison_canvas.axes.clear()
        
        # Get previous, current and next month
        current_date = datetime(year, month, 1)
        prev_date = current_date - relativedelta(months=1)
        next_date = current_date + relativedelta(months=1)
        
        # Get data for all three months
        current_summary = self.controller.get_monthly_summary(current_date.year, current_date.month)
        prev_summary = self.controller.get_monthly_summary(prev_date.year, prev_date.month)
        next_summary = self.controller.get_monthly_summary(next_date.year, next_date.month)
        
        # Prepare data for plotting
        months = [prev_date.strftime('%b %Y'), current_date.strftime('%b %Y'), next_date.strftime('%b %Y')]
        income_values = [prev_summary['total_income'], current_summary['total_income'], next_summary['total_income']]
        expense_values = [prev_summary['total_expenses'], current_summary['total_expenses'], next_summary['total_expenses']]
        net_values = [prev_summary['net_worth'], current_summary['net_worth'], next_summary['net_worth']]
        
        # Set up month positions
        x = np.arange(len(months))
        width = 0.35  # width of the bars
        
        # Create grouped bar chart
        self.comparison_canvas.axes.bar(x - width/2, income_values, width, color='#4CAF50', alpha=0.8, label='Income')
        self.comparison_canvas.axes.bar(x + width/2, expense_values, width, color='#F44336', alpha=0.8, label='Expenses')
        
        # Add net worth as line
        self.comparison_canvas.axes.plot(x, net_values, 'o-', color='#2196F3', linewidth=2, markersize=8, label='Net Worth')
        
        # Add zero line
        self.comparison_canvas.axes.axhline(y=0, color='#888888', linestyle='-', alpha=0.3, linewidth=1)
        
        # Add data labels
        for i, (inc, exp, net) in enumerate(zip(income_values, expense_values, net_values)):
            # Income label
            self.comparison_canvas.axes.annotate(
                f"{inc:,.0f} ₺",
                xy=(x[i] - width/2, inc),
                xytext=(0, 5), textcoords="offset points",
                ha='center', va='bottom',
                fontsize=8, fontweight='bold', color='#2e7d32'
            )
            
            # Expense label
            self.comparison_canvas.axes.annotate(
                f"{exp:,.0f} ₺",
                xy=(x[i] + width/2, exp),
                xytext=(0, 5), textcoords="offset points",
                ha='center', va='bottom',
                fontsize=8, fontweight='bold', color='#c62828'
            )
            
            # Net worth label with arrow indicator
            arrow_char = ''
            if i == 1:  # Current month
                # Compare with previous month
                if net > net_values[0]:
                    arrow_char = '↑ '  # Up arrow
                    net_color = '#4CAF50'  # Green
                elif net < net_values[0]:
                    arrow_char = '↓ '  # Down arrow
                    net_color = '#F44336'  # Red
                else:
                    arrow_char = '→ '  # Right arrow
                    net_color = '#2196F3'  # Blue
                
                # Add percent change
                if net_values[0] != 0:
                    pct_change = ((net - net_values[0]) / abs(net_values[0])) * 100
                    arrow_char += f"{pct_change:+.1f}% "
            else:
                net_color = '#2196F3'  # Blue
            
            self.comparison_canvas.axes.annotate(
                f"{arrow_char}{net:,.0f} ₺",
                xy=(x[i], net),
                xytext=(0, 10), textcoords="offset points",
                ha='center', va='bottom',
                fontsize=8, fontweight='bold', color=net_color
            )
        
        # Highlight current month with vertical line and background
        self.comparison_canvas.axes.axvspan(x[1]-0.4, x[1]+0.4, alpha=0.15, color='#2196F3')
        
        # Set x-axis ticks and labels
        self.comparison_canvas.axes.set_xticks(x)
        self.comparison_canvas.axes.set_xticklabels(months)
        
        # Add a legend
        legend = self.comparison_canvas.axes.legend(loc='upper right', fontsize=8)
        
        # Add title and labels
        self.comparison_canvas.axes.set_title('Monthly Financial Comparison', 
                                          fontsize=11, fontweight='bold', pad=8)
        self.comparison_canvas.axes.set_xlabel('Month', fontsize=9, labelpad=5)
        self.comparison_canvas.axes.set_ylabel('Amount (₺)', fontsize=9, labelpad=5)
        
        self.comparison_canvas.fig.tight_layout()
        self.comparison_canvas.draw()
        
    def update_category_comparison_chart(self, year, month):
        """NEW FEATURE: Compare expense categories between current, previous, and next month"""
        # Clear previous plot
        self.category_comparison_canvas.axes.clear()
        
        # Get previous, current, and next month dates
        current_date = datetime(year, month, 1)
        prev_date = current_date - relativedelta(months=1)
        next_date = current_date + relativedelta(months=1)
        
        # Get transactions for all three months
        current_transactions = self.controller.finance_manager.get_transactions_by_month(
            current_date.year, current_date.month)
        prev_transactions = self.controller.finance_manager.get_transactions_by_month(
            prev_date.year, prev_date.month)
        next_transactions = self.controller.finance_manager.get_transactions_by_month(
            next_date.year, next_date.month)
        
        # Filter for expense transactions only
        current_expenses = [t for t in current_transactions if t.transaction_type.value == 'expense']
        prev_expenses = [t for t in prev_transactions if t.transaction_type.value == 'expense']
        next_expenses = [t for t in next_transactions if t.transaction_type.value == 'expense']
        
        if not current_expenses and not prev_expenses and not next_expenses:
            self.category_comparison_canvas.axes.text(0.5, 0.5, 'No expense transactions to compare',
                                                    horizontalalignment='center',
                                                    verticalalignment='center',
                                                    fontsize=9,
                                                    transform=self.category_comparison_canvas.axes.transAxes)
            self.category_comparison_canvas.draw()
            return
        
        # Group transactions by category for each month
        def group_by_category(transactions):
            categories = defaultdict(float)
            for t in transactions:
                category = t.category if t.category else t.name
                categories[category] += t.amount
            return categories
        
        prev_categories = group_by_category(prev_expenses)
        current_categories = group_by_category(current_expenses)
        next_categories = group_by_category(next_expenses)
        
        # Get all unique categories across all three months
        all_categories = set(list(prev_categories.keys()) + 
                             list(current_categories.keys()) + 
                             list(next_categories.keys()))
        
        # Sort categories by current month amount (or previous if current doesn't exist)
        def get_category_value(category):
            if category in current_categories:
                return current_categories[category]
            elif category in prev_categories:
                return prev_categories[category]
            else:
                return next_categories.get(category, 0)
        
        sorted_categories = sorted(all_categories, key=get_category_value, reverse=True)
        
        # Limit to top 5 categories
        if len(sorted_categories) > 5:
            top_categories = sorted_categories[:5]
            
            # Add an "Other" category for the rest
            other_prev = sum(prev_categories.get(cat, 0) for cat in sorted_categories[5:])
            other_current = sum(current_categories.get(cat, 0) for cat in sorted_categories[5:])
            other_next = sum(next_categories.get(cat, 0) for cat in sorted_categories[5:])
            
            prev_categories["Other"] = other_prev
            current_categories["Other"] = other_current
            next_categories["Other"] = other_next
            
            sorted_categories = top_categories + ["Other"]
        
        # Prepare data for grouped bar chart
        x = np.arange(len(sorted_categories))
        width = 0.25  # width of bars
        
        # Extract values maintaining the sort order
        prev_values = [prev_categories.get(cat, 0) for cat in sorted_categories]
        current_values = [current_categories.get(cat, 0) for cat in sorted_categories]
        next_values = [next_categories.get(cat, 0) for cat in sorted_categories]
        
        # Create grouped bar chart
        self.category_comparison_canvas.axes.bar(x - width, prev_values, width, 
                                               color='#78909C', alpha=0.8, 
                                               label=prev_date.strftime('%b %Y'))
        self.category_comparison_canvas.axes.bar(x, current_values, width, 
                                               color='#F44336', alpha=0.8, 
                                               label=current_date.strftime('%b %Y'))
        self.category_comparison_canvas.axes.bar(x + width, next_values, width, 
                                               color='#FFA726', alpha=0.8, 
                                               label=next_date.strftime('%b %Y'))
        
        # Add data labels for current month
        for i, value in enumerate(current_values):
            if value > 0:
                self.category_comparison_canvas.axes.text(
                    x[i], value, f"{value:,.0f}", 
                    ha='center', va='bottom', fontsize=7, fontweight='bold',
                    rotation=45 if value > max(current_values) * 0.8 else 0
                )
        
        # Add title and labels
        self.category_comparison_canvas.axes.set_title('Expense Categories Comparison', 
                                                     fontsize=11, fontweight='bold', pad=8)
        self.category_comparison_canvas.axes.set_xlabel('Category', fontsize=9, labelpad=5)
        self.category_comparison_canvas.axes.set_ylabel('Amount (₺)', fontsize=9, labelpad=5)
        
        # Set x-axis ticks and labels
        self.category_comparison_canvas.axes.set_xticks(x)
        
        # Rotate labels for better readability
        self.category_comparison_canvas.axes.set_xticklabels(sorted_categories, rotation=25, ha='right')
        
        # Add legend
        self.category_comparison_canvas.axes.legend(loc='upper right', fontsize=8)
        
        self.category_comparison_canvas.fig.tight_layout()
        self.category_comparison_canvas.draw()
        
    def update_forecast_chart(self, year, month):
        """NEW FEATURE: Financial forecast chart for next 6 months based on past trends"""
        # Clear previous plot
        self.forecast_canvas.axes.clear()
        
        # Get historical data for the last 6 months (including current)
        current_date = datetime(year, month, 1)
        historical_data = []
        
        for i in range(5, -1, -1):  # Get 6 months of historical data (including current)
            hist_date = current_date - relativedelta(months=i)
            summary = self.controller.get_monthly_summary(hist_date.year, hist_date.month)
            historical_data.append({
                'date': hist_date,
                'income': summary['total_income'],
                'expenses': summary['total_expenses'],
                'net_worth': summary['net_worth']
            })
        
        # Project next 6 months
        forecast_data = []
        
        # Simple forecasting using average of last 3 months for trend
        if len(historical_data) >= 3:
            # Calculate average monthly change for income and expenses
            avg_income_change = 0
            avg_expense_change = 0
            
            for i in range(len(historical_data) - 1, 0, -1):
                income_change = historical_data[i]['income'] - historical_data[i-1]['income']
                expense_change = historical_data[i]['expenses'] - historical_data[i-1]['expenses']
                
                # Weight recent months more heavily
                weight = 1.0
                if i >= len(historical_data) - 3:  # Last 3 months
                    weight = 2.0
                
                avg_income_change += income_change * weight
                avg_expense_change += expense_change * weight
            
            # Normalize by sum of weights (1.0 for older months, 2.0 for last 3)
            weights_sum = len(historical_data) - 1 + min(3, len(historical_data) - 1)
            if weights_sum > 0:
                avg_income_change /= weights_sum
                avg_expense_change /= weights_sum
            
            # Generate forecasts for next 6 months
            last_income = historical_data[-1]['income']
            last_expense = historical_data[-1]['expenses']
            
            for i in range(1, 7):  # Next 6 months
                forecast_date = current_date + relativedelta(months=i)
                forecast_income = max(0, last_income + (avg_income_change * i))
                forecast_expense = max(0, last_expense + (avg_expense_change * i))
                forecast_net = forecast_income - forecast_expense
                
                forecast_data.append({
                    'date': forecast_date,
                    'income': forecast_income,
                    'expenses': forecast_expense,
                    'net_worth': forecast_net
                })
        
        # Combine historical and forecast data
        all_data = historical_data + forecast_data
        
        # Prepare data for plotting
        dates = [d['date'] for d in all_data]
        incomes = [d['income'] for d in all_data]
        expenses = [d['expenses'] for d in all_data]
        net_worths = [d['net_worth'] for d in all_data]
        
        # Create plot
        # Historical data - solid lines
        hist_dates = dates[:len(historical_data)]
        hist_incomes = incomes[:len(historical_data)]
        hist_expenses = expenses[:len(historical_data)]
        hist_nets = net_worths[:len(historical_data)]
        
        self.forecast_canvas.axes.plot(hist_dates, hist_incomes, 'o-', color='#4CAF50', 
                                     linewidth=2, markersize=5, label='Income (Actual)')
        self.forecast_canvas.axes.plot(hist_dates, hist_expenses, 'o-', color='#F44336', 
                                     linewidth=2, markersize=5, label='Expenses (Actual)')
        self.forecast_canvas.axes.plot(hist_dates, hist_nets, 'o-', color='#2196F3', 
                                     linewidth=2, markersize=5, label='Net Worth (Actual)')
        
        # Forecast data - dashed lines
        if forecast_data:
            forecast_dates = dates[len(historical_data):]
            forecast_incomes = incomes[len(historical_data):]
            forecast_expenses = expenses[len(historical_data):]
            forecast_nets = net_worths[len(historical_data):]
            
            # Add vertical line separating actual from forecast
            self.forecast_canvas.axes.axvline(x=current_date, color='#888888', 
                                           linestyle='--', alpha=0.5)
            
            # Add "Forecast starts" text
            self.forecast_canvas.axes.text(current_date, max(max(incomes), max(expenses)) * 0.9,
                                        ' Forecast →', 
                                        ha='left', va='top',
                                        fontsize=8, fontweight='bold',
                                        bbox=dict(facecolor='white', alpha=0.8, boxstyle='round,pad=0.3'))
            
            # Plot forecast data with dashed lines
            self.forecast_canvas.axes.plot(forecast_dates, forecast_incomes, '--', color='#4CAF50', 
                                        linewidth=2, label='Income (Forecast)')
            self.forecast_canvas.axes.plot(forecast_dates, forecast_expenses, '--', color='#F44336', 
                                        linewidth=2, label='Expenses (Forecast)')
            self.forecast_canvas.axes.plot(forecast_dates, forecast_nets, '--', color='#2196F3', 
                                        linewidth=2, label='Net Worth (Forecast)')
            
            # Add labels for the final forecast point
            self.forecast_canvas.axes.annotate(
                f"{forecast_incomes[-1]:,.0f} ₺",
                xy=(forecast_dates[-1], forecast_incomes[-1]),
                xytext=(5, 0), textcoords="offset points",
                ha='left', va='center',
                fontsize=8, fontweight='bold', color='#4CAF50'
            )
            
            self.forecast_canvas.axes.annotate(
                f"{forecast_expenses[-1]:,.0f} ₺",
                xy=(forecast_dates[-1], forecast_expenses[-1]),
                xytext=(5, 0), textcoords="offset points",
                ha='left', va='center',
                fontsize=8, fontweight='bold', color='#F44336'
            )
            
            self.forecast_canvas.axes.annotate(
                f"{forecast_nets[-1]:,.0f} ₺",
                xy=(forecast_dates[-1], forecast_nets[-1]),
                xytext=(5, 0), textcoords="offset points",
                ha='left', va='center',
                fontsize=8, fontweight='bold', color='#2196F3'
            )
        
        # Add title and labels
        self.forecast_canvas.axes.set_title('6-Month Financial Forecast', 
                                         fontsize=11, fontweight='bold', pad=8)
        self.forecast_canvas.axes.set_xlabel('Month', fontsize=9, labelpad=5)
        self.forecast_canvas.axes.set_ylabel('Amount (₺)', fontsize=9, labelpad=5)
        
        # Format x-axis dates
        self.forecast_canvas.axes.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        if len(dates) > 8:
            self.forecast_canvas.axes.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
        else:
            self.forecast_canvas.axes.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        
        # Rotate date labels for better readability
        plt.setp(self.forecast_canvas.axes.get_xticklabels(), rotation=45, ha='right')
        
        # Add legend
        self.forecast_canvas.axes.legend(loc='upper left', fontsize=8)
        
        # Add horizontal line at zero
        self.forecast_canvas.axes.axhline(y=0, color='#888888', linestyle='-', alpha=0.3)
        
        self.forecast_canvas.fig.tight_layout()
        self.forecast_canvas.draw()
        
    def update_savings_forecast_chart(self, year, month):
        """NEW FEATURE: Savings and financial goals simulation chart"""
        # Clear previous plot
        self.savings_forecast_canvas.axes.clear()
        
        # Current date based on selection
        current_date = datetime(year, month, 1)
        
        # Get current monthly summary
        current_summary = self.controller.get_monthly_summary(year, month)
        current_income = current_summary['total_income']
        current_expenses = current_summary['total_expenses']
        current_savings = current_income - current_expenses
        
        # Get active financial goals
        goals = self.controller.get_goals_by_month(year, month)
        
        # If we have no data, show a message
        if current_income == 0 and current_expenses == 0 and not goals:
            self.savings_forecast_canvas.axes.text(0.5, 0.5, 'No financial data or goals available',
                                                 horizontalalignment='center',
                                                 verticalalignment='center',
                                                 fontsize=9,
                                                 transform=self.savings_forecast_canvas.axes.transAxes)
            self.savings_forecast_canvas.draw()
            return
        
        # Create savings projection scenarios
        # Best case: Income increases by 5%, expenses decrease by 3%
        # Normal case: Income and expenses stay constant
        # Worst case: Income decreases by 3%, expenses increase by 5%
        
        months = 12  # Project for next 12 months
        dates = [current_date + relativedelta(months=i) for i in range(months)]
        
        # Initialize savings scenarios
        best_case = [0] * months
        normal_case = [0] * months
        worst_case = [0] * months
        
        # Calculate cumulative savings for each scenario
        for i in range(months):
            # Best case
            if i == 0:
                best_case[i] = current_savings
            else:
                income_growth = current_income * (1 + 0.05) ** i
                expense_reduction = current_expenses * (1 - 0.03) ** i
                best_case[i] = best_case[i-1] + (income_growth - expense_reduction)
            
            # Normal case
            if i == 0:
                normal_case[i] = current_savings
            else:
                normal_case[i] = normal_case[i-1] + current_savings
            
            # Worst case
            if i == 0:
                worst_case[i] = current_savings
            else:
                income_decline = current_income * (1 - 0.03) ** i
                expense_growth = current_expenses * (1 + 0.05) ** i
                worst_case[i] = worst_case[i-1] + (income_decline - expense_growth)
        
        # Create cumulative savings projection chart
        self.savings_forecast_canvas.axes.plot(dates, best_case, '-', color='#4CAF50', 
                                          linewidth=2, label='Best Case')
        self.savings_forecast_canvas.axes.plot(dates, normal_case, '-', color='#2196F3', 
                                          linewidth=2, label='Expected Case')
        self.savings_forecast_canvas.axes.plot(dates, worst_case, '-', color='#F44336', 
                                          linewidth=2, label='Worst Case')
        
        # Fill between the scenarios to show range
        self.savings_forecast_canvas.axes.fill_between(dates, best_case, normal_case, 
                                                  color='#4CAF50', alpha=0.2)
        self.savings_forecast_canvas.axes.fill_between(dates, normal_case, worst_case, 
                                                  color='#F44336', alpha=0.2)
        
        # Add goal lines if goals exist
        for goal in goals:
            if goal.goal_type.value == 'savings':
                # Draw horizontal line for savings goal
                self.savings_forecast_canvas.axes.axhline(y=goal.amount, color='#9C27B0', 
                                                     linestyle='--', linewidth=1.5)
                
                # Add goal label
                self.savings_forecast_canvas.axes.text(
                    dates[0], goal.amount, 
                    f"Goal: {goal.name} ({goal.amount:,.0f} ₺)", 
                    ha='left', va='bottom',
                    fontsize=8, fontweight='bold', color='#9C27B0',
                    bbox=dict(facecolor='white', alpha=0.8, boxstyle='round,pad=0.2')
                )
                
                # Calculate goal achievement timeline
                if current_savings > 0:
                    # Find intersection with normal case
                    for i, savings in enumerate(normal_case):
                        if savings >= goal.amount:
                            # Mark the intersection point
                            self.savings_forecast_canvas.axes.plot(
                                dates[i], goal.amount, 'o', 
                                color='#9C27B0', markersize=8
                            )
                            
                            # Add achievement date text
                            self.savings_forecast_canvas.axes.text(
                                dates[i], goal.amount,
                                f"Goal reached: {dates[i].strftime('%b %Y')}",
                                ha='right', va='top',
                                fontsize=8, fontweight='bold', color='#9C27B0',
                                bbox=dict(facecolor='white', alpha=0.8, boxstyle='round,pad=0.2')
                            )
                            break
        
        # Add title and labels
        self.savings_forecast_canvas.axes.set_title('Savings Projection (Next 12 Months)', 
                                               fontsize=11, fontweight='bold', pad=8)
        self.savings_forecast_canvas.axes.set_xlabel('Month', fontsize=9, labelpad=5)
        self.savings_forecast_canvas.axes.set_ylabel('Cumulative Savings (₺)', fontsize=9, labelpad=5)
        
        # Format x-axis dates
        self.savings_forecast_canvas.axes.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        self.savings_forecast_canvas.axes.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
        
        # Rotate date labels for better readability
        plt.setp(self.savings_forecast_canvas.axes.get_xticklabels(), rotation=45, ha='right')
        
        # Add horizontal line at zero
        self.savings_forecast_canvas.axes.axhline(y=0, color='#888888', linestyle='-', alpha=0.3)
        
        # Add scenario descriptions
        scenario_text = """
        Scenarios:
        • Best: Income +5%/mo, Expenses -3%/mo
        • Expected: Current rates maintained
        • Worst: Income -3%/mo, Expenses +5%/mo
        """
        
        self.savings_forecast_canvas.axes.text(
            0.02, 0.02, scenario_text,
            transform=self.savings_forecast_canvas.axes.transAxes,
            fontsize=7, va='bottom', ha='left',
            bbox=dict(facecolor='white', alpha=0.8, boxstyle='round,pad=0.3')
        )
        
        # Add starting points annotations
        self.savings_forecast_canvas.axes.annotate(
            f"Start: {current_savings:,.0f} ₺",
            xy=(dates[0], current_savings),
            xytext=(5, 0), textcoords="offset points",
            ha='left', va='center',
            fontsize=8, fontweight='bold', color='#2196F3'
        )
        
        # Add final values annotations
        self.savings_forecast_canvas.axes.annotate(
            f"{best_case[-1]:,.0f} ₺",
            xy=(dates[-1], best_case[-1]),
            xytext=(-5, 0), textcoords="offset points",
            ha='right', va='center',
            fontsize=8, fontweight='bold', color='#4CAF50'
        )
        
        self.savings_forecast_canvas.axes.annotate(
            f"{normal_case[-1]:,.0f} ₺",
            xy=(dates[-1], normal_case[-1]),
            xytext=(-5, 0), textcoords="offset points",
            ha='right', va='center',
            fontsize=8, fontweight='bold', color='#2196F3'
        )
        
        self.savings_forecast_canvas.axes.annotate(
            f"{worst_case[-1]:,.0f} ₺",
            xy=(dates[-1], worst_case[-1]),
            xytext=(-5, 0), textcoords="offset points",
            ha='right', va='center',
            fontsize=8, fontweight='bold', color='#F44336'
        )
        
        # Add legend
        self.savings_forecast_canvas.axes.legend(loc='upper left', fontsize=8)
        
        self.savings_forecast_canvas.fig.tight_layout()
        self.savings_forecast_canvas.draw()