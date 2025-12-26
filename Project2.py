import json
from pathlib import Path

FILE = Path("data3.json")

def load_data():
    if FILE.exists():
        data = json.loads(FILE.read_text(encoding="utf-8"))

        # Ensure required keys exist
        data.setdefault("expenses", [])
        data.setdefault("budgets", [])

        return data

    # Default structure if file does not exist
    return {
        "expenses": [],
        "budgets": []
    }

def save_data(data):
    FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")

# Load file
data = load_data()

Expense_data = data["expenses"]   
budget_data = data["budgets"]     


from datetime import datetime, date


def add_expense():
    user_category = input("Enter category name: ").lower().strip()
    user_cost = (input("Enter cost: ")).strip()
    user_date = (input("Enter (dd/mm/yy): ")).strip()
    
     # validate cost ( should only take floats and integers as input)
    try:
        user_cost = float(user_cost)
        if user_cost <= 0: # it should only take positive numbers.
            raise ValueError
       
    except ValueError:
        raise ValueError("Cost must be a positive number")
    
    # Validate catagory (Letter only)
    if not user_category.isalpha():
        raise ValueError("Error: task must contain letters only (no numbers, spaces, or symbols)")
    
    

    # validate date fotmate (only dd/mm/yy)

    try:
        parsed_date = datetime.strptime(user_date, "%d/%m/%y").date()
    except ValueError:
        raise ValueError("Date must be in dd//mm/yy format")
    
    # day range check (1-30)
    if parsed_date.day > 30:
        raise ValueError("Day (dd) must be between 1 and 30")
    
    # not in the future
    if parsed_date > date.today():
        raise ValueError("Date cannot be in the future")
    
    
    
    expense = {
        "category": user_category,
        "cost": user_cost,
        "date": user_date
    }

    Expense_data.append(expense)
    save_data(data)

    return Expense_data




def delete():
    user_expense = input("Enter delete all or delete category: ").lower().strip()
    
    if user_expense == "delete all":         # this will delte evertyhing in the data list
        Expense_data.clear()
        save_data(data)

        
    elif user_expense == "delete category":
        Expense_delete_expense = input("Enter category to be deleted: ")

         # keep only items NOT matching the category
        Expense_data[:] =[
            item for item in Expense_data
            if item["category"].lower() != Expense_delete_expense
        ]
        save_data(data)

    else:
        print("Invalid choice, Type exactly: delete all or delete category")    
    return Expense_data




def view(): # when selected view it will show the expenses and budget data
 return Expense_data , budget_data




def category_totals(): # it will add all the category costs and return the total. 

    total = 0

    for item in Expense_data:
        total+= item["cost"]
    return  f"total cost: {total} and the full data list : {Expense_data}"  





def add_budget():
    user_category2 = input("Enter category: ").strip().lower()

    # 🔒 Ensure category exists in expenses
    category_found = False
    for e in Expense_data:
        if e["category"].strip().lower() == user_category2:
            category_found = True
            break

    if category_found == False:
        raise ValueError("Category does not exist in expenses. Add an expense first.")

    # 🔒 Prevent duplicate budgets
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

    budget = {
        "category": user_category2,
        "limit": limit
    }

    budget_data.append(budget)
    save_data(data)

    return budget_data

def montly_totals():

    totals = {}

    for i in Expense_data:
        d = datetime.strptime(i["date"], "%d/%m/%y")  
        key = f"{d.year}-{d.month}"

        if key not in totals:
            totals[key] = i["cost"]
        else:
            totals[key] = totals[key] + i["cost"]

    return totals
     
  


def compare_spending_budget():

    Total_budget= 0
    Total_spending= 0

    for i in Expense_data:
       Total_spending+= i["cost"] 
    for x in budget_data:
        Total_budget += x["limit"]

    remaining = Total_budget - Total_spending

    return  {
        "spent": Total_spending,
        "budget": Total_budget,
         "remaining": remaining
    }

def final():
    # This final section creates a conditions of the user choice. if the user selects any input suggested 
     # the functions above will be called and 
 while True:
     user = input("Enter add expense / delete / view  / " \
     "Total category/ monthly totals/ add budget  / " \
     "compare budget and spending / quit: ").strip().lower()

     if user == "add expense":
        add_expense()
     
     elif user == "delete":
          delete()
     
     elif user == "view":
        print(view())
     
     elif user == "total category":
          print(category_totals())
     
     elif user == "monthly totals":
          print(montly_totals())
     
     elif user == "add budget":
          add_budget()
     
     elif user == "compare budget and spending":
          print(compare_spending_budget())
     
     elif user == "quit":
       print("End programme")
       break
     
     else:
         print("wrong input, try again")
         continue
     
final()
     

    
    


