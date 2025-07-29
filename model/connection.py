from dataclasses import dataclass
from typing import Optional


@dataclass
class Connection:
    server: str
    user: str
    password: Optional[str] = None
    keypath: Optional[str] = None