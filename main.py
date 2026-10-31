import asyncio
import multiprocessing
import os
import sys

if __name__ == "__main__":
    multiprocessing.freeze_support()

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from bot_cli.core.config import BotConfig
from bot_cli.app import Application


# Пока что глушим реконнекты (и не только), ибо они ничего не ломают, а срут обильно (спасибо ркн)
def exception_handler(loop, context):
    exception = context.get("exception")
    if isinstance(exception, (AttributeError, ConnectionResetError)):
        return
    loop.default_exception_handler(context)


def bootstrap() -> None:
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.set_exception_handler(exception_handler)

        config = BotConfig.from_cli()
        app = Application(config)
        loop.run_until_complete(app.run())
    except (KeyboardInterrupt, SystemExit):
        print("\nExit")
    except Exception as e:
        print(f"Fatal error: {e}")


if __name__ == "__main__":
    bootstrap()