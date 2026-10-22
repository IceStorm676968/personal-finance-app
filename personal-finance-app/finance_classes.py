# -*- coding: utf-8 -*-
"""Модуль классов и бизнес-логики учета финансов."""

import csv
from enum import Enum
from typing import List, Dict


class TransactionType(Enum):
    """Типы финансовых операций."""

    INCOME = "Доход"
    EXPENSE = "Расход"


class Category:
    """Класс категории доходов/расходов."""

    def __init__(self, name: str, cat_type: TransactionType):
        self.name = name
        self.type = cat_type


class Transaction:
    """Класс отдельной финансовой операции."""

    def __init__(
        self,
        amount: float,
        category: Category,
        date: str,
        description: str = "",
    ):
        self.amount = amount
        self.category = category
        self.date = date
        self.description = description


class FinanceManager:
    """Класс для управления операциями и сохранения в CSV."""

    def __init__(self, filename: str = "transactions.csv"):
        self.filename = filename
        self.transactions: List[Transaction] = []
        self.categories: List[Category] = [
            Category("Зарплата", TransactionType.INCOME),
            Category("Инвестиции", TransactionType.INCOME),
            Category("Продукты", TransactionType.EXPENSE),
            Category("Транспорт", TransactionType.EXPENSE),
            Category("Развлечения", TransactionType.EXPENSE),
        ]
        self.load_from_file()

    def add_transaction(self, transaction: Transaction):
        """Добавление операции в список и файл."""
        self.transactions.append(transaction)
        self.save_to_file()

    def delete_transaction(self, index: int):
        """Удаление операции по индексу."""
        if 0 <= index < len(self.transactions):
            del self.transactions[index]
            self.save_to_file()

    def get_balance(self) -> float:
        """Расчет общего баланса."""
        income = sum(
            t.amount
            for t in self.transactions
            if t.category.type == TransactionType.INCOME
        )
        expenses = sum(
            t.amount
            for t in self.transactions
            if t.category.type == TransactionType.EXPENSE
        )
        return income - expenses

    def get_category_summary(self) -> Dict[str, float]:
        """Расчет итогов по категориям."""
        summary = {}
        for transaction in self.transactions:
            cat_name = transaction.category.name
            if cat_name not in summary:
                summary[cat_name] = 0.0
            if transaction.category.type == TransactionType.INCOME:
                summary[cat_name] += transaction.amount
            else:
                summary[cat_name] -= transaction.amount
        return summary

    def save_to_file(self):
        """Сохранение всех операций в CSV."""
        with open(self.filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(
                ["Amount", "Category", "Type", "Date", "Description"]
            )
            for t in self.transactions:
                writer.writerow(
                    [
                        t.amount,
                        t.category.name,
                        t.category.type.value,
                        t.date,
                        t.description,
                    ]
                )

    def load_from_file(self):
        """Загрузка данных из CSV."""
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    category = next(
                        (
                            cat
                            for cat in self.categories
                            if cat.name == row["Category"]
                        ),
                        None,
                    )
                    if category:
                        transaction = Transaction(
                            amount=float(row["Amount"]),
                            category=category,
                            date=row["Date"],
                            description=row["Description"],
                        )
                        self.transactions.append(transaction)
        except (FileNotFoundError, KeyError, ValueError):
            self.transactions = []