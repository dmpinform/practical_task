import click


def create_cli(abonement_run_alembic_cmd):

    @click.group()
    def cli():
        pass

    @cli.command(context_settings={'ignore_unknown_options': True})
    @click.argument('alembic_args', nargs=-1, type=click.UNPROCESSED)
    def run_alembic(alembic_args):
        abonement_run_alembic_cmd(*alembic_args)

    return cli
