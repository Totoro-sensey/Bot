from sqlalchemy import Column, Integer, String, BigInteger, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


# Таблицы для телеграм-бота
class User(Base):
    __tablename__ = "Users"

    id = Column("Id", BigInteger, primary_key=True)
    user_id = Column("UserId", BigInteger)
    user_name = Column("UserName", Text)
    user_fullname = Column("UserFullName", Text)

    role_id = Column("RolesId", BigInteger, ForeignKey("Roles.Id"),
                     nullable=True)

    Role = relationship("Role", overlaps="User")


# Таблица Ролей
class Role(Base):
    __tablename__ = "Roles"

    id = Column("Id", BigInteger, primary_key=True)
    name = Column("Name", Text, unique=True)

    User = relationship("User", overlaps="Role")


# Категории меню
class MenuCategories(Base):
    __tablename__ = "MenuCategories"

    id = Column("Id", BigInteger, primary_key=True)
    name = Column("Name", Text)
    text = Column("Text", Text, nullable=True)
    parent_id = Column("Parent_Id", BigInteger, nullable=True)
