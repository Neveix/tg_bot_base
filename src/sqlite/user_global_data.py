
from .database_field import DataBaseField
from .data_base_manager import DataBaseManager

class UserGlobalData(DataBaseManager):
    def __init__(self, bot_manager, path: str, fields: list[DataBaseField]=[]):
        super().__init__(path, fields=fields)
        from ..bot_manager import BotManager
        self.bot_manager: BotManager = bot_manager
        bot_manager.user_global_data = self
    def set(self, user_id, field, value):
        cursor = self.connection.cursor()
        self.create_user(user_id)
        kwargs = {}
        kwargs[field] = value
        self.insert(user_id=user_id, **kwargs)
        #print(f"{self.get(user_id, "picture_favorites")=}")
        text = f"UPDATE {self.table_name} SET {field} = ? WHERE user_id = ?"
        args = (value,user_id,)
        #print(f"update {text=} {args=}")
        cursor.execute(text, args)
        #print(f"{self.get(user_id, "picture_favorites")=}")
        cursor.close()
        self.connection.commit()
        #print(f"global data {user_id=} set {field} to `{value}` of type {type(value)} ")
    def get(self, user_id: int, columns: str, default=None):
        """Gets the value from a DataBase's field."""
        result = self.browse(0,1,columns,f"WHERE user_id = {user_id}") or default
        #print(f"global data {user_id=} get {columns} = `{result}` of type {type(result)} ")
        return result
    def create_user(self, user_id):
        cursor = self.connection.cursor()
        result = cursor.execute(f"SELECT * FROM {self.table_name} WHERE user_id = {user_id}").fetchone()
        if result == None:
            cursor.execute(f"INSERT OR IGNORE INTO {self.table_name}({",".join(self.field_names)}) \
VALUES ({",".join("?"*len(self.field_names))})",
                list(map(lambda f: f.default_value,self.fields)))
        cursor.close()
        self.connection.commit()
        