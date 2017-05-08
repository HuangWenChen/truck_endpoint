# -*- coding: utf-8 -*-
from flask import jsonify
from flask_restful import Resource, abort, reqparse
from . import truck_data


class district_search(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('district')
        self.parser.add_argument('stop_time')

    def post(self):
        args = self.parser.parse_args()
        self.__abort_if_value_doesnt_exist(args)
        result = self.__get_search_data(args)
        return jsonify(result)

    # get data from truck_data
    def __get_search_data(self, args):
        tmp = []
        if args['district'] is not '' and args['stop_time'] is not '':
            for search_data in truck_data:
                if args['district'] == search_data['district']:
                    if args['stop_time'][0:2] == search_data['stop_time'][0:2]:
                        tmp.append(search_data)
        return tmp

    # check parameters value
    def __abort_if_value_doesnt_exist(self, args):
        if args['district'] is None or args['stop_time'] is None:
            abort(400, message='Parameters Error')
