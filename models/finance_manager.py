import json
import os
import uuid
from datetime import datetime
from typing import List, Dict, Optional

from .transaction import Transaction, TransactionType

class FinanceManager:
    def __init__(self, file_path="finance_data.json"):
        self.file_path = file_path
        self.transactions = []
        self.load_data()
    
    def load_data(self):
        """Load transactions from JSON file"""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r') as file:
                    data = json.load(file)
                    self.transactions = [Transaction.from_dict(item) for item in data]
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error loading data: {e}")
                self.transactions = []
        else:
            self.transactions = []
    
    def save_data(self):
        """Save transactions to JSON file"""
        with open(self.file_path, 'w') as file:
            json.dump([t.to_dict() for t in self.transactions], file, indent=2)
    
    def add_transaction(self, name: str, amount: float, 
                        transaction_type: TransactionType, 
                        date: Optional[datetime] = None) -> Transaction:
        """Add a new transaction"""
        if date is None:
            date = datetime.now()
        
        # Create a new transaction with a unique ID
        transaction = Transaction(
            id=str(uuid.uuid4()),
            name=name,
            amount=amount,
            transaction_type=transaction_type,
            date=date
        )
        
        self.transactions.append(transaction)
        self.save_data()
        return transaction
    
    def remove_transaction(self, transaction_id: str) -> bool:
        """Remove a transaction by ID"""
        for i, transaction in enumerate(self.transactions):
            if transaction.id == transaction_id:
                del self.transactions[i]
                self.save_data()
                return True
        return False
    
    def get_transactions_by_month(self, year: int, month: int) -> List[Transaction]:
        """Get all transactions for a specific month and year"""
        return [t for t in self.transactions 
                if t.date.year == year and t.date.month == month]
    
    def get_monthly_summary(self, year: int, month: int) -> Dict:
        """Get summary of income, expenses and net worth for a month"""
        transactions = self.get_transactions_by_month(year, month)
        
        total_income = sum(t.amount for t in transactions 
                          if t.transaction_type == TransactionType.INCOME)
        total_expenses = sum(t.amount for t in transactions 
                            if t.transaction_type == TransactionType.EXPENSE)
        net_worth = total_income - total_expenses
        
        return {
            "total_income": total_income,
            "total_expenses": total_expenses,
            "net_worth": net_worth
        }
    
    def get_all_transactions(self) -> List[Transaction]:
        """Get all transactions"""
        return self.transactions
    
    def get_monthly_data_for_year(self, year: int) -> Dict:
        """Get monthly data for an entire year for charting"""
        monthly_data = {}
        
        for month in range(1, 13):
            summary = self.get_monthly_summary(year, month)
            monthly_data[month] = summary
        
        return monthly_data
    
    def get_cumulative_data(self) -> Dict:
        """Get cumulative income, expenses and net worth over time"""
        # Sort transactions by date
        sorted_transactions = sorted(self.transactions, key=lambda t: t.date)
        
        cumulative_income = 0
        cumulative_expenses = 0
        data_points = []
        
        for transaction in sorted_transactions:
            if transaction.transaction_type == TransactionType.INCOME:
                cumulative_income += transaction.amount
            else:
                cumulative_expenses += transaction.amount
            
            cumulative_net = cumulative_income - cumulative_expenses
            
            data_points.append({
                "date": transaction.date,
                "cumulative_income": cumulative_income,
                "cumulative_expenses": cumulative_expenses,
                "cumulative_net": cumulative_net
            })
        
        return data_points
    
    def get_unique_years(self) -> List[int]:
        """Get a list of unique years in the transaction history"""
        years = {t.date.year for t in self.transactions}
        if not years:
            years = {datetime.now().year}
        return sorted(list(years))