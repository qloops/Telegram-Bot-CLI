from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass(frozen=True, slots=True)
class Socks5Proxy:
    host: str
    port: int

    @classmethod
    def parse(cls, endpoint: Optional[str]) -> Optional["Socks5Proxy"]:
        if not endpoint:
            return None
        
        parts = endpoint.strip().split(":")
        if len(parts) != 2:
            raise ValueError("Requirements for proxy format: host:port (example: 127.0.0.1:9090)")

        host, port = parts[0], int(parts[1])
        return cls(host=host, port=port)

    def to_pyrogram_dict(self) -> Dict[str, Any]:
        return {
            "scheme": "socks5",
            "hostname": str(self.host),
            "port": int(self.port)
        }