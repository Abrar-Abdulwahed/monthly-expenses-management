from datetime import date
from typing import Type
from openpyxl import Workbook

from app.core.transactions import Transaction, IncomeTransaction, ExpenseTransaction


class BudgetManager:
    def __init__(self, storage):
        self._storage = storage

    def _add_transaction(
        self,
        tnx_cls: Type[Transaction],
        amount: float,
        category: str,
        description: str = "",
        t_date: date | None = None,
    ):
        if t_date is None:
            t_date = date.today()
        tnx = tnx_cls(t_date, amount, category, description)
        self._storage.save(tnx)

    def add_income(self, amount, category, description="", t_date: date | None = None):
        self._add_transaction(IncomeTransaction, amount, category, description, t_date)

    def add_expense(self, amount, category, description="", t_date: date | None = None):
        self._add_transaction(ExpenseTransaction, amount, category, description, t_date)

    def get_monthly_summary(self, year, month):
        transactions = self._storage.load()

        summary = {
            "total_income": 0.0,
            "total_expense": 0.0,
            "by_category": {},
        }

        for tnx in transactions:
            if tnx.date.year == year and tnx.date.month == month:
                tnx.apply_to_summary(summary)

        return {
            "total_income": summary["total_income"],
            "total_expense": summary["total_expense"],
            "balance": summary["total_income"] - summary["total_expense"],
            "by_category": summary["by_category"],
        }

    def export_monthly_summary_to_excel(self, year: int, month: int, filename: str = "summary.xlsx") -> None:
        summary = self.get_monthly_summary(year, month)
        wb = Workbook()
        ws = wb.active
        ws.title = f"{year}-{month:02d}"
        ws.append(["Metric", "Value"])
        ws.append(["Total income", summary["total_income"]])
        ws.append(["Total expense", summary["total_expense"]])
        ws.append(["Balance", summary["balance"]])
        ws.append([])
        ws.append(["Category", "Amount"])
        for cat, value in summary["by_category"].items():
            ws.append([cat, value])
        wb.save(filename)
