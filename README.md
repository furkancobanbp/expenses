# Personal Finance Manager

A desktop application for tracking personal finances, visualizing financial data, and managing transactions.

## Overview

This application allows users to:
- Add income and expense transactions with custom names and dates
- Visualize financial data with interactive charts
- View monthly summaries of income, expenses, and net worth
- Track financial trends over time

## Features

- **Dashboard**: Visual overview of financial health
  - Monthly income vs expenses chart
  - Cumulative financial overview
  - Monthly trend analysis
  - Expense category breakdown
  
- **Transaction Management**:
  - Add new income/expense transactions
  - Date selection for transaction organization
  - Simple form interface

## Technical Architecture

The application follows the Model-View-Controller (MVC) architectural pattern:

### Models
- `Transaction`: Represents individual financial transactions
- `TransactionType`: Enum for income/expense types
- `FinanceManager`: Manages transaction data and calculations

### Views
- `MainWindow`: Primary container for the application UI
- `Dashboard`: Visualization of financial data with charts
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
│   └── transaction.py
├── views/
│   ├── __init__.py
│   ├── dashboard.py
│   ├── entry_form.py
│   ├── main_window.py
|   └── transaction_list.py
├── finance_data.json    # Transaction data storage
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

### Viewing Financial Data
1. Navigate to the "Dashboard" tab
2. Select the year and month to view
3. Examine the charts for financial insights:
   - Overview tab: Monthly comparison and cumulative charts
   - Insights tab: Trend analysis and expense breakdown

## Data Storage

All transaction data is stored in `finance_data.json` in the application directory. The format is a JSON array with individual transaction objects.

## Customization

The application uses a modern, customizable UI with a blue color scheme. You can modify the stylesheet in `main.py` to change the appearance.

## Future Enhancements

Potential features for future development:
- Data import/export functionality
- Budget planning and analysis
- Transaction categories and tags
- Multiple currency support
- Recurring transaction automation

## Credits

Created by Furkan Coban
