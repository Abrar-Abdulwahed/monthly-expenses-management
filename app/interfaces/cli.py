from datetime import datetime, date
from app.core.budget import BudgetManager


def input_date(prompt):
    value = input(prompt).strip()
    if not value:
        return date.today()
    return datetime.strptime(value, "%Y-%m-%d").date()


def run_cli(storage) -> None:
    manager = BudgetManager(storage)

    while True:
        print("\n=== Personal Expenses Manager ===")
        print("1) Add income")
        print("2) Add expense")
        print("3) Export monthly summary to Excel")
        print("4) Exit")

        choice = input("Choose: ").strip()

        if choice == "1":
            amt = float(input("Amount: "))
            cat = input("Category (e.g. Salary): ").strip()
            desc = input("Description (optional): ").strip()
            t_date = input_date("Date (YYYY-MM-DD, empty for today): ")
            manager.add_income(amt, cat, desc, t_date)

        elif choice == "2":
            amt = float(input("Amount: "))
            cat = input("Category (e.g. Food, Rent): ").strip()
            desc = input("Description (optional): ").strip()
            t_date = input_date("Date (YYYY-MM-DD, empty for today): ")
            manager.add_expense(amt, cat, desc, t_date)


        elif choice == "3":
            year = int(input("Year (e.g. 2025): "))
            month = int(input("Month (1-12): "))
            filename = f"data/summary_cli_{year}_{month:02d}.xlsx"
            manager.export_monthly_summary_to_excel(year, month, filename)
            print(f"Summary exported to {filename}.")

        elif choice == "4":
            break
