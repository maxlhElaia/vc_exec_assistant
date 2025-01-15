import datetime
from pydantic import BaseModel

class Company(BaseModel):
    pass

class Signal(BaseModel):
    id: str
    trigger: datetime.datetime
    # signaltype: str
    title: str
    description: str
    company: Company

class HeadcountChangeSignal(Signal):
    headcount_new: int
    headcount_old: int 

class Action(BaseModel):
    signal: Signal
    title: str
    description: str
    url: str|None
    score: float

class Company(BaseModel):
    name: str
    domain: str
    description: str
    industry: str
    location: str

