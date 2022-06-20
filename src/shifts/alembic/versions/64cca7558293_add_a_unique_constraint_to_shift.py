"""add a unique constraint to shift

Revision ID: 64cca7558293
Revises: 18ef64e6bcb5
Create Date: 2022-06-20 15:25:52.633095

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64cca7558293'
down_revision = '18ef64e6bcb5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('shift_date_shift_slot_uc', 'shifts', ['shift_date', 'shift_slot'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('shift_date_shift_slot_uc', 'shifts', type_='unique')
    # ### end Alembic commands ###