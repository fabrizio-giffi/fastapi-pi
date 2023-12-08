import json
from typing import List

import databases
import sqlalchemy
from fastapi import FastAPI
from pydantic import BaseModel

# SQLAlchemy specific code, as with any other app
DATABASE_URL = "sqlite:///./envs.db"
# DATABASE_URL = "postgresql://user:password@postgresserver/db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

envs = sqlalchemy.Table(
    "envs",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("repo", sqlalchemy.String),
    sqlalchemy.Column("variables", sqlalchemy.JSON),
)


engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)


class EnvWrite(BaseModel):
    repo: str
    variables: dict[str, str]


class Env(BaseModel):
    id: int
    repo: str
    variables: dict[str, str]


app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/envs/", response_model=List[Env])
async def read_notes():
    query = envs.select()
    return await database.fetch_all(query)


@app.post("/envs/", response_model=Env)
async def create_note(env: EnvWrite):
    query = envs.insert().values(repo=env.repo, variables=env.variables)
    last_record_id = await database.execute(query)
    return {**env.dict(), "id": last_record_id}
