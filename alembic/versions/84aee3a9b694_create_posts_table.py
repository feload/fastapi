"""Create Posts Table

Revision ID: 84aee3a9b694
Revises:
Create Date: 2021-12-19 19:21:11.926719

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '84aee3a9b694'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("posts",
                    sa.Column("id", sa.Integer(),
                              nullable=False, primary_key=True),
                    sa.Column("title", sa.String(), nullable=False))


def downgrade():
    op.drop_table("posts")
