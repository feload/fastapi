"""Add foreign key to Posts table

Revision ID: abaae6ad7b95
Revises: ecff44dbd253
Create Date: 2021-12-20 08:09:07.952957

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'abaae6ad7b95'
down_revision = 'ecff44dbd253'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("user_id", sa.Integer(), nullable=False))
    op.create_foreign_key("post_users_fk",
                          source_table="posts", referent_table="users", local_cols=["user_id"], remote_cols=["id"], ondelete="CASCADE")


def downgrade():
    op.drop_constraint("post_users_fk", "posts")
    op.drop_column("posts", "user_id")
