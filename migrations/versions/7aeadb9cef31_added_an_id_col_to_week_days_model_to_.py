"""added an id col to week_days model to eliminate if statements

Revision ID: 7aeadb9cef31
Revises: 10e0ab389a11
Create Date: 2018-11-09 10:29:12.591860

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7aeadb9cef31'
down_revision = '10e0ab389a11'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('week_days', sa.Column('cal_ID', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('week_days', 'cal_ID')
    # ### end Alembic commands ###
