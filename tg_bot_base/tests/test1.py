import asyncio
from telegram import InlineKeyboardMarkup, Message
from .. import ScreenManager, BotManager, EvaluatedMenuDefault
from ..evaluated_menu import EvaluatedMenuHasNotSendedMessage


class TestEvaluatedMenu(EvaluatedMenuDefault):
    async def send(self, bot, chat_id: int):
        print(f"called send {self.text=} with {chat_id=}")
        self.sended_message = Message(message_id = 3, chat=3, date=3)
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
    await screen_manager.set_screen(0, [menu1, menu2])
    # try:
    #     await screen_manager.set_screen(0, [menu1])
    # except EvaluatedMenuHasNotSendedMessage as ex:
    #     old_menu = ex.args[0]
    #     print(id(old_menu))
    #     print(id(menu1))

asyncio.run(main())