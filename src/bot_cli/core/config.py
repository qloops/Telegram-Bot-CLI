import argparse
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

from bot_cli.core.proxy import Socks5Proxy

# TODO: Не забыть указать какие не жалко
DEFAULT_API_ID: Optional[int] = None
DEFAULT_API_HASH: Optional[str] = None


def _load_env() -> None:
    base_dir = (
        Path(sys.executable).resolve().parent
        if getattr(sys, "frozen", False)
        else Path(__file__).resolve().parent.parent.parent.parent
    )
    external_env = base_dir / ".env"
    if external_env.exists():
        load_dotenv(dotenv_path=external_env)


def _ask_proxy_input(current_proxy: Optional[Socks5Proxy] = None) -> Optional[Socks5Proxy]:
    if current_proxy:
        current_str = f"{current_proxy.host}:{current_proxy.port}"
        while True:
            raw = input(f"Proxy [{current_str}] (Enter to keep, 'none' to disable): ").strip()
            if not raw:
                return current_proxy
            if raw.lower() == "none":
                return None
            try:
                return Socks5Proxy.parse(raw)
            except ValueError as e:
                print(f"Proxy error: {e}")

    while True:
        raw = input("Proxy (ip:port) or Enter to skip: ").strip()
        if not raw:
            return None
        try:
            return Socks5Proxy.parse(raw)
        except ValueError as e:
            print(f"Proxy error: {e}")


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
        api_id = int(api_id_env) if api_id_env and api_id_env.strip().isdigit() else DEFAULT_API_ID
        api_hash = os.getenv("TELEGRAM_API_HASH") or DEFAULT_API_HASH

        if not api_id or not api_hash:
            print(
                "TELEGRAM_API_ID or TELEGRAM_API_HASH is missing.\n"
                "Please place a valid .env file next to the application or specify DEFAULT_API_ID/HASH"
            )
            sys.exit(1)

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
        else:
            proxy = _ask_proxy_input()

        return cls(
            bot_token=token,
            api_id=api_id,
            api_hash=api_hash,
            proxy=proxy,
            listen=args.listen,
        )

    def prompt_credentials(self) -> None:
        print("Connection failed. Please re-enter credentials:")
        while True:
            new_token = input("Bot token please: ").strip()
            if new_token:
                self.bot_token = new_token
                break

        self.proxy = _ask_proxy_input(current_proxy=self.proxy)