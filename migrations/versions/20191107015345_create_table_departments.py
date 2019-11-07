"""create_table_departments

Revision ID: 3bfd3a472e4a
Revises: cf51176aae43
Create Date: 2019-11-07 01:53:45.481937

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3bfd3a472e4a'
down_revision = 'cf51176aae43'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'departments',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('department_name', sa.String, nullable=False),
        sa.Column('positions', sa.JSON, server_default='[]', nullable=False),
        sa.Column('created_at', sa.TIMESTAMP, nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP, nullable=True),
    )


def downgrade():
    op.drop_table('departments')
