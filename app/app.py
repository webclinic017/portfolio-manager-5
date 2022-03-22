#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# standard python imports
from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_cors import CORS

from app.resources.coin import Coin, CoinList

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

postgresql = {'host': '0.0.0.0',
         'user': 'binanceuser',
         'passwd': 'gf8MREk!LdCL89qxxg3j8zKw',
         'db': 'binance_db'}

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://{}:{}@{}/{}".format(postgresql['user'], postgresql['passwd'], postgresql['host'], postgresql['db'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

@app.before_first_request
def create_tables():
    from app.db import db
    db.init_app(app)
    db.create_all()

@app.route('/')
def index():
    return render_template('./index.html')

api.add_resource(Coin, '/coin/<string:name>')
api.add_resource(CoinList, '/coins')

if __name__ == '__main__':
    app.run(debug=True)