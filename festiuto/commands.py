import click
from .app import app

@app.cli.command()
def commande():
    """À faire"""
    click.echo("À faire")

# À faire si nécessaire