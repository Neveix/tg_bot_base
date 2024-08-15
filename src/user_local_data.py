from .bot_manager import BotManager
class UserLocalData:
    def __init__(self, bot: BotManager):
        self.__data__: dict[str, dict] = {}
    def set(self, user_id, field, value):
        self.__create_user_if_not_exists__(user_id)
        self.__data__[user_id][field] = value
    def get(self, user_id, field):
        if self.__data__.get(user_id) != None:
            return self.__data__.get(user_id).get(field)
    def __create_user_if_not_exists__(self, user_id):
        if self.__data__.get(user_id) == None:
            self.__data__[user_id] = {}