from bson.json_util import dumps
from flask import Blueprint, make_response, request
from .instances import mongo
import requests
import json
import polyline

shapes = Blueprint('shapes', __name__)

# set db collection
collection = mongo.db.shapes

# endpoint to get all shapes
@shapes.route('/shapes/find/all', methods=['GET'])
def show_all_shapes():
    # this endpoint takes a pagination params so we parse them now
    # throw 400 if something goes wrong
    try:
        page = int(request.args.get('page'))
        results_per_page = int(request.args.get('resultsPerPage'))
    except Exception as e:
        print(e)
        return make_response({'Error': 'Missing or invalid input'}, 400)
    # if params are valid, try to fetch data
    try:
        result = collection.find({}, {'_id': 0}).limit(page * results_per_page)
    except:
        return make_response({}, 500)
    # if nothing goes wrong send back the resutls and a 200
    return make_response(dumps(result), 200)

@shapes.route('/shapes/find', methods=['GET'])
def find_shape_by_id():
    # parse id param from call
    try:
        route_id = request.args.get('id')
        token_id = request.args.get('token')
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
