from bson.json_util import dumps
from flask import Blueprint, make_response, request
from .instances import mongo

stoptimes = Blueprint('stoptimes', __name__)

# set the collection for the blueprint
collection = mongo.db.stoptimes

# find all stoptimes by tripID
@stoptimes.route('/stoptimes/find', methods=['GET'])
def find_stoptimes_by_id(tripID=None):
    # parse id param from call
    if tripID is None:
        try:
            trip_id = request.args.get('tripid')
        except:
            # return error message and 400 if it throws an exeption
            return make_response({'Error': 'Missing or invalid input'}, 400)
    else:
        trip_id = tripID
    # query the stoptimes collection and return whatever we find
    try:
        result = collection.find({'trip_id': trip_id},
                {'_id': 0, 'arrival_time': 1, 'departure_time': 1, 'stop_id': 1})
    except:
        # return none and 500 if any errors happen
        return make_response({}, 500)
    # return json results and send 200
    if tripID is None:
        return make_response(dumps(result), 200)
    else:
        return result
