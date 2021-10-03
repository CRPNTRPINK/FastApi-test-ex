import csv
import databases
from fastapi import FastAPI, status
from sql_database import posts, rubrics
from sqlalchemy import select, delete, insert
from datetime import datetime
from os import environ

POSTGRES_USER = environ.get("POSTGRES_USER", default="postgres")
POSTGRES_PASSWORD = environ.get("POSTGRES_PASSWORD", default="7645")
POSTGRES_SERVER = environ.get("POSTGRES_SERVER", default="localhost")
POSTGRES_DB = environ.get("POSTGRES_DB", default="posts")

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}"
database = databases.Database(DATABASE_URL)
app = FastAPI()


@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()


@app.get('/update')
async def write():
    await database.fetch_all(posts.delete())
    await database.fetch_all(rubrics.delete())
    with open('posts.csv', 'r', newline='') as f:
        csv_read = csv.reader(f, delimiter=',')
        next(csv_read)
        for i in csv_read:
            rubric = eval(i[2])
            rubric_query = insert(rubrics).values(rubric_one=rubric[0], rubric_two=rubric[1], rubric_three=rubric[2])
            rubric_fetch = await database.fetch_one(rubric_query)
            post_query = insert(posts).values(rubrics=rubric_fetch[0], text=i[0],
                                              created_date=datetime.strptime(i[1], '%Y-%m-%d %H:%M:%S'))
            await database.fetch_one(post_query)



@app.get('/text/{text}', status_code=status.HTTP_200_OK)
async def find_by_text(text):
    query = select(
        [posts.c.id, posts.c.rubrics, rubrics.c.rubric_one, rubrics.c.rubric_two, rubrics.c.rubric_three, posts.c.text,
         posts.c.created_date]).select_from(
        posts.join(rubrics)).where(posts.c.text.like('%' + text + '%')).limit(20)
    return await database.fetch_all(query)


@app.delete('/delete/{id}', status_code=status.HTTP_200_OK)
async def delete_by_id(id):
    await database.fetch_one(delete(posts).where(posts.c.id == int(id)))
    await database.fetch_one(delete(rubrics).where(rubrics.c.id == int(id)))
    return 'DELETED'
