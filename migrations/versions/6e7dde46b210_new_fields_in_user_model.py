"""new fields in user model

Revision ID: 6e7dde46b210
Revises: e9ba5e7a5ed0
Create Date: 2024-03-17 19:46:56.709536

"""

from alembic import op
import sqlalchemy as sa
from datetime import datetime, timezone


# revision identifiers, used by Alembic.
revision = "6e7dde46b210"
down_revision = "e9ba5e7a5ed0"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.add_column(sa.Column("about_me", sa.String(length=140), nullable=True))
        batch_op.add_column(
            sa.Column(
                "last_seen",
                sa.DateTime(),
                default=lambda: datetime.now(timezone.utc),
                nullable=True,
            )
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_column("last_seen")
        batch_op.drop_column("about_me")

    # ### end Alembic commands ###
