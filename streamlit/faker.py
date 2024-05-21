import sqlite3
import bcrypt
from datetime import datetime, timedelta
import random
import uuid

# Connexion à la base de données
def connect_db():
    return sqlite3.connect('users.db')

# Création des tables si elles n'existent pas
def create_tables():
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

# Ajout des données utilisateur
def add_userdata(username, password, first_name, last_name, age, sex, profile_image=None):
    with connect_db() as conn:
        c = conn.cursor()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        c.execute('''
            INSERT INTO users(username, hashed_password, first_name, last_name, age, sex, profile_image)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (username, hashed_password, first_name, last_name, age, sex, profile_image))
        conn.commit()

# Ajout des données de poids
def add_weight_data(username, date, weight):
    with connect_db() as conn:
        c = conn.cursor()
        c.execute('''
            INSERT INTO weight_tracking(username, date, weight)
            VALUES (?, ?, ?)
        ''', (username, date, weight))
        conn.commit()

# Génération de données de poids réalistes
def generate_weight_data(start_date, num_days, start_weight, weight_variation=0.1):
    weight_data = []
    current_date = start_date
    current_weight = start_weight

    for _ in range(num_days):
        
        change = random.uniform(-weight_variation, weight_variation)
        current_weight += change
        weight_data.append((current_date.strftime('%Y-%m-%d'), current_weight))
        current_date += timedelta(days=1)

    return weight_data


def generate_logs(filename, users):
    with open(filename, 'w') as f:
        for user in users:
            f.write(f"User: {user['username']}, {user['first_name']} {user['last_name']}, Age: {user['age']}, Sex: {user['sex']}\n")
            f.write(f"Login Info - Username: {user['username']}, Password: {user['password']}\n")
            for date, weight in user['weight_data']:
                f.write(f"{date}: {weight:.2f} kg\n")
            f.write("\n")

def main():
    create_tables()

    users = []
    num_users = 10
    start_date = datetime(2015, 1, 1)
    num_days = 5 * 365  

    for i in range(num_users):
        unique_id = str(uuid.uuid4())[:8]  
        username = f"user_{unique_id}"
        password = "password"
        first_name = f"FirstName{i+1}"
        last_name = f"LastName{i+1}"
        age = random.randint(20, 60)
        sex = random.choice(["Male", "Female"])
        start_weight = random.uniform(60.0, 100.0)
        
        
        add_userdata(username, password, first_name, last_name, age, sex)
        
        
        weight_data = generate_weight_data(start_date, num_days, start_weight)
        for date, weight in weight_data:
            add_weight_data(username, date, weight)
        
        users.append({
            'username': username,
            'password': password,  
            'first_name': first_name,
            'last_name': last_name,
            'age': age,
            'sex': sex,
            'weight_data': weight_data
        })
    
    
    generate_logs("user_logs.txt", users)

if __name__ == '__main__':
    main()
