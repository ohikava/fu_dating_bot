import sqlite3
import os

class DataBase:
    def __init__(self, db_name='bot_database.sqlite'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.initialize_db()

    def initialize_db(self):
        db_exists = os.path.exists(self.db_name)
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

        if not db_exists:
            self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                chat_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                goal INTEGER NOT NULL,
                course INTEGER NOT NULL,
                date_of_birth TEXT NOT NULL,
                sex INTEGER NOT NULL,
                who_is_looking INTEGER NOT NULL,
                description TEXT,
                studygroup TEXT,
                height INTEGER,
                social_networks TEXT,
                grade INTEGER,
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Hobbies (
                chat_id INTEGER,
                hobby_id INTEGER,
                FOREIGN KEY (chat_id) REFERENCES Users(chat_id),
                PRIMARY KEY (chat_id, hobby_id)
            )
        ''')
        self.conn.commit()

    def insert_value(self, chat_id, name, goal, course, date_of_birth, sex, who_is_looking, description=None, studygroup=None, height=None, social_networks=None, grade=None):
        try:
            self.cursor.execute('''
                INSERT INTO Users (chat_id, name, goal, course, date_of_birth, sex, who_is_looking, description, studygroup, height, social_networks, grade)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (chat_id, name, goal, course, date_of_birth, sex, who_is_looking, description, studygroup, height, social_networks, grade))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # Record already exists

    def remove_value(self, user_id):
        self.cursor.execute('DELETE FROM Users WHERE userId = ?', (user_id))
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    def get_user_info(self, chat_id):
        try:
            self.cursor.execute('''
                SELECT * FROM Users
                WHERE chat_id = ?
            ''', (chat_id,))
            user_data = self.cursor.fetchone()
            
            if user_data:
                columns = [description[0] for description in self.cursor.description]
                user_info = dict(zip(columns, user_data))
                
                # Fetch hobbies for the user
                self.cursor.execute('''
                    SELECT hobby_id FROM Hobbies
                    WHERE chat_id = ?
                ''', (chat_id,))
                hobbies = [row[0] for row in self.cursor.fetchall()]
                user_info['hobbies'] = hobbies
                
                return user_info
            else:
                return None
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None

    def __del__(self):
        if self.conn:
            self.conn.close()
