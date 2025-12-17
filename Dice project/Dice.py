import os
def load_env_file(filepath='.env'):
    """Load variables from .env file into a dictionary"""
    env_vars = {}

    if not os.path.exists(filepath):
        return env_vars

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
                    env_vars[key.strip()] = value

    return env_vars


# Usage
env_vars = load_env_file()
password = env_vars.get('PASSWORD')

if password:
    print("Password found!")
else:
    print("Password not found")