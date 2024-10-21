import sqlite3
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

def create_tables():
    """Create the necessary tables in the database."""
    try:
        # Database connection
        with sqlite3.connect("helper/database.db") as conn:
            cur = conn.cursor()

            # Create the 'ticketing_setup' table if it doesn't exist
            cur.execute("""
                CREATE TABLE IF NOT EXISTS ticketing_setup (
                    guild_id INTEGER PRIMARY KEY,
                    ticket_category_id INTEGER NOT NULL,
                    log_channel_id INTEGER NOT NULL,
                    moderator_roles TEXT,
                    github_username TEXT NOT NULL,
                    repository_name TEXT NOT NULL,
                    github_token TEXT NOT NULL
                )
            """)

            # Commit changes to the database
            conn.commit()

            logging.info("Successfully created or verified the 'ticketing_setup' table.")
    
    except sqlite3.Error as e:
        logging.error(f"An error occurred while creating the table: {e}")

def close_connection(cur, conn):
    """Close the database connection and cursor."""
    if cur:
        cur.close()
    if conn:
        conn.close()