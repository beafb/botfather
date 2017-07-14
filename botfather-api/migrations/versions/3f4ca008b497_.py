"""empty message

Revision ID: 3f4ca008b497
Revises: 50a28da6203d
Create Date: 2017-07-14 19:58:17.988550

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '3f4ca008b497'
down_revision = '50a28da6203d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('film', 'duration',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=300),
               existing_nullable=True)
    op.alter_column('film', 'quality',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               type_=sa.String(length=300),
               existing_nullable=True)
    op.alter_column('film', 'stars',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               type_=sa.String(length=300),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('film', 'stars',
               existing_type=sa.String(length=300),
               type_=postgresql.DOUBLE_PRECISION(precision=53),
               existing_nullable=True)
    op.alter_column('film', 'quality',
               existing_type=sa.String(length=300),
               type_=postgresql.DOUBLE_PRECISION(precision=53),
               existing_nullable=True)
    op.alter_column('film', 'duration',
               existing_type=sa.String(length=300),
               type_=sa.INTEGER(),
               existing_nullable=True)
    # ### end Alembic commands ###
