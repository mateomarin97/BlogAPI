"""Create Post Table.

Revision ID: 3bb381b6f404
Revises: 
Create Date: 2025-08-26 14:15:29.480163

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3bb381b6f404'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'blogs',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('body', sa.String(length=1000), nullable=False),
        sa.Column('published', sa.Boolean, server_default='True'),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now()),
    )
    
    #If you want to add a new column to this table in a further revision you can do the following there
    #op.add_column('blogs', sa.Column('new_column', sa.String(length=255), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('blogs')

    #If you want to remove a column from this table in a further revision you can do the following there
    #op.drop_column('blogs', 'column_name')