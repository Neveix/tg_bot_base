from pathlib import Path
import os

def mkpackage(path: Path | str):
    try: os.mkdir(path) 
    except: ...
    with open(path / "__init__.py", mode="w") as fh:
        fh.write("")

def mkmodule(path: Path | str, text: str):
    with open(path, mode="w", encoding="utf-8") as fh:
        fh.write(text)