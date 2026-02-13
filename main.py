def load_data():
    transactions = []

    try:
        with open(r"C:\Users\harip\OneDrive\Documents\GitHub\Finance_Tracker_Application\data.csv", "r") as file:
            next(file)  
            lines = file.readlines()

            for line in lines:
                line = line.strip()
                if line:
                    parts = line.split(",")

                    if len(parts) == 6:
                        transaction = {
                            "id": int(parts[0]),
                            "date": parts[1],
                            "amount": float(parts[2]),
                            "category": parts[3],
                            "description": parts[4],
                            "type": parts[5]
                        }

                        transactions.append(transaction)

    except FileNotFoundError:
        print("data.csv file not found.")

    return {"transactions": transactions}



def main():
    data = load_data()
    print(data)

    while True:
        print("""
1. Add Transaction
2. View Transactions
3. Edit Transaction
4. Delete Transaction
5. Monthly Summary
6. Category Breakdown
7. Set Budget
8. Budget tracking
9. Spending trendds
10. Exit
""")

        choice = input("Choose option: ")

        if choice == "1":
           # add_transaction(data)
           pass
        elif choice == "2":
            pass
           # view_transactions(data)
        elif choice == "3":
            pass
           # edit_transaction(data)
        elif choice == "4":
            pass
           # delete_transaction(data)
        elif choice == "5":
            pass
          #  monthly_summary(data)
        elif choice == "6":
            pass
          #  category_breakdown(data)
        elif choice == "7":
            pass
          #  set_budget(data)
        elif choice == "8":
            pass
           # check_budgets(data)
        elif choice == "9":
            pass
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
