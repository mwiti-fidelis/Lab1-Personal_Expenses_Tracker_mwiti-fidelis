from datetime import datetime
import os

class Current_Balance:
    def __init__(self, balance_file='balance.txt'):
        self.balance_file = balance_file
        if not os.path.exists(self.balance_file):
            with open(self.balance_file, 'w') as file:
                file.write('0.0')
        self.current_balance = self.get_balance()

    def get_balance(self):
        with open(self.balance_file, 'r') as file:
            lines = file.read().strip()
            try:
                return float(lines)
            except ValueError:
                print("Invalid values in balance.txt. Resetting to 0.0")
                with open(self.balance_file, 'w') as f:
                    f.write('0.0')
                return 0.0

    def display_current_balance(self):
        current_balance = self.get_balance()
        total_expenses = 0
        expense_file = f"expenses_{datetime.now().date()}.txt"
        
        try:
            with open(expense_file, "r") as file:
                for line in file:
                    parts = line.strip().split(",")
                    if len(parts) >= 4:
                        amount = parts[-1].strip()
                        try:
                            total_expenses += float(amount)
                        except ValueError:
                            continue
        except FileNotFoundError:
            total_expenses = 0

        available_balance = current_balance - total_expenses
        print("")
        print(f"""
        ----------------------------------------------------
        FINANCIAL REPORT
        ----------------------------------------------------
        CURRENT BALANCE:         ${current_balance:.2f}
        TOTAL EXPENSES TO DATE:  ${total_expenses:.2f}
        AVAILABLE BALANCE:       ${available_balance:.2f}
        """)

    def update_current_balance(self):
        print("")
        print("----------WELCOME TO YOUR BALANCE DEPOSIT PAGE---------------")
        
        current_balance = self.get_balance()
        print(f"Current Balance: ${current_balance:.2f}")
        
        while True:
            choice = input("Do you wish to add money to your current balance? (yes/no): ").strip().lower()
            if choice in ['yes', 'y']:
                while True:
                    add_amount_str = input("Enter the amount you wish to add to your balance: ").strip()
                    try:
                        add_amount = float(add_amount_str)
                        if add_amount <= 0:
                            print("Amount must be positive. Please enter a valid amount.")
                            continue
                        break
                    except ValueError:
                        print("Invalid input. Please enter a valid number (e.g., 50.00)")
                        continue
                
                new_balance = current_balance + add_amount
                with open(self.balance_file, 'w') as f:
                    f.write(str(new_balance))
                
                print("")
                print(f"""
        Successfully added ${add_amount:.2f} to your balance.
        New Balance: ${new_balance:.2f}
        """)
                self.display_current_balance()
                break
                
            elif choice in ['no', 'n']:
                print("-----------Exiting balance update page---------")
                break
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")
                continue


balance_tracker = Current_Balance(balance_file="balance.txt")


def new_expense():
    print("")
    print("--- ADD NEW EXPENSE ---")
    
    available_balance = balance_tracker.get_balance()
    print(f"AVAILABLE BALANCE: ${available_balance:.2f}")
    
    while True:
        date_input = input("Please enter the current date in the format YYYY-MM-DD (e.g., 2025-11-20): ").strip()
        try:
            expense_date = datetime.strptime(date_input, "%Y-%m-%d").date()
            break
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            continue
    
    while True:
        items = input("Enter the name of the item/expense: ").strip()
        if not items:
            print("Item name cannot be empty. Please enter a valid name.")
            continue
        break
    
    while True:
        amount_str = input("Enter the amount spent: ").strip()
        try:
            amount = float(amount_str)
            if amount <= 0:
                print("Amount must be positive. Please enter a valid amount.")
                continue
            break
        except ValueError:
            print("Invalid amount. Please enter a numeric value (e.g., 25.50)")
            continue
    
    print("")
    print(f"""
        --------------------------------------------------------
                                EXPENSE REVIEW
        --------------------------------------------------------
        EXPENSE:        {items}
        AMOUNT SPENT:  ${amount:.2f}
        DATE ENTRY:     {expense_date}
        --------------------------------------------------------
    """)
    
    while True:
        confirmation = input("Is this information correct? (y/n): ").strip().lower()
        if confirmation in ['y', 'yes']:
            break
        elif confirmation in ['n', 'no']:
            print("Expense discarded. Returning to main menu.")
            return
        else:
            print("Please enter 'y' for yes or 'n' for no.")
            continue
    
    if amount > available_balance:
        print("Insufficient balance! Cannot save expense.")
        return
    
    expense_file_name = f"expenses_{expense_date}.txt"
    expense_id = 1
    
    if os.path.exists(expense_file_name):
        with open(expense_file_name, 'r') as f:
            lines = f.readlines()
            if lines:
                last_line = lines[-1]
                parts = last_line.strip().split(',')
                if len(parts) >= 1:
                    try:
                        last_id = int(parts[0])
                        expense_id = last_id + 1
                    except ValueError:
                        pass
    
    timestamp = datetime.now().strftime('%Y-%m-%d,%H:%M:%S')
    
    with open(expense_file_name, 'a') as f:
        f.write(f"{expense_id}, {timestamp}, {items}, {amount:.2f}\n")
    
    new_balance = available_balance - amount
    with open('balance.txt', 'w') as f:
        f.write(str(new_balance))
    
    print("")
    print(f"""
        Successfully added expense
        Expense ID: {expense_id}
        Item: {items}
        Amount: ${amount:.2f}
        Date: {expense_date}
        Remaining Balance: ${new_balance:.2f}
    """)


