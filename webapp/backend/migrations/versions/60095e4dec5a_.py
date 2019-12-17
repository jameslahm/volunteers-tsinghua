"""empty message

Revision ID: 60095e4dec5a
Revises: 2a5946d17946
Create Date: 2019-12-09 12:09:41.907175

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '60095e4dec5a'
down_revision = '2a5946d17946'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('activities', sa.Column('isMessage', sa.Boolean(), nullable=True))
    op.add_column('activities', sa.Column('time', sa.DateTime(), nullable=True))
    op.alter_column('activities', 'isRead',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=True)
    op.alter_column('messages', 'isRead',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=True)
    op.alter_column('useractivities', 'isRead',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('useractivities', 'isRead',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    op.alter_column('messages', 'isRead',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    op.alter_column('activities', 'isRead',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    op.drop_column('activities', 'time')
    op.drop_column('activities', 'isMessage')
    # ### end Alembic commands ###