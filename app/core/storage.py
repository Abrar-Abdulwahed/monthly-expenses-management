from abc import ABC, abstractmethod
from datetime import datetime
import json
import os
from pymongo import MongoClient
from app.core.transactions import Transaction, IncomeTransaction, ExpenseTransaction


TRANSACTION_CLASSES = {
    "income": IncomeTransaction,
    "expense": ExpenseTransaction,
}


class Storage(ABC):
    @abstractmethod
    def save(self, transaction: Transaction):
        pass

    @abstractmethod
    def load(self):
        pass


class MongoStorage(Storage):
    def __init__(
        self,
        uri: str = "mongodb://localhost:27017",
        db_name: str = "budget_app",
        collection_name: str = "transactions",
    ):
        self.client = MongoClient(uri)
        self.collection = self.client[db_name][collection_name]

    def save(self, transaction: Transaction) -> None:
        self.collection.insert_one(
            {
                "date": transaction.date.isoformat(),
                "type": transaction.type,
                "amount": transaction.amount,
                "category": transaction.category,
                "description": transaction.description,
            }
        )

    def load(self):
        transactions = []

        for doc in self.collection.find():
            t_date = datetime.fromisoformat(doc["date"]).date()
            t_type = doc["type"]
            amount = doc["amount"]
            category = doc.get("category", "")
            description = doc.get("description", "")

            tx_cls = TRANSACTION_CLASSES.get(t_type)
            if not tx_cls:
                continue

            tx = tx_cls(t_date, amount, category, description)
            transactions.append(tx)

        return transactions


class JsonStorage(Storage):
    def __init__(self, filename: str = "data/budget.json"):
        self.filename = filename
        self._ensure_file()

    def _ensure_file(self):
        if not os.path.exists(self.filename):
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump([], f)

    def save(self, transaction: Transaction):
        with open(self.filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        data.append(
            {
                "date": transaction.date.isoformat(),
                "type": transaction.type,
                "amount": transaction.amount,
                "category": transaction.category,
                "description": transaction.description,
            }
        )

        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load(self):
        with open(self.filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        transactions = []

        for item in data:
            t_date = datetime.fromisoformat(item["date"]).date()
            t_type = item["type"]
            amount = item["amount"]
            category = item.get("category", "")
            description = item.get("description", "")

            tx_cls = TRANSACTION_CLASSES.get(t_type)
            if tx_cls is None:
                continue

            tx = tx_cls(t_date, amount, category, description)
            transactions.append(tx)

        return transactions
