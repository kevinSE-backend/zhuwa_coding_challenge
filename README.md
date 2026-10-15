## Susu Savings Group Management System
### Overview

The Susu Savings Group Management System is a small Python application that manages a rotating savings group. It allows members to contribute a fixed amount of money each week, tracks partial payments, verifies whether all members have paid, and distributes the total savings pot to members in the order they joined.

The application is designed to demonstrate basic financial record management, input validation, and exact monetary calculations using Python's Decimal module.

## Features
Create a savings group: Configure a fixed weekly contribution amount in Ghanaian cedis (GHS).
Add members: Register members using unique names or IDs while preserving their joining order.
Record contributions: Accept full or partial payments for the current week.
Validate payments: Reject unknown members, duplicate members, invalid amounts, and payments exceeding the outstanding balance.
Close a week: Verify that all members have paid their full contributions before distributing the pot.
Track outstanding balances: Identify members who have not completed their weekly contributions and show how much they owe.
Manage rotating payouts: Pay the entire weekly pot to the next eligible member in joining order.
Generate reports: Display the current week, each member's payment status, outstanding balances, and payout history.
Ensure monetary accuracy: Use Decimal to avoid floating-point rounding errors.
Requirements
Python 3.9 or later
No external dependencies are required.
Installation
Ensure Python is installed on your computer.

## Verify your installation:

python --version

Save the application code in a file named susu.py.
Open a terminal in the directory containing the file.
Usage

Run the application with:

python susu.py


The program displays an interactive menu:

1. Add member
2. Record contribution
3. Close week
4. Show report
5. Exit


Enter the number corresponding to the action you want to perform.

1. ## Add a member

Select option 1 and enter the member's name or ID.

Each member must have a unique identifier. Members are automatically placed in the order they join.

Example:

Enter member name or ID: Ama
Member added successfully.

2. ## Record a contribution

Select option 2, enter the member's name or ID, and provide the payment amount in GHS.

For a group with a weekly contribution of GHS 50.00, a member can pay GHS 20.00 first and the remaining GHS 30.00 later in the same week.

Example:

Enter member name or ID: Ama
Enter payment amount in GHS: 20.00
Payment recorded. Total paid this week: GHS 20.00


The system tracks the outstanding balance automatically.

3. ## Close the week

Select option 3 after members have made their contributions.

If every member has paid in full, the system distributes the total pot to the next member in the rotation and advances to the following week.
If any member still owes money, the week remains open, no payout occurs, and the outstanding balances are displayed.

For example, if four members each contribute GHS 50.00, the total pot is GHS 200.00.

Week 1 closed successfully. Ama receives GHS 200.00.
Now entering week 2.

4. ## Show the report

Select option 4 to view the current group status.

### The report includes:

Weekly contribution amount
Number of registered members
Current week
Amount paid by each member during the current week
Outstanding balance for each member
Payment status for each member
Historical payouts, including the recipient, week, and amount
5. ## Exit

Select option 5 to terminate the application.

Business Rules and Validation

The application enforces the following rules:

The weekly contribution must be greater than zero.
Member names or IDs must not be empty.
Duplicate members cannot be registered.
Contributions can only be recorded for registered members.
Contribution amounts must be positive.
Payments cannot exceed the member's outstanding balance for the current week.
Monetary values cannot have more than two decimal places.
A week cannot be closed while any member owes money.
A payout is made only after all members have contributed the required amount.
Members receive payouts in their joining order, with the rotation restarting after the last member receives a payout.
A week cannot be closed when the group has no members.
Financial Accuracy

The application uses Python's Decimal type to represent monetary values.

Floating-point types such as float can introduce precision errors when performing financial calculations. Using Decimal helps maintain exact decimal arithmetic for amounts represented to two decimal places.

For example:

from decimal import Decimal

contribution = Decimal("50.00")
members = 4

pot = contribution * members

print(f"GHS {pot:.2f}")


Output:

GHS 200.00


Always construct monetary values from strings rather than floating-point values when using Decimal.

Example Scenario

Suppose a savings group has three members:

Ama
Kofi
Abena

Each member contributes GHS 50.00 every week.

Week	Member	Contribution	Payout
1	Ama	GHS 50.00	GHS 150.00
1	Kofi	GHS 50.00	—
1	Abena	GHS 50.00	—
2	Ama	GHS 50.00	—
2	Kofi	GHS 50.00	GHS 150.00
2	Abena	GHS 50.00	—
3	Ama	GHS 50.00	—
3	Kofi	GHS 50.00	—
3	Abena	GHS 50.00	GHS 150.00

Each member contributes GHS 150.00 over three weeks, and each receives the same total pot of GHS 150.00 once.
