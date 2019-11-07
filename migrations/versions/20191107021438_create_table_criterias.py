"""create_table_criterias

Revision ID: fd30b90f1f7d
Revises: 3bfd3a472e4a
Create Date: 2019-11-07 02:14:38.075344

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fd30b90f1f7d'
down_revision = '3bfd3a472e4a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'criterias',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('criterias', sa.JSON, server_default='[]', nullable=False),
        sa.Column('created_at', sa.TIMESTAMP, nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP, nullable=True),
    )


def downgrade():
    op.drop_table('criterias')
