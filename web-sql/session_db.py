import sqlite3
import secrets

from datetime import datetime
from hashlib import sha256

DB_FILE = "session.db"

SHARED_KEY = secrets.token_hex(16)

def generate_token(username):
    """
    Generate a session token for the given username.
    """
    return sha256(f"{username}{SHARED_KEY}{datetime.now()}".encode()).hexdigest()

def add_session(username):
    """
    Add a session for the given username.
    """
    token = generate_token(username)

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO sessions VALUES (?, ?)", (username, token))
    conn.commit()
    conn.close()

    return token

def check_session(token) -> str:
    """
    Check if the given session token is valid.
    """
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT username FROM sessions WHERE token=?", (token,))
    result = c.fetchone()
    conn.close()

    if result:
        return result[0]
    else:
        return ""

def create_db():
    """
    Create the database
    """
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS sessions (username TEXT, token TEXT)")
    conn.commit()
    conn.close()