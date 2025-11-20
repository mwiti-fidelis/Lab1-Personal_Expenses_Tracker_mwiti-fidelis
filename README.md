WELCOME TO THE EXPENSE TRACKING SYSTEM
This command-line menu-driven application tracks expenses and money usage to help users make more informed financial decisions and manage their finances effectively, keeping track of their expenses.
This application contains three main files, namely:

expenses _tracker.py
archive_expenses.sh
balance. Txt

How to run the application.
To start the expense tracker application:
Run the expenses_tracker.py file, initiate and populate the user's menu. The menu has the following functionalities:

Check Current Balance - This menu option executes a function that retrieves data from the balance.txt file, which stores the balance, and then displays the current balance, the total amount spent on expenses, and the available balance.

View Expenses Option - This menu option presents the user with a submenu that provides search options, allowing them to search by name or date of the expense. It then runs a function that retrieves the data from all the expense files in the directory and then prints the results of the searched expense in an attractive manner if the expense exists.

Add New Expense - This menu option prompts the user to input details of a new expense and then saves the user's inputs in a newly created file with a date stamp, e.g., expenses_2025-12-01.txt. This information is then displayed on the terminal and stored in the created file.

Deposit into Balance - This is an additional menu option that allows users to update their balance by adding more money to their existing balance. The 
The balance.txt file contains the current balance as 0.0 and also stores the new balance when the user deposits or adds money to the balance.

We hope you enjoy our services. Thank you!




new balance is then saved in the balance.txt file, overwriting the pre-existing balance.

Exit - This menu option allows you to quit the application. 


Run the bash script file (archive_expenses.sh) to archive and log expenses. When ran:

This file creates a directory called archives if it does not exist and then automatically archives all available expenses files with the pattern “expenses _*.txt” files in the archives directory. At the same time, it then appends the contents of each expense file into the archive_log.txt. 

The user can also search for an archived expense to view its contents by running "./archive_expenses.sh $date", where $date is the date of the expense file.



