"""empty message

Revision ID: e23f45752a79
Revises: c4e46c975b5e
Create Date: 2018-09-28 18:56:56.281923

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e23f45752a79'
down_revision = 'c4e46c975b5e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('list_item', 'updated_on')
    op.add_column('shopping_list', sa.Column('created_on', sa.DateTime(), nullable=True))
    op.add_column('shopping_list', sa.Column('updated_on', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('shopping_list', 'updated_on')
    op.drop_column('shopping_list', 'created_on')
    op.add_column('list_item', sa.Column('updated_on', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
