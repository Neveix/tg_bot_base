from .bot_manager import BotManager
class UserLocalData:
    def __init__(self, bot: BotManager):
        self.__data__: dict[str, dict] = {}
        self.bot_manager = bot
    def set(self, user_id: int, field, value):
        self.create_user_if_not_exists(user_id)
        self.__data__[user_id][field] = value
    def add(self, user_id: int, field, value):
        self.create_user_if_not_exists(user_id)
        old_value = self.get(user_id, field, 0)
        self.__data__[user_id][field] = old_value + value
    def append(self, user_id: int, field, value):
        self.create_user_if_not_exists(user_id)
        list = self.get(user_id, field)
        if list == None:
            self.set(user_id, field, [value])
        else:
            list.append(value)
    def clear(self, user_id):
        if self.__data__.get(user_id) != None:
            self.__data__[user_id] = {}
    def get(self, user_id, field: int, default = None):
        result = None
        if self.__data__.get(user_id) != None:
            result = self.__data__.get(user_id).get(field)
        if result == None:
            return default
        else:
            return result
        
    def create_user_if_not_exists(self, user_id: int):
        if self.__data__.get(user_id) == None:
            self.__data__[user_id] = {}
            
    def browse_user_data(self, user_id: int):
        self.create_user_if_not_exists(user_id)
        return self.__data__[user_id]