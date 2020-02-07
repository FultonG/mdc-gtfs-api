# Flask API Structure

### Initial Setup
to install all of the dependencies run:

`pip3 install -r requirements.txt`

In general, make sure not to move any files around without making sure to refactor everything that depends on it; flask likes very specific file structure when using blueprints, so err on the side of caution.

### app.py
This is the main app that creates the flask instance and runs it.

As of flask 1.1, it's no longer advised to do `python3 app.py` to run the app, instead we do two steps:
1. Set the flask app variable with `FLASK_APP=app.py`
2. Run flask from the command line with `flask run`

To quit, order a keyboard interrupt (`ctrl + c`)

### Blueprints (Controllers)
In order to group similar functions and endpoints, we use [blueprints](https://flask.palletsprojects.com/en/1.1.x/blueprints/)

All blueprints go in the `controllers` folder and are registered in `app.py`.

For an example of a blueprint, look at `controllers/routes.py`.

### Blueprint Structure
Each blueprint should represent a item in the gtfs feed (e.g. shapes, routes, trips, etc.)

To make it easier to pull specific information out of these items, we're going to use dictionaries to make it easy and intuitive to get any specific values we need using key:value syntax. To see the shape of gtfs data items, use the swagger [documentation](https://mdc-gtfs.herokuapp.com/api-docs/#/)

## TODO:
- Write out schemas for the gtfs shapes
- Organize what the endpoints are going to be (in order to remain within the standard)
- Document endpoints using postman and add collaborators
