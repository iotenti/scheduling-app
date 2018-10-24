"""added admin field to teachers

Revision ID: dbfee9936757
Revises: a0440fbd1613
Create Date: 2018-10-24 10:55:18.269759

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dbfee9936757'
down_revision = 'a0440fbd1613'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('accounts', 'home_phone')
    op.create_index(op.f('ix_attendence_was_present'), 'attendence', ['was_present'], unique=False)
    op.create_index(op.f('ix_invoices_invoice_date'), 'invoices', ['invoice_date'], unique=False)
    op.drop_constraint(None, 'students', type_='foreignkey')
    op.drop_column('students', 'attendence_ID')
    op.add_column('teachers', sa.Column('is_admin', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('teachers', 'is_admin')
    op.add_column('students', sa.Column('attendence_ID', sa.INTEGER(), nullable=True))
    op.create_foreign_key(None, 'students', 'attendence', ['attendence_ID'], ['id'])
    op.drop_index(op.f('ix_invoices_invoice_date'), table_name='invoices')
    op.drop_index(op.f('ix_attendence_was_present'), table_name='attendence')
    op.add_column('accounts', sa.Column('home_phone', sa.VARCHAR(length=10), nullable=True))
    # ### end Alembic commands ###
