class DataBaseField:
    def __init__(self, name: str, type: str, default_value: object):
        self.name = name
        self.type = type
        if type=="TEXT":
            self.default_value = ""
        else:
            self.default_value = 0