import random
import sys
BankIsRunning=True
users={}

def register_user():
    global username
    username=input('Enter a username: ')

    if username in users:
        print('That username exists. Try again.')
        return
    
    passcode=input('Enter a passcode: ')

    users[username]={
        "passcode": passcode,
        "balance": 0.0,
        "history": []
    }
    print(f'{username} successfully registered')

def login_user():
    user=input('Enter your username: ')
    passcode=input('Enter your passcode: ')

    if user in users and users[user]["passcode"]==passcode:
        print(f'Login successful. Welcome, {user}.')
        return user
    else:
        print(f'Invalid username or passcode. Try again.')
        return None

def deposit(username):
    try:
        amount=float(input('Enter amount you want to deposit: '))
        if amount<=0:
            print('Amount must be more than 0. Try again.')
            return
        users[username]["balance"]+=amount
        users[username]["history"].append(f'Deposited ${amount}.')
    except ValueError:
        print('Invalid amount.')

def withdraw(username):
    try:
        w_amount=float(input('Enter the amount you would like to withdraw: '))
        if w_amount<=0:
            print('Withdraw must be more than 0. Try again.')
            return
        if w_amount>users[username]["balance"]:
            print("Insufficient funds.")
            return
        users[username]["balance"]-=w_amount
        users[username]["history"].append(f'Withdrew ${w_amount}')
    except ValueError:
        print('Invalid amount.')

def check_balance(username):
    balance=users[username]["balance"]
    print(f'Your balance is ${balance}.')

def show_transaction_history(username):
    history=users[username]["history"]
    if history:
        print("\n---Transaction History---")
        for entry in history:
            print(entry)
    else:
        print("No transactions yet.")



print('Welcome to the bank! You can deposit or withdraw money.')

while True:
    action = input('\nChoose an option: [register] [login] [quit]\n> ').strip().lower()

    if action.startswith('r'):
        register_user()
    elif action.startswith('l'):
        username = login_user()
        if username:
            while True:
                choice = input('\nWhat would you like to do? [deposit] [withdraw] [history] [balance] [logout]\n> ').strip().lower()
                if choice.startswith('d'):
                    deposit(username)
                elif choice.startswith('w'):
                    withdraw(username)
                elif choice.startswith('h'):
                    show_transaction_history(username)
                elif choice.startswith('b'):
                    check_balance(username)
                elif choice.startswith('l'):
                    print(f'Logged out of {username}.')
                    break
                else:
                    print('Invalid option.')
    elif action.startswith('q'):
        print('Goodbye!')
        sys.exit()
    else:
        print('Invalid choice. Try again.')
