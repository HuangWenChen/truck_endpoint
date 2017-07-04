# -*- coding: utf-8 -*-
from flask import Flask
from flask_restful import Api
import json

app = Flask(__name__)
api = Api(app)
truck_data = json.load(open('truck_api/data/truck.json', 'r+'))

from truck_api.district_search import district_search
from truck_api.near_search import near_search

api.add_resource(district_search, '/api/district/search')
api.add_resource(near_search, '/api/near/search')

app.config['JSON_AS_ASCII'] = False

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
