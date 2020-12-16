import click
import os

from src.notes import Notebook

note = Notebook()

@click.group()
def cli():
	pass


@cli.command()
@click.argument('title', nargs=-1, type=str)
@click.option('--tag', type=str)
def new(title, tag):
	combined_title = ' '.join(title)
	tag_list = [tag]

	note.create_note(combined_title, tag_list)


@cli.command()
def list():
	note.list_notes()


@cli.command()
@click.argument('id', nargs=1, type=str)
def read(id):
	note.get_note(id)


if __name__ == '__main__':
    cli()