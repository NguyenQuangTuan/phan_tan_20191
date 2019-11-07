"""create_table_kpis

Revision ID: cf51176aae43
Revises:
Create Date: 2019-11-07 01:46:48.526441

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cf51176aae43'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'kpis',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('type', sa.String, nullable=False),
        sa.Column('criterias', sa.JSON, server_default='[]', nullable=False),
        sa.Column('department_id', sa.Integer, nullable=True),
        sa.Column('employee_id', sa.Integer, nullable=True),
        sa.Column('created_at', sa.TIMESTAMP, nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP, nullable=True),
    )


def downgrade():
    op.drop_table('kpis')
