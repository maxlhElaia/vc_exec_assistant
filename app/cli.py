import click
from services.signals import generate_signals
from domain.models import PressMentionSignal
from services.agents import PressMentionAgent


@click.command()
def run():
    for signal in generate_signals():
        # print(signal)
        if type(signal) == PressMentionSignal:
            print('Press Mention Signal')
            agent = PressMentionAgent()
            actions = agent.process_signals([signal])
            for action in actions:
                print(action)

if __name__ == '__main__':
    run()