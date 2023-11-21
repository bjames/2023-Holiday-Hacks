import sqlite3
import secrets

DB_FILE = "user.db"

def generate_password():
    """
    Generate something resembling a password.

    For this CTF we don't actually care about the
    password, we're really just after the SQL injection.
    """
    return secrets.token_hex(8)

def check_password(username, password) -> str | None:
    """
    Check if the given username/password combination is valid.

    This function is purposely vulnerable to SQL injection.
    """
    conn = sqlite3.connect(f"{DB_FILE}?mode=ro") # open the database in read-only mode
    c = conn.cursor()
    c.execute(f"SELECT * FROM users WHERE username='{username}' AND password='{password}'")
    result = c.fetchone()
    print(result)
    conn.close()

    return result

def create_db():
    """
    Create the database and populate it with some users.
    """

    users_data = (
        {"username": "alice", "password": generate_password()},
        {"username": "bob", "password": generate_password()},
        {"username": "charlie", "password": generate_password()},
        {"username": "dave", "password": generate_password()},
        {"username": "eve", "password": generate_password()},
        {"username": "frank", "password": generate_password()},
        {"username": "grace", "password": generate_password()},
        {"username": "heidi", "password": generate_password()},
        {"username": "ivan", "password": generate_password()},
        {"username": "judy", "password": generate_password()},
        {"username": "kevin", "password": generate_password()},
        {"username": "larry", "password": generate_password()},
        {"username": "mallory", "password": generate_password()},
        {"username": "ned", "password": generate_password()},
        {"username": "olivia", "password": generate_password()},
        {"username": "peggy", "password": generate_password()},
        {"username": "quinn", "password": generate_password()},
        {"username": "rob", "password": generate_password()},
        {"username": "steve", "password": generate_password()},
        {"username": "trent", "password": generate_password()},
        {"username": "ursula", "password": generate_password()},
        {"username": "victor", "password": generate_password()},
        {"username": "wendy", "password": generate_password()},
        {"username": "xavier", "password": generate_password()},
        {"username": "yvonne", "password": generate_password()},
        {"username": "zelda", "password": generate_password()},
    )

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    print(users_data)
    c.execute("CREATE TABLE IF NOT EXISTS users (username text, password text)")
    c.executemany("INSERT INTO users VALUES(:username, :password)", users_data)
    print(c.fetchall())

    conn.commit()
    conn.close()