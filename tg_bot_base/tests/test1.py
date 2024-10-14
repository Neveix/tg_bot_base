import asyncio
from telegram import InlineKeyboardMarkup
from .. import ScreenManager, BotManager, EvaluatedMenu

class TestEvaluatedMenu(EvaluatedMenu):
    async def send(self, bot, chat_id: int):
        print(f"called send {self.text=} with {chat_id=}")
    async def edit_message(self, bot, chat_id: int, message_id: int):
        print(f"called edit_message {self.text=} with {chat_id=} {message_id=}")

menu1 = TestEvaluatedMenu("test text", InlineKeyboardMarkup([]))
menu2 = TestEvaluatedMenu("test text 2", InlineKeyboardMarkup([]))

bot_manager = BotManager()

screen_manager = ScreenManager(bot_manager)

screen_manager.clear_screen(0)

async def main():
    print("Hello, asyncio!")
    await screen_manager.set_screen(0, [menu1])

asyncio.run(main())