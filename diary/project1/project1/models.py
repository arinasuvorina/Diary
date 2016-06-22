from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    ForeignKey,
    Date
    )
from sqlalchemy.orm import (
    relationship
)

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Integer)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(Text)
    password = Column(Text)
    usersId_Articles = relationship("Articles", backref="users")

class ArticlesTypes(Base):
    __tablename__ = 'articlesTypes'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    types = relationship("Articles", backref="articlesTypes")

class Articles(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    text = Column(Text)
    type_id = Column(Integer, ForeignKey('articlesTypes.id'))
    date = Column(Date)
    user_id = Column(Integer, ForeignKey('users.id'))

class CurrentDate(Base):
    __tablename__ = 'currentDate'
    id = Column(Integer, primary_key=True)
    date = Column(Date)

Index('my_index', MyModel.name, unique=True, mysql_length=255)
Index('login_index', User.login, unique=True, mysql_length=255)