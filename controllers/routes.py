from flask import Blueprint

# create the blueprint (controller) for the routes
routes = Blueprint('routes', __name__)

# create GET endpoint to return all routes
# note: instead of calling @app, we call the blueprint (@routes)
@routes.route('/routes', methods=['GET'])
def show_all_routes():
    # return dummy data for now
    return {'routes': [], 'status': 200}
