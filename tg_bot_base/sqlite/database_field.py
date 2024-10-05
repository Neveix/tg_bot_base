class DataBaseField:
    def __init__(self, name: str, type: str, default_value: object = None):
        self.name = name
        self.type = type
        if default_value == None:
            if type=="TEXT":
                self.default_value = ""
            else:
                self.default_value = 0
        else:
            self.default_value = default_value