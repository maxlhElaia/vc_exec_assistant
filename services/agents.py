
from abc import ABC

from domain.models import Action, Signal


class Agent(ABC):
    def process_signals(self, signals: list[Signal]) -> list[Action]:
        raise NotImplemented()
