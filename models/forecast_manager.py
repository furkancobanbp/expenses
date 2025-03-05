import json
import os
import uuid
from datetime import datetime
from typing import List, Dict, Optional

from .transaction import Transaction, TransactionType

class ForecastTransaction(Transaction):
    """
    Extension of Transaction for forecast data.
    Includes additional fields for notes and actual transaction ID for linking.
    """
    @classmethod
    def from_dict(cls, data):
        """Create a ForecastTransaction instance from a dictionary"""
        instance = super().from_dict(data)
        instance.notes = data.get("notes", "")
        instance.actual_transaction_id = data.get("actual_transaction_id", None)
        return instance
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        data = super().to_dict()
        data["notes"] = getattr(self, "notes", "")
        if hasattr(self, "actual_transaction_id") and self.actual_transaction_id:
            data["actual_transaction_id"] = self.actual_transaction_id
        return data

class ForecastManager:
    """Manager for forecast transactions"""
    
    def __init__(self, file_path="forecast_transactions.json"):
        self.file_path = file_path
        self.forecasts = []
        self.load_data()
    
    def load_data(self):
        """Load forecast transactions from JSON file"""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r') as file:
                    data = json.load(file)
                    self.forecasts = [ForecastTransaction.from_dict(item) for item in data]
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error loading forecast data: {e}")
                self.forecasts = []
        else:
            self.forecasts = []
    
    def save_data(self):
        """Save forecast transactions to JSON file"""
        with open(self.file_path, 'w') as file:
            json.dump([t.to_dict() for t in self.forecasts], file, indent=2)
    
    def add_forecast(self, name: str, amount: float, 
                    category_name: str, category_type: TransactionType, 
                    date: datetime, notes: str = "") -> ForecastTransaction:
        """Add a new forecast transaction"""
        # Create a new forecast transaction with a unique ID
        forecast = ForecastTransaction.from_dict({
            "id": str(uuid.uuid4()),
            "name": name,
            "amount": amount,
            "transaction_type": category_type.value,
            "category": category_name,
            "date": date.isoformat(),
            "notes": notes
        })
        
        self.forecasts.append(forecast)
        self.save_data()
        return forecast
    
    def remove_forecast(self, forecast_id: str) -> bool:
        """Remove a forecast transaction by ID"""
        for i, forecast in enumerate(self.forecasts):
            if forecast.id == forecast_id:
                del self.forecasts[i]
                self.save_data()
                return True
        return False
    
    def update_forecast(self, forecast_id: str, name: str = None, amount: float = None,
                       category_name: str = None, category_type: TransactionType = None,
                       date: datetime = None, notes: str = None) -> bool:
        """Update an existing forecast transaction"""
        for forecast in self.forecasts:
            if forecast.id == forecast_id:
                if name is not None:
                    forecast.name = name
                if amount is not None:
                    forecast.amount = amount
                if category_name is not None:
                    forecast.category = category_name
                if category_type is not None:
                    forecast.transaction_type = category_type
                if date is not None:
                    forecast.date = date
                if notes is not None:
                    forecast.notes = notes
                self.save_data()
                return True
        return False
    
    def link_to_actual(self, forecast_id: str, actual_id: str) -> bool:
        """Link a forecast transaction to its actual transaction"""
        for forecast in self.forecasts:
            if forecast.id == forecast_id:
                forecast.actual_transaction_id = actual_id
                self.save_data()
                return True
        return False
    
    def get_forecasts_by_month(self, year: int, month: int) -> List[ForecastTransaction]:
        """Get all forecasts for a specific month and year"""
        return [f for f in self.forecasts 
                if f.date.year == year and f.date.month == month]
    
    def get_all_forecasts(self) -> List[ForecastTransaction]:
        """Get all forecast transactions"""
        return self.forecasts
    
    def get_monthly_summary(self, year: int, month: int) -> Dict:
        """Get summary of forecast income, expenses and net worth for a month"""
        forecasts = self.get_forecasts_by_month(year, month)
        
        total_income = sum(f.amount for f in forecasts 
                          if f.transaction_type == TransactionType.INCOME)
        total_expenses = sum(f.amount for f in forecasts 
                            if f.transaction_type == TransactionType.EXPENSE)
        net_worth = total_income - total_expenses
        
        return {
            "total_income": total_income,
            "total_expenses": total_expenses,
            "net_worth": net_worth
        }
    
    def get_category_summary(self, year: int, month: int) -> Dict:
        """Get categorized summary of forecasts for a month"""
        forecasts = self.get_forecasts_by_month(year, month)
        
        # Group by category
        income_categories = {}
        expense_categories = {}
        
        for forecast in forecasts:
            category = forecast.category
            if forecast.transaction_type == TransactionType.INCOME:
                if category in income_categories:
                    income_categories[category] += forecast.amount
                else:
                    income_categories[category] = forecast.amount
            else:
                if category in expense_categories:
                    expense_categories[category] += forecast.amount
                else:
                    expense_categories[category] = forecast.amount
        
        return {
            "income_categories": income_categories,
            "expense_categories": expense_categories
        }
    
    def compare_with_actual(self, finance_manager, year: int, month: int) -> Dict:
        """Compare forecast data with actual data for a specific month"""
        # Get forecast and actual summaries
        forecast_summary = self.get_monthly_summary(year, month)
        actual_summary = finance_manager.get_monthly_summary(year, month)
        
        # Get category summaries
        forecast_categories = self.get_category_summary(year, month)
        
        # Get actual transactions for the month
        actual_transactions = finance_manager.get_transactions_by_month(year, month)
        
        # Group actual transactions by category
        actual_income_categories = {}
        actual_expense_categories = {}
        
        for transaction in actual_transactions:
            category = transaction.category
            if transaction.transaction_type == TransactionType.INCOME:
                if category in actual_income_categories:
                    actual_income_categories[category] += transaction.amount
                else:
                    actual_income_categories[category] = transaction.amount
            else:
                if category in actual_expense_categories:
                    actual_expense_categories[category] += transaction.amount
                else:
                    actual_expense_categories[category] = transaction.amount
        
        # Calculate variances
        income_variance = actual_summary["total_income"] - forecast_summary["total_income"]
        income_variance_pct = (income_variance / forecast_summary["total_income"] * 100) if forecast_summary["total_income"] > 0 else 0
        
        expense_variance = actual_summary["total_expenses"] - forecast_summary["total_expenses"]
        expense_variance_pct = (expense_variance / forecast_summary["total_expenses"] * 100) if forecast_summary["total_expenses"] > 0 else 0
        
        net_variance = actual_summary["net_worth"] - forecast_summary["net_worth"]
        net_variance_pct = (net_variance / abs(forecast_summary["net_worth"]) * 100) if forecast_summary["net_worth"] != 0 else 0
        
        # Calculate category variances
        income_category_variances = {}
        for category, forecast_amount in forecast_categories["income_categories"].items():
            actual_amount = actual_income_categories.get(category, 0)
            variance = actual_amount - forecast_amount
            variance_pct = (variance / forecast_amount * 100) if forecast_amount > 0 else 0
            income_category_variances[category] = {
                "forecast": forecast_amount,
                "actual": actual_amount,
                "variance": variance,
                "variance_pct": variance_pct
            }
        
        # Add actual categories not in forecast
        for category, amount in actual_income_categories.items():
            if category not in income_category_variances:
                income_category_variances[category] = {
                    "forecast": 0,
                    "actual": amount,
                    "variance": amount,
                    "variance_pct": 100
                }
        
        expense_category_variances = {}
        for category, forecast_amount in forecast_categories["expense_categories"].items():
            actual_amount = actual_expense_categories.get(category, 0)
            variance = actual_amount - forecast_amount
            variance_pct = (variance / forecast_amount * 100) if forecast_amount > 0 else 0
            expense_category_variances[category] = {
                "forecast": forecast_amount,
                "actual": actual_amount,
                "variance": variance,
                "variance_pct": variance_pct
            }
        
        # Add actual expense categories not in forecast
        for category, amount in actual_expense_categories.items():
            if category not in expense_category_variances:
                expense_category_variances[category] = {
                    "forecast": 0,
                    "actual": amount,
                    "variance": amount,
                    "variance_pct": 100
                }
        
        return {
            "summary": {
                "income": {
                    "forecast": forecast_summary["total_income"],
                    "actual": actual_summary["total_income"],
                    "variance": income_variance,
                    "variance_pct": income_variance_pct
                },
                "expenses": {
                    "forecast": forecast_summary["total_expenses"],
                    "actual": actual_summary["total_expenses"],
                    "variance": expense_variance,
                    "variance_pct": expense_variance_pct
                },
                "net_worth": {
                    "forecast": forecast_summary["net_worth"],
                    "actual": actual_summary["net_worth"],
                    "variance": net_variance,
                    "variance_pct": net_variance_pct
                }
            },
            "income_categories": income_category_variances,
            "expense_categories": expense_category_variances
        }