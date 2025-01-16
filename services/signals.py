import datetime
import json
import logging
import random
import typing
from domain.models import (
    Company,
    FollowerCountChangeSignal,
    HeadcountChangeSignal,
    NewCompetitorSignal,
    PressMentionSignal,
    Signal,
)

from domain.models import Company, HeadcountChangeSignal, Signal
from services.startupradar import generate_competitors

LOGGER = logging.getLogger(__name__)


def generate_signals(companies: list[Company]) -> typing.Iterable[Signal]:
    signals = []

    for company in companies:
        company_signals = generate_signals_for_company(company)
        LOGGER.info(f"generated {len(company_signals)} signals for {company.name}")

        signals.extend(company_signals)

    return signals


def generate_signals_for_company(company: Company) -> typing.Iterable[Signal]:
    hc_old = random.randint(10, 100)
    hc_new = max(hc_old + random.randint(-10, 10), 0)
    diff = hc_new - hc_old

    if random.random() < 0.0:
        return [
            HeadcountChangeSignal(
                id=f"headcount_change_{company.name}",
                start_time=datetime.datetime.now(),
                end_time=datetime.datetime.now(),
                title=f"Headcount {'grew' if diff > 0 else 'shrank'}",
                description=f"The headcount of this company {'grew' if diff > 0 else 'shrank'} from {hc_old} to {hc_new} in the last month",
                company=company,
                headcount_old=hc_old,
                headcount_new=hc_new,
            )
        ]
    else:
        competitors = list(generate_competitors(company))
        if competitors:
            competitor = random.choice(competitors)

            signal = NewCompetitorSignal(
                id=f"new_competitor_{company.name}_{competitor.name}",
                start_time=datetime.datetime.now(),
                end_time=datetime.datetime.now(),
                title=f"New competitor: {competitor.name}",
                description=f"{competitor.name} is a new competitor to {company.name}",
                company=company,
                competitor=competitor,
            )
            return [signal]


def generate_dummy_signals(companies: list[Company]) -> typing.Iterable[Signal]:
    yield from generate_linkedin_from_file()

    for i in range(1):
        company = Company(
            name=f"company {i}",
            description="very great company",
            domain="example.com",
            industry="example",
            location="Paris, France",
            linkedin_url=None,
            primary_contact=None,
        )

        signal = HeadcountChangeSignal(
            id=str(i),
            start_time=datetime.datetime.now(),
            end_time=datetime.datetime.now(),
            title="",
            description="",
            company=company.model_dump(),
            headcount_old=i,
            headcount_new=i + 5,
        )
        yield signal

        signal = PressMentionSignal(
            id=str(i),
            start_time=datetime.datetime.now(),
            end_time=datetime.datetime.now(),
            title="",
            description="""
                The human papillomavirus (HPV) causes almost all instances of cervical cancer.
                But according to our recent 12-country survey, half the population has a limited understanding of HPV.
                Learn where your country stacks up in its understanding of human papillomavirus (HPV) by reading this report.
                With every HPV test, we grow closer to a world without cervical hashtag#cancer. """,
            company=company.model_dump(),
            url_link="https://www.linkedin.com/feed/?highlightedUpdateType=TRENDING_IN_PAGE_YOU_FOLLOW&highlightedUpdateUrn=urn%3Ali%3Aactivity%3A7282652304695046147",
            plateform="linkedin",
            source_name="Roche",
            post_date=datetime.datetime.now(),
            engagement_count=323,
        )

        yield signal


def generate_linkedin_from_file():
    types = {
        HeadcountChangeSignal: "headcount",
        FollowerCountChangeSignal: "followers",
    }
    for type_, filename in types.items():
        with open(f".data/signals/linkedin/{filename}.json", "r") as fp:
            singals_raw = json.load(fp)
            for signal_raw in singals_raw:
                yield type_.model_validate(signal_raw)


if __name__ == "__main__":
    signals = generate_linkedin_from_file()
    # signals = generate_signals([])
    # for signal in signals:
    #     print(signal)
