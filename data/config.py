from environs import Env
from sqlalchemy import create_engine

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")

DB_ENGINE = env.str("DATABASE_ENGINE")
DB_USER = env.str("DATABASE_USER")
DB_PASSWORD = env.str("DATABASE_PASSWORD")
DB_HOST = env.str("DATABASE_HOST")
DB_NAME = env.str("DATABASE_NAME")

ENGINE = create_engine(
    "{0}://{1}:{2}@{3}/{4}".format(DB_ENGINE, DB_USER, DB_PASSWORD, DB_HOST, DB_NAME),
    pool_pre_ping=True,
)
