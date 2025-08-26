"""Create Users Table.

Revision ID: 987e7bf9224b
Revises: 3bb381b6f404
Create Date: 2025-08-26 14:40:43.231301

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '987e7bf9224b'
down_revision: Union[str, Sequence[str], None] = '3bb381b6f404'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    #We create the users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False, unique=True, index=True),
        sa.Column('password', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now()),
    )
    #Now that the users table is created, we can add a foreign key to the blogs table
    op.add_column('blogs', sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete="CASCADE"), nullable=False))

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('blogs', 'user_id')
    op.drop_table('users')
