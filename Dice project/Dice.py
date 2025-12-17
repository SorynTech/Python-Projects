import os
import random
from fileinput import close

badeffects=("give one coin to player next to you","no turn","reverse turn order","go back the amount of spaces you rolled")
goodeffects=("take one coin","take another turn","go forwards +4","Roll for next player")
goodeffect=random.choice(goodeffects)
badeffect=random.choice(badeffects)
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
password = os.getenv('PASSWORD')

if password:
    print("Password found!")
else:
    print("Password not found")
#storing dicerolls
open(f'dicerolls.txt', 'a').close()
#DICE here
def diceroll():
    diceroll=random.randint(1,6)
    goodchance=random.randint(1,100)
    badchance=random.randint(1,100)
    gchance=str(goodchance)
    bchance=str(badchance)
    droll=str(diceroll)
    with open('dicerolls.txt', 'a') as f:
        f.write(f"good chance: {gchance} \n Bad chance:{bchance} \n final roll: \n {droll}")
        open(f'dicerolls.txt', 'a').close()
    if goodchance>badchance:
        diceroll=diceroll+1
        print(diceroll)
        print(goodeffect)
    if badchance>goodchance:
        diceroll=diceroll-1
        print(diceroll)
        print(badeffect)
def gooddice():
    passwordprotection=input("What is the password")
    if passwordprotection != password:
        print("Passwords do not match")
        user_input = input("Would you Like to Roll the Random, Good Or bad dice")
    else:
        print(goodeffect)
        diceroll=random.randint(1,6)
        diceroll=diceroll+1
        droll=str(diceroll)
        with open('dicerolls.txt', 'a') as f:
            f.write(f"final roll: \n {droll}")
        open(f'dicerolls.txt', 'a').close()

def baddice():
    passwordprotection=input("What is the password")
    if passwordprotection != password:
        print("Passwords do not match")
    else:
        print(badeffect)
        diceroll=random.randint(1,6)
        diceroll=diceroll-1
        droll=str(diceroll)
        with open('dicerolls.txt', 'a') as f:
            f.write(f"final roll: \n {droll}")
        open(f'dicerolls.txt', 'a').close()

user_input=input("Would you Like to Roll the Random, Good Or bad dice")
if user_input == "Random":
    diceroll()
    exit()
if user_input == "Good":
    gooddice()
    exit()
else:
    baddice()
    exit()