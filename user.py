import sqlite3

class User:
    def __init__(self, user_id, name, age):
        self.user_id = user_id
        self.name = name
        self.age = age

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users
            (user_id INTEGER PRIMARY KEY, name TEXT, age INTEGER)
        ''')

    def insert_user(self, name, age):
        try:
            self.cursor.execute('INSERT INTO users (name, age) VALUES (?, ?)', (name, age))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error inserting user: {e}")
            return None

    def get_user(self, user_id):
        try:
            self.cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error fetching user: {e}")
            return None

    def update_user(self, user_id, name, age):
        try:
            self.cursor.execute('UPDATE users SET name = ?, age = ? WHERE user_id = ?', (name, age, user_id))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error updating user: {e}")

    def delete_user(self, user_id):
        try:
            self.cursor.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error deleting user: {e}")

class UserService:
    def __init__(self, db):
        self.db = db

    def create_user(self, name, age):
        user_id = self.db.insert_user(name, age)
        if user_id:
            return {"user_id": user_id, "name": name, "age": age}, 201
        else:
            return {"error": "Failed to create user"}, 500

    def get_user(self, user_id):
        user = self.db.get_user(user_id)
        if user:
            return {"user_id": user[0], "name": user[1], "age": user[2]}, 200
        else:
            return {"error": "User not found"}, 404
    
    def update_user(self, user_id, name, age):
        user = self.db.get_user(user_id)
        if user:
            self.db.update_user(user_id, name, age)
            return {"user_id": user_id, "name": name, "age": age}, 200
        else:
            return {"error": "User not found"}, 404

    def delete_user(self, user_id):
        user = self.db.get_user(user_id)
        if user:
            self.db.delete_user(user_id)
            return {"message": "User deleted successfully"}, 200
        else:
            return {"error": "User not found"}, 404
