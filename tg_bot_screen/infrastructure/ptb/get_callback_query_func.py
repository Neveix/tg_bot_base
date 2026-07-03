from telegram import Update

from tg_bot_screen.infrastructure.callback_query_handler import CallbackQueryHandlerTBS


def get_callback_query_func_ptb(callback_query_handler: CallbackQueryHandlerTBS):
    async def handle_callback_query(update: Update, _):
        assert update.callback_query
        assert update.callback_query.from_user
        assert update.callback_query.data

        user_id = update.callback_query.from_user.id
        query_data = update.callback_query.data
        await update.callback_query.answer()

        await callback_query_handler.handle(
            user_id,
            query_data,
        )

    return handle_callback_query
