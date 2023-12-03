"""empty message

Revision ID: 78fe6f72d12d
Revises: 2cd3306b7e79
Create Date: 2023-12-03 17:00:50.481959

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78fe6f72d12d'
down_revision = '2cd3306b7e79'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('bird_inventory', schema=None) as batch_op:
        batch_op.add_column(sa.Column('pinying', sa.String(length=300), nullable=True))
        batch_op.add_column(sa.Column('simple_pinying', sa.String(length=300), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('bird_inventory', schema=None) as batch_op:
        batch_op.drop_column('simple_pinying')
        batch_op.drop_column('pinying')

    # ### end Alembic commands ###