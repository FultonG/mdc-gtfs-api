from bson.json_util import dumps
from flask import Blueprint, make_response, request
from .instances import mongo

# create the blueprint (controller) for the routes
routes = Blueprint('routes', __name__)

# set the collection for the blueprint
collection = mongo.db.routes

# create GET endpoint to return all routes
# note: instead of calling @app, we call the blueprint (@routes)
@routes.route('/routes/find/all', methods=['GET'])
def show_all_routes():
    try:
        # equivalent to db.routes.find({})
        result = collection.find({}, {'_id':0})
    except Exception as e:
        print(e)
        # if there's an error, return a 500 and no data
        return make_response({}, 500)
    # if nothing goes wrong return all of the data and return a 200
    return make_response(dumps(result), 200)

@routes.route('/routes/find', methods=['GET'])
def find_route_by_id(routeID=None):
    # parse id param from call
    try:
        if routeID is None:
            route_id = request.args.get('id')
        else:
            route_id = routeID
    except:
        # return error message and 400 if it throws an exeption
        return make_response({'Error': 'Missing or invalid input'}, 400)
    # query the routes collection and return whatever we find
    try:
        if routeID is None:
            result = collection.find({'route_id': route_id},
                {'_id': 0, 'route_id': 1, 'route_short_name': 1, 'route_long_name': 1, 'route_color': 1})
        else:
            result = collection.find({'route_id': route_id}, {'_id':0, 'route_long_name':1, 'route_color':1})
    except:
        # return none and 500 if any errors happen
        return make_response({}, 500)
    # return json results and send 200
    if routeID is None: 
        return make_response(dumps(result), 200)
    else:
        return result
