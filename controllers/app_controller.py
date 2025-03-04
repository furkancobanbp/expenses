from datetime import datetime
from typing import List, Dict

from models.finance_manager import FinanceManager
from models.transaction import TransactionType
from models.financial_goal import GoalType, FinancialGoal

class AppController:
    def __init__(self, finance_manager: FinanceManager):
        self.finance_manager = finance_manager

    def add_transaction(self, name: str, amount: float, transaction_type: TransactionType, date: datetime) -> bool:
        """Add New Transaction"""
        try:
            self.finance_manager.add_transaction(name, amount, transaction_type, date)
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
    
    # Financial Goals Methods
    
    def add_goal(self, name: str, amount: float, goal_type: GoalType, year: int, month: int) -> bool:
        """Add a new financial goal"""
        try:
            self.finance_manager.add_goal(name, amount, goal_type, year, month)
            return True
        except Exception as e:
            print(f"Error adding goal: {e}")
            return False
    
    def update_goal(self, goal_id: str, name: str = None, amount: float = None, 
                   goal_type: GoalType = None, year: int = None, month: int = None,
                   active: bool = None) -> bool:
        """Update an existing goal"""
        try:
            return self.finance_manager.update_goal(
                goal_id, name, amount, goal_type, year, month, active
            )
        except Exception as e:
            print(f"Error updating goal: {e}")
            return False
    
    def remove_goal(self, goal_id: str) -> bool:
        """Remove a goal"""
        try:
            return self.finance_manager.remove_goal(goal_id)
        except Exception as e:
            print(f"Error removing goal: {e}")
            return False
    
    def get_goals_by_month(self, year: int, month: int) -> List[FinancialGoal]:
        """Get all goals for a specific month"""
        return self.finance_manager.get_goals_by_month(year, month)
    
    def get_goal_progress(self, goal_id: str) -> Dict:
        """Get progress information for a specific goal"""
        return self.finance_manager.get_goal_progress(goal_id)
    
    def get_all_goals(self) -> List[FinancialGoal]:
        """Get all financial goals"""
        return self.finance_manager.get_all_goals()