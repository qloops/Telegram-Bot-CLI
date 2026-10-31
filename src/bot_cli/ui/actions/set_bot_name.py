import asyncio
from bot_cli.ui.actions.base import Action
from bot_cli.core.bot import TelegramBotSession
from pyrogram.errors import RPCError

class SetBotNameAction(Action):
    @property
    def id(self) -> int:
        return 3

    @property
    def description(self) -> str:
        return "setBotName"

    async def execute(self, session: TelegramBotSession) -> None:
        new_name = (await asyncio.to_thread(input, "name: ")).strip()
        if not new_name:
            print("{name} cannot be empty")
            return

        try:
            result = await session.client.set_bot_name(name=new_name)

            if result:
                print(f"Bot name updated to: '{new_name}'")
                session.me.first_name = new_name
            else:
                print("Telegram returned False")

        except RPCError as e:
            print(f"Telegram error: {e.MESSAGE}")
        except Exception as e:
            print(f"Network error: {e}")