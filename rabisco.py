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


def remove_last_newline(content):
    if content[-1] == '\n':
        content = content[:-1]

    return content


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
                title = remove_last_newline(title)

            created_at = note.name.split('_')[0]

            notes[index] = {
                'datetime': datetime.strptime(created_at, DATETIME_FORMAT),
                'title': title,
                'file': note,
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

    def get_or_error(self, id):
        notes = self.list_notes()

        try:
            return notes[id]
        except KeyError:
            click.secho('Note %s not found' % id, fg='red')
            sys.exit(1)

    def open(self, id):
        note = self.get_or_error(id)
        note_file = str(note['file'])
        self.open_editor(note_file)

    def cat(self, id):
        note = self.get_or_error(id)
        with note['file'].open() as f:
            content = f.read()

        content = remove_last_newline(content)
        click.echo(content)

    def rm(self, id):
        note = self.get_or_error(id)
        note_file = str(note['file'])
        os.remove(note_file)
