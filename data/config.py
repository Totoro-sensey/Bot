from sqlalchemy import create_engine
from environs import Env

env = Env()
env.read_env()

# try:
#     STATUS = env.str("STATUS")
# except:
#     STATUS = "DEV"
#
# if STATUS == "DEV":
#     BOT_TOKEN = env.str("BOT_TOKEN")
#     ADMINS = env.list("ADMINS")
#
#     # Database
#     DB_NAME = env.str("DATABASE_NAME")
#     DB_HOST = env.str("DATABASE_HOST")
#     DB_PASSWORD = env.str("DATABASE_PASSWORD")
#     DB_USER = env.str("DATABASE_USER")
#     DB_ENGINE = env.str("DATABASE_ENGINE")
#
#     PAGE = env.int("PAGE")
#
# else:
BOT_TOKEN = "5825884474:AAFsL02YwTqIjYY1A7J_ixTew8rwD_0vEdw"
ADMINS = [1000356353]

# Database
DB_NAME = "testdeam"
DB_HOST = "localhost"
DB_PASSWORD = "1909"
DB_USER = "polina"
DB_ENGINE = "postgresql+psycopg2"

PAGE = 5

ENGINE = create_engine("{0}://{1}:{2}@{3}/{4}".format(DB_ENGINE, DB_USER,
                                                      DB_PASSWORD, DB_HOST, DB_NAME
                                                      ), pool_pre_ping=True
                       )