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
        result = self.__get_near_distance_or_time(args)
        return jsonify(result)

    # check parameters value
    def __abort_if_value_doesnt_exits(self, args):
        if args['latitude'] is None or args['longitude'] is None or \
                args['hour'] is None or args['min'] is None:
            abort(400)
        if not (args['hour'].isdigit() and args['min'].isdigit()):
            abort(400, message="hour or min isn't number")

    # calculate distance and return nearest distance or time between two
    # locations ,according to mode parameter (distance 0, time 1)
    def __get_near_distance_or_time(self, args):
        result = []
        range_distance = 1000
        time = 300
        if args['latitude'] is not ''and args['longitude'] is not '':
            total_min = int(args['hour'])*60+int(args['min'])
            now_location = (float(args['latitude']), float(args['longitude']))
            if total_min >= 1346:
                return result
            for data in truck_data:
                if data['stop_time'] in ['', '短暫停靠']:
                    continue
                data_min = int(data['stop_time'][0:2])*60+int(data['stop_time'][3:5])
                if total_min < data_min:
                    diff_time = data_min - total_min
                    if diff_time >= time:
                        continue
                    near_location = (float(data['latitude']), float(data['longitude']))
                    diff_distance = vincenty(now_location, near_location).meters
                    if diff_distance < range_distance:
                        data['distance'] = diff_distance
                        data['diff_time'] = diff_time
                        result.append(data)

        if args['mode'] is '0':
            result.sort(key=lambda x: (x['distance'], x['diff_time']))
        else:
            result.sort(key=lambda x: (x['diff_time'], x['distance']))

        return result[:5]
