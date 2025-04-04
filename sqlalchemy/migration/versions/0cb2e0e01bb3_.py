"""empty message

Revision ID: 0cb2e0e01bb3
Revises: 
Create Date: 2025-01-28 16:01:29.521016

"""
from typing import Sequence, Union

from alembic import op

import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '0cb2e0e01bb3'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'sensors', sa.Column('name', sa.String(), nullable=False),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'union_sensors', sa.Column('type', sa.String(), nullable=False),
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('one_level', sa.Float(), nullable=True),
        sa.Column('two_level', sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'carbon_dioxide_sensors',
        sa.Column('co2_level', sa.Float(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ['id'],
            ['sensors.id'],
        ), sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'moisture_sensors',
        sa.Column('moisture_level', sa.Float(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ['id'],
            ['sensors.id'],
        ), sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'oxygen_sensors', sa.Column('oxygen_level', sa.Float(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ['id'],
            ['sensors.id'],
        ), sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('oxygen_sensors')
    op.drop_table('moisture_sensors')
    op.drop_table('carbon_dioxide_sensors')
    op.drop_table('union_sensors')
    op.drop_table('sensors')
    # ### end Alembic commands ###
