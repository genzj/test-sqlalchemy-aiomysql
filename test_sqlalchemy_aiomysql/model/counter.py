# -*- encoding: utf-8 -*-
from datetime import datetime

from test_sqlalchemy_aiomysql.model.db import db


class Counter(db.Model):
    __tablename__ = 'counter'

    id = db.Column(db.Integer, primary_key=True)
    counter = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=False), default=datetime.utcnow)

