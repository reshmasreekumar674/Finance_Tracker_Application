
import os
import csv
import random
from datetime import datetime
import json
import re
from typing import Dict, Any
# Accepted date format is yyyy/mm/dd
ACCEPTED_DATE_FORMATS = ["%Y/%m/%d"]
VALUES_FILE = "values.json"

def load_values():
    """Load data from values.json"""
    if not os.path.isfile(VALUES_FILE):
        default = {
            "categories": {"items": ["Food", "Transport", "Rent", "Utilities", "Entertainment", "Salary", "Miscellaneous"]},
            "budgets": {}
        }
        save_values(default)
        return default
    with open(VALUES_FILE, "r") as f:
        return json.load(f) # return the data loaded from values.json in the form of a dictionary


def save_values(data):
    """Write data back to values.json."""
    with open(VALUES_FILE, "w") as f:
        json.dump(data, f, indent=4) # write the data to values.json in the form of json


def get_categories():
    """Return the current list of categories from values.json."""
    return load_values()["categories"]["items"] # return the list of categories from values.json

default_catagories = get_categories()

transactions = [] # list to store all transactions in memory
#{"id": "123", "date": "2024/03/01", "amount": 50.0, "category": "Food", ...}

def main():
    """Main menu"""
    while True:
        print("""
=============================
      Finance Tracker
=============================
  1. Add Transaction
  2. View Transactions
  3. Edit Transaction
  4. Delete Transaction
  5. Manage Budgets
  6. Manage Categories
  7. View Reports
  8. Exit
        """)
        choice = input("Select an option: ").strip() 
        if choice == "1":
            add_transaction()
        elif choice == "2":
            view_transactions()
        elif choice == "3":
            edit_transaction()
        elif choice == "4":
            delete_transaction()
        elif choice == "5":
            manage_budgets()
        elif choice == "6":
            manage_categories()
        elif choice == "7":
            view_reports()
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please select from the menu.\n")

def manage_categories():
    while True:
        print("""
--- Manage Categories ---
1. View Categories
2. Add Category
3. Delete Category
5. Exit
""")

        choice = input("Select option: ").strip()

        if choice == "1":
            data = load_values()
            categories = data["categories"]["items"]

            print("\nCategories:")
            for i, category in enumerate(categories, 1):
                print(f"{i}. {category}")

        elif choice == "2":
            data = load_values()
            categories = data["categories"]["items"]

            category = input("\nEnter category name: ").strip()

            if not category:
                print("Category name cannot be empty.")
            elif category in categories:
                print(f"Category '{category}' already exists.")
            else:
                categories.append(category)
                save_values(data)
                print(f"Category '{category}' added successfully!")

        elif choice == "3":
            data = load_values()
            categories = data["categories"]["items"]

            print("\nDelete Category")
            for i, category in enumerate(categories, 1):
                print(f"{i}. {category}")

            category_num = input("Select category number to delete: ").strip()

            if category_num.isdigit() and 1 <= int(category_num) <= len(categories):
                idx = int(category_num) - 1
                removed = categories.pop(idx)

                # Also remove the budget entry if it exists
                data["budgets"].pop(removed, None)

                save_values(data)
                print(f"Category '{removed}' deleted successfully!")
            else:
                print("Invalid selection.")

        elif choice == "5":
            return

        else:
            print("Invalid option. Please select from the menu.\n")


def manage_budgets():
    """Manage budgets"""
    while True:
        print("\n--- Manage Budgets ---")
        print("""
  1. View Budget
  2. Edit Budget
  3. Exit
        """)
        choice = input("Enter your choice (1-3): ").strip()
        if choice == "1":
            view_budget()
        elif choice == "2":
            edit_budget()
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 3.")





def add_transaction():
    """Add transaction manually or from CSV file"""
    print("\n--- Add Transaction ---")
    confirm = input("\n (1) Add transaction from CSV file\n (2) Add transaction manually\n (3) Exit\nHow do you want to add the transaction? : ").strip()
    if confirm == "3":
        print("Returning to main menu...\n")
        return
    elif confirm == "2":
        add_transaction_manually()
    elif confirm == "1":
        add_transaction_from_csv()
    else:
        print("Invalid option. Returning to main menu...\n")



