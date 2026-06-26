import asyncio
from typing import Protocol

from tg_bot_screen.infrastructure.screen_diff_service import calc_screen_difference

from ..core.interfaces import (
    BotAdapter,
    ScreenService,
    CallbackDataMapping,
    UserStateStore,
    ScreenRegistry,
)
from ..core.models.screen import UnSentScreen, SentScreen
from ..core.models.message import UnSentMessage, SentMessage


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
    ):
        self.callback_data_mapping_factory = callback_data_mapping_factory
        self.user_state_store = user_state_store
        self.screen_registry = screen_registry
        self.bot_adapter = bot_adapter

    async def clear(self, user_id: int, delete_messages: bool = True):
        user_data = self.user_state_store.get(user_id)
        screen = user_data.screen
        if screen and delete_messages:
            await screen.delete(self.bot_adapter)
        user_data.screen = None

    async def set(self, user_id: int, screen: UnSentScreen):
        mapping = _map_callback_data(
            self.callback_data_mapping_factory,
            user_id,
            screen,
            self.user_state_store,
        )

        old_screen = self.get(user_id)
        user_data = self.user_state_store.get(user_id)
        delete, edit, send = calc_screen_difference(
            old_screen,
            screen,
            UnSentMessage,
            SentMessage,
        )

        new_screen = SentScreen()
        tasks = []
        for message in delete:
            tasks.append(message.delete(user_id, self.bot_adapter))

        for old_message, new_message in edit:
            tasks.append(old_message.edit(new_message, self.bot_adapter, mapping))
            new_screen.extend([old_message])

        for message in send:
            new_message = await message.send(user_id, self.bot_adapter, mapping)
            new_screen.extend([new_message])

        await asyncio.gather(*tasks)

        user_data.screen = new_screen

    async def set_by_name(
        self, user_id: int, screen_name: str, stack: bool = True, **kwargs
    ):
        user_data = self.user_state_store.get(user_id)
        directory_stack = user_data.directory_stack

        if not stack:
            if len(directory_stack) == 0:
                print(
                    f"{user_id} попытался перейти на экран {screen_name!r} "
                    f"в режиме stack=False, но len(directory_stack) было 0"
                )
                return

            if directory_stack.last() == screen_name:
                print(
                    f"{user_id} попытался перейти на экран {screen_name!r} "
                    f"но он уже находился на этом экране"
                )
                return
            user_data.directory_stack.pop()
            user_data.directory_stack.append(screen_name)
        else:
            if len(directory_stack) == 0 or directory_stack.last() != screen_name:
                directory_stack.append(screen_name)

        screen = self.screen_registry.get(screen_name)
        if screen is None:
            raise KeyError(
                f"Попытка получить экран с названием {screen_name!r}, "
                "но его не существует"
            )
        evaluated_screen = await screen.evaluate(
            user_id, sys_user_data=user_data, **kwargs
        )

        await self.set(user_id, evaluated_screen)

    async def update(self, user_id: int):
        directory_stack = self.user_state_store.get(user_id).directory_stack
        last_screen_name = directory_stack.last()
        if last_screen_name:
            await self.set_by_name(user_id, last_screen_name)

    async def step_back(self, user_id: int, times: int = 1) -> None:
        directory_stack = self.user_state_store.get(user_id).directory_stack
        for _ in range(times):
            if len(directory_stack) <= 1:
                return
            directory_stack.pop()
        self.user_state_store.get(user_id).sessions.update_all()
        last_screen_name = directory_stack.last()
        if last_screen_name:
            await self.set_by_name(user_id, last_screen_name)

    async def buffer(self, user_id: int):
        user_data = self.user_state_store.get(user_id)
        unsent = None
        if user_data.screen:
            unsent = user_data.screen.get_unsent()
            await user_data.screen.delete(self.bot_adapter)

        user_data.screen_buffer = unsent
        user_data.screen = None

    async def unbuffer(self, user_id: int):
        screen = self.user_state_store.get(user_id).screen_buffer
        if not screen:
            print(f"у {user_id} нет screen в unbuffer")
            return
        try:
            await self.set(user_id, screen)
        except Exception as e:
            print(f"у {user_id} ошибка в unbuffer: {e!r}")

    def get(self, user_id: int) -> SentScreen | None:
        user_state = self.user_state_store.get(user_id)
        return user_state.screen
