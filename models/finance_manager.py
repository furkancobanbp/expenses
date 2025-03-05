import json
import os
import uuid
from datetime import datetime
from typing import List, Dict, Optional

from .transaction import Transaction, TransactionType
from .financial_goal import FinancialGoal, GoalType

class FinanceManager:
    def __init__(self, file_path="finance_data.json", goals_path="financial_goals.json"):
        self.file_path = file_path
        self.goals_path = goals_path
        self.transactions = []
        self.goals = []
        self.load_data()
        self.load_goals()
    
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
    
    def load_goals(self):
        """Load financial goals from JSON file"""
        if os.path.exists(self.goals_path):
            try:
                with open(self.goals_path, 'r') as file:
                    data = json.load(file)
                    self.goals = [FinancialGoal.from_dict(item) for item in data]
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error loading goals: {e}")
                self.goals = []
        else:
            self.goals = []
    
    def save_data(self):
        """Save transactions to JSON file"""
        with open(self.file_path, 'w') as file:
            json.dump([t.to_dict() for t in self.transactions], file, indent=2)
    
    def save_goals(self):
        """Save financial goals to JSON file"""
        with open(self.goals_path, 'w') as file:
            json.dump([g.to_dict() for g in self.goals], file, indent=2)
    
    def add_transaction(self, name: str, amount: float, 
                    category_name: str, category_type: TransactionType, 
                    date: Optional[datetime] = None) -> Transaction:
        """Add a new transaction with category name and type"""
        if date is None:
            date = datetime.now()
        
        # Create a new transaction with a unique ID
        transaction = Transaction(
            id=str(uuid.uuid4()),
            name=name,
            amount=amount,
            transaction_type=category_type,
            category=category_name,
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
    
    # Financial Goals Methods
    
    def add_goal(self, name: str, amount: float, goal_type: GoalType, 
                year: int, month: int) -> FinancialGoal:
        """Add a new financial goal"""
        # Create a new goal with a unique ID
        goal = FinancialGoal.create_new(
            name=name,
            amount=amount,
            goal_type=goal_type,
            year=year,
            month=month
        )
        
        self.goals.append(goal)
        self.save_goals()
        return goal
    
    def update_goal(self, goal_id: str, name: str = None, amount: float = None, 
                   goal_type: GoalType = None, year: int = None, month: int = None,
                   active: bool = None) -> bool:
        """Update an existing goal by ID"""
        for goal in self.goals:
            if goal.id == goal_id:
                if name is not None:
                    goal.name = name
                if amount is not None:
                    goal.amount = amount
                if goal_type is not None:
                    goal.goal_type = goal_type
                if year is not None:
                    goal.year = year
                if month is not None:
                    goal.month = month
                if active is not None:
                    goal.active = active
                    
                self.save_goals()
                return True
        return False
    
    def remove_goal(self, goal_id: str) -> bool:
        """Remove a goal by ID"""
        for i, goal in enumerate(self.goals):
            if goal.id == goal_id:
                del self.goals[i]
                self.save_goals()
                return True
        return False
    
    def get_goals_by_month(self, year: int, month: int) -> List[FinancialGoal]:
        """Get all active goals for a specific month and year"""
        return [g for g in self.goals 
                if g.year == year and g.month == month and g.active]
    
    def get_goal_progress(self, goal_id: str) -> Dict:
        """Get progress information for a specific goal"""
        goal = next((g for g in self.goals if g.id == goal_id), None)
        
        if not goal:
            return {
                "goal": None,
                "current_amount": 0,
                "percentage": 0,
                "remaining": 0
            }
        
        # Get transactions for the goal's month
        transactions = self.get_transactions_by_month(goal.year, goal.month)
        
        # Calculate current amount based on goal type
        if goal.goal_type == GoalType.INCOME:
            current_amount = sum(t.amount for t in transactions 
                               if t.transaction_type == TransactionType.INCOME)
        elif goal.goal_type == GoalType.EXPENSE:
            current_amount = sum(t.amount for t in transactions 
                               if t.transaction_type == TransactionType.EXPENSE)
        elif goal.goal_type == GoalType.SAVINGS:
            income = sum(t.amount for t in transactions 
                       if t.transaction_type == TransactionType.INCOME)
            expenses = sum(t.amount for t in transactions 
                         if t.transaction_type == TransactionType.EXPENSE)
            current_amount = income - expenses
        
        # Calculate percentage and remaining
        percentage = (current_amount / goal.amount) * 100 if goal.amount > 0 else 0
        
        # For expense goals, we want to stay under the amount, so invert the logic
        if goal.goal_type == GoalType.EXPENSE:
            # If we're under budget, that's good!
            percentage = min(100, (current_amount / goal.amount) * 100)
            remaining = max(0, goal.amount - current_amount)
        else:
            # For income/savings, we want to meet or exceed the goal
            percentage = min(100, (current_amount / goal.amount) * 100)
            remaining = max(0, goal.amount - current_amount)
        
        return {
            "goal": goal,
            "current_amount": current_amount,
            "percentage": percentage,
            "remaining": remaining
        }
    
    def get_all_goals(self) -> List[FinancialGoal]:
        """Get all financial goals"""
        return self.goals