from abc import ABC
import datetime
from pydantic import BaseModel

class Company(BaseModel):
    pass

class Signal(BaseModel):
    id: str
    trigger: datetime
    # signaltype: str
    title: str
    description: str
    company: Company

class Action(BaseModel):
    signal: Signal
    title: str
    description: str
    url: str|None
    score: float

class Company:
    name: str
    domain: str
    description: str
    industry: str
    location: str

class Agent(ABC):
    def process_signals(self, signals: list[Signal]) -> list[Action]
        raise NotImplemented()
