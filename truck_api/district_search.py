# -*- coding: utf-8 -*-
from flask import jsonify
from flask_restful import Resource, abort, reqparse
from . import truck_data


class district_search(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('district')
        self.parser.add_argument('stop_time')
        self.parser.add_argument('village')

    def post(self):
        args = self.parser.parse_args()
        self.__abort_if_value_doesnt_exist(args)
        result = self.__get_search_data(args)
        return jsonify(result)

    # get data from truck_data
    def __get_search_data(self, args):
        result = []
        if args['district'] is not '' and args['stop_time'] is not '' \
                and args['village'] is not '':
            for search_data in truck_data:
                if args['district'] == search_data['district'] \
                        and args['village'] == search_data['village']:
                    if args['stop_time'][0:2] == search_data['stop_time'][0:2]:
                        result.append(search_data)
        return result

    # check parameters value
    def __abort_if_value_doesnt_exist(self, args):
        if args['district'] is None or args['stop_time'] is None \
                or args['village'] is None:
            abort(400, message='Parameters Error')
