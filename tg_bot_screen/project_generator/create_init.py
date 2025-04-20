from .common import *

def create_init(cwd: Path): 
    mkpackage(cwd)
    mkmodule(cwd / "app.py", """\
from os import environ
from telegram.ext import Application
from src.model.bot_manager import BotManager

token = environ.get("BOT_TOKEN")

application = Application.builder().token(token).build()

bot = application.bot

botm = BotManager(application).build()""")
    
    mkmodule(cwd / "config.py", """\
from pathlib import Path
from json import loads, dumps
from .app import botm

file_path = Path("config/config.json")
file_path.parent.mkdir(parents=True, exist_ok=True)
defaults = botm.config.defaults
    
def load_config():
    check_fields = False
    if file_path.exists():
        try:
            json = loads(file_path.read_text("utf-8"))
            check_fields = True
        except:
            json = defaults
    else:
        json = defaults
    
    if check_fields:
        for name in defaults:
            if name not in json:
                json[name] = defaults[name]
    
    botm.config.set_config(file_path, json)""")
    
    mkmodule(cwd / "main.py", """\
from telegram.ext import CommandHandler
from .app import botm, application
from .screens import load_screens
from .config import load_config
from .start import start, start_inner

load_screens()
load_config()

botm.start_inner = start_inner

# application.job_queue.run_repeating(action, interval=60, first=1)

application.add_handler(CommandHandler("start", start), 0)
botm.add_handlers()

print("Запрашивание...")
application.run_polling(0.1)""")

    mkmodule(cwd / "screens.py", R"""\
import importlib
from pathlib import Path

def load_screens():
    p = Path("src/screen")
    for path in p.rglob("*.py"):
        if path.name.startswith("_"):
            continue
        fullpath = str(path)
        module_name = fullpath[:-3].replace("/", ".").replace("\\", ".")
        importlib.import_module(module_name)""")
    
    mkmodule(cwd / "start.py", """\
from telegram import Update
from src.init.app import botm

async def start(update: Update, _):
    user_id = update.message.from_user.id
    print(f"{user_id} написал")
    await start_inner(user_id) 

async def start_inner(user_id: int):    
    sud = botm.system_user_data.get(user_id)
    if sud and sud.screen:
        try: await sud.screen.delete(botm.bot)
        except: ...
    
    botm.system_user_data.reset(user_id)
    botm.reset_user_data(user_id)
    
    await botm.screen.set_by_name(user_id, "welcome")""")