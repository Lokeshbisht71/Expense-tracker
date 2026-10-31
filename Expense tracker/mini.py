import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date


class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("1000x650")
        self.root.minsize(760, 520)
        self.root.configure(bg="#F1F5F9")

        # Temporary storage: no database
        self.expenses = []
        self.next_id = 1

        self.date_var = tk.StringVar(value=date.today().isoformat())
        self.category_var = tk.StringVar(value="Food")
        self.amount_var = tk.StringVar()
        self.description_var = tk.StringVar()
        self.search_var = tk.StringVar()
        self.filter_var = tk.StringVar(value="All")

        self.setup_style()
        self.create_header()
        self.create_dashboard()
        self.create_form()
        self.create_search_bar()
        self.create_table()
        self.create_footer()
        self.refresh_table()

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background="white",
            foreground="#1E293B",
            fieldbackground="white",
            rowheight=30,
            font=("Segoe UI", 10)
        )
        style.configure(
            "Treeview.Heading",
            background="#DBEAFE",
            foreground="#1E3A8A",
            font=("Segoe UI", 10, "bold")
        )
        style.map(
            "Treeview",
            background=[("selected", "#BFDBFE")],
            foreground=[("selected", "#1E3A8A")]
        )

    def create_header(self):
        header = tk.Frame(self.root, bg="#1E3A8A", height=85)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header, text="EXPENSE TRACKER",
            bg="#1E3A8A", fg="white",
            font=("Segoe UI", 22, "bold")
        ).pack(anchor="w", padx=24, pady=(13, 0))

        tk.Label(
            header, text="Track your daily spending easily",
            bg="#1E3A8A", fg="#DBEAFE",
            font=("Segoe UI", 10)
        ).pack(anchor="w", padx=26)

    def create_dashboard(self):
        panel = tk.Frame(self.root, bg="#F1F5F9")
        panel.pack(fill="x", padx=20, pady=12)

        self.total_label = self.create_card(
            panel, "Total Expenses", "#2563EB"
        )
        self.count_label = self.create_card(
            panel, "Transactions", "#7C3AED"
        )
        self.average_label = self.create_card(
            panel, "Average Expense", "#059669"
        )

    def create_card(self, parent, title, color):
        card = tk.Frame(
            parent, bg="white",
            highlightbackground="#E2E8F0",
            highlightthickness=1
        )
        card.pack(side="left", fill="x", expand=True, padx=5)

        tk.Label(
            card, text=title, bg="white",
            fg="#64748B", font=("Segoe UI", 10)
        ).pack(pady=(10, 2))

        value = tk.Label(
            card, text="₹0.00", bg="white",
            fg=color, font=("Segoe UI", 18, "bold")
        )
        value.pack(pady=(0, 10))
        return value

    def create_form(self):
        form = tk.LabelFrame(
            self.root, text=" Add New Expense ",
            bg="white", fg="#1E3A8A",
            font=("Segoe UI", 10, "bold"),
            padx=12, pady=10
        )
        form.pack(fill="x", padx=25, pady=4)

        for col in range(4):
            form.columnconfigure(col, weight=1)

        fields = [
            ("Date (YYYY-MM-DD)", self.date_var, 0),
            ("Category", self.category_var, 1),
            ("Amount (₹)", self.amount_var, 2),
            ("Description", self.description_var, 3)
        ]

        for label, variable, col in fields:
            tk.Label(
                form, text=label, bg="white",
                fg="#334155", font=("Segoe UI", 9)
            ).grid(row=0, column=col, sticky="w",
                   padx=5, pady=(0, 4))

            if label == "Category":
                widget = ttk.Combobox(
                    form, textvariable=variable,
                    values=[
                        "Food", "Transport", "Shopping",
                        "Education", "Bills", "Health",
                        "Entertainment", "Other"
                    ],
                    state="readonly"
                )
            else:
                widget = tk.Entry(
                    form, textvariable=variable,
                    font=("Segoe UI", 10),
                    relief="solid", bd=1
                )

            widget.grid(
                row=1, column=col, sticky="ew",
                padx=5, ipady=5
            )

        tk.Button(
            form, text="Add Expense",
            command=self.add_expense,
            bg="#2563EB", fg="white",
            activebackground="#1D4ED8",
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat", cursor="hand2",
            padx=16, pady=7
        ).grid(
            row=2, column=0, columnspan=4,
            sticky="w", padx=5, pady=(12, 0)
        )

    def create_search_bar(self):
        bar = tk.Frame(self.root, bg="#F1F5F9")
        bar.pack(fill="x", padx=25, pady=(10, 4))

        tk.Label(
            bar, text="Search:",
            bg="#F1F5F9", fg="#334155",
            font=("Segoe UI", 10, "bold")
        ).pack(side="left", padx=(0, 7))

        search_entry = tk.Entry(
            bar, textvariable=self.search_var,
            font=("Segoe UI", 10), width=23
        )
        search_entry.pack(side="left", ipady=4)
        search_entry.bind(
            "<KeyRelease>", lambda event: self.refresh_table()
        )

        tk.Label(
            bar, text="Category:",
            bg="#F1F5F9", fg="#334155",
            font=("Segoe UI", 10, "bold")
        ).pack(side="left", padx=(15, 7))

        filter_box = ttk.Combobox(
            bar, textvariable=self.filter_var,
            values=[
                "All", "Food", "Transport", "Shopping",
                "Education", "Bills", "Health",
                "Entertainment", "Other"
            ],
            state="readonly", width=16
        )
        filter_box.pack(side="left")
        filter_box.bind(
            "<<ComboboxSelected>>",
            lambda event: self.refresh_table()
        )

        tk.Button(
            bar, text="Delete Selected",
            command=self.delete_expense,
            bg="#DC2626", fg="white",
            activebackground="#B91C1C",
            activeforeground="white",
            relief="flat", cursor="hand2",
            font=("Segoe UI", 9, "bold"),
            padx=10, pady=5
        ).pack(side="right")

    def create_table(self):
        container = tk.Frame(self.root, bg="white")
        container.pack(
            fill="both", expand=True, padx=25, pady=7
        )

        columns = (
            "id", "date", "category", "amount", "description"
        )
        self.table = ttk.Treeview(
            container, columns=columns,
            show="headings", selectmode="browse"
        )

        headings = {
            "id": ("ID", 45),
            "date": ("Date", 120),
            "category": ("Category", 135),
            "amount": ("Amount (₹)", 120),
            "description": ("Description", 300)
        }

        for col, (heading, width) in headings.items():
            self.table.heading(col, text=heading)
            self.table.column(
                col, width=width, minwidth=45, anchor="w"
            )

        scrollbar = ttk.Scrollbar(
            container, orient="vertical",
            command=self.table.yview
        )
        self.table.configure(yscrollcommand=scrollbar.set)

        self.table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_footer(self):
        self.footer = tk.Label(
            self.root, text="Ready",
            bg="#E2E8F0", fg="#475569",
            font=("Segoe UI", 9), anchor="w", padx=15
        )
        self.footer.pack(fill="x", side="bottom")

    def add_expense(self):
        expense_date = self.date_var.get().strip()
        category = self.category_var.get()
        amount_text = self.amount_var.get().strip()
        description = self.description_var.get().strip()

        if not amount_text:
            messagebox.showwarning(
                "Missing Amount", "Please enter an expense amount."
            )
            return

        try:
            date.fromisoformat(expense_date)
        except ValueError:
            messagebox.showerror(
                "Invalid Date", "Use YYYY-MM-DD date format."
            )
            return

        try:
            amount = float(amount_text)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Invalid Amount",
                "Enter a valid amount greater than zero."
            )
            return

        expense = {
            "id": self.next_id,
            "date": expense_date,
            "category": category,
            "amount": amount,
            "description": description
        }

        self.expenses.append(expense)
        self.next_id += 1

        self.amount_var.set("")
        self.description_var.set("")
        self.date_var.set(date.today().isoformat())

        self.refresh_table()
        self.footer.config(text="Expense added successfully.")

    def delete_expense(self):
        selection = self.table.selection()

        if not selection:
            messagebox.showwarning(
                "Select Expense", "Select an expense row first."
            )
            return

        expense_id = int(selection[0])

        if not messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this expense?"
        ):
            return

        self.expenses = [
            item for item in self.expenses
            if item["id"] != expense_id
        ]

        self.refresh_table()
        self.footer.config(text="Expense deleted successfully.")

    def refresh_table(self):
        for item in self.table.get_children():
            self.table.delete(item)

        query = self.search_var.get().strip().lower()
        category_filter = self.filter_var.get()

        visible = [
            item for item in self.expenses
            if (
                query in item["category"].lower()
                or query in item["description"].lower()
            )
            and (
                category_filter == "All"
                or item["category"] == category_filter
            )
        ]

        for item in visible:
            self.table.insert(
                "", "end", iid=str(item["id"]),
                values=(
                    item["id"], item["date"],
                    item["category"],
                    f'{item["amount"]:,.2f}',
                    item["description"]
                )
            )

        self.update_dashboard()

        self.footer.config(
            text=f"Showing {len(visible)} of "
                 f"{len(self.expenses)} expenses"
        )

    def update_dashboard(self):
        total = sum(item["amount"] for item in self.expenses)
        count = len(self.expenses)
        average = total / count if count else 0

        self.total_label.config(text=f"₹{total:,.2f}")
        self.count_label.config(text=str(count))
        self.average_label.config(text=f"₹{average:,.2f}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
