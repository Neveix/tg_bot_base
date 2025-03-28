from .command import Command

class CommandManager:
    __command_dict__ : dict[str, Command]
    def __init__(self, bot):
        self.bot = bot
        self.__command_dict__ = {}
    def add(self, command: Command):
        command.command_manager = self
        self.__command_dict__[command.name] = command
    def get(self, name: str):
        return self.__command_dict__.get(name)
    def get_all_handlers(self):
        result = []
        for key in self.__command_dict__:
            result.append(self.get(key).to_command_handler())
        return result
