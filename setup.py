import sys
from setuptools import setup # type: ignore

extras_require = {
   "ptb": [
      # Дополнительные зависимости для расширения
      "python-telegram-bot[job-queue]>=21.9",
   ],}

package_data = {
   "tg_bot_base": ["*.py"],
}

if any("ptb" in arg for arg in sys.argv):
   package_data["tg_bot_base"].extend(["ext/*.py", "ext/ptb/*.py"])


setup(
   name="tg_bot_base",
   version="1.4.1",
   description="It is useful for creating simple telegram bots",
   author="Neveix",
   author_email="neveix2003@mail.ru",
   packages=["tg_bot_base"],
   install_requires=[],
   extras_require=extras_require,
   package_data=package_data
)