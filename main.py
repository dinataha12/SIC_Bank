import json
import re
import os

USER_FILE = 'users.json'

def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, 'r') as file:
        return json.load(file)

def save_users(users):
    with open(USER_FILE, 'w') as file:
        json.dump(users, file, indent=4)

def find_user(users, user_id):
    for user in users:
        if user['id'] == user_id:
            return user
    return None

def get_next_user_id(users):
    if not users:
        return 1
    return max(int(uid) for uid in users.keys()) + 1

exchange_rates = {
    "USD": 30,
    "SAR": 8,
    "EGP": 1
}

def register(users):
    print("\n***************************Welcome to the sign up page****************************\n")
    name = input("Please enter your name: ")
    password = input("Please enter your password: ")
    phone = input("Please enter your phone number: ")
    email = input("Please enter your email: ")
    gender = input("Please enter your gender: ")
    age = input("Please enter your age: ")
    city = input("Please enter your city: ")


    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        print("Invalid email format. Please try again.")
        return

    user_id = get_next_user_id(users)
    users[str(user_id)] = {
        "name": name,
        "password": password,
        "phone": phone,
        "email": email,
        "gender": gender,
        "age": age,
        "city": city,
        "balance": 0
    }
    save_users(users)
    print(f"Sign up successfully, your ID is {user_id}")

def login(users):
    print("\n**********************Welcome to the login page***********************\n")
    user_id = input("Please enter your ID: ")
    password = input("Please enter your password: ")

    if user_id in users and users[user_id]["password"] == password:
        print(f"Welcome back {users[user_id]['name']}")
        return user_id
    else:
        print("Invalid ID or password. Please try again.")
        return None

def deposit(users, user_id):
    print("Please enter the amount you want to deposit and the currency in this format 'amount currency'")
    input_str = input().strip()
    try:
        amount, currency = input_str.split()
        amount = float(amount)
        if currency not in exchange_rates:
            print("Unsupported currency. Please try again.")
            return
        egp_amount = amount * exchange_rates[currency]
        users[user_id]["balance"] += egp_amount
        save_users(users)
        print(f"{amount} {currency} was deposited successfully!")
        print(f"Your balance is {users[user_id]['balance']} EGP")
    except Exception as e:
        print("Invalid input format. Please try again.")

def withdraw(users, user_id):
    print("Please enter the amount you want to withdraw and the currency in this format 'amount currency'")
    input_str = input().strip()
    try:
        amount, currency = input_str.split()
        amount = float(amount)
        if currency not in exchange_rates:
            print("Unsupported currency. Please try again.")
            return
        egp_amount = amount * exchange_rates[currency]
        if users[user_id]["balance"] >= egp_amount:
            users[user_id]["balance"] -= egp_amount
            save_users(users)
            print(f"{amount} {currency} was withdrawn successfully!")
            print(f"Your balance is {users[user_id]['balance']} EGP")
        else:
            print("Insufficient funds. Please try again.")
    except Exception as e:
        print("Invalid input format. Please try again.")



def transfer_money(users, user_id, to_user_id, amount):
    from_user = find_user(users, user_id)
    to_user = find_user(users, to_user_id)

    if not from_user:
        print(f"User with ID {user_id} does not exist.")
        return False

    if not to_user:
        print(f"User with ID {to_user_id} does not exist.")
        return False

    if amount > users[str(user_id)]['balance']:
        print("Insufficient balance.")
        return False

    users[str(user_id)]['balance'] -= amount
    users[str(to_user_id)]['balance'] += amount

    print(f"{amount} EGP was transferred to {users[str(to_user_id)]['name']} successfully!!")
    print(f"Your balance is {users[str(user_id)]['balance']} EGP")
    return True


def main():
    users = load_users()
    while True:
        print("\n**********************Welcome to SIC bank management system*******************\n")
        print("If you already have an account, please enter 'login'")
        print("If you don't have an account, please enter 'register'")
        choice = input().strip().lower()

        if choice == 'login':
            user_id = login(users)
            if user_id:
                while True:
                    print("Enter 'deposit' to deposit money\nEnter 'withdraw' to withdraw money\nEnter 'transfer' to transfer money \nEnter 'info' to check your information: \nEnter 'logout' to logout")

                    action = input().strip().lower()
                    if action == 'deposit':
                        deposit(users, user_id)
                    elif action == 'withdraw':
                        withdraw(users, user_id)
                    elif action == 'transfer':
                        user_id = int(input("Please enter your user ID: "))
                        amount = int(input("Please enter the amount you want to transfer: "))
                        to_user_id = int(input("Please enter the ID of the user you want to transfer money to: "))
                        if transfer_money(users, user_id, to_user_id, amount):
                            save_users(users)

                    elif action == 'info':
                        print(f"ID: {user_id}")
                        print(f"Name: {users[user_id]['name']}")
                        print(f"Phone: {users[user_id]['phone']}")
                        print(f"Mail: {users[user_id]['email']}")
                        print(f"Age: {users[user_id]['age']}")
                        print(f"Gender: {users[user_id]['gender']}")
                        print(f"City: {users[user_id]['city']}")
                        print(f"Balance: {users[user_id]['balance']} EGP")


                    elif action == 'logout':
                        break
                    else:
                        print("Invalid choice. Please enter 'deposit', 'withdraw', 'transfer', 'info', or 'logout'.")
        elif choice == 'register':
            register(users)
        else:
            print("Invalid choice. Please enter 'login' or 'register'.")


main()
