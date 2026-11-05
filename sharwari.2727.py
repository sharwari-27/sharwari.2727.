
import json
import os
from datetime import datetime

# ==============================================
#          NOVA BANK MANAGEMENT SYSTEM
# ==============================================

FILE_NAME = "nova_bank_data.json"


# Load account data from file
def load_accounts():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            print("Unable to load account data.")
    return {}


# Save account data
def save_accounts():
    with open(FILE_NAME, "w") as file:
        json.dump(accounts, file, indent=4)


accounts = load_accounts()


# Initialize default customer account
def initialize_account():
    acc_no = "2727"

    if acc_no not in accounts:
        accounts[acc_no] = {
            "name": "Sharwari",
            "pin": "2727",
            "balance": 250000.00,
            "history": [
                "Initial Deposit: Rs. 250000.00"
            ]
        }
        save_accounts()


# Add transaction history
def add_transaction(acc_no, message):
    time = datetime.now().strftime(
        "%d-%m-%Y %I:%M:%S %p"
    )

    accounts[acc_no]["history"].append(
        f"{time} | {message}"
    )


# Display welcome screen
def welcome_screen():
    print("\n" + "=" * 55)
    print("              WELCOME TO NOVA BANK")
    print("           BANK ACCOUNT MANAGEMENT")
    print("=" * 55)


# Verify account and PIN
def verify_account():
    acc_no = input("\nEnter Account Number: ")

    if acc_no not in accounts:
        print("Account not found!")
        return None

    pin = input("Enter 4-Digit PIN: ")

    if accounts[acc_no]["pin"] != pin:
        print("Incorrect PIN! Access Denied.")
        return None

    print("\nLogin Successful!")
    return acc_no


# Create a new bank account
def create_account():
    print("\n========== CREATE NEW ACCOUNT ==========")

    name = input("Enter Customer Name: ").strip()
    acc_no = input("Enter Account Number: ").strip()

    if not name or not acc_no:
        print("Name and account number cannot be empty!")
        return

    if acc_no in accounts:
        print("Account already exists!")
        return

    pin = input("Create 4-Digit PIN: ")

    if len(pin) != 4 or not pin.isdigit():
        print("PIN must contain exactly 4 digits!")
        return

    try:
        amount = float(input("Enter Initial Deposit: Rs. "))

        if amount < 0:
            print("Invalid initial deposit!")
            return

    except ValueError:
        print("Please enter a valid amount!")
        return

    accounts[acc_no] = {
        "name": name,
        "pin": pin,
        "balance": amount,
        "history": [
            f"Initial Deposit: Rs. {amount:.2f}"
        ]
    }

    save_accounts()

    print("\nACCOUNT CREATED SUCCESSFULLY!")
    print("Customer Name :", name)
    print("Account Number:", acc_no)
    print(f"Initial Balance: Rs. {amount:,.2f}")


# Display account details
def account_details():
    print("\n========== ACCOUNT DETAILS ==========")

    acc_no = verify_account()

    if acc_no:
        account = accounts[acc_no]

        print("\nCustomer Name  :", account["name"])
        print("Account Number :", acc_no)
        print(
            f"Available Balance: Rs. {account['balance']:,.2f}"
        )


# Check account balance
def check_balance():
    print("\n========== ACCOUNT BALANCE ==========")

    acc_no = verify_account()

    if acc_no:
        account = accounts[acc_no]

        print("\nAccount Holder :", account["name"])
        print("Account Number :", acc_no)
        print(
            f"Available Balance: Rs. {account['balance']:,.2f}"
        )


# Deposit money
def deposit_money():
    print("\n========== DEPOSIT MONEY ==========")

    acc_no = verify_account()

    if acc_no:
        try:
            amount = float(
                input("Enter Deposit Amount: Rs. ")
            )

            if amount <= 0:
                print("Enter a positive amount!")
                return

            previous = accounts[acc_no]["balance"]

            accounts[acc_no]["balance"] += amount

            add_transaction(
                acc_no,
                f"Deposited Rs. {amount:.2f}"
            )

            save_accounts()

            print("\nDEPOSIT SUCCESSFUL!")
            print(f"Previous Balance: Rs. {previous:,.2f}")
            print(f"Deposited Amount: Rs. {amount:,.2f}")
            print(
                f"New Balance: Rs. {accounts[acc_no]['balance']:,.2f}"
            )

        except ValueError:
            print("Invalid amount!")


