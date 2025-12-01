from dataclasses import dataclass
from datetime import date


@dataclass
class Transaction:
    date: date
    amount: float
    category: str
    description: str = ""

    @property
    def type(self):
        return "transaction"



@dataclass
class IncomeTransaction(Transaction):
    @property
    def type(self):
        return "income"
    
    def apply_to_summary(self, summary):
        summary["total_income"] += self.amount


@dataclass
class ExpenseTransaction(Transaction):
    @property
    def type(self):
        return "expense"
    
    def apply_to_summary(self, summary):
        summary["total_expense"] += self.amount
        summary["by_category"][self.category] = summary["by_category"].get(self.category, 0.0) + self.amount