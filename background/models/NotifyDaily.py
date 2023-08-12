from dataclasses import dataclass


@dataclass
class NotifyDaily:
    login: str
    message: str
