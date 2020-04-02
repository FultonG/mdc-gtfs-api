from flask import Flask
from flask_cors import CORS
from controllers.routes import routes
from controllers.users import users
from controllers.shapes import shapes
from controllers.instances import app, mongo
from controllers.stops import stops
from controllers.tokens import tokens
from controllers.train import trains
from controllers.stations import stations

# enable cors for the flask instance
CORS(app)

# register the blueprints
app.register_blueprint(routes)
app.register_blueprint(users)
app.register_blueprint(shapes)
app.register_blueprint(stops)
app.register_blueprint(tokens)
app.register_blueprint(trains)
app.register_blueprint(stations)

# default index route returns 200
@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    # note: you can return dict, arrays, strings, and lots of other types
    # usually, returning a dict is best b/c it's interpreted as json data
    return {'OK': 200}

if __name__ == '__main__':
    # run flask app on host:port
    app.run(host='localhost', port=8000)
