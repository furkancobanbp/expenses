from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import uuid

class GoalType(Enum):
    INCOME = "income"
    EXPENSE = "expense"
    SAVINGS = "savings"

@dataclass
class FinancialGoal:
    id: str  # UUID
    name: str
    amount: float
    goal_type: GoalType
    year: int
    month: int
    active: bool = True
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "amount": self.amount,
            "goal_type": self.goal_type.value,
            "year": self.year,
            "month": self.month,
            "active": self.active
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            name=data["name"],
            amount=data["amount"],
            goal_type=GoalType(data["goal_type"]),
            year=data["year"],
            month=data["month"],
            active=data.get("active", True)
        )
    
    @classmethod
    def create_new(cls, name, amount, goal_type, year, month):
        """Create a new goal with a unique ID"""
        return cls(
            id=str(uuid.uuid4()),
            name=name,
            amount=amount,
            goal_type=goal_type,
            year=year,
            month=month
        )