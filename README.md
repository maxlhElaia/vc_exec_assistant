
Data-Driven Hackathon

# Midas AI: VC Executive Assistant - Team 8

![alt text](https://i.imgur.com/O8vZHPM.png)

> This project was built as part of the Data-Driven VC Hackathon organized by [Red River West](https://redriverwest.com) & [Bivwak! by BNP Paribas](https://bivwak.bnpparibas/)

## Installation
This creates a data
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run
```
python -m app.cli
```

## dumping and reading data
```
from pydantic.json import pydantic_encoder

...

# dumping
with open('.data/signals/linkedin/signals.json', 'w') as fp:
    json.dump([signal.model_dump() for signal in signals], fp, indent=2, default=pydantic_encoder)

# loading
with open('.data/signals/linkedin/signals.json', 'r') as fp:
    data = json.load(fp)
    for elem in data:
        print(HeadcountChangeSignal.model_validate(elem))
```