# -*- encoding: utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base
from aiomysql.sa import create_engine

from sqlalchemy import Column, Integer, String, DateTime


class Db(object):
    Column = Column
    Integer = Integer
    String = String
    DateTime = DateTime

    def __init__(self):
        self.Model = declarative_base()
        self.engine = None

    async def init_engine(self, *args, **kwargs):
        self.engine = await create_engine(*args, **kwargs)


db = Db()
