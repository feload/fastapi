"""empty message

Revision ID: 34c7bf8c1968
Revises: abaae6ad7b95
Create Date: 2021-12-20 08:14:07.438416

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import null


# revision identifiers, used by Alembic.
revision = '34c7bf8c1968'
down_revision = 'abaae6ad7b95'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("published", sa.Boolean(),
                  nullable=False, server_default="TRUE"),)
    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(
        timezone=True), nullable=False, server_default=sa.text("now()")),)


def downgrade():
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
