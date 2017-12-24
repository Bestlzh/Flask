"""empty message

Revision ID: fccc5037ed40
Revises: e62c4aa6dc3f
Create Date: 2017-11-03 15:42:46.842903

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fccc5037ed40'
down_revision = 'e62c4aa6dc3f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('goods', sa.Column('viemcount', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('goods', 'viemcount')
    # ### end Alembic commands ###