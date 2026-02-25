
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




#Report Generation

* Monthly summary 
* Category wise spending 
* Budget tracking 

