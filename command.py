class Command:
    def __init__(self, name: str, action: function):
        self.name = name
        self.action = action
        if not self.command_manager:
            self.command_manager = None