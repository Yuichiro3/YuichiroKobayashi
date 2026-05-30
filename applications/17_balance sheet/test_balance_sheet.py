"""Unit tests for the balance sheet core logic.

Run with:

    python -m unittest test_balance_sheet.py
"""

import tempfile
import unittest
from pathlib import Path

from balance_sheet import ASSET, LIABILITY, BalanceSheet


class BalanceSheetTests(unittest.TestCase):
    def setUp(self) -> None:
        self.sheet = BalanceSheet()

    def test_net_worth_is_assets_minus_liabilities(self) -> None:
        self.sheet.add_item("Savings", "Bank account", 5000, ASSET)
        self.sheet.add_item("Stocks", "Investments", 3000, ASSET)
        self.sheet.add_item("Credit card", "Credit card", 1200, LIABILITY)

        self.assertEqual(self.sheet.total_assets(), 8000)
        self.assertEqual(self.sheet.total_liabilities(), 1200)
        self.assertEqual(self.sheet.net_worth(), 6800)

    def test_net_worth_can_be_negative(self) -> None:
        self.sheet.add_item("Cash", "Cash", 100, ASSET)
        self.sheet.add_item("Student loan", "Student loan", 500, LIABILITY)
        self.assertEqual(self.sheet.net_worth(), -400)

    def test_totals_by_category(self) -> None:
        self.sheet.add_item("Checking", "Bank account", 1000, ASSET)
        self.sheet.add_item("Savings", "Bank account", 2000, ASSET)
        self.sheet.add_item("ETF", "Investments", 500, ASSET)
        totals = self.sheet.totals_by_category(ASSET)
        self.assertEqual(totals, {"Bank account": 3000, "Investments": 500})

    def test_add_item_strips_whitespace(self) -> None:
        item = self.sheet.add_item("  Wallet  ", "  Cash  ", 50, ASSET)
        self.assertEqual(item.name, "Wallet")
        self.assertEqual(item.category, "Cash")

    def test_add_item_rejects_bad_input(self) -> None:
        with self.assertRaises(ValueError):
            self.sheet.add_item("", "Cash", 10, ASSET)
        with self.assertRaises(ValueError):
            self.sheet.add_item("Wallet", "", 10, ASSET)
        with self.assertRaises(ValueError):
            self.sheet.add_item("Wallet", "Cash", -10, ASSET)
        with self.assertRaises(ValueError):
            self.sheet.add_item("Wallet", "Cash", "not a number", ASSET)
        with self.assertRaises(ValueError):
            self.sheet.add_item("Wallet", "Cash", 10, "something else")

    def test_remove_item(self) -> None:
        self.sheet.add_item("Cash", "Cash", 100, ASSET)
        self.sheet.add_item("Loan", "Car loan", 200, LIABILITY)
        removed = self.sheet.remove_item(0)
        self.assertEqual(removed.name, "Cash")
        self.assertEqual(len(self.sheet.items), 1)
        with self.assertRaises(IndexError):
            self.sheet.remove_item(5)

    def test_items_property_is_a_copy(self) -> None:
        self.sheet.add_item("Cash", "Cash", 100, ASSET)
        self.sheet.items.clear()
        self.assertEqual(len(self.sheet.items), 1)

    def test_save_and_load_round_trip(self) -> None:
        self.sheet.add_item("Savings", "Bank account", 5000, ASSET)
        self.sheet.add_item("Credit card", "Credit card", 1200, LIABILITY)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sheet.json"
            self.sheet.save(path)
            loaded = BalanceSheet.load(path)
        self.assertEqual(loaded.net_worth(), self.sheet.net_worth())
        self.assertEqual([i.name for i in loaded.items], ["Savings", "Credit card"])


if __name__ == "__main__":
    unittest.main()
