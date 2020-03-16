from bson.json_util import dumps
from flask import Blueprint, make_response, request
from .instances import mongo
import requests
import json
from cerberus import Validator
# create the blueprint (controller) for the routes
routes = Blueprint('routes', __name__)


def schema_validator(token=None, route=None):
    schema = {'token':{'type':'string', 'maxlength':36}, 'route':{'type':'string','maxlength':10}}
    v = Validator(schema)
    input_info = {}
    for info in [('token', token), ('route', route)]:
        info_key, info_value = info
        if info_value:
            input_info[info_key] = info_value
    return v.validate(input_info)


# create GET endpoint to return all routes
# note: instead of calling @app, we call the blueprint (@routes)
@routes.route('/routes/find/all', methods=['GET'])
def show_all_routes():
    try:
        # equivalent to db.routes.find({})
        token_id = request.args.get('token')
        assert(schema_validator(token_id))
    except Exception as e:
        print(e)
        # if there's an error, return a 500 and no data
        return make_response({}, 500)

    try:
        result = requests.get('https://rest.tsoapi.com/routes/getRouteFromToken?tkn={}&routeId=-1'.format(token_id), verify=False)
        result_json = result.json()
        data = json.loads(result_json)
        data_keys = ['routes', 'points', 'stops']
        for key in data_keys:
            if not data[key]:
                del data[key]
        if not data:
            data = None
    except:
        return make_response({}, 500)
    # if nothing goes wrong return all of the data and return a 200
    if data:
        return make_response(data, 200)
    else:
        return make_response('', 204)

@routes.route('/routes/find', methods=['GET'])
def find_route_by_id():
    # parse id param from call
    try:
        route_id = request.args.get('id')
        token_id = request.args.get('token')
        assert(schema_validator(token_id, route_id))
    except:
        # return error message and 400 if it throws an exeption
        return make_response({'Error': 'Missing or invalid input'}, 400)
    # query the routes collection and return whatever we find
    try:
        result = requests.get('https://rest.tsoapi.com/routes/getRouteFromToken?tkn={}&routeId={}'.format(token_id, route_id), verify=False)
        result_json = result.json()
        data = json.loads(result_json)
    except:
        # return none and 500 if any errors happen
        return make_response({}, 500)
    # return json results and send 200
    return make_response(data, 200)