# Withdraw money
def withdraw_money():
    print("\n========== WITHDRAW MONEY ==========")

    acc_no = verify_account()

    if acc_no:
        try:
            amount = float(
                input("Enter Withdrawal Amount: Rs. ")
            )

            if amount <= 0:
                print("Enter a positive amount!")

            elif amount > accounts[acc_no]["balance"]:
                print("INSUFFICIENT BALANCE!")

            else:
                previous = accounts[acc_no]["balance"]

                accounts[acc_no]["balance"] -= amount

                add_transaction(
                    acc_no,
                    f"Withdrawn Rs. {amount:.2f}"
                )

                save_accounts()

                print("\nWITHDRAWAL SUCCESSFUL!")
                print(f"Previous Balance: Rs. {previous:,.2f}")
                print(f"Withdrawn Amount: Rs. {amount:,.2f}")
                print(
                    f"Remaining Balance: Rs. {accounts[acc_no]['balance']:,.2f}"
                )

        except ValueError:
            print("Invalid amount!")


# Transfer money between accounts
def transfer_money():
    print("\n========== MONEY TRANSFER ==========")

    sender = verify_account()

    if sender:
        receiver = input(
            "Enter Receiver Account Number: "
        )

        if receiver not in accounts:
            print("Receiver account not found!")
            return

        if sender == receiver:
            print("Cannot transfer to the same account!")
            return

        try:
            amount = float(
                input("Enter Transfer Amount: Rs. ")
            )

            if amount <= 0:
                print("Enter a positive amount!")

            elif amount > accounts[sender]["balance"]:
                print("INSUFFICIENT BALANCE!")

            else:
                accounts[sender]["balance"] -= amount
                accounts[receiver]["balance"] += amount

                add_transaction(
                    sender,
                    f"Transferred Rs. {amount:.2f} to {receiver}"
                )

                add_transaction(
                    receiver,
                    f"Received Rs. {amount:.2f} from {sender}"
                )

                save_accounts()

                print("\nTRANSFER SUCCESSFUL!")
                print(
                    "Sender:", accounts[sender]["name"]
                )
                print(
                    "Receiver:", accounts[receiver]["name"]
                )
                print(f"Transfer Amount: Rs. {amount:,.2f}")

        except ValueError:
            print("Invalid amount!")


# Display transaction history
def transaction_history():
    print("\n========== TRANSACTION HISTORY ==========")

    acc_no = verify_account()

    if acc_no:
        account = accounts[acc_no]

        print("\nCustomer Name :", account["name"])
        print("Account Number:", acc_no)
        print("-" * 55)

        if account["history"]:
            for index, transaction in enumerate(
                account["history"], start=1
            ):
                print(f"{index}. {transaction}")
        else:
            print("No transactions available!")

        print("-" * 55)
        print(
            f"Current Balance: Rs. {account['balance']:,.2f}"
        )


# Main banking menu
def main():

    initialize_account()

    while True:

        welcome_screen()

        print("1. Create New Account")
        print("2. Account Details")
        print("3. Check Balance")
        print("4. Deposit Money")
        print("5. Withdraw Money")
        print("6. Transfer Money")
        print("7. Transaction History")
        print("8. Exit")

        print("=" * 55)

        choice = input("Enter Your Choice (1-8): ")

        if choice == "1":
            create_account()

        elif choice == "2":
            account_details()

        elif choice == "3":
            check_balance()

        elif choice == "4":
            deposit_money()

        elif choice == "5":
            withdraw_money()

        elif choice == "6":
            transfer_money()

        elif choice == "7":
            transaction_history()

        elif choice == "8":
            print("\nThank you for choosing NOVA BANK!")
            print("Have a great day!")
            break

        else:
            print("\nInvalid choice! Please try again.")


# Execute the program
if __name__ == "__main__":
    main()
