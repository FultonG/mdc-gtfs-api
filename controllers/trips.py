from bson.json_util import dumps
from flask import Blueprint, make_response, request
from .instances import mongo

# create the blueprint (controller) for the trips
trips = Blueprint('trips', __name__)

# set the collection for the blueprint
collection = mongo.db.trips

# create GET endpoint to return all trips
# note: instead of calling @app, we call the blueprint (@trips)
@trips.route('/trips/find/all', methods=['GET'])
def show_all_trips():
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
