
from .database_field import DataBaseField
from .data_base_manager import DataBaseManager

class UserGlobalData(DataBaseManager):
    def __init__(self, bot_manager, path: str, fields: list[DataBaseField]=[]):
        fields.insert(0,DataBaseField("user_id","INT PRIMARY KEY",0))
        super().__init__(path, fields=fields)
        from ..bot_manager import BotManager
        self.bot_manager: BotManager = bot_manager
        bot_manager.user_global_data = self
    def set(self, user_id, field, value):
        cursor = self.connection.cursor()
        self.create_user(user_id)
        cursor.execute(f"UPDATE {self.table_name} SET {field} = {value} WHERE user_id = {user_id}")
        cursor.close()
        self.connection.commit()
    def get(self, user_id: int, columns: str, default=None):
        """Gets the value from a DataBase's field."""
        result = self.browse(0,1,columns,f"WHERE user_id = {user_id}") or default
        return result
    def create_user(self, user_id):
        cursor = self.connection.cursor()
        result = cursor.execute(f"SELECT * FROM {self.table_name} WHERE user_id = {user_id}").fetchone()
        if result == None:
            cursor.execute(f"INSERT INTO {self.table_name} VALUES ({",".join(map(lambda f: f.default_value,self.fields))})")
        cursor.close()
        self.connection.commit()
        