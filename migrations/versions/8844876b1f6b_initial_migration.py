"""Initial migration

Revision ID: 8844876b1f6b
Revises: 
Create Date: 2022-07-07 15:53:34.608875

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8844876b1f6b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('devotee',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uid', sa.Text(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('phone', sa.Text(), nullable=False),
    sa.Column('email', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('phone')
    )
    op.create_index(op.f('ix_devotee_uid'), 'devotee', ['uid'], unique=True)
    op.create_table('pooja',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uid', sa.Text(), nullable=True),
    sa.Column('media', sa.JSON(), nullable=True),
    sa.Column('temple', sa.Text(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('specific', sa.Boolean(), nullable=False),
    sa.Column('dates', sa.JSON(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('link', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_pooja_uid'), 'pooja', ['uid'], unique=True)
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uid', sa.Text(), nullable=True),
    sa.Column('deleted', sa.Boolean(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.Column('media', sa.JSON(), nullable=True),
    sa.Column('type', sa.Text(), nullable=False),
    sa.Column('title', sa.Text(), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('priority', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_post_uid'), 'post', ['uid'], unique=True)
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uid', sa.Text(), nullable=True),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_role_uid'), 'role', ['uid'], unique=True)
    op.create_table('setting',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uid', sa.Text(), nullable=True),
    sa.Column('key', sa.Text(), nullable=False),
    sa.Column('value', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_setting_uid'), 'setting', ['uid'], unique=True)
    op.create_table('volunteer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uid', sa.Text(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('phone', sa.Text(), nullable=False),
    sa.Column('occupation', sa.Text(), nullable=False),
    sa.Column('email', sa.Text(), nullable=True),
    sa.Column('identification', sa.Text(), nullable=True),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('address', sa.Text(), nullable=True),
    sa.Column('city', sa.Text(), nullable=True),
    sa.Column('pincode', sa.Integer(), nullable=True),
    sa.Column('comments', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_volunteer_uid'), 'volunteer', ['uid'], unique=True)
    op.create_table('donation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uid', sa.Text(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('devotee_id', sa.Integer(), nullable=True),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('type', sa.Text(), nullable=False),
    sa.Column('aadhaar', sa.Text(), nullable=True),
    sa.Column('pan', sa.Text(), nullable=True),
    sa.Column('recurring_interval', sa.Text(), nullable=True),
    sa.Column('number', sa.Integer(), nullable=True),
    sa.Column('start_date', sa.Date(), nullable=True),
    sa.Column('payment_id', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['devotee_id'], ['devotee.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_donation_uid'), 'donation', ['uid'], unique=True)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uid', sa.Text(), nullable=True),
    sa.Column('deleted', sa.Boolean(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('password_hash', sa.Text(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('email', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_user_uid'), 'user', ['uid'], unique=True)
    op.create_table('booking',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uid', sa.Text(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('devotee_id', sa.Integer(), nullable=True),
    sa.Column('temple', sa.Text(), nullable=False),
    sa.Column('pooja', sa.Text(), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('gotra', sa.Text(), nullable=True),
    sa.Column('nakshatra', sa.Text(), nullable=True),
    sa.Column('days', sa.JSON(), nullable=False),
    sa.Column('payment_id', sa.Text(), nullable=False),
    sa.Column('booked_by_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['booked_by_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['devotee_id'], ['devotee.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_booking_uid'), 'booking', ['uid'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_booking_uid'), table_name='booking')
    op.drop_table('booking')
    op.drop_index(op.f('ix_user_uid'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_donation_uid'), table_name='donation')
    op.drop_table('donation')
    op.drop_index(op.f('ix_volunteer_uid'), table_name='volunteer')
    op.drop_table('volunteer')
    op.drop_index(op.f('ix_setting_uid'), table_name='setting')
    op.drop_table('setting')
    op.drop_index(op.f('ix_role_uid'), table_name='role')
    op.drop_table('role')
    op.drop_index(op.f('ix_post_uid'), table_name='post')
    op.drop_table('post')
    op.drop_index(op.f('ix_pooja_uid'), table_name='pooja')
    op.drop_table('pooja')
    op.drop_index(op.f('ix_devotee_uid'), table_name='devotee')
    op.drop_table('devotee')
    # ### end Alembic commands ###
