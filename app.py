from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "expenses.db"
DEFAULT_CATEGORIES = [
    "Transporte",
    "Faculdade",
    "Academia",
    "Conta de Internet",
    "Consórcio",
    "Alimentação",
    "Moradia",
    "Saúde",
    "Lazer",
    "Outros",
]


def get_db_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    with get_db_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                expense_date TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def format_currency(value: float) -> str:
    return f"R$ {value:,.2f}"


def get_default_month() -> str:
    return datetime.now().strftime("%Y-%m")


def fetch_months() -> list[str]:
    with get_db_connection() as connection:
        rows = connection.execute(
            "SELECT DISTINCT strftime('%Y-%m', expense_date) AS month FROM expenses ORDER BY month DESC"
        ).fetchall()
    return [row["month"] for row in rows] if rows else [get_default_month()]


def build_month_summary(selected_month: str):
    with get_db_connection() as connection:
        expenses = connection.execute(
            """
            SELECT * FROM expenses
            WHERE strftime('%Y-%m', expense_date) = ?
            ORDER BY expense_date DESC, id DESC
            """,
            (selected_month,),
        ).fetchall()

        category_totals = connection.execute(
            """
            SELECT category, ROUND(SUM(amount), 2) AS total
            FROM expenses
            WHERE strftime('%Y-%m', expense_date) = ?
            GROUP BY category
            ORDER BY total DESC
            """,
            (selected_month,),
        ).fetchall()

        monthly_totals = connection.execute(
            """
            SELECT strftime('%Y-%m', expense_date) AS month, ROUND(SUM(amount), 2) AS total
            FROM expenses
            GROUP BY month
            ORDER BY month DESC
            """
        ).fetchall()

    total_amount = sum(float(item["amount"]) for item in expenses)
    biggest_category = None
    if category_totals:
        biggest_category = category_totals[0]["category"]
        biggest_total = float(category_totals[0]["total"])
    else:
        biggest_total = 0.0

    return {
        "expenses": expenses,
        "category_totals": [
            {"category": item["category"], "total": float(item["total"])} for item in category_totals
        ],
        "monthly_totals": [
            {"month": item["month"], "total": float(item["total"])} for item in monthly_totals
        ],
        "total_amount": total_amount,
        "biggest_category": biggest_category,
        "biggest_total": biggest_total,
    }


@app.route("/", methods=["GET", "POST"])
def index():
    selected_month = request.args.get("month") or get_default_month()

    if request.method == "POST":
        description = request.form["description"].strip()
        category = request.form["category"].strip()
        amount = float(request.form["amount"])
        expense_date = request.form["date"]

        if not description or not category or amount <= 0 or not expense_date:
            return redirect(url_for("index", month=selected_month))

        with get_db_connection() as connection:
            connection.execute(
                "INSERT INTO expenses (description, category, amount, expense_date) VALUES (?, ?, ?, ?)",
                (description, category, amount, expense_date),
            )

        return redirect(url_for("index", month=selected_month))

    months = fetch_months()
    if selected_month not in months:
        selected_month = months[0]

    summary = build_month_summary(selected_month)

    return render_template(
        "index.html",
        selected_month=selected_month,
        months=months,
        expenses=summary["expenses"],
        category_totals=summary["category_totals"],
        monthly_totals=summary["monthly_totals"],
        total_amount=summary["total_amount"],
        biggest_category=summary["biggest_category"],
        biggest_total=summary["biggest_total"],
        default_categories=DEFAULT_CATEGORIES,
        format_currency=format_currency,
    )


@app.route("/delete/<int:expense_id>", methods=["POST"])
def delete_expense(expense_id: int):
    selected_month = request.form.get("month") or get_default_month()

    with get_db_connection() as connection:
        connection.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))

    return redirect(url_for("index", month=selected_month))


if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)
