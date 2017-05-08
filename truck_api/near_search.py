# -*- coding: utf-8 -*-
from flask import jsonify
from flask_restful import Resource, abort, reqparse
from geopy.distance import vincenty
from . import truck_data


class near_search(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('latitude')
        self.parser.add_argument('longitude')
        self.parser.add_argument('hour')
        self.parser.add_argument('min')
        self.parser.add_argument('mode')

    def post(self):
        args = self.parser.parse_args()
        self.__abort_if_value_doesnt_exits(args)
        if args['mode'] is '0':
            result = self.__get_near_distance(args)
        elif args['mode'] is '1':
            result = self.__get_near_time(args)
        return jsonify(result)

    # check parameters value
    def __abort_if_value_doesnt_exits(self, args):
        if args['latitude'] is None or args['longitude'] is None or \
                args['hour'] is None or args['min'] is None:
            abort(404)
        if not (args['hour'].isdigit() and args['min'].isdigit()):
            abort(404, message="hour or min isn't number")

    # calculate distance and return nearest distance between two locations
    def __get_near_distance(self, args):
        tmp = []
        distance = 99999.0
        time = 99999
        if args['latitude'] is not ''and args['longitude'] is not '':
            total_min = int(args['hour'])*60+int(args['min'])
            now_location = (float(args['latitude']), float(args['longitude']))
            if total_min >= 1346:
                return tmp
            for data in truck_data:
                if data['stop_time'] in ['', '短暫停靠']:
                    continue
                tmp_min = int(data['stop_time'][0:2])*60+int(data['stop_time'][3:5])
                if total_min < tmp_min:
                    near_location = (float(data['latitude']), float(data['longitude']))
                    tmp_distance = vincenty(now_location, near_location).meters
                    if distance > tmp_distance:
                        tmp = []
                        distance = tmp_distance
                        time = tmp_min
                        tmp.append(data)
                    elif distance == tmp_distance and tmp_min < time:
                        tmp = []
                        time = tmp_min
                        tmp.append(data)
        return tmp

    # calculate distance and return nearest time between two locations
    def __get_near_time(self, args):
        tmp = []
        range_distance = 1000
        distance = 99999
        time = 99999
        if args['latitude'] is not ''and args['longitude'] is not '':
            total_min = int(args['hour'])*60+int(args['min'])
            now_location = (float(args['latitude']), float(args['longitude']))
            if total_min >= 1346:
                return tmp
            for data in truck_data:
                if data['stop_time'] in ['', '短暫停靠']:
                    continue
                tmp_min = int(data['stop_time'][0:2])*60+int(data['stop_time'][3:5])
                near_location = (float(data['latitude']), float(data['longitude']))
                tmp_distance = vincenty(now_location, near_location).meters
                if tmp_distance < range_distance and total_min < tmp_min:
                    diff_time = tmp_min - total_min
                    if diff_time < time:
                        tmp = []
                        distance = tmp_distance
                        time = diff_time
                        tmp.append(data)
                    elif diff_time == time and distance > tmp_distance:
                        tmp = []
                        distance = tmp_distance
                        tmp.append(data)
        return tmp
