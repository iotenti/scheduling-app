"""starting over

Revision ID: 10e0ab389a11
Revises: 
Create Date: 2018-11-08 14:15:27.263291

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '10e0ab389a11'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('accounts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('primary_fname', sa.String(length=50), nullable=True),
    sa.Column('primary_lname', sa.String(length=50), nullable=True),
    sa.Column('primary_cell_phone', sa.String(length=10), nullable=True),
    sa.Column('primary_email', sa.String(length=120), nullable=True),
    sa.Column('primary_home_phone', sa.String(length=10), nullable=True),
    sa.Column('secondary_fname', sa.String(length=50), nullable=True),
    sa.Column('secondary_lname', sa.String(length=50), nullable=True),
    sa.Column('secondary_cell_phone', sa.String(length=10), nullable=True),
    sa.Column('secondary_email', sa.String(length=120), nullable=True),
    sa.Column('account_bal', sa.Float(precision=10), nullable=True),
    sa.Column('account_credit', sa.Float(precision=10), nullable=True),
    sa.Column('secondary_home_phone', sa.String(length=10), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('instruments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('instrument', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('recurring_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('recurring_type', sa.String(length=15), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('teachers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('first_name', sa.String(length=50), nullable=True),
    sa.Column('last_name', sa.String(length=50), nullable=True),
    sa.Column('phone_num', sa.String(length=10), nullable=True),
    sa.Column('address', sa.String(length=120), nullable=True),
    sa.Column('city', sa.String(length=50), nullable=True),
    sa.Column('state', sa.String(length=2), nullable=True),
    sa.Column('zipcode', sa.String(length=5), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('notes', sa.String(length=500), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_teachers_email'), 'teachers', ['email'], unique=True)
    op.create_index(op.f('ix_teachers_username'), 'teachers', ['username'], unique=True)
    op.create_table('week_days',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('day_of_week', sa.String(length=2), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('invoices',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('account_id', sa.Integer(), nullable=True),
    sa.Column('invoice_date', sa.DateTime(), nullable=True),
    sa.Column('invoice_total', sa.Float(precision=10), nullable=True),
    sa.Column('payment_total', sa.Float(precision=10), nullable=True),
    sa.Column('invoice_due_date', sa.DateTime(timezone=50), nullable=True),
    sa.Column('payment_date', sa.DateTime(timezone=50), nullable=True),
    sa.ForeignKeyConstraint(['account_id'], ['accounts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_invoices_invoice_date'), 'invoices', ['invoice_date'], unique=False)
    op.create_table('students',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('account_ID', sa.Integer(), nullable=True),
    sa.Column('teacher_ID', sa.Integer(), nullable=True),
    sa.Column('first_name', sa.String(length=50), nullable=True),
    sa.Column('last_name', sa.String(length=50), nullable=True),
    sa.Column('instrument', sa.String(length=50), nullable=True),
    sa.Column('notes', sa.String(length=500), nullable=True),
    sa.ForeignKeyConstraint(['account_ID'], ['accounts.id'], ),
    sa.ForeignKeyConstraint(['teacher_ID'], ['teachers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('attendance',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('student_ID', sa.Integer(), nullable=True),
    sa.Column('account_ID', sa.Integer(), nullable=True),
    sa.Column('was_present', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['account_ID'], ['accounts.id'], ),
    sa.ForeignKeyConstraint(['student_ID'], ['students.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_attendance_was_present'), 'attendance', ['was_present'], unique=False)
    op.create_table('lessons',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('student_ID', sa.Integer(), nullable=True),
    sa.Column('teacher_ID', sa.Integer(), nullable=True),
    sa.Column('start_date', sa.DateTime(), nullable=False),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.Column('start_time', sa.String(length=10), nullable=False),
    sa.Column('end_time', sa.String(length=10), nullable=True),
    sa.Column('is_hour', sa.Boolean(), nullable=False),
    sa.Column('is_recurring', sa.Boolean(), nullable=False),
    sa.Column('created_by', sa.String(length=50), nullable=True),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['student_ID'], ['students.id'], ),
    sa.ForeignKeyConstraint(['teacher_ID'], ['teachers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_lessons_start_time'), 'lessons', ['start_time'], unique=False)
    op.create_table('recurring_pattern',
    sa.Column('lesson_ID', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('recurring_type_id', sa.Integer(), nullable=True),
    sa.Column('max_occurrences', sa.Integer(), nullable=True),
    sa.Column('day_of_week_ID', sa.Integer(), nullable=True),
    sa.Column('day_of_month', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['day_of_week_ID'], ['week_days.id'], ),
    sa.ForeignKeyConstraint(['lesson_ID'], ['lessons.id'], ),
    sa.ForeignKeyConstraint(['recurring_type_id'], ['recurring_type.id'], ),
    sa.PrimaryKeyConstraint('lesson_ID')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('recurring_pattern')
    op.drop_index(op.f('ix_lessons_start_time'), table_name='lessons')
    op.drop_table('lessons')
    op.drop_index(op.f('ix_attendance_was_present'), table_name='attendance')
    op.drop_table('attendance')
    op.drop_table('students')
    op.drop_index(op.f('ix_invoices_invoice_date'), table_name='invoices')
    op.drop_table('invoices')
    op.drop_table('week_days')
    op.drop_index(op.f('ix_teachers_username'), table_name='teachers')
    op.drop_index(op.f('ix_teachers_email'), table_name='teachers')
    op.drop_table('teachers')
    op.drop_table('recurring_type')
    op.drop_table('instruments')
    op.drop_table('accounts')
    # ### end Alembic commands ###
