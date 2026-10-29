import argparse
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

from bot_cli.core.proxy import Socks5Proxy

DEFAULT_API_ID: int = None
DEFAULT_API_HASH: str = None


def _get_base_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent.parent.parent


def _load_env() -> None:
    env_path = _get_base_dir() / ".env"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)


@dataclass(slots=True)
class BotConfig:
    bot_token: str
    api_id: int
    api_hash: str
    proxy: Optional[Socks5Proxy] = None
    listen: bool = False

    @classmethod
    def from_cli(cls) -> "BotConfig":
        _load_env()

        api_id_env = os.getenv("TELEGRAM_API_ID")
        api_id = int(api_id_env) if api_id_env and api_id_env.isdigit() else DEFAULT_API_ID
        api_hash = os.getenv("TELEGRAM_API_HASH") or DEFAULT_API_HASH

        parser = argparse.ArgumentParser(prog="telegram-cli")
        parser.add_argument("-t", "--token", default=None)
        parser.add_argument("-p", "--proxy", default=None)
        parser.add_argument("-l", "--listen", action="store_true", default=False)

        args = parser.parse_args()

        token = args.token
        while not token:
            token = input("Bot token please: ").strip()

        proxy: Optional[Socks5Proxy] = None
        if args.proxy:
            try:
                proxy = Socks5Proxy.parse(args.proxy) if isinstance(args.proxy, str) else args.proxy
            except ValueError as e:
                print(f"Proxy error: {e}")
        elif os.getenv("PROXY_HOST") and os.getenv("PROXY_PORT"):
            host = os.getenv("PROXY_HOST").strip()
            port = os.getenv("PROXY_PORT").strip()
            if host and port:
                proxy = Socks5Proxy(host=host, port=port)
        elif os.getenv("PROXY"):
            try:
                proxy = Socks5Proxy.parse(os.getenv("PROXY"))
            except ValueError as e:
                print(f"Proxy error: {e}")

        return cls(
            bot_token=token,
            api_id=api_id,
            api_hash=api_hash,
            proxy=proxy,
            listen=args.listen
        )

    def prompt_credentials(self) -> None:
        while True:
            new_token = input("Bot token please: ").strip()
            if new_token:
                self.bot_token = new_token
                break

        if not self.proxy:
            while True:
                proxy_raw = input("Proxy (ip:port) or Enter, if skip: ").strip()
                if not proxy_raw:
                    self.proxy = None
                    break
                try:
                    self.proxy = Socks5Proxy.parse(proxy_raw)
                    break
                except ValueError as e:
                    print(e)