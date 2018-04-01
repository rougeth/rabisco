import os
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from subprocess import call

import click
from slugify import slugify

DATETIME_FORMAT = '%y%m%d%H%M%S'


def get_default_path():
    return str(Path.home() / '.rabisco')


class Rabisco:
    editor = os.environ.get('EDITOR', 'vim')

    def __init__(self, path):
        self.path = Path(path)
        self.path.mkdir(exist_ok=True)

    def open_editor(self, filename):
        call([self.editor, filename])

    def note_from_editor(self):
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.md') as f:
            self.open_editor(f.name)
            return f.read()

    def now(self):
        now = datetime.now()
        return now.strftime(DATETIME_FORMAT)

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
            click.secho('Aborted', fg='yellow')
            sys.exit(1)

        filename = self.filename_from_content(content)
        with filename.open('w') as f:
            f.write(content)

        click.secho('Note created', fg='green')

    def list_notes(self):
        notes = {}
        index = 0
        for note in sorted(self.path.iterdir()):
            with note.open() as f:
                title = f.readline()
                if title[-1] == '\n':
                    title = title[:-1]

            created_at = note.name.split('_')[0]

            notes[index] = {
                'datetime': datetime.strptime(created_at, DATETIME_FORMAT),
                'title': title,
                'filename': note,
            }

            index += 1

        return notes

    def ls(self):
        notes = self.list_notes()

        for index, note in notes.items():
            click.echo('{index}: {title}'.format(
               index=click.style(str(index), fg='cyan'),
               title=note['title'],
            ))

    def open(self, id):
        notes = self.list_notes()
        try:
            note_file = str(notes[id]['filename'])
        except KeyError:
            click.secho('Note %s not found' % id, fg='red')
            sys.exit(1)

        self.open_editor(note_file)

    def rm(self, id):
        notes = self.list_notes()
        try:
            note_file = notes[id]['filename']
        except KeyError:
            click.secho('Note %s not found' % id, fg='red')
            sys.exit(1)

        os.remove(str(note_file))
