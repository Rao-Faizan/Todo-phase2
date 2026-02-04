import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import models in a controlled way to avoid conflicts
import warnings
from sqlalchemy.exc import SAWarning
warnings.filterwarnings("ignore", category=SAWarning)

# Import other necessary modules after path setup