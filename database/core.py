import oursql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import settings.python as settings


def utf8mb4_connect(**kwargs):
    connection = oursql.Connection(
        host=settings.database['host'], user=settings.database['user'],
        db=settings.database['db'], passwd=settings.database['passwd'],
        **kwargs)
    cursor = connection.cursor()
    cursor.execute("SET NAMES 'utf8mb4' COLLATE 'utf8mb4_bin'")
    return connection


engine = create_engine(
    'mysql+oursql://', echo=settings.database['echo'], encoding='utf_8',
    creator=utf8mb4_connect)


Base = declarative_base()


Session = sessionmaker(bind=engine)


def transaction(func):
    def new_func(*args, **kwargs):
        s = Session()
        return func(s, *args, **kwargs)
    new_func.__name__ = func.__name__
    new_func.__module__ = func.__module__
    new_func.__doc__ = func.__doc__

    return new_func
