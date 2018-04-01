import click
from rabisco import Rabisco, get_default_path


@click.group()
@click.option('--path', envvar='RABISCO_PATH', default=get_default_path())
@click.pass_context
def cli(ctx, path):
    """Rabisco"""
    ctx.obj = Rabisco(path=path)


@cli.command()
@click.pass_obj
def mk(rabisco):
    """Create a note"""
    rabisco.mk()


@cli.command()
@click.pass_obj
def ls(rabisco):
    """List notes"""
    rabisco.ls()


@cli.command()
@click.argument('id', type=click.INT)
@click.pass_obj
def rm(rabisco, id):
    """Remove a note"""
    rabisco.rm(id)


@cli.command()
@click.argument('id', type=click.INT)
@click.pass_obj
def open(rabisco, id):
    """Open a note to edition"""
    rabisco.open(id)


@cli.command()
@click.argument('id', type=click.INT)
@click.pass_obj
def cat(rabisco, id):
    """Read note content"""
    rabisco.cat(id)
