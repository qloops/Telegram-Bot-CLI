import asyncio
from typing import Dict
from bot_cli.core.bot import TelegramBotSession
from bot_cli.ui.actions.base import Action


class ConsoleMenu:
    def __init__(self, session: TelegramBotSession) -> None:
        self._session = session
        self._actions: Dict[int, Action] = {}

    def register(self, action: Action) -> "ConsoleMenu":
        self._actions[action.id] = action
        return self

    async def loop(self) -> None:
        exit_code = 0
        while True:
            print("Option:")
            for idx in sorted(self._actions.keys()):
                print(f" {idx}. {self._actions[idx].description}")
            print(f" {exit_code}. Exit")

            user_choice = (await asyncio.to_thread(input, "Choice num: ")).strip()

            if not user_choice.isdigit():
                print("Error: choice not num")
                continue

            cmd = int(user_choice)
            if cmd == exit_code:
                break

            action = self._actions.get(cmd)
            if not action:
                print("IDK")
                continue

            try:
                await action.execute(self._session)
            except Exception as e:
                print(f"Error choice: {e}")