from dataclasses import dataclass, field
from datetime import datetime

from .types import now_utc


@dataclass
class SessionTurn:
    role: str
    content: str
    created_at: datetime = field(default_factory=now_utc)


class SessionMemory:
    def __init__(self):
        self._turns: list[SessionTurn] = []

    def add_turn(self, role: str, content: str) -> SessionTurn:
        turn = SessionTurn(role=role, content=content)
        self._turns.append(turn)
        return turn

    def get_turns(self) -> list[SessionTurn]:
        return list(self._turns)

    def summarize(self, max_turns: int | None = None) -> str:
        turns = self._turns[-max_turns:] if max_turns else self._turns
        return "\n".join(f"{turn.role}: {turn.content}" for turn in turns)
