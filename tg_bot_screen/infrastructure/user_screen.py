import asyncio
from typing import Protocol

from tg_bot_screen.core.exceptions import (
    CannotTransformMessage,
    EmptyStackError,
    MessageNotModified,
    NoScreenToUnbuffer,
    ScreenAlreadyActiveError,
    ScreenNotFoundError,
)
from tg_bot_screen.core.models.message_actions import MessageActions
from tg_bot_screen.infrastructure.screen_diff_service import calc_screen_difference

from ..core.interfaces import (
    BotAdapter,
    ScreenService,
    CallbackDataMapping,
    UserStateStore,
    ScreenRegistry,
)
from ..core.models.screen import UnSentScreen, SentScreen


class CallbackDataMappingFactory(Protocol):
    def __call__(self) -> CallbackDataMapping: ...


def _map_callback_data(
    callback_data_mapping_factory: CallbackDataMappingFactory,
    user_id: int,
    screen: UnSentScreen,
    user_state_store: UserStateStore,
) -> CallbackDataMapping:
    mapping = callback_data_mapping_factory()
    callback_data_list = screen.get_callback_data()
    for callback_data in callback_data_list:
        mapping.add(callback_data)
    user_state_store.get(user_id).callback_mapping = mapping
    return mapping


class ScreenServiceImpl(ScreenService):
    def __init__(
        self,
        callback_data_mapping_factory: CallbackDataMappingFactory,
        user_state_store: UserStateStore,
        screen_registry: ScreenRegistry,
        bot_adapter: BotAdapter,
        message_actions: MessageActions,
    ):
        self.callback_data_mapping_factory = callback_data_mapping_factory
        self.user_state_store = user_state_store
        self.screen_registry = screen_registry
        self.bot_adapter = bot_adapter
        self.message_actions = message_actions

    async def clear(self, user_id: int, delete_messages: bool = True):
        user_data = self.user_state_store.get(user_id)
        screen = user_data.screen
        if screen and delete_messages:
            await screen.delete(self.bot_adapter)
        user_data.screen = None

    async def set_by_screen(self, user_id: int, screen: UnSentScreen):
        mapping = _map_callback_data(
            self.callback_data_mapping_factory,
            user_id,
            screen,
            self.user_state_store,
        )

        old_screen = self.get(user_id)
        user_data = self.user_state_store.get(user_id)
        delete, edit, send = calc_screen_difference(
            old_screen, screen, self.message_actions.editor
        )

        new_screen = SentScreen()
        tasks = []
        for message in delete:
            tasks.append(
                self.message_actions.deleter.delete(
                    message,
                    self.bot_adapter,
                )
            )

        for old_message, new_message in edit:
            tasks.append(
                self.message_actions.editor.edit(
                    old_message,
                    new_message,
                    self.bot_adapter,
                    mapping,
                )
            )
            new_screen.extend([old_message])

        for message in send:
            new_message = await self.message_actions.sender.send(
                message,
                user_id,
                self.bot_adapter,
                mapping,
            )
            new_screen.extend([new_message])

        user_data.screen = new_screen

        results = await asyncio.gather(*tasks, return_exceptions=True)
        continue_types: list[type[Exception]] = [
            MessageNotModified,
            CannotTransformMessage,
        ]
        for result in results:
            if isinstance(result, Exception):
                for continue_type in continue_types:
                    if isinstance(result, continue_type):
                        break
                else:
                    raise result

                continue

    async def set(
        self,
        user_id: int,
        screen_name: str,
        stack: bool = True,
        raise_on_error: bool = True,
        **kwargs,
    ):
        user_data = self.user_state_store.get(user_id)
        directory_stack = user_data.directory_stack

        try:
            if directory_stack.last() == screen_name:
                raise ScreenAlreadyActiveError(
                    f"{user_id} attempted to navigate to {screen_name!r} "
                    f"but already on this screen"
                )

            if not stack:
                if len(directory_stack) == 0:
                    raise EmptyStackError(
                        f"{user_id} attempted to navigate to {screen_name!r} "
                        f"with stack=False but stack is empty"
                    )

                user_data.directory_stack.pop()
                user_data.directory_stack.append(screen_name)
            else:
                if len(directory_stack) == 0:
                    directory_stack.append(screen_name)

            screen = self.screen_registry.get(screen_name)
            if screen is None:
                raise ScreenNotFoundError(
                    f"Attempted to retrieve screen named {screen_name!r}, "
                    "but it does not exist"
                )
            evaluated_screen = await screen.evaluate(
                user_id, sys_user_data=user_data, **kwargs
            )

            await self.set_by_screen(user_id, evaluated_screen)

        except Exception:
            if raise_on_error:
                raise

    async def update(self, user_id: int):
        directory_stack = self.user_state_store.get(user_id).directory_stack
        last_screen_name = directory_stack.last()
        if last_screen_name:
            try:
                await self.set(user_id, last_screen_name)

            except ScreenAlreadyActiveError:
                return

    async def step_back(self, user_id: int, times: int = 1) -> None:
        directory_stack = self.user_state_store.get(user_id).directory_stack
        for _ in range(times):
            if len(directory_stack) <= 1:
                return
            directory_stack.pop()

        self.user_state_store.get(user_id).sessions.update_all()
        last_screen_name = directory_stack.last()
        if last_screen_name:
            await self.set(user_id, last_screen_name)

    async def buffer(self, user_id: int):
        user_data = self.user_state_store.get(user_id)
        unsent = None
        if user_data.screen:
            unsent = user_data.screen.get_unsent()
            await user_data.screen.delete(self.bot_adapter)

        user_data.screen_buffer = unsent
        user_data.screen = None

    async def unbuffer(
        self,
        user_id: int,
        raise_on_error: bool = True,
    ):
        screen = self.user_state_store.get(user_id).screen_buffer
        if not screen:
            raise NoScreenToUnbuffer(
                f"{user_id} attempted to unbuffer screen, but it doesn't exist"
            )
        try:
            await self.set_by_screen(user_id, screen)
        except Exception:
            if raise_on_error:
                raise

    def get(self, user_id: int) -> SentScreen | None:
        user_state = self.user_state_store.get(user_id)
        return user_state.screen
