import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# 1. Load environment variables from .env file
load_dotenv()

# Read credentials
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "Embula")

def create_database_if_not_exists():
    """
    Connects to MySQL server (without selecting a specific DB)
    and creates the database if it doesn't exist.
    """
    # Connection URL without database name
    # Format: mysql+mysqlconnector://user:password@host:port
    server_url = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}"
    
    print(f"Connecting to MySQL server at {DB_HOST}:{DB_PORT}...")
    
    # Create engine for the server connection
    engine = create_engine(server_url)
    
    try:
        # Use raw connection to avoid SQLAlchemy transaction wrapping for CREATE DATABASE
        # and to bypass isolation_level issues with some drivers
        conn = engine.raw_connection()
        try:
            cursor = conn.cursor()
            print(f"Checking if database '{DB_NAME}' exists...")
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
            print(f"Database '{DB_NAME}' ensured.")
            cursor.close()
            conn.commit()
        finally:
            conn.close()
    except Exception as e:
        print(f"Error creating database: {e}")
        raise
    finally:
        engine.dispose()

def test_connection():
    """
    Connects to the specific database to verify everything is working.
    """
    # Connection URL WITH database name
    # Format: mysql+mysqlconnector://user:password@host:port/dbname
    db_url = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    print(f"Connecting to database '{DB_NAME}'...")
    
    engine = create_engine(db_url)
    
    try:
        with engine.connect() as conn:
            # Simple query to verify connection
            result = conn.execute(text("SELECT 1"))
            print("Successfully connected to the database!")
            
            # Verify the actual database name we are connected to
            db_name_result = conn.execute(text("SELECT DATABASE()"))
            current_db = db_name_result.scalar()
            print(f"Current Database: '{current_db}'")
            
            if current_db == DB_NAME:
                print(f"✅ VERIFIED: Connected to '{DB_NAME}'")
            else:
                print(f"❌ WARNING: Connected to '{current_db}' instead of '{DB_NAME}'")
    except SQLAlchemyError as e:
        print(f"Error connecting to database: {e}")
    finally:
        engine.dispose()

if __name__ == "__main__":
    print("--- Starting Database Connection Test ---")
    try:
        create_database_if_not_exists()
        test_connection()
        print("--- Test Completed Successfully ---")
    except Exception as e:
        print(f"--- Test Failed: {e} ---")
