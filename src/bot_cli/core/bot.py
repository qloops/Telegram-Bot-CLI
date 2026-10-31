from typing import Optional

from pyrogram import Client
from pyrogram.types import User, Message
from pyrogram.handlers import MessageHandler
from pyrogram.errors import RPCError

from bot_cli.core.config import BotConfig


class TelegramBotSession:
    def __init__(self, config: BotConfig) -> None:
        self._config = config
        self._is_listening: bool = self._config.listen
        
        proxy_dict = None
        if self._config.proxy:
            proxy_dict = self._config.proxy.to_pyrogram_dict()

        self._client = Client(
            name="session",
            api_id=self._config.api_id,
            api_hash=self._config.api_hash,
            bot_token=self._config.bot_token,
            proxy=proxy_dict,
            in_memory=True
        )
        self._client.add_handler(MessageHandler(self._on_incoming_message))
        self._me: Optional[User] = None

    @property
    def client(self) -> Client:
        return self._client

    @property
    def me(self) -> User:
        if not self._me:
            raise RuntimeError("No initialization session")
        return self._me

    @property
    def is_listening(self) -> bool:
        return self._is_listening

    def toggle_listener(self) -> bool:
        self._is_listening = not self._is_listening
        return self._is_listening

    async def _on_incoming_message(self, client: Client, message: Message) -> None:
        if not self._is_listening:
            return

        sender = (
            message.from_user.username 
            if (message.from_user and message.from_user.username) 
            else (message.from_user.id if message.from_user else "<Empty>")
        )
        text = message.text or message.caption or "<Empty>"
        print(f"\n[MESSAGE] [{message.chat.id} | @{sender}]: {text}")

    async def __aenter__(self) -> "TelegramBotSession":
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.stop()

    async def start(self) -> None:
        try:
            await self._client.start()
            self._me = await self._client.get_me()
        except RPCError as e:
            await self.stop()
            raise ConnectionError(f"Telegram API error: {e.MESSAGE}") from e
        except Exception as e:
            await self.stop()
            raise ConnectionError(f"Network error: {e}") from e

    async def stop(self) -> None:
        try:
            if self._client and self._client.is_connected:
                await self._client.stop()
        except Exception:
            pass

    def print_identity(self) -> None:
        print("\n", "\\/" * 20, sep="")
        print(f"ID:           {self.me.id}")
        print(f"Bot name:     {self.me.first_name}")
        print(f"Username:     @{self.me.username}")
        if self._config.proxy:
            print(f"Proxy:        {self._config.proxy.host}:{self._config.proxy.port}")
        print(f"Live Listen:  {'On' if self._is_listening else 'Off'}")
        print("\\/" * 20 + "\n")