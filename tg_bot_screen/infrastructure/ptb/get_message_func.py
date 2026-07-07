from telegram import Update

from tg_bot_screen.infrastructure.input_message_handler import MessageHandler


def get_message_func_ptb(message_handler: MessageHandler):
    async def handle_message(update: Update, _):
        assert update.message
        assert update.message.from_user

        user_id = update.message.from_user.id

        await message_handler.handle(
            user_id,
            message=update.message,
        )

    return handle_message
