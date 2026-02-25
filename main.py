

import os
import csv
import random
from datetime import datetime
import json
from typing import Dict, Any

# Accepted date format is yyyy/mm/dd
ACCEPTED_DATE_FORMATS = ["%Y/%m/%d"]
FILE_NAME = "values.json"
#default catagories are listed below
default_catagories = ["Food", "Transport", "Rent", "Utilities", "Entertainment", "Salary", "Miscellaneous"]

transactions = []


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
  6. View Reports
 10. Exit
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
            view_reports()
        elif choice == "10":
            print("Goodbye!")
            break
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


def view_reports():
    """View reports"""
    while True:
        print("\n--- View Reports ---")
        print("""
  1. Monthly Summary
  2. Category Summary
  3. Budget Tracking
  4. Top Spending Categories
  5. Exit
        """)
        choice = input("Enter your choice (1-5): ").strip()
        if choice == "1":
            monthly_summary()
        elif choice == "2":
            category_summary()
        elif choice == "3":
            budget_tracking()
        elif choice == "4":
            top_spending_categories()
        elif choice == "5":
            return
        else:
            print("Invalid choice.")


def budget_tracking():
    print("\n--- Budget Tracking ---")


def top_spending_categories():
    print("\n--- Top Spending Categories ---")


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
    existing_ids = {t["id"] for t in transactions}
    while True:
        transaction_id = str(random.randint(100, 999))
        if transaction_id not in existing_ids:
            break

    date_input = input("Enter date (YYYY/MM/DD): ").strip()
    parsed_date = parse_date(date_input)
    if parsed_date is None:
        print("Invalid date format. Please use YYYY/MM/DD.")
        return
    if parsed_date > datetime.now():
        print("Future date is not allowed.")
        return

    try:
        amount = float(input("Enter amount: ").strip())
    except ValueError:
        print("Invalid amount. Please enter a numeric value.")
        return

    print("Select a category from the following options:")
    for i, category in enumerate(default_catagories):
        print(f"  {i+1}. {category}")
    try:
        choice = int(input("Enter category number: ").strip())
        if choice < 1 or choice > len(default_catagories):
            raise IndexError
        category = default_catagories[choice - 1]
    except (ValueError, IndexError):
        print("Invalid category selection.")
        return

    description = input("Enter description: ").strip()
    trans_type = input("Enter type (income/expense): ").strip().lower()
    if trans_type not in ("income", "expense"):
        print("Invalid type. Must be 'income' or 'expense'.")
        return

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
    print(f"Transaction added successfully with ID: {transaction_id}\n")


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
        print(f"Failed to read file.\n")
        return

    if errors:
        print(f"\nFile rejected — found {len(errors)} row(s) with errors:")
        for line_num, row_errors in errors:
            print(f"  Line {line_num}:")
            for err in row_errors:
                print(f"    - {err}")
        print("\nPlease fix all errors in the file and try again.\n")
        return

    # Generate unique IDs for each row
    existing_ids = {t["id"] for t in transactions}
    new_rows = []
    for row in valid_rows:
        while True:
            new_id = str(random.randint(100, 999))
            if new_id not in existing_ids:
                row["id"] = new_id
                existing_ids.add(new_id)
                break
        new_rows.append(row)

    if not new_rows:
        print("\nNo new transactions to import.\n")
        return

    transactions.extend(new_rows)
    save_to_csv()
    print(f"\nSuccessfully imported {len(new_rows)} transaction(s)!\n")
    print(f"{'ID':<5} {'Date':<12} {'Amount':>10} {'Type':<10} {'Category':<15} Description")
    print("-" * 70)
    for t in new_rows:
        print(f"{t['id']:<5} {t['date']:<12} {t['amount']:>10.2f} {t['type']:<10} {t['category']:<15} {t['description']}")
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
        print(f"{t['id']:<5} {t['date']:<12} {t['amount']:>10.2f} {t['type']:<10} {t['category']:<15} {t['description']}")
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
        print(f"{t['id']:<5} {t['date']:<12} {t['amount']:>10.2f} {t['type']:<10} {t['category']:<15} {t['description']}")
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
            reader = csv.DictReader(f)
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
    for fmt in ACCEPTED_DATE_FORMATS:
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except ValueError:
            continue
    return None


def validate_csv_file(filepath):
    """Validate the CSV file"""
    required_columns = {"date", "amount", "category", "description", "type"}
    valid_rows = []
    errors = []

    with open(filepath, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        if not required_columns.issubset(set(reader.fieldnames or [])):
            missing = required_columns - set(reader.fieldnames or [])
            raise ValueError(f"Please add headings properly in the order: si,date,amount,category,description,typeMissing required columns: {', '.join(missing)}")

        for line_num, row in enumerate(reader, start=2):
            row_errors = []
            parsed_date = parse_date(row.get("date", ""))
            if parsed_date is None:
                row_errors.append(f"Invalid date '{row.get('date', '')}' (accepted format: YYYY/MM/DD)")
            elif parsed_date > datetime.now():
                row_errors.append(f"Future date '{row.get('date', '')}' is not allowed")

            try:
                float(row.get("amount", ""))
            except ValueError:
                row_errors.append(f"Invalid amount '{row.get('amount', '')}'")

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


def load_budgets() -> Dict[str, Dict[str, float]]:
    """Load budgets from JSON file values.json"""
    if not os.path.exists(FILE_NAME):
        return {"budgets": {}}
    with open(FILE_NAME, "r") as f:
        data: Dict[str, Dict[str, float]] = json.load(f)
    return data


def save_budgets(data: Dict[str, Dict[str, float]]) -> None:
    """Save budgets to JSON file values.json"""
    with open(FILE_NAME, "w") as f:
        json.dump(data, f, indent=4)


def edit_budget() -> None:
    data = load_budgets()
    budgets: Dict[str, float] = data.setdefault("budgets", {})
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


def monthly_summary():
    print("\n--- Monthly Summary ---")
    

def category_summary():
    print("\n--- Category Summary ---")



if __name__ == "__main__":
    main()