def view_expenses():
    print("")
    print("---------- VIEW EXPENSES ---------")
    
    while True:
        print("")
        print(f"""
        ---------------------------------
           WELCOME TO THE EXPENSES PAGE
        ---------------------------------
        1. Search by Item Name
        2. Search by Amount
        3. Back to Main Menu
        ---------------------------------
        """)
        
        menu_choice = input("Select option (1-3): ").strip()
        try:
            menu_choice = int(menu_choice)
        except ValueError as e:
            print("Invalid menu option. Please select 1-3")
            exit()
        
        if menu_choice == '1':
            item_name = input("Enter item name to search: ").strip().lower()
            found_expenses = []
            
            for filename in os.listdir('.'):
                if filename.startswith('expenses_') and filename.endswith('.txt'):
                    try:
                        with open(filename, 'r') as f:
                            for line in f:
                                parts = line.strip().split(',')
                                if len(parts) >= 4:
                                    expense_id = parts[0].strip()
                                    timestamp = parts[1].strip()
                                    item = parts[2].strip()
                                    amount = parts[3].strip()
                                    
                                    if item.lower() == item_name:
                                        found_expenses.append({
                                            'id': expense_id,
                                            'timestamp': timestamp,
                                            'item': item,
                                            'amount': amount,
                                            'file': filename
                                        })
                    except Exception as e:
                        continue
            
            if found_expenses:
                print("")
                print(f"Found {len(found_expenses)} expense(s) matching '{item_name}':")
                for exp in found_expenses:
                    print(f"""
                    -------------------------------
                    Expense ID:  {exp['id']}
                    Date/Time:   {exp['timestamp']}
                    Item:        {exp['item']}
                    Amount:     ${exp['amount']}
                    File:        {exp['file']}
                    -------------------------------
                    """)
            else:
                print(f"No expenses found for item: {item_name}")
        
        elif menu_choice == '2':
            amount_str = input("Enter amount to search: ").strip()
            try:
                search_amount = float(amount_str)
            except ValueError:
                print("Invalid amount. Please enter a number.")
                continue
            
            found_expenses = []
            
            for filename in os.listdir('.'):
                if filename.startswith('expenses_') and filename.endswith('.txt'):
                    try:
                        with open(filename, 'r') as f:
                            for line in f:
                                parts = line.strip().split(',')
                                if len(parts) >= 4:
                                    amount = parts[3].strip()
                                    try:
                                        if abs(float(amount) - search_amount) < 0.01:
                                            found_expenses.append({
                                                'id': parts[0].strip(),
                                                'timestamp': parts[1].strip(),
                                                'item': parts[2].strip(),
                                                'amount': amount,
                                                'file': filename
                                            })
                                    except ValueError:
                                        continue
                    except Exception as e:
                        continue
            
            if found_expenses:
                print("")
                print(f"Found {len(found_expenses)} expense(s) with amount ${search_amount:.2f}:")
                for exp in found_expenses:
                    print(f"""
                    -------------------------------
                    Expense ID: {exp['id']}
                    Date/Time:  {exp['timestamp']}
                    Item:       {exp['item']}
                    Amount:     ${exp['amount']}
                    File:       {exp['file']}
                    -------------------------------
                    """)
            else:
                print(f"No expenses found with amount: ${search_amount:.2f}")
        
        elif menu_choice == '3':
            print("-----RETURNING TO MAIN MENU-------")
            break
        
        else:
            print("Invalid option. Please select 1-3.")


def main_menu_system():
    print("")
    print(f"""
    :::::::::::::::::::::::::::::::::::::::::::::::::::::::
         WELCOME TO THE EXPENSES TRACKER APPLICATION
    :::::::::::::::::::::::::::::::::::::::::::::::::::::::
    """)
    
    while True:
        print("")
        print(f"""
        1. CHECK REMAINING BALANCE
        2. VIEW EXPENSES
        3. ADD NEW EXPENSE
        4. DEPOSIT INTO BALANCE
        5. EXIT
        """)
        
        menu_choice = input("Select the menu options 1-5: ").strip()
        
        if menu_choice == '1':
            print("")
            balance_tracker.display_current_balance()
            
        elif menu_choice == '2':
            print("")
            view_expenses()
            
        elif menu_choice == '3':
            print("")
            new_expense()
            
        elif menu_choice == '4':
            print("")
            balance_tracker.update_current_balance()
            
        elif menu_choice == '5':
            print(":::::::::EXITING, GOODBYE::::::::::")
            break
            
        else:
            print("Invalid menu option selected. Please select 1-5.")
            continue


if __name__ == "__main__":
    main_menu_system()
