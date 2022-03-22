#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# standard python imports
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from app.models.coin import CoinModel
from app.util.logz import create_logger
from binance.client import Client
import os
import numpy as np
class Coin(Resource):
    parser = reqparse.RequestParser()  # only allow quote changes, no name changes allowed
    parser.add_argument('quote', type=float, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('quote', type=int, required=True,
                        help='Must enter the store id')

    def __init__(self):
        self.logger = create_logger()

    def get(self, symbol):
        coin = CoinModel.find_by_name(symbol)
        self.logger.info(f'returning coin: {coin.json()}')
        if coin:
            return coin.json()
        return {'message': 'Coin not found'}, 404

    def post(self, symbol):
        self.logger.info(f'parsed args: {Coin.parser.parse_args()}')

        if CoinModel.find_by_name(symbol):
            return {'message': "An coin with name '{}' already exists.".format(
                symbol)}, 400
        data = Coin.parser.parse_args()
        coin = CoinModel(symbol, data['base'], data['quote'])

        try:
            coin.save_to_db()
        except:
            return {"message": "An error occurred inserting the coin."}, 500
        return coin.json(), 201

    def delete(self, symbol):

        coin = CoinModel.find_by_name(symbol)
        if coin:
            coin.delete_from_db()

            return {'message': 'coin has been deleted'}

    def put(self, symbol):
        data = Coin.parser.parse_args()
        coin = CoinModel.find_by_name(symbol)

        if coin is None:
            coin = CoinModel(symbol, data['quote'])
        else:
            coin.quote = data['quote']

        coin.save_to_db()

        return coin.json()


class CoinList(Resource):

    def get(self):
        client = Client("0Gq8w61pP0NM32dtZ8iOBqCwoQ0oUxP5irBh1ok8nXrScM2twvnvhaSXbLQxD3f4", "bWd3hUrQxQakHbvf8kab6ZSVf1Vu4uBkZo4YYE0trF3gLFMLIyFJcnreWKqxOuU8", tld='us')
        exchange_info = client.get_exchange_info()
        coin_list = list(np.array(exchange_info['symbols']))
        for coin in coin_list:
            coin_old = CoinModel.find_by_symbol(coin['symbol'])
            if coin_old is None:
                CoinModel(coin['symbol'], coin['baseAsset'], coin['quoteAsset']).save_to_db()
        return { 'coins': [coin.json() for coin in CoinModel.query.all()]}
