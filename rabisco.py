import os
import tempfile
import sys
from datetime import datetime
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

    def open_editor(self, filename):
        call([EDITOR, filename])

    def note_from_editor(self):
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.md') as f:
            self.open_editor(f.name)
            return f.read()

    def now(self):
        now = datetime.now()
        return now.strftime('%y%m%d%H%M')

    def filename_from_content(self, content):
        partial = slugify(content[:42], separator='_')
        now = self.now()
        filename = '{datetime}_{partial_name}.md'.format(
            datetime=now,
            partial_name=partial
        )

        return self.path / filename

    def mk(self):
        content = self.note_from_editor()
        if not content:
            click.echo('Aborted')
            sys.exit(1)

        filename = self.filename_from_content(content)
        with filename.open('w') as f:
            f.write(content)

        click.echo('saved')

    def ls(self):
        files = os.listdir(str(self.path))
        for f in files:
            click.echo(f)
