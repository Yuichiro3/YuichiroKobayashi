"""Core logic for a personal balance sheet manager.

A personal balance sheet lists what you own (assets) and what you owe
(liabilities). The difference between the two is your net worth:

    Net worth = Total assets - Total liabilities

This module keeps the data model and persistence independent of any user
interface so the same logic can be reused from the GUI (app.py), a CLI, or
the unit tests (test_balance_sheet.py).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List

# The two sides of a balance sheet.
ASSET = "asset"
LIABILITY = "liability"

# Suggested categories. They are only hints for the user interface; the logic
# accepts any non-empty category string.
ASSET_CATEGORIES = ["Cash", "Bank account", "Investments", "Real estate", "Vehicle", "Other"]
LIABILITY_CATEGORIES = ["Mortgage", "Student loan", "Car loan", "Credit card", "Other"]


@dataclass
class Item:
    """A single line on the balance sheet (one asset or one liability)."""

    name: str
    category: str
    amount: float
    kind: str  # ASSET or LIABILITY


class BalanceSheet:
    """An ordered collection of assets and liabilities with summary helpers."""

    def __init__(self) -> None:
        self._items: List[Item] = []

    # -- Reading -----------------------------------------------------------
    @property
    def items(self) -> List[Item]:
        """All items in insertion order (a copy, so callers can't mutate it)."""
        return list(self._items)

    @property
    def assets(self) -> List[Item]:
        return [item for item in self._items if item.kind == ASSET]

    @property
    def liabilities(self) -> List[Item]:
        return [item for item in self._items if item.kind == LIABILITY]

    def total_assets(self) -> float:
        return sum(item.amount for item in self.assets)

    def total_liabilities(self) -> float:
        return sum(item.amount for item in self.liabilities)

    def net_worth(self) -> float:
        return self.total_assets() - self.total_liabilities()

    def totals_by_category(self, kind: str) -> dict:
        """Sum the amounts grouped by category for one side of the sheet."""
        totals: dict = {}
        for item in self._items:
            if item.kind == kind:
                totals[item.category] = totals.get(item.category, 0.0) + item.amount
        return totals

    # -- Writing -----------------------------------------------------------
    def add_item(self, name: str, category: str, amount: float, kind: str) -> Item:
        """Validate and append a new item, returning it."""
        name = (name or "").strip()
        category = (category or "").strip()
        if not name:
            raise ValueError("Item name must not be empty.")
        if not category:
            raise ValueError("Category must not be empty.")
        if kind not in (ASSET, LIABILITY):
            raise ValueError(f"kind must be '{ASSET}' or '{LIABILITY}', got {kind!r}.")
        try:
            amount = float(amount)
        except (TypeError, ValueError):
            raise ValueError(f"Amount must be a number, got {amount!r}.")
        if amount < 0:
            raise ValueError("Amount must not be negative.")

        item = Item(name=name, category=category, amount=amount, kind=kind)
        self._items.append(item)
        return item

    def remove_item(self, index: int) -> Item:
        """Remove and return the item at the given position."""
        if not 0 <= index < len(self._items):
            raise IndexError(f"No item at index {index}.")
        return self._items.pop(index)

    def clear(self) -> None:
        self._items.clear()

    # -- Persistence -------------------------------------------------------
    def to_dict(self) -> dict:
        return {"items": [asdict(item) for item in self._items]}

    @classmethod
    def from_dict(cls, data: dict) -> "BalanceSheet":
        sheet = cls()
        for raw in data.get("items", []):
            sheet.add_item(
                name=raw["name"],
                category=raw["category"],
                amount=raw["amount"],
                kind=raw["kind"],
            )
        return sheet

    def save(self, path: str | Path) -> None:
        Path(path).write_text(json.dumps(self.to_dict(), indent=2), encoding="utf-8")

    @classmethod
    def load(cls, path: str | Path) -> "BalanceSheet":
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls.from_dict(data)
