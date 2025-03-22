from setuptools import setup # type: ignore

setup(
   name='tg_bot_base',
   version='1.3.22',
   description='It is useful for creating simple telegram bots',
   author='Neveix',
   author_email='neveix2003@mail.ru',
   packages=['tg_bot_base'],
   install_requires=[],
   extras_require={
      'ptb': [
         # Дополнительные зависимости для расширения
         'python-telegram-bot[job-queue]>=21.9',
      ],
   },
)