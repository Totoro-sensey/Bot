from sqlalchemy.orm import sessionmaker

from data.config import ENGINE
from data.models import Base


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class DBEngine(metaclass=SingletonMeta):
    connection = None

    @classmethod
    def connect(cls):
        if cls.connection is None:
            cls.connection = sessionmaker(bind=ENGINE)()
            return cls.connection


class DBCommands:
    def __init__(self):
        self.pool = DBEngine.connect()

    async def create_tables(self):
        """
        Creating tables
        :return:
        """
        Base.metadata.create_all(ENGINE)
