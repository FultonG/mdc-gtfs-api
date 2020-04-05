from flask import Blueprint, request, make_response, jsonify
from bson import ObjectId
from cerberus import Validator
from .instances import mongo
import bcrypt

# init blueprint
users = Blueprint('users', __name__)
col = mongo.db.users

# init pymongo client to users collection
def schema_validator(username, password, email=None):
    if email is not None:
        schema = {'username':{'type':'string', 'minlength':6, 'maxlength': 100},
                'password':{'type':'string','minlength':8, 'maxlength': 100},
                'email': {'type': 'string', 'minlength':1}}
        input_info = {'username': username, 'password': password, 'email': email}
    else:
        schema = {'username':{'type':'string', 'minlength':6, 'maxlength': 100},
                'password':{'type':'string','minlength':8, 'maxlength': 100}}
        input_info = {'username': username, 'password': password}

    v = Validator(schema)
    v.validate(input_info)
    return v.errors

# method that creates a user with given params
def create_user(username, password, email):
    user = {'username': username,
            'password': bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()),
            'email': email,
            'aboutMe': '',
            'profilePicture': None}
    return user


@users.route('/register', methods=['POST'])
def register_user():
    # pre defined list for errors
    errors = []
    # parse args from request and verify that input is safe
    try:
        data = request.get_json(force=True)
        username = data['user']
        password = data['pwd']
        email = data['email']
        # validate against schema
        errors = schema_validator(username, password, email)
        assert(len(errors) is 0)
    except Exception as e:
        print('exception:', e)
        return make_response({'Error': errors}, 400)
    try:
        # check if user exists
        duplicate = (col.find_one({'username' : username}) is not None)
    except Exception as e:
        print(e)
        return make_response({'Error': 'Internal server error, please try again in a few minutes'}, 500)
    if duplicate:
        return make_response({'Error': 'User already exists'}, 406)
    else:
        # make user and insert to db
        user = create_user(username, password, email)
        col.insert_one(user)
        return make_response(jsonify({'success': True}), 200)


@users.route('/login', methods=['GET'])
def login_user():
    # parse args from request
    try:
        username = request.form.get('user', '')
        password = request.form.get('pwd', '')
        errors = schema_validator(username, password)
        assert(len(errors) is 0)
    except Exception as e:
        print('exception:', e)
        return make_response({'Error': errors}, 400)
    # lookup user in db and compare hashes
    user = col.find_one({'username': username}, {'_id': 0, 'password': 1})
    # return 400 if user doesnt exist
    if (user is None):
        return make_response(jsonify({'error': 'User not found'}), 404)
    # hash pwd and compare
    match = bcrypt.checkpw(password.encode('utf-8'), user['password'])
    if match:
        return make_response(jsonify({'success': True}),200)
    else:
        return make_response(jsonify({'success': False, 'error': 'Incorrect password'}),400)
