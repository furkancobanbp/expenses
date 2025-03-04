from datetime import datetime
from typing import List, Dict

from models.finance_manager import FinanceManager
from models.transaction import TransactionType

class AppController:
    def __init__(self, finance_manager: FinanceManager):
        self.finance_manager = finance_manager

    def add_transaction(self, name: str, amount: float, transaction_type: TransactionType, date: datetime) -> bool:
        """Add New Transaction"""
        try:
            self. finance_manager.add_transaction(name, amount, transaction_type, date)
            return True
        except Exception as e:
            print(f"Error adding transaction: {e}")
            return False

    def get_monthly_summary(self, year: int, month: int) -> Dict:
        """Get monthly summary of finances"""
        return self.finance_manager.get_monthly_summary(year, month)
    
    def get_monthly_data_for_year(self, year: int) -> Dict:
        """Get financial data for each month in a year"""
        return self.finance_manager.get_monthly_data_for_year(year)
    
    def get_cumulative_data(self) -> List[Dict]:
        """Get cumulative financial data over time"""
        return self.finance_manager.get_cumulative_data()
    
    def get_unique_years(self) -> List[int]:
        """Get list of years that have transaction data"""
        return self.finance_manager.get_unique_years()