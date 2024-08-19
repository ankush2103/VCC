import sys
import os
from pathlib import Path

# Add the virtual environment's site-packages to sys.path
sys.path.insert(0, '/var/www/myapp/venv/lib/python3.8/site-packages')

# Add your application's directory to the sys.path
sys.path.insert(0, '/var/www/myapp')

# Load the Flask app
from app import app as application
