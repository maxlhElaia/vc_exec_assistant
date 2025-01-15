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

