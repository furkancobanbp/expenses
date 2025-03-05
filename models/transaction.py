from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class TransactionType(Enum):
    INCOME = "income"
    EXPENSE = "expense"

@dataclass
class Transaction:
    id: str  # UUID
    name: str
    amount: float
    transaction_type: TransactionType
    date: datetime  # only month and year will be used
    category: str = None  # Now a string instead of enum
    
    def to_dict(self):
        data = {
            "id": self.id,
            "name": self.name,
            "amount": self.amount,
            "transaction_type": self.transaction_type.value,
            "date": self.date.isoformat()
        }
        
        # Add category if it exists
        if self.category:
            data["category"] = self.category
            
        return data

    @classmethod
    def from_dict(cls, data):
        # Get the category if it exists
        category = data.get("category", None)
        
        return cls(
            id=data["id"],
            name=data["name"],
            amount=data["amount"],
            transaction_type=TransactionType(data["transaction_type"]),
            date=datetime.fromisoformat(data["date"]),
            category=category
        )