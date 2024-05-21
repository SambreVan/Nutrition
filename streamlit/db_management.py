# db_management.py
import sqlite3
import bcrypt
import os

def connect_db():
    return sqlite3.connect('users.db')

def create_usertable():
    with connect_db() as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                hashed_password TEXT,
                first_name TEXT,
                last_name TEXT,
                age INTEGER,
                sex TEXT,
                profile_image TEXT
            )
        ''')
        conn.commit()

def create_weight_table():
    with connect_db() as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS weight_tracking(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                date TEXT,
                weight REAL,
                FOREIGN KEY(username) REFERENCES users(username)
            )
        ''')
        conn.commit()

def create_tables():
    create_usertable()
    create_weight_table()

def add_userdata(username, password, first_name, last_name, age, sex, profile_image):
    with connect_db() as conn:
        c = conn.cursor()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        if profile_image is not None:
            file_path = save_image(profile_image)
        else:
            file_path = None
        c.execute('''
            INSERT INTO users(username, hashed_password, first_name, last_name, age, sex, profile_image)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (username, hashed_password, first_name, last_name, age, sex, file_path))
        conn.commit()

def save_image(image_file):
    if image_file is not None:
        base_path = "./profile_images"
        if not os.path.exists(base_path):
            os.makedirs(base_path)
        file_path = os.path.join(base_path, image_file.name)
        with open(file_path, "wb") as f:
            f.write(image_file.getbuffer())
        return file_path
    return None

def login_user(username, password):
    with connect_db() as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ?', (username,))
        user_data = c.fetchone()
        if user_data:
            hashed_password = user_data[2]
            if isinstance(hashed_password, str):
                hashed_password = hashed_password.encode('utf-8')
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                return user_data
        return None

def get_user_data(username):
    with connect_db() as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ?', (username,))
        user_data = c.fetchone()
        return user_data

def get_latest_weight(username):
    with connect_db() as conn:
        c = conn.cursor()
        c.execute('''
            SELECT weight FROM weight_tracking 
            WHERE username = ? ORDER BY date DESC LIMIT 1
        ''', (username,))
        weight = c.fetchone()
        return weight[0] if weight else None
