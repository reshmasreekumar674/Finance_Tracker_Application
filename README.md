
# Finance Tracker Application

A command-line  menu driven finance management application built in Python.
This tool allows users to track income and expenses, manage budgets, import transactions from CSV file, and generate financial reports.

# Features

* Add transactions manually
* Import transactions from CSV
* View all transactions
* Filter transactions by date range
* Edit transactions
* Delete transactions
* Manage budgets 


# Requirements

* Python 3.8+


# CSV Import Format

The CSV file must include these exact headers:
si,date,amount,category,description,type


Example:
si,date,amount,category,description,type
2025/01/05,1200,Salary,January Salary,income
2025/01/10,50,Food,Groceries,expense


Validation rules:

* Date format must be "YYYY/MM/DD"
* No future dates
* Amount must be numeric
* Type must be "income or expense"

# Default Categories

* Food
* Transport
* Rent
* Utilities
* Entertainment
* Salary
* Miscellaneous


# Data Storage

* Transactions are appended to data.csv file
* Budgets are stored in values.json file




# Report Generation

* Monthly summary 
* Category wise spending 
* Budget tracking 
* Top Spending Category

# Features/ Functionalities of the Finance Tracker Application

### 1. Transaction Management

* **Add Transaction**

  * Add manually
  * Import from CSV

* **View Transactions**

  * View all transactions
  * View by date range
* **Edit Transaction**

  * Modify date, amount, category, description, type
* **Delete Transaction**

  * Delete by transaction ID

### 2. CSV Import System

* Import transactions from external CSV files
* Validates:

  * Required columns
  * Empty fields
  * Date format (YYYY/MM/DD)
  * Future dates
  * Numeric amounts
  * Valid transaction type (income or expense)
  * Rejects file if any row contains errors
  * Auto-generates unique transaction IDs
  * Displays imported transactions summary
  * Duplicates are allowed as there might be multiple transactions with the same values on the same day

### 3. Data Storage

* **CSV storage (data.csv)**

  * Saves all transactions
  * Loads transactions automatically at startup
* **JSON storage (values.json)**

  * Stores categories
  * Stores budgets

### 4. Category Management

* View all categories
* Add new category
* Delete category
* Automatically removes associated budget when deleting a category

### 5. Budget Management

* View budgets per category
* Edit/set budget amount for each category
* Stores budgets in JSON

### 6. Reporting System

**Full Monthly Report**
Includes:

* Monthly financial summary

  * Total income
  * Total expenses
  * Savings
* Category summary

  * Income per category
  * Expenses per category
* Budget tracking

  * Budget vs spent
  * Percentage used
  * Status:

    * Within budget
    * Near limit
    * Exceeded budget
* Top spending categories ranking

### 7. Data Validation

* Date format validation
* Prevents future dates
* Numeric validation for amounts
* Required field checks
* Valid transaction type check
* CSV structure validation

### 8. Automatic ID Generation

* Random unique transaction IDs (1000–9999)
* Ensures no duplicates

### 9. View Transactions

* View all transactions
* View by date range







