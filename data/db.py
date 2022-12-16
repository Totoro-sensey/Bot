from sqlalchemy.orm import sessionmaker
from data.models import Base, Role, User, MenuCategories
from data.config import ENGINE


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class DBManager(metaclass=SingletonMeta):
    connection = None

    @classmethod
    def connect(cls):
        if cls.connection is None:
            cls.connection = sessionmaker(bind=ENGINE)()
        return cls.connection


class DBCommands:
    def __init__(self):
        self.pool = DBManager.connect()

    @staticmethod
    def create_tables():
        Base.metadata.create_all(ENGINE)

    def get(self, model, **kwargs):
        instance = self.pool.query(model).filter_by(**kwargs).first()
        return instance or None

    def get_all(self, model, **kwargs):
        instance = self.pool.query(model).filter_by(**kwargs)
        return instance or None

    def create_role(self, name):
        """
        Создает новую роль в таблице Roles
        :param name: Наименование роли
        """
        role = Role(name=name)
        self.pool.add(role)
        self.pool.commit()

    def get_user(self, user_id: int):
        """
        Получение экземпляра пользователя из БД по его Ид
        :param : Идентификатор
        """
        return self.get(User, user_id=user_id)

    def create_user(self, user_id: int, fullname: str, username: str, role_id: int):
        """
        Создание нового пользователя в БД
        :return:
        """
        new_user = User(
            user_id=user_id,
            user_fullname=fullname,
            user_name=username,
            role_id=role_id,
        )
        self.pool.add(new_user)
        self.pool.commit()

    def create_category(self, name, text, parent_id):
        """
        Создание новой категории
        :return: None
        """
        category = MenuCategories(
            name=name,
            text=text,
            parent_id=parent_id
        )

        self.pool.add(category)
        self.pool.commit()

    def delete_category(self, category_id):
        """
        Создание новой категории
        :return: None
        """
        self.pool.query(MenuCategories).filter_by(id=category_id).delete()
        self.pool.commit()
