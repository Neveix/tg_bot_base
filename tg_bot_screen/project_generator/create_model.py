from .common import *

def create_model(cwd: Path): 
    mkpackage(cwd)
    mkmodule(cwd / "bot_manager.py", """\
from typing import Callable
from telegram.ext import Application
from tg_bot_screen.ptb import BotManager as BaseBotManager
from .user_data import UserDataManager
from .config_manager import ConfigManager

class BotManager(BaseBotManager):
    def __init__(self, application: Application):
        super().__init__(application)
        self.user_data_m = UserDataManager()
        self.config = ConfigManager()
        
        self.start_inner: Callable = None
    
    def get_user_data(self, user_id: int):
        return self.user_data_m.get(user_id)

    def reset_user_data(self, user_id: int):
        self.user_data_m.reset(user_id)
        
    async def mapping_key_error(self, user_id: int):
        await self.start_inner(user_id)""")
    
    mkmodule(cwd / "config_manager.py", """\
from json import dumps
from pathlib import Path
from typing import Any

class ConfigManager:
    def __init__(self):
        self.__path: Path = None
        self.__json: dict[str, Any] = None
        self.defaults = {
            "test" : 0
        }
    
    def set_config(self, path: Path, json: dict):
        self.__path = path
        self.__json = json
        self.dump_to_file()
    
    def dump_to_file(self):
        self.__path.touch(exist_ok=True)
        self.__path.write_text(dumps(self.__json, indent=4, ensure_ascii=False), 
            encoding="utf-8")
    
    @property
    def test(self) -> int:
        return self.__json["test"]
    
    @test.setter
    def test(self, value: int):
        self.__json["test"] = value
        self.dump_to_file()
    """)
    mkmodule(cwd / "user_data.py", """\
class UserData:
    def __init__(self):
        self.last_error: str = None 

class UserDataManager:
    def __init__(self):
        self.users_data: dict[int, UserData] = {}
    
    def get(self, user_id: int):
        if user_id not in self.users_data:
            ud = UserData()
            self.users_data[user_id] = ud
            return ud
        
        return self.users_data[user_id]

    def reset(self, user_id: int):
        self.users_data[user_id] = UserData()""")