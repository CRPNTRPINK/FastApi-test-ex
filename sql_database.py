from sqlalchemy import MetaData, Column, Integer, String, Date, ForeignKey, Table, Text
metadata = MetaData()

posts = Table(
    "posts",
    metadata,
    Column('id', Integer, primary_key=True),
    Column('rubrics', Integer, ForeignKey('rubrics.id')),
    Column('text', Text, nullable=False, index=True),
    Column('created_date', Date, nullable=False)
)

rubrics = Table(
    "rubrics",
    metadata,
    Column('id', Integer, primary_key=True),
    Column('rubric_one', String(50), nullable=False),
    Column('rubric_two', String(50), nullable=False),
    Column('rubric_three', String(50), nullable=False)
)