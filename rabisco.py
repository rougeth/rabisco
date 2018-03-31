import os
import tempfile
import sys
from subprocess import call
from pathlib import Path

import click
from slugify import slugify


EDITOR = os.environ.get('EDITOR', 'vim')


def get_default_path():
    return str(Path.home() / '.rabisco')


class Rabisco:
    def __init__(self, path):
        self.path = Path(path)
        self.path.mkdir(exist_ok=True)

    def _open_editor(self, filename):
        call([EDITOR, filename])

    def _edit_note(self):
        with tempfile.NamedTemporaryFile(mode='w+') as f:
            self._open_editor(f.name)
            return f.read()

    def mk(self):
        content = self._edit_note()
        if not content:
            click.echo('Aborted')
            sys.exit(1)

        filename = self.path / slugify(content[:40], separator='_')
        with filename.open('w') as f:
            f.write(content)

        click.echo('saved')

    def ls(self):
        files = os.listdir(str(self.path))
        for f in files:
            click.echo(f)
