import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QComboBox, 
                           QLabel, QSizePolicy, QFrame, QGridLayout, QTabWidget)
from PyQt5.QtCore import Qt, pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import calendar
from collections import defaultdict

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
                                          fontsize=11, fontweight='bold', pad=8)
        self.monthly_canvas.axes.set_xlabel('Month', fontsize=9, labelpad=5)
        self.monthly_canvas.axes.set_ylabel('Amount (₺)', fontsize=9, labelpad=5)
        self.monthly_canvas.axes.set_xticks(x)
        self.monthly_canvas.axes.set_xticklabels([calendar.month_abbr[m] for m in months])
        
        # Legend
        legend = self.monthly_canvas.axes.legend(loc='upper right', frameon=True, 
                                               fancybox=True, framealpha=0.9, 
                                               shadow=True, fontsize=8)
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
                                           fontsize=9,
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
                                        color='#2e7d32', linewidth=1.5, marker='o', 
                                        markersize=3, markerfacecolor='white')
        self.cumulative_canvas.axes.plot(dates, expenses, '-', label='Expenses', 
                                        color='#c62828', linewidth=1.5, marker='o', 
                                        markersize=3, markerfacecolor='white')
        self.cumulative_canvas.axes.plot(dates, net, '-', label='Net Worth', 
                                        color='#1565c0', linewidth=2, marker='o', 
                                        markersize=4, markerfacecolor='white')
        
        # Add labels and formatting with improved styling
        self.cumulative_canvas.axes.set_title('Cumulative Financial Overview', 
                                              fontsize=11, fontweight='bold', pad=8)
        self.cumulative_canvas.axes.set_xlabel('Date', fontsize=9, labelpad=5)
        self.cumulative_canvas.axes.set_ylabel('Amount (₺)', fontsize=9, labelpad=5)
        
        # Format the dates on x-axis
        self.cumulative_canvas.axes.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        self.cumulative_canvas.axes.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
        
        # Legend
        legend = self.cumulative_canvas.axes.legend(loc='upper left', frameon=True, 
                                                  fancybox=True, framealpha=0.9, 
                                                  shadow=True, fontsize=8)
        legend.get_frame().set_edgecolor('#cccccc')
        
        # Rotate date labels for better readability
        plt.setp(self.cumulative_canvas.axes.get_xticklabels(), rotation=45, ha='right')
        
        self.cumulative_canvas.fig.tight_layout()
        self.cumulative_canvas.draw()
        
    def update_trend_chart(self, year):
        """Update the income vs expense trend chart - NEW CHART"""
        monthly_data = self.controller.get_monthly_data_for_year(year)
        
        # Clear previous plot
        self.trend_canvas.axes.clear()
        
        months = list(range(1, 13))
        income_values = [monthly_data[m]['total_income'] for m in months]
        expense_values = [monthly_data[m]['total_expenses'] for m in months]
        net_values = [monthly_data[m]['net_worth'] for m in months]
        
        # Create line chart with area fill
        x = range(len(months))
        
        # Plot income
        self.trend_canvas.axes.plot(x, income_values, '-', label='Income', 
                                  color='#2e7d32', linewidth=2, marker='o', 
                                  markersize=4, markerfacecolor='white')
        self.trend_canvas.axes.fill_between(x, income_values, alpha=0.2, color='#2e7d32')
        
        # Plot expenses
        self.trend_canvas.axes.plot(x, expense_values, '-', label='Expenses', 
                                  color='#c62828', linewidth=2, marker='o', 
                                  markersize=4, markerfacecolor='white')
        self.trend_canvas.axes.fill_between(x, expense_values, alpha=0.2, color='#c62828')
        
        # Add savings/deficit as bars
        for i, (inc, exp) in enumerate(zip(income_values, expense_values)):
            if inc > exp:  # Savings
                self.trend_canvas.axes.bar(i, inc-exp, bottom=exp, color='#2e7d32', alpha=0.3, width=0.5)
            elif exp > inc:  # Deficit
                self.trend_canvas.axes.bar(i, inc-exp, bottom=inc, color='#c62828', alpha=0.3, width=0.5)
        
        # Add labels and formatting
        self.trend_canvas.axes.set_title(f'Monthly Income vs Expense Trend ({year})', 
                                       fontsize=11, fontweight='bold', pad=8)
        self.trend_canvas.axes.set_xlabel('Month', fontsize=9, labelpad=5)
        self.trend_canvas.axes.set_ylabel('Amount (₺)', fontsize=9, labelpad=5)
        self.trend_canvas.axes.set_xticks(x)
        self.trend_canvas.axes.set_xticklabels([calendar.month_abbr[m] for m in months])
        
        # Add a legend
        from matplotlib.patches import Patch
        from matplotlib.lines import Line2D
        legend_elements = [
            Line2D([0], [0], color='#2e7d32', lw=2, marker='o', markersize=4, markerfacecolor='white', label='Income'),
            Line2D([0], [0], color='#c62828', lw=2, marker='o', markersize=4, markerfacecolor='white', label='Expenses'),
            Patch(facecolor='#2e7d32', alpha=0.3, label='Savings'),
            Patch(facecolor='#c62828', alpha=0.3, label='Deficit')
        ]
        self.trend_canvas.axes.legend(handles=legend_elements, loc='upper right', fontsize=8)
        
        self.trend_canvas.fig.tight_layout()
        self.trend_canvas.draw()
        
    def update_category_chart(self, year, month):
        """Update the expense category breakdown pie chart - NEW CHART"""
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
        
        # Extract main keywords from transaction names to create categories
        categories = defaultdict(float)
        
        for transaction in expense_transactions:
            # Simple category extraction - use first word as category
            # In a real app, you'd have proper categories
            category = transaction.name.split()[0] if ' ' in transaction.name else transaction.name
            categories[category] += transaction.amount
        
        # Sort by amount and get top categories
        sorted_categories = dict(sorted(categories.items(), key=lambda x: x[1], reverse=True))
        
        # Limit to top 6 categories and group the rest as "Other"
        if len(sorted_categories) > 6:
            top_categories = dict(list(sorted_categories.items())[:5])
            other_amount = sum(list(sorted_categories.values())[5:])
            top_categories["Other"] = other_amount
            sorted_categories = top_categories
        
        # Prepare data for pie chart
        labels = list(sorted_categories.keys())
        sizes = list(sorted_categories.values())
        
        # Calculate percentages
        total = sum(sizes)
        percentages = [(size/total)*100 for size in sizes]
        
        # Set an aspect ratio for the pie chart
        self.category_canvas.axes.set_aspect('equal')
        
        # Create pie chart with custom colors
        colors = ['#FF5252', '#FF7043', '#FFCA28', '#9CCC65', '#4FC3F7', '#7986CB', '#BA68C8']
        explode = [0.05] * len(labels)  # Slightly explode all slices
        
        wedges, texts, autotexts = self.category_canvas.axes.pie(
            sizes, 
            labels=labels,
            colors=colors[:len(labels)],
            explode=explode,
            autopct='%1.1f%%',
            shadow=True,
            startangle=90,
            textprops={'fontsize': 8},
            wedgeprops={'edgecolor': 'white', 'linewidth': 1}
        )
        
        # Styling for the percentage text
        for autotext in autotexts:
            autotext.set_fontsize(7)
            autotext.set_weight('bold')
            autotext.set_color('white')
        
        # Add title
        self.category_canvas.axes.set_title(f'Expense Breakdown - {calendar.month_name[month]} {year}', 
                                          fontsize=11, fontweight='bold', pad=8)
        
        # Add transaction count information
        transaction_count = len(expense_transactions)
        self.category_canvas.axes.text(0.5, -0.1, 
                                     f'Total: {total:,.2f} ₺ ({transaction_count} transactions)',
                                     horizontalalignment='center',
                                     verticalalignment='center',
                                     fontsize=8,
                                     transform=self.category_canvas.axes.transAxes)
        
        self.category_canvas.fig.tight_layout()
        self.category_canvas.draw()