"""added relationship to teachers table

Revision ID: 1c23fd316f98
Revises: d95b8c587fce
Create Date: 2018-10-18 13:48:20.571468

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1c23fd316f98'
down_revision = 'd95b8c587fce'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('accounts', 'home_phone')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('accounts', sa.Column('home_phone', sa.VARCHAR(length=10), nullable=True))
    # ### end Alembic commands ###