"""Initial migration

Revision ID: a58e19d3c967
Revises:
Create Date: 2024-02-11 02:44:04.830794

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a58e19d3c967'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    #  link table
    op.create_table(
        "link",
        sa.Column("id", sa.String(length=12), nullable=False),
        sa.Column("original_url", sa.String(length=150), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("deleted", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_link_created_at"), "link", ["created_at"], unique=False
    )
    #  transfer table
    op.create_table(
        "transfer",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("date", sa.DateTime(), nullable=True),
        sa.Column("client_host", sa.String(length=50), nullable=True),
        sa.Column("link_id", sa.String(), nullable=True),

        sa.ForeignKeyConstraint(
            ["link_id"],
            ["link.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_transfer_date"), "transfer", ["date"], unique=False
    )




def downgrade() -> None:
    op.drop_index(op.f("ix_link_created_at"), table_name="link")
    op.drop_table("link")

    op.drop_index(op.f("ix_transfer_date"), table_name="transfer")
    op.drop_table("transfer")
