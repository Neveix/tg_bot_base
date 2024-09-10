import sqlite3

from database_field import DataBaseField

class UserGlobalData:
    
    def __init__(self, bot_manager, path: str, fields: dict[str, DataBaseField]):
        self.bot_manager = bot_manager
        self.fields = fields
        self.connection = sqlite3.connect(path)
        cur = self.connection.cursor()
        cur.execute(f"CREATE TABLE IF NOT EXISTS UserGlobalData({",".join(map(lambda f: f.name+f.value,fields))})") 
        cur.close()
        self.connection.commit()
    def set(self, user_id, field, value):
        cursor = self.connection.cursor()
    def create_user(self, user_id):
        cursor = self.connection.cursor()
        result = cursor.execute(f"SELECT FROM {__class__.__name__}").fetchone()
        if result == None:
            cursor.execute(f"INSERT INTO UserGlobalData VALUES ({",".join(map(lambda f: f.default_value,self.fields))})")
        cursor.close()
        self.connection.commit()
        