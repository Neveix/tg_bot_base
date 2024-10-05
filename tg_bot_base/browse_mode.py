from telegram import Update, Bot
from telegram.ext import CallbackContext
from .bot_manager import BotManager
from .menu import Menu

class BrowseMode:
    SEND = 0
    RETURN = 1
    EDIT = 2
    @staticmethod
    async def browse_with_mode(bot_manager: BotManager, user_id: int, menu: Menu, update: Update, context: CallbackContext, mode: "BrowseMode", **kwargs):
        bot: Bot = context.bot
        text = menu.text
        reply_markup = menu.buttons
        input_media_list = menu.photos
        chat_id = -1
        message = None
        if update.callback_query != None:
            chat_id = update.callback_query.message.chat.id
            message = update.callback_query.message
        elif update.message != None:
            chat_id = update.message.chat.id
            message = update.message
        else:
            return
        new_kwargs = dict(kwargs)
        new_kwargs["user_id"] = user_id
        new_kwargs["bot_manager"] = bot_manager
        if mode == BrowseMode.SEND:
            reply_markup = Menu.buttons_to_inline_keyboard(reply_markup, **new_kwargs)
            if input_media_list:
                await bot.send_media_group(chat_id=chat_id, media=input_media_list)
            await bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
        elif mode == BrowseMode.EDIT:
            reply_markup = Menu.buttons_to_inline_keyboard(reply_markup, **new_kwargs)
            if input_media_list:
                await bot.edit_message_media(media=input_media_list[0], chat_id=chat_id, message_id=message.id-1)
            await bot.edit_message_text(chat_id=chat_id, text=text, message_id=message.id)
            await bot.edit_message_reply_markup(chat_id=chat_id, 
                message_id=message.id, reply_markup=reply_markup)
        elif mode == BrowseMode.RETURN:
            result = {}
            result["bot"] = bot
            result["chat_id"] = chat_id
            result["text"] = text
            result["reply_markup"] = reply_markup
            if input_media_list:
                result["media"] = input_media_list
            return result