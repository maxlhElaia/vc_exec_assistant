import click
from services.signals import generate_signals


@click.command()
def run():
    for signal in generate_signals():
        print(signal)

if __name__ == '__main__':
    run()