# Personal Finance Manager

A desktop application for tracking personal finances, visualizing financial data, managing transactions, and setting financial goals.

## Overview

This application allows users to:
- Add income and expense transactions with custom names and dates
- Visualize financial data with interactive charts
- View monthly summaries of income, expenses, and net worth
- Track financial trends over time
- Set and monitor financial goals for income, expenses, and savings

## Features

- **Dashboard**: Visual overview of financial health
  - Monthly income vs expenses chart
  - Cumulative financial overview
  - Monthly trend analysis
  - Expense category breakdown
  
- **Transaction Management**:
  - Add new income/expense transactions
  - View transactions by period (current month, previous month, etc.)
  - Sort and filter transactions
  - Date selection for transaction organization
  
- **Financial Goals**:
  - Set income, expense, and savings goals
  - Track progress toward financial targets
  - Visual indicators of goal completion status
  - Period-specific goals (monthly targets)

## Technical Architecture

The application follows the Model-View-Controller (MVC) architectural pattern:

### Models
- `Transaction`: Represents individual financial transactions
- `TransactionType`: Enum for income/expense types
- `FinanceManager`: Manages transaction data and calculations
- `FinancialGoal`: Represents a financial target with type and period
- `GoalType`: Enum for income/expense/savings goals

### Views
- `MainWindow`: Primary container for the application UI
- `Dashboard`: Visualization of financial data with charts
- `TransactionList`: Organized display of income and expense transactions
- `GoalsTab`: Goal creation and tracking interface
- `EntryForm`: Form for adding new transactions

### Controllers
- `AppController`: Intermediary between views and models

## Project Structure

```
├── controllers/
│   ├── __init__.py
│   └── app_controller.py
├── models/
│   ├── __init__.py
│   ├── finance_manager.py
│   ├── transaction.py
│   └── financial_goal.py
├── views/
│   ├── __init__.py
│   ├── dashboard.py
│   ├── entry_form.py
│   ├── transaction_list.py
│   ├── goals.py
│   └── main_window.py
├── finance_data.json    # Transaction data storage
├── financial_goals.json # Goals data storage
└── main.py              # Application entry point
```

## Requirements

- Python 3.6+
- PyQt5
- Matplotlib

## Installation

1. Clone the repository:
```
git clone https://github.com/yourusername/personal-finance-manager.git
cd personal-finance-manager
```

2. Install dependencies:
```
pip install PyQt5 matplotlib
```

3. Run the application:
```
python main.py
```

## Usage

### Adding Transactions
1. Navigate to the "Add Transaction" tab
2. Fill in transaction details:
   - Name: Description of the transaction
   - Amount: Value in Turkish Lira (₺)
   - Type: Income or Expense
   - Date: Month and year of the transaction
3. Click "Add Transaction"

### Viewing Transactions
1. Navigate to the "Transactions" tab
2. Select a time period from the dropdown (current month, previous month, etc.)
3. View income and expense transactions separately
4. See transaction totals for each category

### Setting Financial Goals
1. Navigate to the "Financial Goals" tab
2. Fill out the goal creation form:
   - Name: Description of your financial goal
   - Target Amount: The amount you aim to reach or stay under
   - Goal Type: Income, Expense Budget, or Savings Target
   - Period: The month and year for the goal
3. Click "Add Goal"

### Tracking Goal Progress
1. Navigate to the "Financial Goals" tab
2. Select the month/year to view goals for that period
3. View progress bars and completion percentages
4. See current amounts and remaining amounts for each goal

### Viewing Financial Data
1. Navigate to the "Dashboard" tab
2. Select the year and month to view
3. Examine the charts for financial insights:
   - Overview tab: Monthly comparison and cumulative charts
   - Insights tab: Trend analysis and expense breakdown

## Data Storage

All transaction data is stored in `finance_data.json` and goals data is stored in `financial_goals.json` in the application directory.

## Customization

The application uses a modern, customizable UI with a blue color scheme. You can modify the stylesheet in `main.py` to change the appearance.

## Future Enhancements

Potential features for future development:
- Data import/export functionality
- Budget planning templates
- Transaction categories and tags
- Multiple currency support
- Recurring transaction automation
- Goal achievement notifications
- Debt reduction planning


## Credits

Created by Furkan Çoban