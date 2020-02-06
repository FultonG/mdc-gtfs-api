from flask import Flask
from controllers.routes import routes

# start flask instance
app = Flask(__name__)

# enable flask debug mode for stack tracing
app.config['DEBUG'] = True

# register the blueprints
app.register_blueprint(routes)

# default index route returns 200
@app.route('/')
@app.route('/index')
def index():
    # note: you can return dict, arrays, strings, and lots of other types
    # usually, returning a dict is best b/c it's interpreted as json data
    return {'OK': 200}

if __name__ == '__main__':
    # run flask app on host:port
    app.run(host='localhost', port=3000)
