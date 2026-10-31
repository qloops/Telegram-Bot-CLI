import asyncio

from bot_cli.ui.actions.base import Action
from bot_cli.core.bot import TelegramBotSession
from bot_cli.utils.parsers import parse_target_ids
from pyrogram.errors import RPCError


class SendMessageAction(Action):
    @property
    def id(self) -> int:
        return 1

    @property
    def description(self) -> str:
        return "sendMessage"

    async def execute(self, session: TelegramBotSession) -> None:
        while True:
            target_raw = (await asyncio.to_thread(input, "chat_id: (exemple: a,-b,c-d) ")).strip()
            if not target_raw:
                print("{chat_id} cannot be empty")
                return

            targets = parse_target_ids(target_raw)
            if not targets:
                print("No available IDs found")
                return

            text = (await asyncio.to_thread(input, "text: ")).strip()
            if not text:
                print("{text} cannot be empty")
                return

            success_count = 0
            for chat_id in targets:
                try:
                    await session.client.send_message(chat_id=chat_id, text=text)
                    print(f"[{chat_id}] Success.")
                    success_count += 1
                except RPCError as e:
                    print(f"[{chat_id}] Telegram error: {e.MESSAGE}")
                except Exception as e:
                    print(f"[{chat_id}] Network error: {e}")
                await asyncio.sleep(0.1)

            if targets:
                print(f"Success {success_count}/{len(targets)} messages.")
            break