"""added relationship between invoices and accounts

Revision ID: af3e1959d978
Revises: f5ba915b6b84
Create Date: 2018-10-19 10:18:43.893567

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'af3e1959d978'
down_revision = 'f5ba915b6b84'
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