import datetime
from domain.models import Company, HeadcountChangeSignal, Signal


def generate_signals() -> iter[Signal]:
    for i in range(100):
        company = Company(
            name='company {i}'
            description='very great company',
            domain='example.com',
            industry='example',
            location='Paris, France',
        )

        signal = HeadcountChangeSignal(
            id=str(i),
            trigger=datetime.now(),
            title='',
            description='',
            company=company,
            headcount_old=i,
            headcount_new=i+5
        )

        yield signal