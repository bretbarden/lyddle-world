"""empty message

Revision ID: d7ea95e76ac7
Revises: 351f92f441e0
Create Date: 2023-10-16 15:37:44.460590

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd7ea95e76ac7'
down_revision = '351f92f441e0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chatgpt_responses', schema=None) as batch_op:
        batch_op.alter_column('front_cover',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('title_page',
               existing_type=sa.VARCHAR(),
               nullable=True)

    with op.batch_alter_table('dalle_responses', schema=None) as batch_op:
        batch_op.alter_column('front_cover_imageurl',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('page01_imageurl',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('page02_imageurl',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('page03_imageurl',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('page04_imageurl',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('page05_imageurl',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('page06_imageurl',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('page07_imageurl',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('page08_imageurl',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('page09_imageurl',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('page10_imageurl',
               existing_type=sa.VARCHAR(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('dalle_responses', schema=None) as batch_op:
        batch_op.alter_column('page10_imageurl',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('page09_imageurl',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('page08_imageurl',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('page07_imageurl',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('page06_imageurl',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('page05_imageurl',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('page04_imageurl',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('page03_imageurl',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('page02_imageurl',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('page01_imageurl',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('front_cover_imageurl',
               existing_type=sa.VARCHAR(),
               nullable=False)

    with op.batch_alter_table('chatgpt_responses', schema=None) as batch_op:
        batch_op.alter_column('title_page',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('front_cover',
               existing_type=sa.VARCHAR(),
               nullable=False)

    # ### end Alembic commands ###
