import datetime
import typing
from domain.models import Company, HeadcountChangeSignal, Signal


def generate_signals() -> typing.Iterable[Signal]:
    for i in range(100):
        company = Company(
            name=f'company {i}',
            description='very great company',
            domain='example.com',
            industry='example',
            location='Paris, France',
            primary_contact=None,
        )

        signal = HeadcountChangeSignal(
            id=str(i),
            trigger=datetime.datetime.now(),
            title='',
            description='',
            company=company.model_dump(),
            headcount_old=i,
            headcount_new=i+5
        )

        yield signal