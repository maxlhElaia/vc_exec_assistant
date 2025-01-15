import datetime
import json
import typing
from domain.models import Company, FollowerCountChangeSignal, HeadcountChangeSignal, PressMentionSignal, Signal

from domain.models import Company, HeadcountChangeSignal, Signal

# class Company(BaseModel):
#     model_config = ConfigDict(from_attributes=True)

#     name: str
#     domain: str
#     linkedin_url: str|None
#     description: str
#     industry: str
#     location: str
#     primary_contact: Contact|None

def generate_signals(companies: list[Company]) -> typing.Iterable[Signal]:
    yield from generate_linkedin_from_file()

    for i in range(1):
        company = Company(
            name=f'company {i}',
            description='very great company',
            domain='example.com',
            industry='example',
            location='Paris, France',
            linkedin_url=None,
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

def generate_linkedin_from_file():
    types = {
        HeadcountChangeSignal: 'headcount',
        FollowerCountChangeSignal: 'followers',
    }
    for type_, filename in types.items():
        with open(f'.data/signals/linkedin/{filename}.json', 'r') as fp:
            singals_raw = json.load(fp)
            for signal_raw in singals_raw:
                yield type_.model_validate(signal_raw)

if __name__ == '__main__':
    signals = generate_linkedin_from_file()
    # signals = generate_signals([])
    # for signal in signals:
    #     print(signal)