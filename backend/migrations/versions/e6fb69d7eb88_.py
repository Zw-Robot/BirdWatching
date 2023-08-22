"""empty message

Revision ID: e6fb69d7eb88
Revises: 1a6e4ff326f2
Create Date: 2023-08-21 23:18:38.726301

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e6fb69d7eb88'
down_revision = '1a6e4ff326f2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('bird_group', schema=None) as batch_op:
        batch_op.drop_constraint('bird_group_ibfk_1', type_='foreignkey')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('bird_group', schema=None) as batch_op:
        batch_op.create_foreign_key('bird_group_ibfk_1', 'bird_match', ['match_id'], ['id'])

    # ### end Alembic commands ###