import json
import os
import uuid
from datetime import datetime
from typing import List, Dict, Optional, Tuple

from .transaction import Transaction, TransactionType

class ForecastTransaction(Transaction):
    """
    Extension of Transaction for forecast data.
    Includes additional fields for notes and actual transaction ID for linking.
    """
    def __init__(self, id: str, name: str, amount: float, transaction_type: TransactionType,
                 date: datetime, category: str = None, notes: str = "", 
                 actual_transaction_id: str = None, realized: bool = False):
        super().__init__(id, name, amount, transaction_type, date, category)
        self.notes = notes
        self.actual_transaction_id = actual_transaction_id
        self.realized = realized
        
    @classmethod
    def from_dict(cls, data):
        """Create a ForecastTransaction instance from a dictionary"""
        instance = super().from_dict(data)
        instance.notes = data.get("notes", "")
        instance.actual_transaction_id = data.get("actual_transaction_id", None)
        instance.realized = data.get("realized", False)
        return instance
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        data = super().to_dict()
        data["notes"] = getattr(self, "notes", "")
        data["realized"] = getattr(self, "realized", False)
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
                with open(self.file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    self.forecasts = [ForecastTransaction.from_dict(item) for item in data]
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error loading forecast data: {e}")
                self.forecasts = []
        else:
            self.forecasts = []
    
    def save_data(self):
        """Save forecast transactions to JSON file"""
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump([t.to_dict() for t in self.forecasts], file, indent=2, ensure_ascii=False)
    
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
    
    def find_matching_forecast(self, transaction: Transaction) -> Optional[ForecastTransaction]:
        """Find a matching forecast for a transaction"""
        # Find forecasts for the same month/year
        forecasts = self.get_forecasts_by_month(transaction.date.year, transaction.date.month)
        
        # Look for a match on category and transaction type
        matches = []
        for forecast in forecasts:
            # Skip already realized forecasts
            if getattr(forecast, "realized", False):
                continue
                
            # Check if the category and type match
            if (forecast.category == transaction.category and 
                forecast.transaction_type == transaction.transaction_type):
                matches.append(forecast)
        
        if not matches:
            return None
            
        # Find the closest match by amount
        closest_match = min(matches, key=lambda f: abs(f.amount - transaction.amount))
        
        # Only consider a match if the amount is within 10% difference
        if abs(closest_match.amount - transaction.amount) <= (closest_match.amount * 0.1):
            return closest_match
            
        return None
    
    def mark_forecast_realized(self, forecast_id: str, transaction_id: str) -> bool:
        """Mark a forecast as realized with a specific transaction"""
        for forecast in self.forecasts:
            if forecast.id == forecast_id:
                forecast.actual_transaction_id = transaction_id
                forecast.realized = True
                self.save_data()
                return True
        return False
    
    def link_to_actual(self, forecast_id: str, actual_id: str) -> bool:
        """Link a forecast transaction to its actual transaction"""
        for forecast in self.forecasts:
            if forecast.id == forecast_id:
                forecast.actual_transaction_id = actual_id
                forecast.realized = True
                self.save_data()
                return True
        return False
    
    def create_forecast_from_transaction(self, transaction: Transaction) -> ForecastTransaction:
        """Create a new forecast based on an existing transaction"""
        forecast = ForecastTransaction.from_dict({
            "id": str(uuid.uuid4()),
            "name": f"[Forecast] {transaction.name}",
            "amount": transaction.amount,
            "transaction_type": transaction.transaction_type.value,
            "category": transaction.category,
            "date": transaction.date.isoformat(),
            "notes": f"Created from transaction {transaction.id}"
        })
        
        self.forecasts.append(forecast)
        self.save_data()
        return forecast
    
    def bulk_convert_to_forecasts(self, transactions: List[Transaction]) -> int:
        """Convert a list of transactions to forecasts and return the count"""
        count = 0
        for transaction in transactions:
            self.create_forecast_from_transaction(transaction)
            count += 1
        return count
    
    def check_realization_against_actual(self, actual_transactions: List[Transaction]) -> Tuple[int, int]:
        """
        Check which forecasts have been realized by actual transactions
        Returns a tuple of (matched_count, total_forecasts)
        """
        unrealized_forecasts = [f for f in self.forecasts if not getattr(f, "realized", False)]
        
        matched_count = 0
        for transaction in actual_transactions:
            matching_forecast = self.find_matching_forecast(transaction)
            if matching_forecast:
                self.mark_forecast_realized(matching_forecast.id, transaction.id)
                matched_count += 1
                
        return (matched_count, len(unrealized_forecasts))
    
    def get_monthly_forecast_summary(self, year: int, month: int) -> Dict:
        """Alias for get_monthly_summary"""
        return self.get_monthly_summary(year, month)
    
    def get_comparison_data(self, actual_data: Dict, year: int, month: int) -> Dict:
        """Get comparison data between forecast and actual"""
        forecast_summary = self.get_monthly_summary(year, month)
        
        # Calculate variances
        income_variance = actual_data["total_income"] - forecast_summary["total_income"]
        income_variance_pct = (income_variance / forecast_summary["total_income"] * 100) if forecast_summary["total_income"] > 0 else 0
        
        expense_variance = actual_data["total_expenses"] - forecast_summary["total_expenses"]
        expense_variance_pct = (expense_variance / forecast_summary["total_expenses"] * 100) if forecast_summary["total_expenses"] > 0 else 0
        
        net_variance = actual_data["net_worth"] - forecast_summary["net_worth"]
        net_variance_pct = (net_variance / abs(forecast_summary["net_worth"]) * 100) if forecast_summary["net_worth"] != 0 else 0
        
        return {
            "income": {
                "forecast": forecast_summary["total_income"],
                "actual": actual_data["total_income"],
                "variance": income_variance,
                "variance_pct": income_variance_pct
            },
            "expenses": {
                "forecast": forecast_summary["total_expenses"],
                "actual": actual_data["total_expenses"],
                "variance": expense_variance,
                "variance_pct": expense_variance_pct
            },
            "net_worth": {
                "forecast": forecast_summary["net_worth"],
                "actual": actual_data["net_worth"],
                "variance": net_variance,
                "variance_pct": net_variance_pct
            }
        }
    
    def get_category_comparison(self, actual_transactions: List[Transaction], 
                             year: int, month: int) -> Dict:
        """Get category-level comparison between forecast and actual"""
        # Group forecasts by category
        forecasts = self.get_forecasts_by_month(year, month)
        forecast_categories = {"income": {}, "expense": {}}
        
        for forecast in forecasts:
            category = forecast.category if forecast.category else "Uncategorized"
            if forecast.transaction_type == TransactionType.INCOME:
                if category in forecast_categories["income"]:
                    forecast_categories["income"][category] += forecast.amount
                else:
                    forecast_categories["income"][category] = forecast.amount
            else:
                if category in forecast_categories["expense"]:
                    forecast_categories["expense"][category] += forecast.amount
                else:
                    forecast_categories["expense"][category] = forecast.amount
        
        # Group actual transactions by category
        actual_categories = {"income": {}, "expense": {}}
        
        for transaction in actual_transactions:
            category = transaction.category if transaction.category else "Uncategorized"
            if transaction.transaction_type == TransactionType.INCOME:
                if category in actual_categories["income"]:
                    actual_categories["income"][category] += transaction.amount
                else:
                    actual_categories["income"][category] = transaction.amount
            else:
                if category in actual_categories["expense"]:
                    actual_categories["expense"][category] += transaction.amount
                else:
                    actual_categories["expense"][category] = transaction.amount
        
        # Calculate variances
        category_variances = {"income": {}, "expense": {}}
        
        # Income categories
        all_income_categories = set(list(forecast_categories["income"].keys()) + 
                                   list(actual_categories["income"].keys()))
        
        for category in all_income_categories:
            forecast_amount = forecast_categories["income"].get(category, 0)
            actual_amount = actual_categories["income"].get(category, 0)
            variance = actual_amount - forecast_amount
            variance_pct = (variance / forecast_amount * 100) if forecast_amount > 0 else 0
            
            category_variances["income"][category] = {
                "forecast": forecast_amount,
                "actual": actual_amount,
                "variance": variance,
                "variance_pct": variance_pct
            }
        
        # Expense categories
        all_expense_categories = set(list(forecast_categories["expense"].keys()) + 
                                    list(actual_categories["expense"].keys()))
        
        for category in all_expense_categories:
            forecast_amount = forecast_categories["expense"].get(category, 0)
            actual_amount = actual_categories["expense"].get(category, 0)
            variance = actual_amount - forecast_amount
            variance_pct = (variance / forecast_amount * 100) if forecast_amount > 0 else 0
            
            category_variances["expense"][category] = {
                "forecast": forecast_amount,
                "actual": actual_amount,
                "variance": variance,
                "variance_pct": variance_pct
            }
        
        return category_variances
    
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