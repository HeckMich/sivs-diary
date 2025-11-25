import logging
import os
import psycopg2
from dotenv import load_dotenv, find_dotenv
from psycopg2 import sql

logging.basicConfig(level=logging.INFO)
load_dotenv(find_dotenv())
DB_CONFIG = {
    "dbname": os.environ.get("POSTGRES_DB"),
    "user": os.environ.get("POSTGRES_USER"),
    "password": os.environ.get("POSTGRES_PASSWORD"),
    "host": os.environ.get("POSTGRES_HOST", "localhost"),
    "port": os.environ.get("POSTGRES_PORT", "5432")
}


def execute_query(query, values=(), fetch=True):
    """
    Connects to the DB, executes a query, commits if successful, and returns results.
    Handles connection lifecycle for each query.
    """
    conn = None
    try:
        # 1. Establish connection
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # 2. Execute query with parameterization (security fix)
        cursor.execute(query, values)

        # 3. Commit changes (DML/DDL operations)
        conn.commit()

        # 4. Fetch and return results if requested
        if fetch and cursor.description:
            return cursor.fetchall()

        return True  # Return True for successful non-SELECT operations

    except (psycopg2.Error, Exception) as ex:
        logging.error("Database Query Error: %s", ex)
        # 5. Rollback on error
        if conn:
            conn.rollback()
        return None
    finally:
        # 6. Close connection
        if conn:
            conn.close()


def create_tables():
    """Initializes the database with Users and DiaryEntries tables."""
    logging.info("Attempting to create tables...")

    # Using 'IF NOT EXISTS' prevents errors if tables already exist.
    create_users_table = f"""
                CREATE TABLE IF NOT EXISTS Users (
                        id SERIAL PRIMARY KEY,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        secret_question TEXT NOT NULL,
                        secret_answer TEXT NOT NULL
                    );
                         """

    create_diary_entries_table = f"""
       CREATE TABLE IF NOT EXISTS DiaryEntries (
            id SERIAL PRIMARY KEY,
            entry_title TEXT NOT NULL,
            entry_content TEXT NOT NULL,
            entry_date TEXT NOT NULL,
            user_id INTEGER REFERENCES Users(id)
        );                      
                                 """

    execute_query(create_users_table, fetch=False)
    execute_query(create_diary_entries_table, fetch=False)
    logging.info("Tables checked/created successfully.")


def populate_sample_data():
    """Inserts sample users and diary entries."""
    logging.info("Inserting sample data...")

    # 1. Insert Users
    insert_user_query = "INSERT INTO Users (username, password, secret_question, secret_answer) VALUES (%s, %s, %s, %s) RETURNING id"

    # Execute query and capture the returned ID (RETURNING id)
    alice_id_result = execute_query(insert_user_query, ('alice', 'password123', 'Was ist mein Lieblingstier?', 'Hund'))
    bob_id_result = execute_query(insert_user_query, ('bob', 'securepwd', 'Was ist 7+7?', '14'))
    charlie_id_result = execute_query(insert_user_query, ('charlie', 'pass123word', 'Welches Auto fahre ich?', 'BMW'))

    # Check if insertion was successful and extract IDs
    alice_id = alice_id_result[0][0] if alice_id_result else None
    bob_id = bob_id_result[0][0] if bob_id_result else None
    charlie_id = charlie_id_result[0][0] if charlie_id_result else None

    if not all([alice_id, bob_id, charlie_id]):
        logging.error("Failed to insert all users or retrieve IDs.")
        return

    # 2. Insert Diary Entries
    # Note: Removed "COMMIT;" from the query string. The function handles the commit.
    insert_entry_query = "INSERT INTO DiaryEntries (entry_title, entry_content, user_id, entry_date) VALUES (%s, %s, %s, %s)"

    # Entries for Alice
    execute_query(insert_entry_query, ("Lovely Day", "Today was a good day.", alice_id, "2022-11-11"), fetch=False)
    execute_query(insert_entry_query, ("New Coffee", "Visited the new cafe in town.", alice_id, "2022-11-12"),
                  fetch=False)  # Changed date to avoid duplicate entries

    # Entries for Bob
    execute_query(insert_entry_query, ("New Project", "Worked on a new project.", bob_id, "2022-11-13"), fetch=False)
    execute_query(insert_entry_query, ("Watched a movie", "Watched a movie at home.", bob_id, "2022-11-14"),
                  fetch=False)

    # Entries for Charlie
    execute_query(insert_entry_query, ("A walk", "Took a long walk in the park.", charlie_id, "2022-11-15"),
                  fetch=False)
    execute_query(insert_entry_query, ("Dinner with friends", "Cooked dinner for friends.", charlie_id, "2022-11-16"),
                  fetch=False)

    logging.info("Sample data inserted successfully.")


if __name__ == '__main__':
    # 💥 NOTE: The previous script's execute_query("COMMIT;", None) was incorrect and removed.
    # COMMIT is handled automatically within the execute_query function.

    create_tables()
    populate_sample_data()
