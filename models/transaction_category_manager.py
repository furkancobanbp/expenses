# models/transaction_category_manager.py
import json
import os
from enum import Enum
from typing import List, Dict, Optional

from models.transaction import TransactionType

class CategoryManager:
    """Manager for custom transaction categories"""
    
    def __init__(self, file_path="transaction_categories.json"):
        self.file_path = file_path
        self.categories = []
        self.load_categories()
        
        # Add default categories if none exist
        if not self.categories:
            self._add_default_categories()
    
    def load_categories(self):
        """Load categories from JSON file"""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r') as file:
                    self.categories = json.load(file)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading categories: {e}")
                self.categories = []
        else:
            self.categories = []
    
    def save_categories(self):
        """Save categories to JSON file"""
        try:
            with open(self.file_path, 'w') as file:
                json.dump(self.categories, file, indent=2)
        except IOError as e:
            print(f"Error saving categories: {e}")
    
    def _add_default_categories(self):
        """Add default categories"""
        defaults = [
            {"name": "Salary", "type": "income"},
            {"name": "Bank Loan", "type": "expense"},
            {"name": "Debt to Person", "type": "expense"},
            {"name": "Parental Expenses", "type": "expense"}
        ]
        
        for category in defaults:
            self.add_category(category["name"], TransactionType(category["type"]))
    
    def add_category(self, name: str, category_type: TransactionType) -> bool:
        """Add a new category"""
        # Check if category already exists
        if any(c["name"] == name for c in self.categories):
            return False
        
        self.categories.append({
            "name": name,
            "type": category_type.value
        })
        
        self.save_categories()
        return True
    
    def remove_category(self, name: str) -> bool:
        """Remove a category by name"""
        for i, category in enumerate(self.categories):
            if category["name"] == name:
                del self.categories[i]
                self.save_categories()
                return True
        return False
    
    def update_category(self, old_name: str, new_name: str, category_type: TransactionType) -> bool:
        """Update an existing category"""
        # Check if the new name already exists (unless it's the same as old name)
        if old_name != new_name and any(c["name"] == new_name for c in self.categories):
            return False
            
        for category in self.categories:
            if category["name"] == old_name:
                category["name"] = new_name
                category["type"] = category_type.value
                self.save_categories()
                return True
        return False
    
    def get_all_categories(self) -> List[Dict]:
        """Get all categories"""
        return self.categories
    
    def get_categories_by_type(self, category_type: TransactionType) -> List[str]:
        """Get all category names of a specific type"""
        return [c["name"] for c in self.categories if c["type"] == category_type.value]
    
    def get_category_type(self, name: str) -> Optional[TransactionType]:
        """Get the type of a category by name"""
        for category in self.categories:
            if category["name"] == name:
                return TransactionType(category["type"])
        return None