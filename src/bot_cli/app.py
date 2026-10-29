from bot_cli.core.config import BotConfig
from bot_cli.core.bot import TelegramBotSession
from bot_cli.ui.menu import ConsoleMenu
from bot_cli.ui.actions.send_message import SendMessageAction
from bot_cli.ui.actions.toggle_listener import ToggleListenerAction
from bot_cli.ui.actions.get_messages import GetMessagesAction

class Application:
    def __init__(self, config: BotConfig) -> None:
        self._config = config

    async def run(self) -> None:
        while True:
            try:
                async with TelegramBotSession(self._config) as session:
                    session.print_identity()

                    menu = ConsoleMenu(session)
                    menu.register(SendMessageAction())
                    menu.register(ToggleListenerAction())
                    menu.register(GetMessagesAction())
                    await menu.loop()
                    return

            except ConnectionError as e:
                print(f"Connect error: {e}")
                self._config.prompt_credentials()
            except Exception as e:
                print(f"App error: {e}")
                self._config.prompt_credentials()