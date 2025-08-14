import sqlite3
import hashlib

def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    # Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    # Profiles Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            left_click_action TEXT DEFAULT '',
            right_click_action TEXT DEFAULT '',
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        hashed = hash_password(password)
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
        conn.commit()

        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        user_id = cursor.fetchone()[0]
        conn.commit()

        cursor.execute("INSERT into profiles (user_id, name, left_click_action, right_click_action) VALUES (?, ?, ?, ?)",
                       (user_id, "Profile1", "Left blink", "Right blink")
                       )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def validate_login(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    hashed = hash_password(password)
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed))
    user = cursor.fetchone()
    conn.close()
    return user 

def show_all_users():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

def get_user_id(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    
    if not row and username == "Guest":
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, ""))
        conn.commit()
        cursor.execute("SELECT id from users WHERE username = ?", (username,))
        row = cursor.fetchone()
    
    conn.close()
    return row[0] if row else None

def add_profile(user_id, name, left_click_action="", right_click_action=""):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO profiles (user_id, name, left_click_action, right_click_action) values (?, ?, ?, ?)", (user_id, name, left_click_action, right_click_action))
    conn.commit()
    conn.close()

def get_profiles(user_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM profiles WHERE user_id = ?", (user_id,))
    profiles = cursor.fetchall()
    conn.close()
    return profiles

def update_profile_name(profile_id, new_name):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE profiles SET name = ? WHERE id = ?", (new_name, profile_id))
    conn.commit()
    conn.close()

def delete_profile(profile_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM profiles WHERE id = ?", (profile_id,))
    conn.commit()
    conn.close()

def get_profile_settings(profile_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT left_click_action, right_click_action FROM profiles WHERE id = ?", (profile_id, ))
    settings = cursor.fetchone()
    conn.close()
    return settings
