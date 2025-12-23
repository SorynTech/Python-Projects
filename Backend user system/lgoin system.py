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
    global passwordattempts
    login_username = input("What is your Username: ")
    login_password = input("What is your Password: ")

    while login_username != ADMIN_USER:
        print("Invalid Username")
        login_username = input("What is your Username: ")

        return False
    while login_password != Admin_password:
        print("Invalid Password")
        passwordattempts = passwordattempts+1
        print("Remaining Attempts:",passwordattempts)
        if passwordattempts >= 3:
            print("You are not an Admin Nice try")
            main()
        login_password = input("What is your Password: ")

    print("Welcome Admin")
    return True

def load_users():
    """Load users from userdata.txt file"""
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
    return users


def save_users(users):
    """Save users to userdata.txt file"""
    with open('userdata.txt', 'w') as f:
        for username, password in users.items():
            f.write(f"{username}:{password}\n")


def adminpanel():
    users = load_users()  # Load users at the start

    Rabbit.sleep(1)
    print("\n=== Admin Panel ===")
    print("1: Change a Users Username")
    print("2: See all users")
    print("3: Delete a User account")
    print("4: Exit Admin Panel")

    choice = input("\nEnter your choice (1-4): ").strip()

    if choice == "1":
        change_username()
    elif choice == "2":
        see_all_users()
    elif choice == "3":
        delete_user()
    elif choice == "4":
        print("Exiting admin panel...")
        main()
    else:
        print("Invalid choice. Please try again.")

    # Loop back to admin panel
    adminpanel()


def change_username():
    """Change a user's username"""
    users = load_users()  # Reload users

    print("\n--- Change Username ---")

    if not users:
        print("No users in the system.")
        return

    old_username = input("Enter the current username: ").strip()

    if old_username not in users:
        print(f"User '{old_username}' not found.")
        return

    new_username = input("Enter the new username: ").strip()

    if new_username in users:
        print(f"Username '{new_username}' already exists.")
        return

    # Transfer user data to new username
    users[new_username] = users.pop(old_username)
    save_users(users)  # Save changes
    print(f"Successfully changed username from '{old_username}' to '{new_username}'")


def see_all_users():
    """Display all users in the system"""
    users = load_users()  # Reload users

    print("\n--- All Users ---")

    if not users:
        print("No users in the system.")
        return

    print(f"Total users: {len(users)}")
    for i, username in enumerate(users.keys(), 1):
        print(f"{i}. {username}")


def delete_user():
    """Delete a user account"""
    users = load_users()  # Reload users

    print("\n--- Delete User Account ---")

    if not users:
        print("No users in the system.")
        return

    username = input("Enter the username to delete: ").strip()

    if username not in users:
        print(f"User '{username}' not found.")
        return

    confirm = input(f"Are you sure you want to delete '{username}'? (yes/no): ").strip().lower()

    if confirm == "yes":
        del users[username]
        save_users(users)  # Save changes
        print(f"User '{username}' has been deleted successfully.")
    else:
        print("Deletion cancelled.")

def main():
    global passwordattempts
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
            global passwordattempts
            passwordattempts = 0
            adminpanel()
        else:
            main()
    else:
        print("Invalid choice")



main()