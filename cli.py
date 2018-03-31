from pathlib import Path

import click
from rabisco import Rabisco, get_default_path


@click.group()
@click.option('--path', envvar='RABISCO_PATH', default=get_default_path())
@click.pass_context
def cli(ctx, path):
    ctx.obj = Rabisco(path=path)


@cli.command()
@click.pass_obj
def mk(rabisco):
    rabisco.mk()


@cli.command()
@click.pass_obj
def ls(rabisco):
    rabisco.ls()


@cli.command()
@click.argument('id', type=click.INT)
@click.pass_obj
def rm(rabisco, id):
    rabisco.rm(id)
