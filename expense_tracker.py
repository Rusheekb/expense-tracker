#expense_tracker
import json
import os

FILENAME = "expenses.json"

def save_expenses():
    with open(FILENAME, "w") as file:
        json.dump(expenses, file)

def load_expenses():
    global expenses
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as file:
            try:
                expenses = json.load(file)
            except json.JSONDecodeError:
                expenses = []

expenses = []
from datetime import datetime

def add_expense():
    name = input("Enter expense name: ")
    try:
        amount = float(input("Enter expense amount: "))
    except ValueError:
        print("Invalid input! Please enter a numerical value for amount.")
        return
        
    category = input("Enter expense category: ")
    date = datetime.today().strftime('%Y-%m-%d') 


    expense = {"name" : name, "amount" : amount, "category": category, "date": date}
    expenses.append(expense)
    save_expenses()
    print("Expense added successfully")

def view_expenses():
    if not expenses:
        print("No expenses recorded yet.\n")
        return
    
    print("\n--- Expense List ---")
    for index, expense in enumerate(expenses, start=1):
        print(f"{index}. {expense['date']} {expense['name']} - $ {expense['amount']} ({expense['category']})")
    print()
    
def expense_summary():
    if not expenses:
        print("No expenses recorded yet.\n")
        return

    summary = {}
    for expense in expenses:
        category = expense["category"]
        amount = expense["amount"]
        summary[category] = summary.get(category, 0) + amount
        
    print("\n--- Expense Summary ---")
    for category, total in summary.items():
        print(f"{category}: ${total:.2f}")
    print()

def monthly_expense_summary():
    month = input("Enter month (YYYY-MM): ")

    filtered_expenses = [e for e in expenses if e["date"].startswith(month)]

    if not filtered_expenses:
        print("No expenses found for this month.")
        return
    
    total = sum(e["amount"] for e in filtered_expenses)
    print(f"\n--- Expenses for {month} ---")
    for e in filtered_expenses:
        print(f"{e['date']} - {e['name']} - ${e['amount']} ({e['category']})")
    print(f"Total: ${total:.2f}\n")

def main():
    load_expenses()
    while True:
        print("\nExpense Tracker")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Expense Summary")
        print("4. Monthly Expense Summary")
        print("5. Exit")


        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            expense_summary()
        elif choice == "4":
            monthly_expense_summary()
        elif choice == "5":
            print("Goodbye")
            break
        else:
            print("Invalid choice. Please try again.\n")

if __name__ == '__main__':
    main()