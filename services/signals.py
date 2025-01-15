from dataclasses import dataclass
import datetime
import json
import typing
from domain.models import Company, HeadcountChangeSignal, PressMentionSignal, Signal

import psycopg2
from domain.models import Company, HeadcountChangeSignal, Signal
from services.companies import generate_companies


def generate_signals(companies: list[Company]) -> typing.Iterable[Signal]:
    for i in range(1):
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
            start_time=datetime.datetime.now(),
            end_time=datetime.datetime.now(),
            title='',
            description='',
            company=company.model_dump(),
            headcount_old=i,
            headcount_new=i+5
        )
        yield signal

        signal = PressMentionSignal(
            id=str(i),
            start_time=datetime.datetime.now(),
            end_time=datetime.datetime.now(),
            title='',
            description="""
                The human papillomavirus (HPV) causes almost all instances of cervical cancer.
                But according to our recent 12-country survey, half the population has a limited understanding of HPV.
                Learn where your country stacks up in its understanding of human papillomavirus (HPV) by reading this report.
                With every HPV test, we grow closer to a world without cervical hashtag#cancer. """,
            company=company.model_dump(),
            url_link='https://www.linkedin.com/feed/?highlightedUpdateType=TRENDING_IN_PAGE_YOU_FOLLOW&highlightedUpdateUrn=urn%3Ali%3Aactivity%3A7282652304695046147',
            plateform='linkedin',
            source_name='Roche',
            post_date=datetime.datetime.now(),
            engagement_count=323
        )

        yield signal