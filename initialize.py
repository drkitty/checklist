#!/usr/bin/env python3

import oursql
from database import Base
from database.core import engine

from settings import python as settings


if __name__ == '__main__':
    conn = oursql.Connection(
        host=settings.database['host'],
        user=settings.database['user'],
        passwd=settings.database['passwd'],
    )
    cur = conn.cursor()

    try:
        cur.execute('DROP DATABASE {}'.format(settings.database['db']))
    except oursql.ProgrammingError as e:
        if e.errno != 1008:  # "Can't drop database {}; database doesn't exist"
            raise
    cur.execute(
        'CREATE DATABASE {} CHARACTER SET utf8mb4 COLLATE utf8mb4_bin'.format(
            settings.database['db']))

    Base.metadata.create_all(engine)
