import os
import time as Rabbit

passwordattempts = 0


def load_env_file(filepath='.env'):
    """Load variables from .env file into os.environ"""
    if not os.path.exists(filepath):
        print(f"Warning: {filepath} not found")
        return

    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            # Skip empty lines and comments
            if line and not line.startswith('#'):
                # Split on first = sign
                if '=' in line:
                    key, value = line.split('=', 1)
                    # Remove quotes if present
                    value = value.strip().strip('"').strip("'")
                    # Set in os.environ so it's accessible everywhere
                    os.environ[key.strip()] = value


# Load the variables
load_env_file()

# Now it will work with os.getenv()
Admin_password = os.getenv('ADMIN_PASSWORD')
ADMIN_USER = os.getenv('ADMIN_USERNAME')
login_secret = os.getenv('LOGIN_SECRET')

if Admin_password:
    print("Password found!")
else:
    print("Password not found")
if ADMIN_USER:
    print("Username found!")
else:
    print("Username not found")
if login_secret:
    print("secret found!")
else:
    print("secret not found")


def signup():
    # Load existing users
    users = {}
    try:
        with open('userdata.txt', 'r') as f:
            for line in f:
                line = line.strip()
                if ':' in line:
                    username, password = line.split(':')
                    users[username] = password
    except FileNotFoundError:
        # File doesn't exist yet, that's okay
        pass

    username = input("What do you want your username to be: ")

    # Check username length (max 12 characters)
    while len(username) > 12:
        print("Username too long (max 12 characters)")
        username = input("What do you want your username to be: ")

    # Check if username already exists
    if username in users:
        print("Username already taken!")
        return

    print("Username ok")

    password = input("What would you like to be your password: ")

    # Check password length (min 8 characters)
    while len(password) < 8:
        print("Password too short (min 8 characters)")
        password = input("What would you like to be your password: ")

    print("Password Accepted")

    # Add new user to dictionary
    users[username] = password

    # Write all users back to file
    with open('userdata.txt', 'w') as f:
        for user, pwd in users.items():
            f.write(f"{user}:{pwd}\n")

    print("Signup successful!")


def login():
    global passwordattempts

    username_login = input("What is your Username: ")
    password_login = input("What is your Password: ")

    # Load all users into a dictionary
    users = {}
    try:
        with open('userdata.txt', 'r') as file:
            for line in file:
                line = line.strip()
                if ':' in line:
                    username, password = line.split(':')
                    users[username] = password
    except FileNotFoundError:
        print("No users found. Please sign up first!")
        return False

    # Check login credentials
    if username_login in users:
        if users[username_login] == password_login:
            print("Login successful!")
            print("Welcome " + username_login + "!")
            passwordattempts = 0  # Reset on successful login
            return True
        else:
            print("Incorrect password")
            passwordattempts += 1
            if passwordattempts >= 3:
                print("Access denied - too many failed attempts")
                exit()
            return False
    else:
        print("Username not found")
        return False


def adminlogin():
    login_username = input("What is your Username: ")
    login_password = input("What is your Password: ")

    if login_username != ADMIN_USER:
        print("Invalid Username")
        return False
    if login_password != Admin_password:
        print("Invalid Password")
        return False

    print("Welcome Admin")
    return True


def main():
    print("1. Signup")
    print("2. Login")
    choice = input("Choose: ")

    if choice == "1":
        signup()
    elif choice == "2":
        if login():
            print("Welcome! You are now logged in.")
            # Continue with your program
        else:
            print("Login failed. Please try again.")
    elif choice == login_secret:
        if adminlogin():
            print("Admin access granted!")
        else:
            print("Admin login failed.")
    else:
        print("Invalid choice")

main()