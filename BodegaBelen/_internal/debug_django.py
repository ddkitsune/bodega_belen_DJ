import os
import django
import sys

print("Setting up environment...")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bodega_belen.settings')
print(f"Python executable: {sys.executable}")
print(f"CWD: {os.getcwd()}")

try:
    print("Running django.setup()...")
    django.setup()
    print("Django setup complete.")
except Exception as e:
    print(f"Error during setup: {e}")
