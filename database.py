import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime

# Load credentials from the .env file
load_dotenv()

class DatabaseLogger:
    def __init__(self):
        self.conn = None
        self.connect()
        self.create_table()

    def connect(self):
        """Establishes a connection to the PostgreSQL database."""
        try:
            self.conn = psycopg2.connect(
                host=os.getenv("DB_HOST"),
                database=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                port=os.getenv("DB_PORT")
            )
            self.conn.autocommit = True
            print("Successfully connected to the PostgreSQL database.")
        except Exception as e:
            print(f"Database connection failed: {e}")

    def create_table(self):
        """Creates the logging table (and forces a reset to fix the VARCHAR limit)."""
        if not self.conn:
            return
            
        create_table_query = """
        DROP TABLE IF EXISTS attack_logs; -- This nukes the old broken table!
        
        CREATE TABLE attack_logs (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP NOT NULL,
            prompt TEXT NOT NULL,
            layer_failed VARCHAR(255) NOT NULL,
            threat_score FLOAT NOT NULL
        );
        """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(create_table_query)
                print("Attack logs table successfully reset and ready.")
        except Exception as e:
            print(f"Error creating table: {e}")

    def log_attack(self, prompt, layer_failed, threat_score):
        """Inserts a blocked attack into the database."""
        if not self.conn:
            print("Cannot log: No database connection.")
            return

        insert_query = """
        INSERT INTO attack_logs (timestamp, prompt, layer_failed, threat_score)
        VALUES (%s, %s, %s, %s);
        """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(insert_query, (datetime.now(), prompt, layer_failed, threat_score))
                print(f"[DB LOG]: Malicious prompt safely logged to database.")
        except Exception as e:
            print(f"Error inserting log: {e}")

# Quick Test
if __name__ == "__main__":
    db = DatabaseLogger()
    # Let's insert a fake attack to make sure it works!
    db.log_attack("system prompt bypass test", "Layer 1: Heuristics", 10.0)