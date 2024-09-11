import sqlite3

from .database_field import DataBaseField

class UserGlobalData:
    def is_valid_column_name(column_name):
        from re import match
        # Регулярное выражение для проверки имени колонки
        pattern = r'^[a-zA-Z_][a-zA-Z0-9_]*$'
        # Список зарезервированных слов SQLite
        reserved_keywords = {
            "SELECT", "INSERT", "DELETE", "UPDATE", "FROM", "WHERE", 
            "JOIN", "CREATE", "DROP", "TABLE", "ALTER", "COLUMN", 
            "INDEX", "VIEW", "TRIGGER", "PRIMARY", "KEY", "FOREIGN", 
            "UNIQUE", "NOT", "NULL", "AND", "OR", "LIKE", "IN", 
            "BETWEEN", "AS", "IS", "GROUP", "ORDER", "HAVING"
        }
        # Проверка по регулярному выражению
        if match(pattern, column_name) and column_name.upper() not in reserved_keywords:
            return True
        return False
    def __init__(self, bot_manager, path: str, fields: list[DataBaseField]):
        self.bot_manager = bot_manager
        bot_manager.user_global_data = self
        fields.insert(0,DataBaseField("user_id","INT PRIMARY KEY",0))
        self.fields = fields
        self.connection = sqlite3.connect(path)
        cur = self.connection.cursor()
        cur.execute(f"CREATE TABLE IF NOT EXISTS UserGlobalData({",".join(map(lambda f: f.name+f.type,fields))})") 
        cur.close()
        self.connection.commit()
    def set(self, user_id, field, value):
        cursor = self.connection.cursor()
        self.create_user(user_id)
        cursor.execute(f"UPDATE UserGlobalData SET {field} = {value} WHERE user_id = {user_id}")
        cursor.close()
        self.connection.close()
    def get(self, user_id, field):
        """Gets the value from a DataBase's field."""
        cur = self.__con__.cursor()
        field = self.__convert_field__(field)
        # creates a user if not exists
        self.create_user(user_id)
        result = None
        if field in self.__available_column_names__:
            result = cur.execute(f"SELECT {field} FROM UserGlobalData WHERE user_id = {user_id}").fetchone()
            if result:
                result = result[0]
        cur.close()
        self.__con__.commit()
        return result
    def create_user(self, user_id):
        cursor = self.connection.cursor()
        result = cursor.execute(f"SELECT FROM UserGlobalData WHERE user_id = {user_id}").fetchone()
        if result == None:
            cursor.execute(f"INSERT INTO UserGlobalData VALUES ({",".join(map(lambda f: f.default_value,self.fields))})")
        cursor.close()
        self.connection.commit()
        