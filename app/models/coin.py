#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# standard python imports

from app.db import db

class CoinModel(db.Model):
    __tablename__ = 'coins'

    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10))
    base = db.Column(db.String(10))
    quote = db.Column(db.String(10))

    def __init__(self, symbol, base, quote):
        self.symbol = symbol
        self.base = base
        self.quote = quote

    def json(self):
        return {'symbol': self.symbol, 'base': self.base, 'quote': self.quote}

    @classmethod
    def find_by_symbol(cls, symbol):
        return cls.query.filter_by(symbol=symbol).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
