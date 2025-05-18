import os
import argparse
from pathlib import Path
from .project_generator.common import *
from .project_generator.create_init import create_init
from .project_generator.create_model import create_model
from .project_generator.create_screen import create_screen
from .project_generator.create_types import create_types


def main():
    parser = argparse.ArgumentParser(
        description='python -m tg_bot_screen', 
        usage='%(prog)s [options]')
    parser.add_argument("--ptb", "--python-telegram-bot", action="store_true")
    
    args = parser.parse_args()
    
    if args.ptb is False:
        good_use = R"python -m tg_bot_screen --ptb"
        print(f"""
Ошибка: Не передан аргумент, который отражает библиотеку, которая будет использована
Например --ptb
\tИспользование:
\t{good_use}
""")
        return
    
    mkmodule("run.py", "from src.init import main")
    basewd = Path("src") # Working Directory
    
    mkpackage(basewd)
    
    create_init(basewd / "init")
    
    create_model(basewd / "model")
    
    create_screen(basewd / "screen")
    
    create_types(basewd / "types")


if __name__ == "__main__":
    main()
