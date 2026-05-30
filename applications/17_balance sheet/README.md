# Purpose:
- A small personal app to manage a personal balance sheet.
- Track assets (what you own) and liabilities (what you owe), and see your net worth update live.

  Net worth = Total assets - Total liabilities

# Tool information
- Language: Python (standard library only)
- UI api: Tkinter
- Data format: JSON (save / open your sheet from the File menu)

# Files
- `balance_sheet.py` - core logic (data model, totals, net worth, save/load). No UI dependency.
- `app.py` - the Tkinter desktop app.
- `test_balance_sheet.py` - unit tests for the core logic.

# How to run
- App: `python app.py`
- Tests: `python -m unittest test_balance_sheet.py`

# Note
- The logic is separated from the UI so the same `BalanceSheet` class can be reused from a GUI, a CLI, or tests.
