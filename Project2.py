import json
from pathlib import Path
from datetime import datetime, date

FILE = Path("data3.json")


def load_data():
    if FILE.exists():
        data = json.loads(FILE.read_text(encoding="utf-8"))
        # Ensure required keys exist
        data.setdefault("expenses", [])
        data.setdefault("budgets", [])
        return data

    # Default structure if file does not exist
    return {"expenses": [], "budgets": []}


def save_data(data):
    FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")


# Load file
data = load_data()
Expense_data = data["expenses"]
budget_data = data["budgets"]


def add_expense():
    user_category = input("Enter category name: ").strip().lower()
    user_cost = input("Enter cost: ").strip()
    user_date = input("Enter (dd/mm/yy): ").strip()

    # validate cost (floats/ints, positive)
    try:
        user_cost = float(user_cost)
        if user_cost <= 0:
            raise ValueError
    except ValueError:
        raise ValueError("Cost must be a positive number")

    # Validate category (letters only)
    if not user_category.isalpha():
        raise ValueError("Category must contain letters only (no numbers, spaces, or symbols)")

    # validate date format (dd/mm/yy)
    try:
        parsed_date = datetime.strptime(user_date, "%d/%m/%y").date()
    except ValueError:
        raise ValueError("Date must be in dd/mm/yy format")

    # day range check (1-30) (note: this is an unusual rule, but kept as you wrote it)
    if parsed_date.day > 30:
        raise ValueError("Day (dd) must be between 1 and 30")

    # not in the future
    if parsed_date > date.today():
        raise ValueError("Date cannot be in the future")

    expense = {"category": user_category, "cost": user_cost, "date": user_date}
    Expense_data.append(expense)
    save_data(data)
    return Expense_data


def delete():
    user_expense = input("Enter delete all or delete category: ").strip().lower()

    if user_expense == "delete all":
        Expense_data.clear()
        save_data(data)

    elif user_expense == "delete category":
        cat_to_delete = input("Enter category to be deleted: ").strip().lower()

        # keep only items NOT matching the category
        Expense_data[:] = [
            item for item in Expense_data
            if item["category"].strip().lower() != cat_to_delete
        ]
        save_data(data)

    else:
        print("Invalid choice. Type exactly: delete all OR delete category")

    return Expense_data


def view():
    # show expenses and budgets data
    return Expense_data, budget_data


def category_totals():
    total = 0.0
    for item in Expense_data:
        total += float(item["cost"])
    return f"total cost: {total} and the full data list : {Expense_data}"


def add_budget():
    user_category2 = input("Enter category: ").strip().lower()

    # Ensure category exists in expenses
    category_found = False
    for e in Expense_data:
        if e["category"].strip().lower() == user_category2:
            category_found = True
            break

    if not category_found:
        raise ValueError("Category does not exist in expenses. Add an expense first.")

    # Prevent duplicate budgets
    for x in budget_data:
        if x["category"].strip().lower() == user_category2:
            raise ValueError("Budget already exists for this category")

    user_limit = input("Enter budget limit: ").strip()

    try:
        limit = float(user_limit)
        if limit <= 0:
            raise ValueError
    except ValueError:
        raise ValueError("Budget must be a positive number")

    budget = {"category": user_category2, "limit": limit}
    budget_data.append(budget)
    save_data(data)
    return budget_data


def monthly_totals():
    totals = {}

    for i in Expense_data:
        d = datetime.strptime(i["date"], "%d/%m/%y")
        key = f"{d.year}-{d.month:02d}"  # 2025-01, 2025-12 (cleaner)

        totals[key] = totals.get(key, 0) + float(i["cost"])

    return totals


def compare_spending_budget():
    total_budget = 0.0
    total_spending = 0.0

    for i in Expense_data:
        total_spending += float(i["cost"])

    for x in budget_data:
        total_budget += float(x["limit"])

    remaining = total_budget - total_spending

    return {"spent": total_spending, "budget": total_budget, "remaining": remaining}


def final():
    while True:
        user = input(
            "Enter add expense / delete / view / "
            "total category / monthly totals / add budget / "
            "compare budget and spending / quit: "
        ).strip().lower()

        if user == "add expense":
            add_expense()

        elif user == "delete":
            delete()

        elif user == "view":
            print(view())

        elif user == "total category":
            print(category_totals())

        elif user == "monthly totals":
            print(monthly_totals())

        elif user == "add budget":
            add_budget()

        elif user == "compare budget and spending":
            print(compare_spending_budget())

        elif user == "quit":
            print("End programme")
            break

        else:
            print("wrong input, try again")


if __name__ == "__main__":
    final()