def add_transaction_manually():
    """Add transaction manually"""
    print("\n--- Add Transaction Manually ---")
    existing_ids = {t["id"] for t in transactions} # loops every transaction and adds the id to the set of existing IDs
    while True:
        transaction_id = str(random.randint(1000, 9999))
        if transaction_id not in existing_ids: # checks if the generated id is not in the set of existing IDs
            break

    while True:
        date_input = input("Enter date (YYYY/MM/DD): ").strip()
        parsed_date = parse_date(date_input)
        if parsed_date is None:
            print("Invalid date format. Please use YYYY/MM/DD.")
        elif parsed_date > datetime.now(): # checks if the date is in the future
            print("Future date is not allowed.")
        else:
            break

    while True:
        try:
            amount = float(input("Enter amount: ").strip())
            break
        except ValueError:
            print("Invalid amount. Please enter a numeric value.")

    print("Select a category from the following options:")
    for i, category in enumerate(default_catagories):
        print(f"  {i+1}. {category}")
    while True:
        try:
            choice = int(input("Enter category number: ").strip())
            if choice < 1 or choice > len(default_catagories):
                raise IndexError
            category = default_catagories[choice - 1]
            break
        except (ValueError, IndexError):
            print(f"Invalid selection. Please enter a number between 1 and {len(default_catagories)}.")

    while True:
        description = input("Enter description: ").strip()
        if description:
            break
        print("Description cannot be empty.")

    while True:
        trans_type = input("Enter type (income/expense): ").strip().lower()
        if trans_type in ("income", "expense"):
            break
        print("Invalid type. Must be 'income' or 'expense'.")

    new_transaction = {
        "id": transaction_id,
        "date": date_input,
        "amount": amount,
        "category": category,
        "description": description,
        "type": trans_type,
    }

    transactions.append(new_transaction)
    save_to_csv()
    print(f"\nTransaction added successfully with ID: {transaction_id}\n")


def add_transaction_from_csv():
    """Add transaction from CSV file"""
    filepath = input("Enter the CSV file path: ").strip()
    if not os.path.isfile(filepath):
        print(f"File not found: '{filepath}'\n")
        return
    if not filepath.lower().endswith(".csv"):
        print("Not a valid file. Only CSV files are accepted.\n")
        return

    print(f"\nReading file: '{filepath}'...")
    try:
        valid_rows, errors = validate_csv_file(filepath)
    except ValueError as e:
        print(f"File structure error: {e}\n")
        return
    except Exception as e:
        print(f"Failed to read file. {e}\n")
        return

   # errors format= [(2, ["Invalid date '2024/13/01'", "Invalid amount 'abc'"]),(5, ["Invalid type 'xyz'"])]
   

    if errors: 
        print(f"\nFile rejected — found {len(errors)} row(s) with errors:")
        for line_num, row_errors in errors:
            print(f"  Line {line_num}:")
            for err in row_errors: #
                print(f"    - {err}")
        print("\nPlease fix all errors in the file and try again.\n")
        return

    # Generate unique IDs for each row
    existing_ids = {t["id"] for t in transactions}
    new_rows = []
    for row in valid_rows:
        while True:
            new_id = str(random.randint(1000, 9999)) #random number
            if new_id not in existing_ids:
                row["id"] = new_id
                existing_ids.add(new_id)
                break
        new_rows.append(row)

    if not new_rows:
        print("\nNo new transactions to import.\n")
        return

    transactions.extend(new_rows) #add multiple elements from one list to the transaction list
    save_to_csv()
    print(f"\nSuccessfully imported {len(new_rows)} transaction(s)!\n")
    print(f"{'ID':<5} {'Date':<12} {'Amount':>10} {'Type':<10} {'Category':<15} Description") #formating
    print("-" * 70)
    for t in new_rows:
        print(f"{t['id']:<5} {t['date']:<12} {t['amount']:>15.2f} {t['type']:<10} {t['category']:<15} {t['description']}") #>10.2f right-align in 10 characters and show exactly 2 decimal
    print()


