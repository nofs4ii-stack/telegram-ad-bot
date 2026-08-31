import os
from dotenv import load_dotenv
from supabase import create_client, Client
import logging

# Load environment variables from .env if it exists
load_dotenv()

# Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

# Initialize client
try:
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("Supabase environment variables not set.")
    
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    logging.info("Supabase client initialized.")
except Exception as e:
    logging.error(f"Failed to initialize Supabase client: {e}")
    supabase = None

def check_db_connection():
    """
    Tests reading from the 'ads' table to verify connection.
    Returns True if successful, False otherwise.
    """
    if not supabase:
        logging.error("Supabase client not available.")
        return False

    try:
        # Perform a simple query (limit to 1 to minimize overhead)
        response = supabase.table("ads").select("*").limit(1).execute()
        logging.info("Supabase connection health check passed.")
        return True
    except Exception as e:
        logging.error(f"Supabase connection health check failed: {e}")
        return False
