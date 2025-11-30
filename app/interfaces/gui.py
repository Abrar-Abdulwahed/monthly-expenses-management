import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
from app.core.budget import BudgetManager


class BudgetApp(tk.Tk):
    def __init__(self, manager: BudgetManager):
        super().__init__()
        self.manager = manager

        self.title("Personal Expenses Manager")
        self.geometry("900x500")
        self.minsize(800, 450)

        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("TFrame", background="#f5f7fb")
        style.configure("Card.TFrame", background="#ffffff", relief="groove", borderwidth=1)
        style.configure("TLabel", background="#f5f7fb", font=("Segoe UI", 10))
        style.configure("Card.TLabel", background="#ffffff", font=("Segoe UI", 10))
        style.configure("Title.TLabel", background="#f5f7fb", font=("Segoe UI", 14, "bold"))
        style.configure("CardTitle.TLabel", background="#ffffff", font=("Segoe UI", 12, "bold"))
        style.configure("TButton", font=("Segoe UI", 10))

        container = ttk.Frame(self, padding=16)
        container.pack(fill="both", expand=True)

        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)
        container.rowconfigure(0, weight=1)

        self._build_form_panel(container)
        self._build_summary_panel(container)

    def _build_form_panel(self, parent: ttk.Frame):
        frame = ttk.Frame(parent, style="Card.TFrame", padding=16)
        frame.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        title = ttk.Label(frame, text="Add Transaction", style="CardTitle.TLabel")
        title.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))

        self.tx_type_var = tk.StringVar(value="income")
        income_rb = ttk.Radiobutton(frame, text="Income", value="income", variable=self.tx_type_var)
        expense_rb = ttk.Radiobutton(frame, text="Expense", value="expense", variable=self.tx_type_var)
        income_rb.grid(row=1, column=0, sticky="w")
        expense_rb.grid(row=1, column=1, sticky="w")

        ttk.Label(frame, text="Amount", style="Card.TLabel").grid(row=2, column=0, sticky="w", pady=(12, 2))
        self.amount_var = tk.StringVar()
        amount_entry = ttk.Entry(frame, textvariable=self.amount_var)
        amount_entry.grid(row=2, column=1, sticky="ew", pady=(12, 2))

        ttk.Label(frame, text="Category", style="Card.TLabel").grid(row=4, column=0, sticky="w", pady=(8, 2))
        self.category_var = tk.StringVar()
        category_entry = ttk.Entry(frame, textvariable=self.category_var)
        category_entry.grid(row=4, column=1, sticky="ew", pady=(8, 2))

        ttk.Label(frame, text="Description", style="Card.TLabel").grid(row=5, column=0, sticky="w", pady=(8, 2))
        self.description_var = tk.StringVar()
        description_entry = ttk.Entry(frame, textvariable=self.description_var)
        description_entry.grid(row=5, column=1, sticky="ew", pady=(8, 2))

        ttk.Label(frame, text="Date (YYYY-MM-DD)", style="Card.TLabel").grid(
            row=6, column=0, sticky="w", pady=(8, 2)
        )
        self.date_var = tk.StringVar()
        date_entry = ttk.Entry(frame, textvariable=self.date_var)
        date_entry.grid(row=6, column=1, sticky="ew", pady=(8, 2))

        add_btn = ttk.Button(frame, text="Save Transaction", command=self._handle_add_transaction)
        add_btn.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(16, 0))

        frame.columnconfigure(0, weight=0)
        frame.columnconfigure(1, weight=1)

    def _build_summary_panel(self, parent: ttk.Frame):
        frame = ttk.Frame(parent, style="Card.TFrame", padding=16)
        frame.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        title = ttk.Label(frame, text="Monthly Summary", style="CardTitle.TLabel")
        title.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))

        ttk.Label(frame, text="Year", style="Card.TLabel").grid(row=1, column=0, sticky="w", pady=(4, 2))
        self.year_var = tk.StringVar(value=str(date.today().year))
        year_entry = ttk.Entry(frame, textvariable=self.year_var, width=10)
        year_entry.grid(row=1, column=1, sticky="w", pady=(4, 2))

        ttk.Label(frame, text="Month (1-12)", style="Card.TLabel").grid(row=2, column=0, sticky="w", pady=(4, 2))
        self.month_var = tk.StringVar(value=str(date.today().month))
        month_entry = ttk.Entry(frame, textvariable=self.month_var, width=10)
        month_entry.grid(row=2, column=1, sticky="w", pady=(4, 2))

        refresh_btn = ttk.Button(frame, text="Show Summary", command=self._handle_show_summary)
        refresh_btn.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(12, 4))

        export_btn = ttk.Button(frame, text="Export to Excel", command=self._handle_export_summary)
        export_btn.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(4, 8))

        self.income_label = ttk.Label(frame, text="Total income: 0.0", style="Card.TLabel")
        self.expense_label = ttk.Label(frame, text="Total expense: 0.0", style="Card.TLabel")
        self.balance_label = ttk.Label(frame, text="Balance: 0.0", style="Card.TLabel")

        self.income_label.grid(row=5, column=0, columnspan=2, sticky="w", pady=(8, 2))
        self.expense_label.grid(row=6, column=0, columnspan=2, sticky="w", pady=(2, 2))
        self.balance_label.grid(row=7, column=0, columnspan=2, sticky="w", pady=(2, 8))


        ttk.Label(frame, text="Expenses by category:", style="Card.TLabel").grid(
            row=7, column=0, columnspan=2, sticky="w", pady=(4, 2)
        )

        self.category_tree = ttk.Treeview(
            frame,
            columns=("category", "amount"),
            show="headings",
            height=8,
        )
        self.category_tree.heading("category", text="Category")
        self.category_tree.heading("amount", text="Amount")
        self.category_tree.column("category", anchor="w", width=150)
        self.category_tree.column("amount", anchor="e", width=100)
        self.category_tree.grid(row=8, column=0, columnspan=2, sticky="nsew", pady=(4, 0))

        frame.rowconfigure(8, weight=1)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

    def _parse_date_or_today(self, value: str) -> date:
        value = value.strip()
        if not value:
            return date.today()
        return datetime.strptime(value, "%Y-%m-%d").date()

    def _handle_add_transaction(self):
        try:
            amount = float(self.amount_var.get())
        except ValueError:
            messagebox.showerror("Invalid input", "Amount must be a number.")
            return

        category = self.category_var.get().strip()
        description = self.description_var.get().strip()


        if not category:
            messagebox.showerror("Invalid input", "Category is required.")
            return

        try:
            t_date = self._parse_date_or_today(self.date_var.get())
        except ValueError:
            messagebox.showerror("Invalid date", "Date must be in format YYYY-MM-DD.")
            return

        tx_type = self.tx_type_var.get()

        if tx_type == "income":
            self.manager.add_income(amount, category, description, t_date)
        else:
            self.manager.add_expense(amount, category, description, t_date)

        messagebox.showinfo("Success", "Transaction saved.")
        self.amount_var.set("")
        self.category_var.set("")
        self.description_var.set("")
        self.date_var.set("")

    def _handle_show_summary(self):
        try:
            year = int(self.year_var.get())
            month = int(self.month_var.get())
        except ValueError:
            messagebox.showerror("Invalid input", "Year and month must be numbers.")
            return

        if month < 1 or month > 12:
            messagebox.showerror("Invalid month", "Month must be between 1 and 12.")
            return

        summary = self.manager.get_monthly_summary(year, month)

        self.income_label.config(text=f"Total income: {summary['total_income']}")
        self.expense_label.config(text=f"Total expense: {summary['total_expense']}")
        self.balance_label.config(text=f"Balance: {summary['balance']}")

        for item in self.category_tree.get_children():
            self.category_tree.delete(item)

        for cat, value in summary["by_category"].items():
            self.category_tree.insert("", "end", values=(cat, value))

    def _handle_export_summary(self):
        try:
            year = int(self.year_var.get())
            month = int(self.month_var.get())
        except ValueError:
            messagebox.showerror("Invalid input", "Year and month must be numbers.")
            return

        if month < 1 or month > 12:
            messagebox.showerror("Invalid month", "Month must be between 1 and 12.")
            return

        filename = f"data/summary_{year}_{month:02d}.xlsx"
        self.manager.export_monthly_summary_to_excel(year, month, filename)
        messagebox.showinfo("Export", f"Summary exported to {filename}.")



def run_gui(storage):
    manager = BudgetManager(storage)
    app = BudgetApp(manager)
    app.mainloop()


if __name__ == "__main__":
    run_gui()
