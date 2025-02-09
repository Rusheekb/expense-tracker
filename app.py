from flask import Flask, render_template, jsonify, request, redirect
import json
import os
from datetime import datetime

app = Flask(__name__)

FILENAME = "expenses.json"
BUDGET_LIMIT = 500.0

def load_expenses():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as file:
            try:
                return json.load (file)
            except json.JSONDecodError:
                return []
    return []

def save_expenses(expenses):
    with open(FILENAME, "w") as file:
        json.dump(expenses, file, indent=4)

@app.route("/")
def index():
    expenses = load_expenses()
    total_spent = sum(exp["amount"] for exp in expenses)
    over_budget = total_spent > BUDGET_LIMIT
    return render_template("index.html", expenses = expenses, total_spent = total_spent, over_budget = over_budget, budget_limit = BUDGET_LIMIT)

@app.route("/expenses")
def get_expenses():
    expenses = load_expenses()
    return jsonify(expenses)

@app.route("/add", methods=["POST"])
def add_expense():
    name = request.form["name"]
    amount = float(request.form["amount"])
    category = request.form["category"]
    date = datetime.today().strftime('%Y-%m-%d')

    expenses = load_expenses()
    expenses.append({"name": name, "amount": amount, "category": category, "date": date})
    save_expenses(expenses)

    return redirect("/")

@app.route("/delete/<int:index>", methods = ["POST"])
def delete_expense(index):
    expenses = load_expenses()

    if 0 <= index < len(expenses):
        del expenses[index]
        save_expenses(expenses)
    return redirect("/")

@app.route("/chart-data")
def chart_data():
    expenses = load_expenses()

    category_totals = {}
    for exp in expenses:
        category_totals[exp["category"]] = category_totals.get(exp["category"], 0) + exp["amount"]
    return jsonify(category_totals)

if __name__ == '__main__':
    app.run(debug=True)