def display_all_transactions():
    """Display all transactions that are present in the transactions list"""
    if not transactions:
        print("\nNo transactions found. Please add transactions first.\n")
        return
    print("\n--- All Transactions ---")
    print(f"{'ID':<5} {'Date':<12} {'Amount':>10} {'Type':<10} {'Category':<15} Description")
    print("-" * 70)
    for t in transactions:
        print(f"{t['id']:<5} {t['date']:<12} {t['amount']:>15.2f} {t['type']:<10} {t['category']:<15} {t['description']}")
    print()


def display_transactions_by_date_range(start_date, end_date):
    """Display transactions within a date range"""
    if not transactions:
        print("\nNo transactions found.\n")
        return
    filtered = [t for t in transactions if start_date <= t["date"] <= end_date]
    if not filtered:
        print(f"\nNo transactions found between {start_date} and {end_date}.\n")
        return
    print(f"\n--- Transactions from {start_date} to {end_date} ---")
    print(f"{'ID':<5} {'Date':<12} {'Amount':>10} {'Type':<10} {'Category':<15} Description")
    print("-" * 70)
    for t in filtered:
        print(f"{t['id']:<5} {t['date']:<12} {t['amount']:>15.2f} {t['type']:<10} {t['category']:<15} {t['description']}")
    print()


def view_transactions():
    """View transactions"""
    if not transactions:
        print("\nNo transactions found. Please add transactions first.\n")
        return
    print("\nHow do you want to display transactions?")
    confirm = input(" (1) All transactions\n (2) By date range\nSelect: ").strip()
    if confirm == "1":
        display_all_transactions()
    elif confirm == "2":
        start_date = input("Enter the start date (YYYY/MM/DD): ").strip()
        end_date = input("Enter the end date (YYYY/MM/DD): ").strip()
        if parse_date(start_date) is None:
            print("Invalid start date format. Use YYYY/MM/DD.\n")
            return
        if parse_date(end_date) is None:
            print("Invalid end date format. Use YYYY/MM/DD.\n")
            return
        if start_date > end_date:
            print("Start date cannot be after end date.\n")
            return
        display_transactions_by_date_range(start_date, end_date)
    else:
        print("Invalid option. Returning to main menu...\n")

def load_transactions_from_csv():
    """Load existing transactions from data.csv"""
    if os.path.isfile("data.csv"):
        with open("data.csv", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f) #row will be converted as a dictionary. {'id': '101', 'date': '2024/03/01', 'amount': '50', 'category': 'Food'}{'id': '102', 'date': '2024/03/02', 'amount': '20', 'category': 'Transport'}
            for row in reader:
                transactions.append({
                    "id": row["id"].strip(),
                    "date": row["date"].strip(),
                    "amount": float(row["amount"].strip()),
                    "category": row["category"].strip(),
                    "description": row["description"].strip(),
                    "type": row["type"].strip().lower(),
                })


load_transactions_from_csv()

def parse_date(date_str):
    """This function is used to validate and convert a date string into a datetime object."""
    
    if not re.fullmatch(r"\d{4}/\d{2}/\d{2}", date_str.strip()): #pattern matching
        return None
    for fmt in ACCEPTED_DATE_FORMATS:
        try:
            return datetime.strptime(date_str.strip(), fmt) #convert string to datetime object
        except ValueError:
            continue
    return None

