"""create_table_kpi_results

Revision ID: fb83ff2a9cea
Revises: fd30b90f1f7d
Create Date: 2019-11-18 23:12:26.308602

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fb83ff2a9cea'
down_revision = 'fd30b90f1f7d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'kpi_results',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('type', sa.String, nullable=False),
        sa.Column('criterias', sa.JSON, server_default='[]', nullable=False),
        sa.Column('department_id', sa.Integer, nullable=True),
        sa.Column('employee_id', sa.Integer, nullable=True),
        sa.Column('project_id', sa.Integer, nullable=True),
        sa.Column('created_at', sa.TIMESTAMP, nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP, nullable=True),
    )


def downgrade():
    op.drop_table('kpi_results')
