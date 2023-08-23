"""empty message

Revision ID: de535b33673f
Revises: 23c8a68e6a52
Create Date: 2023-08-23 23:54:26.464131

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'de535b33673f'
down_revision = '23c8a68e6a52'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('feedbacks', schema=None) as batch_op:
        batch_op.add_column(sa.Column('resolve_res', mysql.LONGTEXT(), nullable=True, comment='处理结果'))
        batch_op.alter_column('feedback_text',
               existing_type=mysql.VARCHAR(collation='utf8mb4_general_ci', length=500),
               type_=mysql.LONGTEXT(),
               existing_comment='反馈内容',
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('feedbacks', schema=None) as batch_op:
        batch_op.alter_column('feedback_text',
               existing_type=mysql.LONGTEXT(),
               type_=mysql.VARCHAR(collation='utf8mb4_general_ci', length=500),
               existing_comment='反馈内容',
               existing_nullable=False)
        batch_op.drop_column('resolve_res')

    # ### end Alembic commands ###