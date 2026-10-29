from bot_cli.ui.actions.base import Action
from bot_cli.core.bot import TelegramBotSession


class ToggleListenerAction(Action):
    @property
    def id(self) -> int:
        return 9

    @property
    def description(self) -> str:
        return "On/Off listening message"

    async def execute(self, session: TelegramBotSession) -> None:
        state = session.toggle_listener()
        status_text = "On" if state else "Off"
        print(f"[INFO] Listening message: {status_text}")