import time
import psycopg2
import psycopg2.pool
from psycopg2 import OperationalError
from .common import log_error, log_debug
from .config import config

# Configuration for the connection pool
MIN_CONN = 10
MAX_CONN = 50

# Initialize db_pool at the module level
db_pool = None

def init_db_connection_pool():
    global db_pool
    try:
        db_pool = psycopg2.pool.SimpleConnectionPool(
            MIN_CONN,
            MAX_CONN,
            database=config.db_name,
            user=config.db_user,
            password=config.db_password,
            host=config.db_host,
            port=config.db_port
        )
        if db_pool:
            log_debug("Connection pool created successfully")
    except OperationalError as e:
        log_error(f"Error creating connection pool: {e}")
        raise

def get_db_connection(retry=3, delay=5):
    global db_pool
    if db_pool is None:
        init_db_connection_pool()
    
    conn = None
    while retry > 0:
        try:
            conn = db_pool.getconn()
            if conn:
                log_debug("Successfully retrieved a connection from the pool")
                return conn
        except OperationalError as e:
            log_error(f"Failed to retrieve a connection. Retrying in {delay} seconds...", e)
            time.sleep(delay)
            retry -= 1
    raise Exception("Failed to retrieve a connection from the pool after several attempts.")

def store_emails(emails, batch_size=30):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "INSERT INTO emails (user_id, message_id, sender, receiver, subject, message, received_at, history_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (message_id) DO NOTHING"
        batch = []

        for email in emails:
            batch.append((email.user_id, email.message_id, email.sender, email.receiver, email.subject, email.message, email.received_at, email.history_id))

            if len(batch) == batch_size:
                cursor.executemany(query, batch)
                conn.commit()
                batch = []

        if batch:
            cursor.executemany(query, batch)
            conn.commit()

        cursor.close()
        conn.close()
    except Exception as e:
        log_error("Error storing emails in the database", e)

def store_credentials(email, encrypted_creds):
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("INSERT INTO users (email, token, is_active) VALUES (%s, %s, %s) ON CONFLICT (email) DO UPDATE SET token = EXCLUDED.token", 
                  (email, encrypted_creds, True))
        conn.commit()
    except Exception as e:
        log_error("Error storing credentials in the database", e)
    finally:
        if conn:
            conn.close()

def fetch_credentials(email):
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT id, token FROM users WHERE email = %s", (email,))
        result = c.fetchone()
        if result:
            user_id, token = result
        else:
            user_id, token = None, None
        return user_id, token
    except Exception as e:
        log_error("Error fetching credentials from the database", e)
        raise
    finally:
        if conn:
            conn.close()

def select_email_asread():
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT message_id FROM emails WHERE is_read = TRUE")
        message_data = []
        result = c.fetchall()
        for (message_id,) in result:
            message_data.append(message_id)
        return message_data
    except Exception as e:
        log_error("Error fetching credentials from the database", e)
        raise
    finally:
        if conn:
            conn.close()
