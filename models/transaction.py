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

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "amount": self.amount,
            "transaction_type": self.transaction_type.value,
            "date": self.date.isoformat()
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            name=data["name"],
            amount=data["amount"],
            transaction_type=TransactionType(data["transaction_type"]),
            date=datetime.fromisoformat(data["date"])
        )