from abc import ABC, abstractmethod
from bot_cli.core.bot import TelegramBotSession


class Action(ABC):
    @property
    @abstractmethod
    def id(self) -> int:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    async def execute(self, session: TelegramBotSession) -> None:
        pass