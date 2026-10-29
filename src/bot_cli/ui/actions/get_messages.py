import asyncio
from typing import List, Union

from bot_cli.ui.actions.base import Action
from bot_cli.core.bot import TelegramBotSession
from bot_cli.utils.parsers import parse_target_ids
from pyrogram.types import Message
from pyrogram.errors import RPCError


class GetMessagesAction(Action):
    @property
    def id(self) -> int:
        return 2

    @property
    def description(self) -> str:
        return "getMessages"

    async def execute(self, session: TelegramBotSession) -> None:
        default_id = session.me.id
        raw_chat_id = (await asyncio.to_thread(input, f"chat_id: (default: {default_id}) ")).strip()

        if not raw_chat_id:
            chat_id = default_id
        else:
            chat_id = int(raw_chat_id) if raw_chat_id.lstrip("-").isdigit() else raw_chat_id

        raw_ids = (await asyncio.to_thread(input, "message_ids: (exemple: a,-b,c-d) ")).strip()
        if not raw_ids:
            print("{message_ids} cannot be empty")
            return

        raw_reverse = (await asyncio.to_thread(input, "Reverse order? (y/n) [n]: ")).strip().lower()
        is_reversed = raw_reverse.lower() in ("y", "yes")

        message_ids = parse_target_ids(raw_ids, reverse=is_reversed)
        if not message_ids:
            print("No available IDs found")
            return

        chunks = [message_ids[i:i + 200] for i in range(0, len(message_ids), 200)]
        found_count = 0

        try:
            for chunk in chunks:
                response: Union[Message, List[Message]] = await session.client.get_messages(
                    chat_id=chat_id,
                    message_ids=chunk
                )

                messages = response if isinstance(response, list) else [response]

                for msg in messages:
                    if not msg or getattr(msg, "empty", False):
                        continue

                    sender = (
                        msg.from_user.username
                        if (msg.from_user and msg.from_user.username)
                        else (msg.from_user.id if msg.from_user else "<Empty>")
                    )
                    sender_str = f"@{sender}" if sender else "<Empty>"
                    text = msg.text or msg.caption or "<Empty>"
                    date_str = msg.date.strftime("%d/%m %H:%M:%S") if msg.date else "--/-- --:---"

                    print(f"\n[OLD_MESSAGE] [{msg.chat.id} | {sender_str} | {date_str}]: {text}")
                    found_count += 1
            await asyncio.sleep(0.1)
            print(f"\nTotal fetched: {found_count}/{len(message_ids)} messages")

        except RPCError as e:
            print(f"Telegram error: {e.MESSAGE}")
        except Exception as e:
            print(f"Network error: {e}")