def validate_csv_file(filepath):
    """Validate the CSV file"""
    required_columns = {"date", "amount", "category", "description", "type"}
    valid_rows = []
    errors = []

    with open(filepath, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile) #Opens and reads the CSV with dictionary-style row access.
        if not required_columns.issubset(set(reader.fieldnames or [])): #issubset checks all required columns exist in the headers., reader.fieldnames or [] handles the case where fieldnames is None
            missing = required_columns - set(reader.fieldnames or []) #find missing coloumn
            raise ValueError(f"Please add headings properly in the order: id,date,amount,category,description,type. Missing required columns: {', '.join(missing)}")

        for line_num, row in enumerate(reader, start=2):
            row_errors = []

            # Check for null/empty values in all required fields
            null_fields = [
                col for col in required_columns
                if row.get(col) is None or not str(row.get(col)).strip()
            ]
            if null_fields:
                row_errors.append(f"Some column values are null, please upload a proper CSV file")
                errors.append((line_num, row_errors))
                continue  # Skip further checks for this row

            # Validate date
            parsed_date = parse_date(row.get("date", ""))
            if parsed_date is None:
                row_errors.append(f"Invalid date '{row.get('date', '')}' (accepted format: YYYY/MM/DD)")
            elif parsed_date > datetime.now():
                row_errors.append(f"Future date '{row.get('date', '')}' is not allowed")

            # Validate amount
            try:
                float(row.get("amount", ""))
            except ValueError:
                row_errors.append(f"Invalid amount '{row.get('amount', '')}'")

            # Validate type
            if row.get("type", "").strip().lower() not in ("income", "expense"):
                row_errors.append(f"Invalid type '{row.get('type', '')}' (must be 'income' or 'expense')")

            if row_errors:
                errors.append((line_num, row_errors))
            elif parsed_date is not None:
                valid_rows.append({
                    "date": parsed_date.strftime("%Y/%m/%d"),
                    "amount": float(row["amount"].strip()),
                    "category": row["category"].strip(),
                    "description": row["description"].strip(),
                    "type": row["type"].strip().lower(),
                })

    return valid_rows, errors


