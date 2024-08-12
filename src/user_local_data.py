class UserLocalData:
    __data__: dict[str, dict]
    def __init__(self):
        UserLocalData.__data__ = {}
    def set(self, user_id, field, value):
        UserLocalData.__create_user_if_not_exists__(user_id)
        UserLocalData.__data__[user_id][field] = value
    def get(self, user_id, field):
        if UserLocalData.__data__.get(user_id) != None:
            return UserLocalData.__data__.get(user_id).get(field)
    def __create_user_if_not_exists__(self, user_id):
        if UserLocalData.__data__.get(user_id) == None:
            UserLocalData.__data__[user_id] = {}