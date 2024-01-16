from reports.adapters.cli import create_cli

from .alembic_runner import run_cmd as abonement_run_alembic_cmd

cli = create_cli(abonement_run_alembic_cmd)
