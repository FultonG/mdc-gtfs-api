from flask import Flask
from controllers.routes import routes
from controllers.trips import trips
from controllers.stoptimes import stoptimes
from controllers.shapes import shapes
from controllers.instances import app, mongo

# register the blueprints
app.register_blueprint(routes)
app.register_blueprint(shapes)
app.register_blueprint(trips)
app.register_blueprint(stoptimes)

# default index route returns 200
@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    # note: you can return dict, arrays, strings, and lots of other types
    # usually, returning a dict is best b/c it's interpreted as json data
    return {'OK': 200}

if __name__ == '__main__':
    # run flask app on host:port
    app.run(host='localhost', port=3000)
