import asyncio
from database import create_db_and_tables

def startup():
    """Initialize the database on startup"""
    print("Initializing database tables...")
    create_db_and_tables()
    print("Database initialized successfully!")

if __name__ == "__main__":
    startup()