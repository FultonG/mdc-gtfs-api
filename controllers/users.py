import bcrypt
import base64
from flask import Blueprint, request, make_response, jsonify
from bson import ObjectId
from cerberus import Validator
from .instances import mongo

# init blueprint
users = Blueprint('users', __name__)
col = mongo.db.users

# init pymongo client to users collection
def schema_validator(username, password=None, email=None, about_me=None):
    # registration
    if email is not None:
        schema = {'username':{'type':'string', 'minlength':6, 'maxlength': 100},
                'password':{'type':'string','minlength':8, 'maxlength': 100},
                'email': {'type': 'string', 'minlength':1}}
        input_info = {'username': username, 'password': password, 'email': email}
    # login
    elif password is not None and email is None:
        schema = {'username':{'type':'string', 'minlength':6, 'maxlength': 100},
                'password':{'type':'string','minlength':8, 'maxlength': 100}}
        input_info = {'username': username, 'password': password}
    # about me
    elif about_me is not None and username is not None:
        schema = {'username':{'type':'string', 'minlength':6, 'maxlength': 100},
                'about_me':{'type':'string','minlength':0, 'maxlength': 500}}
        input_info = {'username': username, 'about_me': password}
    # just username
    else:
        schema = {'username':{'type':'string', 'minlength':6, 'maxlength': 100}}
        input_info = {'username': username}


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
        data = request.get_json(force=True)
        username = data['user']
        password = data['pwd']
        errors = schema_validator(username, password)
        assert(len(errors) is 0)
    except Exception as e:
        print('exception:', e)
        return make_response({'Error': errors}, 400)
    # lookup user in db and compare hashes
    user = col.find_one({'username': username}, {'_id': 0, 'password': 1})
    # return 400 if user doesnt exist
    if (user is None):
        return make_response(jsonify({'Error': 'User not found'}), 404)
    # hash pwd and compare
    match = bcrypt.checkpw(password.encode('utf-8'), user['password'])
    if match:
        return make_response(jsonify({'success': True}),200)
    else:
        return make_response(jsonify({'success': False, 'error': 'Incorrect password'}),400)

@users.route('/update', methods=['PATCH'])
def update_info():
    try:
        data = request.form
        username = data['user']
        errors = schema_validator(username)
        assert(len(errors) is 0)
    except Exception as e:
        # no data passed
        print(e)
        return make_response(jsonify({'Error': 'errors'}), 400)
    # check if user exists first
    try:
        exists = (col.find_one({'username' : username}) is not None)
    except Exception as e:
        print(e)
        return make_response(jsonify({'Error': 'Internal server error, please try again in a few minutes'}), 500)
    if not exists:
        return make_response(jsonify({'Error': 'User does not exist'}), 400)

    # try to get image here if one was provided
    picture = 'file' in request.files
    text = data.get('aboutMe') is not None and len(data.get('aboutMe')) is not 0

    if picture:
        # upload picture to db under the user's document
        profile_pic = request.files['file']
        filename = profile_pic.filename
        extension = filename[-3:]
        if filename == '':
            return make_response(jsonify({'Error': 'Missing file'}), 400)
        # check for valid file types
        elif extension == 'jpg' or extension == 'png':
            # upload file to mongodb using gridfs
            mongo.save_file('profile.' + extension, profile_pic)
        else:
            return make_response(jsonify({'Error': 'Wrong file extension (only png and jpg allowed)'}), 400)
    if text:
        try:
            # modify the user's document and update it to the text
            about_me = data['aboutMe']
            user_doc = col.update({'username' : username}, {'$set': {'aboutMe': about_me, 'profilePicture': filename}})
        except Exception as e:
            print(e)
            return make_response(jsonify({'Error': 'Error updating user about me text'}), 500)
    # if nothing else, return 200
    return make_response(jsonify({'Success': True}), 200)

@users.route('/about', methods=['GET'])
def get_aboutme():
    # get passed in data
    try:
        data = request.form
        username = data['user']
        errors = schema_validator(username)
        assert(len(errors) is 0)
    except Exception as e:
        print(e)
        return make_response(jsonify({'Error': errors}), 400)
    # check if user exists
    try:
        exists = (col.find_one({'username' : username}) is not None)
    except Exception as e:
        print(e)
        return make_response(jsonify({'Error': 'Internal server error, please try again in a few minutes'}), 500)
    if not exists:
        return make_response(jsonify({'Error': 'User does not exist'}), 400)
    # get data and return it
    try:
        user_doc = col.find_one({'username': username}, {'_id': 0, 'aboutMe': 1, 'profilePicture': 1})
    except Exception as e:
        print(e)
        return make_response(jsonify({'Error': 'Internal server error, please try again in a few minutes'}), 500)
    # return the data
    extension = user_doc['profilePicture'][-3:]
    picture = mongo.send_file('profile.' + extension)
    picture.direct_passthrough = False
    encoded = str(base64.b64encode(picture.data))[2:-1]
    return make_response(jsonify({'aboutMe': user_doc['aboutMe'], 'profilePicture': encoded}), 200)

