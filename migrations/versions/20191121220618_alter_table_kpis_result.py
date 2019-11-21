"""alter_table_kpis_result

Revision ID: 732286f5f95d
Revises: 267317d2f2b7
Create Date: 2019-11-21 22:06:18.156834

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '732286f5f95d'
down_revision = '267317d2f2b7'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('kpi_results', 'project_id', type_=sa.String)
    op.alter_column('kpi_results', 'employee_id', type_=sa.String)


def downgrade():
    op.alter_column('kpi_results', 'project_id', type_=sa.Integer)
    op.alter_column('kpi_results', 'employee_id', type_=sa.Integer)
