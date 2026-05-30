"""A small desktop app to manage a personal balance sheet.

Run it with:

    python app.py

It lets you add assets and liabilities, see your totals and net worth update
live, and save/load the sheet as a JSON file. All the financial logic lives in
balance_sheet.py; this file only wires it to a Tkinter window.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from balance_sheet import (
    ASSET,
    ASSET_CATEGORIES,
    LIABILITY,
    LIABILITY_CATEGORIES,
    BalanceSheet,
)


def format_money(amount: float) -> str:
    """Format a number as money with thousands separators, e.g. 1,250.00."""
    return f"{amount:,.2f}"


class BalanceSheetApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Personal Balance Sheet")
        self.geometry("720x540")
        self.sheet = BalanceSheet()
        self.current_path: str | None = None

        self._build_input_form()
        self._build_table()
        self._build_summary()
        self._build_menu()
        self._refresh()

    # -- Layout ------------------------------------------------------------
    def _build_input_form(self) -> None:
        form = ttk.LabelFrame(self, text="Add an item")
        form.pack(fill="x", padx=10, pady=(10, 5))

        ttk.Label(form, text="Name").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.name_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.name_var, width=20).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form, text="Type").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.kind_var = tk.StringVar(value=ASSET)
        kind_box = ttk.Combobox(
            form,
            textvariable=self.kind_var,
            values=[ASSET, LIABILITY],
            state="readonly",
            width=10,
        )
        kind_box.grid(row=0, column=3, padx=5, pady=5)
        kind_box.bind("<<ComboboxSelected>>", lambda _e: self._update_category_choices())

        ttk.Label(form, text="Category").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.category_var = tk.StringVar()
        self.category_box = ttk.Combobox(form, textvariable=self.category_var, width=18)
        self.category_box.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form, text="Amount").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.amount_var = tk.StringVar()
        amount_entry = ttk.Entry(form, textvariable=self.amount_var, width=12)
        amount_entry.grid(row=1, column=3, padx=5, pady=5)
        amount_entry.bind("<Return>", lambda _e: self._on_add())

        ttk.Button(form, text="Add", command=self._on_add).grid(row=1, column=4, padx=5, pady=5)
        self._update_category_choices()

    def _build_table(self) -> None:
        wrapper = ttk.Frame(self)
        wrapper.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("type", "name", "category", "amount")
        self.tree = ttk.Treeview(wrapper, columns=columns, show="headings", selectmode="browse")
        headings = {"type": "Type", "name": "Name", "category": "Category", "amount": "Amount"}
        for col in columns:
            self.tree.heading(col, text=headings[col])
            anchor = "e" if col == "amount" else "w"
            self.tree.column(col, anchor=anchor, width=140)

        scrollbar = ttk.Scrollbar(wrapper, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        ttk.Button(self, text="Remove selected", command=self._on_remove).pack(pady=(0, 5))

    def _build_summary(self) -> None:
        summary = ttk.Frame(self)
        summary.pack(fill="x", padx=10, pady=(0, 10))

        self.assets_label = ttk.Label(summary, text="")
        self.assets_label.grid(row=0, column=0, padx=10, sticky="w")
        self.liabilities_label = ttk.Label(summary, text="")
        self.liabilities_label.grid(row=0, column=1, padx=10, sticky="w")
        self.net_worth_label = ttk.Label(summary, text="", font=("TkDefaultFont", 11, "bold"))
        self.net_worth_label.grid(row=0, column=2, padx=10, sticky="w")

    def _build_menu(self) -> None:
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New", command=self._on_new)
        file_menu.add_command(label="Open...", command=self._on_open)
        file_menu.add_command(label="Save as...", command=self._on_save)
        file_menu.add_separator()
        file_menu.add_command(label="Quit", command=self.destroy)
        menubar.add_cascade(label="File", menu=file_menu)
        self.config(menu=menubar)

    # -- Behaviour ---------------------------------------------------------
    def _update_category_choices(self) -> None:
        choices = ASSET_CATEGORIES if self.kind_var.get() == ASSET else LIABILITY_CATEGORIES
        self.category_box["values"] = choices
        if self.category_var.get() not in choices:
            self.category_var.set(choices[0])

    def _on_add(self) -> None:
        try:
            self.sheet.add_item(
                name=self.name_var.get(),
                category=self.category_var.get(),
                amount=self.amount_var.get(),
                kind=self.kind_var.get(),
            )
        except ValueError as error:
            messagebox.showerror("Invalid input", str(error))
            return
        self.name_var.set("")
        self.amount_var.set("")
        self._refresh()

    def _on_remove(self) -> None:
        selection = self.tree.selection()
        if not selection:
            messagebox.showinfo("Remove item", "Select a row to remove first.")
            return
        index = self.tree.index(selection[0])
        self.sheet.remove_item(index)
        self._refresh()

    def _on_new(self) -> None:
        if self.sheet.items and not messagebox.askyesno("New sheet", "Discard the current sheet?"):
            return
        self.sheet.clear()
        self.current_path = None
        self._refresh()

    def _on_open(self) -> None:
        path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if not path:
            return
        try:
            self.sheet = BalanceSheet.load(path)
        except (OSError, ValueError, KeyError) as error:
            messagebox.showerror("Could not open file", str(error))
            return
        self.current_path = path
        self._refresh()

    def _on_save(self) -> None:
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
        )
        if not path:
            return
        try:
            self.sheet.save(path)
        except OSError as error:
            messagebox.showerror("Could not save file", str(error))
            return
        self.current_path = path
        messagebox.showinfo("Saved", f"Balance sheet saved to:\n{path}")

    def _refresh(self) -> None:
        """Redraw the table and the summary line from the current sheet."""
        self.tree.delete(*self.tree.get_children())
        for item in self.sheet.items:
            self.tree.insert(
                "",
                "end",
                values=(item.kind, item.name, item.category, format_money(item.amount)),
            )

        self.assets_label.config(text=f"Total assets: {format_money(self.sheet.total_assets())}")
        self.liabilities_label.config(
            text=f"Total liabilities: {format_money(self.sheet.total_liabilities())}"
        )
        self.net_worth_label.config(text=f"Net worth: {format_money(self.sheet.net_worth())}")


if __name__ == "__main__":
    BalanceSheetApp().mainloop()