def save_to_csv():
    """Save current transactions list to data.csv."""
    try:
        with open("data.csv", "w", newline="") as f:
            fieldnames = ["id", "date", "amount", "category", "description", "type"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(transactions)
    except Exception as e:
        print(f"Error updating data.csv: {e}")


def delete_transaction():
    """Delete a transaction by ID"""
    if not transactions:
        print("\nNo transactions found.\n")
        return
    view_transactions()
    transaction_id = input("Enter the ID of the transaction you want to delete: ").strip()
    transaction = next((t for t in transactions if t["id"] == transaction_id), None)
    if transaction is None:
        print(f"\nNo transaction found with ID '{transaction_id}'.\n")
        return
    confirm = input(f"Are you sure you want to delete transaction ID '{transaction_id}'? (y/n): ").strip().lower()
    if confirm != "y":
        print("Deletion cancelled. Returning to main menu...\n")
        return
    transactions.remove(transaction)
    save_to_csv()
    print(f"\nSuccessfully deleted transaction with ID '{transaction_id}'.\n")


def edit_transaction():
    """Edit a transaction by ID"""
    if not transactions:
        print("\nNo transactions found.\n")
        return
    print("\n--- Edit Transaction ---")
    view_transactions()
    transaction_id = input("Enter the ID of the transaction you want to edit: ").strip()
    transaction = next((t for t in transactions if t["id"] == transaction_id), None)
    if transaction is None:
        print(f"\nNo transaction found with ID '{transaction_id}'.\n")
        return

    updated = transaction.copy()
    print(f"\nEditing Transaction ID: {transaction_id}")
    print("Leave a field blank and press Enter to keep the current value.\n")

    while True:
        new_date = input(f"Date (current: {updated['date']}): ").strip()
        if new_date == "":
            break
        parsed_date = parse_date(new_date)
        if parsed_date is None:
            print("  Invalid date format. Use YYYY/MM/DD.")
        elif parsed_date > datetime.now():
            print("  Future dates are not allowed.")
        else:
            updated["date"] = parsed_date.strftime("%Y/%m/%d")
            break

    while True:
        new_amount = input(f"Amount (current: {updated['amount']:.2f}): ").strip()
        if new_amount == "":
            break
        try:
            updated["amount"] = float(new_amount)
            break
        except ValueError:
            print("Invalid amount. Please enter a number.")

    print("Select a category from the following options:")
    for i, category in enumerate(default_catagories):
        print(f"  {i+1}. {category}")
    while True:
        choice = input(f"Enter category number (current: {updated['category']}) or press Enter to keep: ").strip()
        if choice == "":
            break
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(default_catagories):
                updated["category"] = default_catagories[idx - 1]
                break
            else:
                print("Invalid selection. Choose a valid number.")
        else:
            print("Please enter a valid number.")

    new_description = input(f"Description (current: {updated['description']}): ").strip()
    if new_description != "":
        updated["description"] = new_description

    while True:
        new_type = input(f"Type (current: {updated['type']}) [income/expense]: ").strip().lower()
        if new_type == "":
            break
        if new_type in ("income", "expense"):
            updated["type"] = new_type
            break
        print("  Invalid type. Enter 'income' or 'expense'.")

    print("\nPlease review the updated transaction details:")
    print(f"  Date        : {updated['date']}")
    print(f"  Amount      : {updated['amount']:.2f}")
    print(f"  Category    : {updated['category']}")
    print(f"  Description : {updated['description']}")
    print(f"  Type        : {updated['type']}")

    while True:
        confirm = input("\nPress 'y' to save changes or 'n' to cancel: ").strip().lower()
        if confirm == "y":
            transaction.update(updated)
            save_to_csv()
            print(f"\nTransaction ID '{transaction_id}' updated successfully!\n")
            break
        elif confirm == "n":
            print("\nEdit cancelled. No changes were saved.\n")
            return
        else:
            print("Invalid input. Enter 'y' or 'n'.")




def view_budget():
    """View budgets"""
    data = load_budgets()
    budgets = data.get("budgets", {})
    print("\n--- Current Budgets ---")
    for category in default_catagories:
        amount = budgets.get(category, 0)
        print(f"  {category}: ${amount}")


def load_budgets() -> Dict[str, Dict[str, float]]: # returns a dictionary of dictionaries
    """Load budgets from JSON file values.json"""
    if not os.path.exists(VALUES_FILE):
        return {"budgets": {}}
    with open(VALUES_FILE, "r") as f:
        data: Dict[str, Dict[str, float]] = json.load(f)
    return data


def save_budgets(data: Dict[str, Dict[str, float]]) -> None:
    """Save budgets to JSON file values.json"""
    with open(VALUES_FILE, "w") as f:
        json.dump(data, f, indent=4)


def edit_budget() -> None:
    data = load_budgets()
    budgets: Dict[str, float] = data.setdefault("budgets", {}) #returns the existing "budgets" dict if it exists, or inserts and returns an empty dict {} if it doesn't 
    print("\nSelect category to edit:")
    for i, category in enumerate(default_catagories, 1):
        print(f"  {i}. {category}")
    try:
        choice = int(input("Enter choice: "))
        category = default_catagories[choice - 1]
        amount = float(input(f"Enter new budget for {category}: "))
        budgets[category] = amount
        save_budgets(data)
        print("Budget updated successfully.")
    except (ValueError, IndexError):
        print("Invalid input.")

    


def view_reports():
    """View reports"""
    while True:
        print("\n--- View Reports ---")
        print("""
  1. Full Monthly Report
  2. Exit
        """)
        choice = input("Enter your choice (1-2): ").strip()
        if choice == "1":
            full_monthly_report()
        elif choice == "2":
            return
        else:
            print("Invalid choice.")


def full_monthly_report():
    """Show full report for a selected month"""
    if not transactions:
        print("\nNo transactions found.\n")
        return

    #  Get unique months from transactions
    months = sorted(set(t["date"][:7] for t in transactions)) #slice date yyyy/mm

    # Display available months
    print("""
    ==========================================
              FULL MONTHLY REPORT
    ==========================================
    """)
    print("\nAvailable Months:")
    for i, month in enumerate(months, start=1):
        print(f"  {i}. {month}")

    choice = input("\nSelect a month from the list by number (or 'b' to go back): ").strip()
    if choice.lower() == "b":
        return
    if not choice.isdigit() or not (1 <= int(choice) <= len(months)):
        print("Invalid choice.")
        return

    selected_month = months[int(choice) - 1] 

    # Step 3 — Filter transactions for selected month
    filtered = [t for t in transactions if t["date"][:7] == selected_month] #Filters transactions by slicing each date to YYYY/MM and comparing to the selected month.

    print(f"""
    ==============================================
             FULL REPORT — {selected_month}
    ==============================================
    """)

    _monthly_summary(filtered)
    _category_summary(filtered)
    _budget_tracking(filtered)
    _top_spending_categories(filtered)

    # Ask to view another month
    again = input("\nView another month? (y/n): ").strip().lower()
    if again == "y":
        full_monthly_report()


def _monthly_summary(filtered):
    """Monthly summary section"""
    total_income = sum(t["amount"] for t in filtered if t["type"] == "income")
    total_expenses = sum(t["amount"] for t in filtered if t["type"] == "expense")
    savings = total_income - total_expenses

    print("\n=================================== Monthly Summary ===================================")
    print(f"  Total Income:    {total_income:>10.2f}$")
    print(f"  Total Expenses:  {total_expenses:>10.2f}$")
    print(f"  Savings:         {savings:>10.2f}$")


def _category_summary(filtered):
    """Category summary section"""
    print("\n=================================== Category Summary ===================================")
    print(f"  {'Category':<20} {'Income':>10}  {'Expenses':>10}")
    print(f"  {'-'*20} {'-'*10}  {'-'*10}")

    # Get all unique categories in this month's transactions
    categories = sorted(set(t["category"] for t in filtered))

    for category in categories:
        income = sum(t["amount"] for t in filtered if t["category"] == category and t["type"] == "income")
        expenses = sum(t["amount"] for t in filtered if t["category"] == category and t["type"] == "expense")
        print(f"  {category:<20}  {income:>9.2f}$  {expenses:>9.2f}$")



def _budget_tracking(filtered):
    """Budget tracking section"""
    data = load_values()

    raw_budgets = data.get("budgets", {})
    if not isinstance(raw_budgets, dict): #isinstance verifies raw_budgets is a dictionary
        print("No budgets set. Please set budgets first.")
        return


    budgets: Dict[str, float] = {}
    for k, v in raw_budgets.items(): #Filters out any non-numeric values that might be in the JSON
        if isinstance(v, (int, float)):
            budgets[k] = float(v)

    if not budgets:
        print("No budgets set. Please set budgets first.")
        return

    print("\n=================================== Budget Tracking===================================")
    print(f"  {'Category':<15} {'Budget':>8}  {'Spent':>8}  {'Used':>6}  Status")
    print(f"  {'-'*15} {'-'*8}  {'-'*8}  {'-'*6}  {'-'*20}")

    for category, budget in budgets.items():
        spent = sum(t["amount"] for t in filtered if t["category"] == category and t["type"] == "expense")
        percent = (spent / budget) * 100 if budget > 0 else 0 #Ternary operator prevents division by zero if someone sets a budget of 0

        if spent > budget:
            status = " Exceeded budget"
        elif percent >= 80:
            status = " Near limit"
        else:
            status = " Within budget"

        print(f"  {category:<15} {budget:>7.2f}$  {spent:>7.2f}$  {percent:>5.1f}%  {status}") 


def _top_spending_categories(filtered):
    """Top spending categories section"""
    category_totals = {}
    for t in filtered:
        if t["type"] == "expense":
            category = t["category"]
            category_totals[category] = category_totals.get(category, 0) + t["amount"] #Builds a running total per category. .get(category, 0) returns 0 the first time a category is seen, then accumulates the amount on top.

    sorted_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True) #.items() returns (category, total) tuples. key=lambda x: x[1] sorts by the total (second element). reverse=True puts highest spender first

    print("\n=================================== Top Spending Categories ===================================")
    for rank, (category, total) in enumerate(sorted_categories, start=1):#enumerate provides the rank number. Tuple unpacking (category, total) directly from each item. {rank}. creates the numbered list format.
        print(f"  {rank}. {category:<20} {total:.2f}$")
    print()


if __name__ == "__main__":
    main()