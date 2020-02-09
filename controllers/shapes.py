from bson.json_util import dumps
from flask import Blueprint, make_response, request
from .instances import mongo

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
        shape_id = request.args.get('id')
    except:
        # return error message and 400 if it throws an exeption
        return make_response({'Error': 'Missing or invalid input'}, 400)
    # query the shapes collection and return whatever we find
    try:
        result = collection.find({'shape_id': shape_id}, {'_id': 0})
    except:
        # return none and 500 if any errors happen
        return make_response({}, 500)
    # return json results and send 200
    return make_response(dumps(result), 200)
