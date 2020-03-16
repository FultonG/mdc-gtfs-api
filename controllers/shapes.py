from bson.json_util import dumps
from flask import Blueprint, make_response, request
from .instances import mongo
import requests
import json
import polyline
from cerberus import Validator

shapes = Blueprint('shapes', __name__)

def schema_validator(token, route):
    schema = {'token':{'type':'string', 'maxlength':36}, 'route':{'type':'string','maxlength':10}}
    v = Validator(schema)
    input_info = {'token':token, 'route':route}
    return v.validate(input_info)

@shapes.route('/shapes/find', methods=['GET'])
def find_shape_by_id():
    # parse id param from call
    try:
        route_id = request.args.get('id')
        token_id = request.args.get('token')
        assert(schema_validator(token_id, route_id))
    except:
        # return error message and 400 if it throws an exeption
        return make_response({'Error':'Missing or invalid input'}, 400)
    # call enpoint with token and route
    try:
        result = requests.get('https://rest.tsoapi.com/routes/getRouteFromToken?tkn={}&routeId={}'.format(token_id, route_id), verify=False)
        # turn result into json
        result_json = result.json()
        data = json.loads(result_json)
        # only usefull info in our result is the 'routes' key with value of [{}]
        route_data = data['routes'][0]
        # store the info we want to return in seperate variable
        data_info = {'Names':route_data['Name1'], 'RouteId':route_data['RouteId'], 'LineColor':route_data['LineColor'], 'RoutePath':polyline.decode(route_data['RoutePath'])}
    # raise error if exception
    except:
        return make_response({}, 500)
    # return data_info
    return make_response(dumps(data_info), 200)
