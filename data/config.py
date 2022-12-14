from pathlib import Path
from environs import Env
from sqlalchemy import create_engine

env = Env()
env.read_env()

BOT_TOKEN = "5523355053:AAHGX5SCIgEoXoqbSTsIg4En7WBtKSGnvLg" # env.str("BOT_TOKEN")
ADMINS = "1000356353" # env.list("ADMINS")

DB_ENGINE = "postgresql+psycopg2" # env.str("DATABASE_ENGINE")
DB_USER = "postgres" # env.str("DATABASE_USER")
DB_PASSWORD = "1909" # env.str("DATABASE_PASSWORD")
DB_HOST = "172.17.0.2:5432" # env.str("DATABASE_HOST")
DB_NAME = "new" # env.str("DATABASE_NAME")

ENGINE = create_engine(
    "{0}://{1}:{2}@{3}/{4}".format(DB_ENGINE, DB_USER, DB_PASSWORD, DB_HOST, DB_NAME),
    pool_pre_ping=True,
)
