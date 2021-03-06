"""composite unique in devotee

Revision ID: 18cfe7fe1083
Revises: 8844876b1f6b
Create Date: 2022-07-19 16:09:41.600362

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '18cfe7fe1083'
down_revision = '8844876b1f6b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('unique_devotee', 'devotee', ['name', 'phone'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('unique_devotee', 'devotee', type_='unique')
    # ### end Alembic commands ###
