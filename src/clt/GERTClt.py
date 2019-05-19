import click
import requests

@click.group()
def cli():
    pass

@cli.command()
def testServiceAPI():
    r = requests.get(url = "http://localhost:5000")
    print(r.text)

@cli.command()
def startDataCollectionRoutine():
    r = requests.get(url = "http://localhost:5000/routines/datacollection/start")
    print(r.text)


if __name__ == '__main__':
    cli()