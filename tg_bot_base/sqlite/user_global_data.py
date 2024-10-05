import sqlite3
from typing import Any

class UserGlobalData:
    def __init__(self, path: str):
        self.con = sqlite3.connect(path)
        self.table_name = "UserGlobalData"
    def create_table(self, column_defs: str):
        cur = self.con.cursor()
        column_defs = f"user_id INTEGER PRIMARY KEY NOT NULL,{column_defs}"
        cur.execute(f"CREATE TABLE IF NOT EXISTS {self.table_name} ({column_defs})")
        cur.close()
        self.con.commit()
    def add_column(self, column_def: str):
        cur = self.con.cursor()
        cur.execute(f"ALTER TABLE {self.table_name} ADD COLUMN {column_def}")
        cur.close()
        self.con.commit()
    def __del__(self):
        self.con.close()
    def get(self, user_id: int, fields: str, default: Any = None):
        cur = self.con.cursor() 
        result = cur.execute(f"SELECT {fields} FROM {self.table_name} WHERE user_id = {user_id}").fetchall()
        return result or default
    def set(self, user_id: int, field: str, value):
        cur = self.con.cursor() 
        row_count = cur.execute(f"SELECT count() FROM {self.table_name} WHERE user_id = {user_id}").fetchall()[0][0]
        if row_count == 0:
            cur.execute(f"INSERT INTO {self.table_name} (user_id,{field}) VALUES ({user_id},?)", (value,))
        else:
            cur.execute(f"UPDATE {self.table_name} SET {field} = ? WHERE user_id = {user_id}", (value,))
        cur.close()
        self.con.commit()
    def add(self, user_id: int, field: str, value: Any):
        cur = self.con.cursor() 
        row_count = cur.execute(f"SELECT count() FROM {self.table_name} WHERE user_id = {user_id}").fetchall()[0][0]
        if row_count == 0:
            cur.execute(f"INSERT INTO {self.table_name} (user_id,{field}) VALUES ({user_id},?)", (value,))
        else:
            cur.execute(f"UPDATE {self.table_name} SET {field} = {field} + ? WHERE user_id = {user_id}", (value,))
        cur.close()
        self.con.commit()
    def add_to_list(self, user_id: int, field: str, value: Any):
        cur = self.con.cursor() 
        selected = cur.execute(f"SELECT {field} FROM {self.table_name} WHERE user_id = {user_id}").fetchall()
        from json import dumps
        from json import loads
        if len(selected) == 0:
            list = [value]
            list_str = dumps(list)
            cur.execute(f"INSERT INTO {self.table_name} (user_id,{field}) VALUES ({user_id},?)", (list_str,))
        else:
            list_str = selected[0][0]
            List = []
            if list_str != None:
                List = loads(list_str)
            List.append(value)
            list_str = dumps(List)
            cur.execute(f"UPDATE {self.table_name} SET {field} = ? WHERE user_id = {user_id}", (list_str,))
        cur.close()
        self.con.commit()
    def remove_from_list(self, user_id: int, field: str, value: Any):
        cur = self.con.cursor() 
        row_count = cur.execute(f"SELECT count() FROM {self.table_name} WHERE user_id = {user_id}").fetchall()[0][0]
        from json import dumps
        from json import loads
        if row_count > 0:
            list_str = cur.execute(f"SELECT {field} FROM {self.table_name} WHERE user_id = {user_id}").fetchall()[0][0]
            List: list = loads(list_str)
            List.remove(value)
            list_str = dumps(List)
            cur.execute(f"UPDATE {self.table_name} SET {field} = ? WHERE user_id = {user_id}", (list_str,))
        cur.close()
        self.con.commit()
    def delete_user(self, user_id: int, sql: str = ""):
        """executes: DELETE FROM {self.table_name} WHERE user_id = {user_id} {sql} """
        cur = self.con.cursor()
        cur.execute(f"DELETE FROM {self.table_name} WHERE user_id = {user_id} {sql}")
        cur.close()
        self.con.commit()
    def select(self, columns: str="*", sql: str = ""):
        """returns: cur.execute(f"SELECT {columns} FROM {self.table_name} {sql}").fetchall()"""
        cur = self.con.cursor() 
        return cur.execute(f"SELECT {columns} FROM {self.table_name} {sql}").fetchall()