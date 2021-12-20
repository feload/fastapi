"""Add content column to posts table

Revision ID: b35bd73eaccb
Revises: 84aee3a9b694
Create Date: 2021-12-19 19:27:17.942801

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import null


# revision identifiers, used by Alembic.
revision = 'b35bd73eaccb'
down_revision = '84aee3a9b694'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))


def downgrade():
    op.drop_column("posts", "content")
