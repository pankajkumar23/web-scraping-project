"""update_hotel_table

Revision ID: 2fe7e7802026
Revises: 
Create Date: 2025-05-13 12:07:43.175302

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2fe7e7802026'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('hotel_data', schema=None) as batch_op:
        batch_op.add_column(sa.Column('hotel_description', sa.Text(), nullable=True))
        batch_op.drop_column('exceptional_facilities')
        batch_op.drop_column('comfortable_accommodations')
        batch_op.drop_column('dining_experience')
        batch_op.drop_column('location')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('hotel_data', schema=None) as batch_op:
        batch_op.add_column(sa.Column('location', sa.TEXT(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('dining_experience', sa.TEXT(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('comfortable_accommodations', sa.TEXT(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('exceptional_facilities', sa.TEXT(), autoincrement=False, nullable=True))
        batch_op.drop_column('hotel_description')

    # ### end Alembic commands ###
