from bson.json_util import dumps
from flask import Blueprint, make_response, request
from .instances import mongo
from controllers.shapes import find_shape_by_id
from controllers.stoptimes import find_stoptimes_by_id
from controllers.trips import find_trips_by_id

getIDs = Blueprint('getIDs', __name__)

@getIDs.route('/getIDs', methods=['GET'])
def get_all_ids():
	#get the route id, which is needed for everything else
	try:
		route_id = request.args.get('id')
	except:
		# return error message and 400 if it throws an exeption
		return make_response({'Error': 'Missing or invalid input'}, 400)

	#once route_id is given run find_trips_by_id method to return route_id, shapes_id, and trip_id
	allTrips = find_trips_by_id(route_id)
	result = []
	#since tripsInfo is an array of every trip with that route_id iterate through it
	for i in allTrips:
		#every element in the tripInfo array is a dictionary so iterate through that as well
		#the ditionary should have trip_id, route_id, and shape_id
		trip = {}
		trip['route_id'] = i['route_id']
		trip['trip_id'] = i['trip_id']
		trip['shape_id'] = i['shape_id']
		trip['shape_info'] = []
		for j in find_shape_by_id(i['shape_id']):
			trip['shape_info'].append([j['loc'][1], j['loc'][0]])
		trip['timeInfo'] = find_stoptimes_by_id(i['trip_id'])
		result.append(trip)

	#dump everything out
	return make_response(dumps(result), 200)

