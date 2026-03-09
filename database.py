import sqlite3
from datetime import datetime

DB_NAME = "email_ai.db"


# -----------------------------
# Database Connection
# -----------------------------
def get_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn


# -----------------------------
# Initialize Database
# -----------------------------
def init_db():

    conn = get_db()
    cursor = conn.cursor()

    # -----------------------------
    # USERS
    # -----------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # -----------------------------
    # CONVERSATIONS
    # -----------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS conversations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # -----------------------------
    # MESSAGES
    # -----------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        conversation_id INTEGER,
        role TEXT,
        content TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # -----------------------------
    # FEATURE USAGE
    # -----------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS feature_usage (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        feature_name TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # -----------------------------
    # METRICS EVENTS
    # -----------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS metrics_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_type TEXT,
        feature TEXT,
        tokens INTEGER,
        latency REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # -----------------------------
    # ERRORS
    # -----------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS errors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        error_message TEXT,
        location TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # -----------------------------
    # AI RESPONSE RATINGS
    # -----------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ratings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        conversation_id INTEGER,
        rating INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


# Initialize DB when file loads
init_db()


# -----------------------------
# USER FUNCTIONS
# -----------------------------
def get_user_id(session_id):

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT OR IGNORE INTO users(session_id) VALUES(?)",
        (session_id,)
    )

    conn.commit()

    cursor.execute(
        "SELECT id FROM users WHERE session_id=?",
        (session_id,)
    )

    user_id = cursor.fetchone()[0]

    conn.close()

    return user_id


# -----------------------------
# CONVERSATION FUNCTIONS
# -----------------------------
def create_conversation(user_id, title="New Chat"):

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO conversations(user_id, title) VALUES(?,?)",
        (user_id, title)
    )

    conn.commit()

    conv_id = cursor.lastrowid

    conn.close()

    return conv_id


# -----------------------------
# MESSAGE FUNCTIONS
# -----------------------------
def save_message(conversation_id, role, content):

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO messages(conversation_id, role, content) VALUES(?,?,?)",
        (conversation_id, role, content)
    )

    conn.commit()
    conn.close()


def load_messages(conversation_id):

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT role, content FROM messages WHERE conversation_id=?",
        (conversation_id,)
    )

    messages = cursor.fetchall()

    conn.close()

    return messages


# -----------------------------
# FEATURE TRACKING
# -----------------------------
def log_feature(feature):

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO feature_usage(feature_name) VALUES(?)",
        (feature,)
    )

    conn.commit()
    conn.close()


# -----------------------------
# METRICS LOGGING
# -----------------------------
def log_metrics(event_type, feature=None, tokens=0, latency=0):

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO metrics_events(event_type,feature,tokens,latency)
    VALUES(?,?,?,?)
    """, (event_type, feature, tokens, latency))

    conn.commit()
    conn.close()


# -----------------------------
# ERROR LOGGING
# -----------------------------
def log_error(message, location):

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO errors(error_message,location)
    VALUES(?,?)
    """, (message, location))

    conn.commit()
    conn.close()


# -----------------------------
# AI RATING
# -----------------------------
def save_rating(conversation_id, rating):

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO ratings(conversation_id,rating)
    VALUES(?,?)
    """, (conversation_id, rating))

    conn.commit()
    conn.close()