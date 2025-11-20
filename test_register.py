import runpy
import uuid
from pathlib import Path

# Load the module as a script to access its functions/variables
mod = runpy.run_path('Authentication system.py')
register_user = mod['register_user']
USERS_FILE = mod['USERS_FILE']

username = 'testuser_' + uuid.uuid4().hex[:6]
password = 'Password1A'

print(f"Registering user: {username}")
register_user(username, password)

print(f"Users file: {USERS_FILE}")
with open(USERS_FILE, 'r', encoding='utf-8') as f:
    lines = [l.strip() for l in f.readlines() if l.strip()]

print('Last entry in users.txt:')
print(lines[-1])
