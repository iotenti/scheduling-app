"""added instruments

Revision ID: de31ceb7cfd6
Revises: 05a38ebe80f5
Create Date: 2018-10-02 09:35:11.736280

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de31ceb7cfd6'
down_revision = '05a38ebe80f5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('instruments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('instrument', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('students', sa.Column('instrument', sa.String(length=50), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('students', 'instrument')
    op.drop_table('instruments')
    # ### end Alembic commands ###
