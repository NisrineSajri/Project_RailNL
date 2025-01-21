import os
import sys

# Get the path to the code directory (parent of tests directory)
code_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the code directory to Python path
sys.path.append(code_dir)