"""alter_table_kpis

Revision ID: 267317d2f2b7
Revises: fb83ff2a9cea
Create Date: 2019-11-21 21:59:41.001948

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '267317d2f2b7'
down_revision = 'fb83ff2a9cea'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('kpis', 'project_id', type_=sa.String)
    op.alter_column('kpis', 'employee_id', type_=sa.String)


def downgrade():
    op.alter_column('kpis', 'project_id', type_=sa.Integer)
    op.alter_column('kpis', 'employee_id', type_=sa.Integer)
