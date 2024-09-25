import sqlite3

from .database_field import DataBaseField

class DataBaseManager:
    def __init__(self, path: str, table_name: str = "DefaultTable", fields: list[DataBaseField] = []):
        self.fields: list[DataBaseField] = [
            DataBaseField("id","INTEGER PRIMARY KEY AUTOINCREMENT", 0)
        ]
        self.fields.extend(fields)
        self.field_names = list(map(lambda field: field.name, self.fields))
        self.connection = sqlite3.connect(path)
        self.table_name = table_name
        self.field_names_types = list(map(lambda field: field.name+" "+field.type,self.fields))
        cursor = self.connection.cursor()
        columns = ",".join(self.field_names_types)
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.table_name}({columns})")
        from sqlite3 import OperationalError
        for field in self.fields:
            try:
                cursor.execute(f"ALTER TABLE {self.table_name} ADD COLUMN {field.name} {field.type}")
            except OperationalError:
                pass
        cursor.close()
        self.connection.commit()
    def get_by_id(self, id: int = -1, columns: str = ""):
        if id == -1:
            return
        result = self.browse(0,1,columns,f"WHERE id = {id}")[0]
        return result
    def insert(self, **kwargs):
        cursor = self.connection.cursor()
        field_names = []
        field_values = []
        for field in self.fields:
            if field.name in kwargs:
                field_names.append(field.name)
                field_values.append(kwargs.get(field.name))
        field_values = tuple(field_values)
        text = f"INSERT OR IGNORE INTO {self.table_name}({",".join(field_names)}) VALUES ({",".join("?"*len(field_names))})"
        # print(f"insert, {text=} {field_values=}")
        cursor.execute(text,field_values)
        cursor.close()
        self.connection.commit()
    def delete(self, sql: str = ""):
        cursor = self.connection.cursor()
        cursor.execute(f"DELETE FROM {self.table_name} {sql}")
        cursor.close()
        self.connection.commit()
    def browse(self, page: int, count: int, columns: str = "", sql: str = ""):
        cursor = self.connection.cursor()
        if columns == "":
            columns = ",".join(map(lambda field: field.name, self.fields))
        result = cursor.execute(f"SELECT {columns} FROM {self.table_name} {sql} LIMIT {count} OFFSET {page*count}").fetchall()
        cursor.close()
        return result
    def count(self, sql: str) -> int:
        cursor = self.connection.cursor()
        result = cursor.execute(f"SELECT COUNT(*) FROM {self.table_name} {sql}").fetchone()[0]
        cursor.close()
        return result
    def not_contain_reserved_keyword(text: str):
        # Список зарезервированных слов SQLite
        reserved_keywords = {
            "SELECT", "INSERT", "DELETE", "UPDATE", "FROM", "WHERE", 
            "JOIN", "CREATE", "DROP", "TABLE", "ALTER", "COLUMN", 
            "INDEX", "VIEW", "TRIGGER", "PRIMARY", "KEY", "FOREIGN", 
            "UNIQUE", "NOT", "NULL", "AND", "OR", "LIKE", "IN", 
            "BETWEEN", "AS", "IS", "GROUP", "ORDER", "HAVING"
        }
        text = text.upper()
        return all(map(lambda word: word not in text,reserved_keywords))
    def is_valid_column_name(column_name):
        from re import match
        # Регулярное выражение для проверки имени колонки
        pattern = r'^[a-zA-Z_][a-zA-Z0-9_]*$'
        # Проверка по регулярному выражению
        if match(pattern, column_name) and DataBaseManager.not_contain_reserved_keyword(column_name):
            return True
        return False