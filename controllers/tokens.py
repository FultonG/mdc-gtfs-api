from bson.json_util import dumps
from flask import Blueprint, make_response, request
from .instances import mongo
import requests
import json

tokens = Blueprint('tokens', __name__)

# endpoint to get all shapes
@tokens.route('/tokens', methods=['GET'])
def send_tokens():
    # parse id param from call
    tokens = ['C6B3CFCC-C1B2-47B4-9FD3-EEFB2A46E3C6', '582EB861-9C13-4C89-B491-15F0AFBF9F47', '825894C5-2B5F-402D-A055-88F2297AF99A', 'DB13899C-1B19-4577-9CA2-D4DDD773384D', '81E39EC9-D773-447E-BE29-D7F30AB177BC']
    return make_response(tokens, 200)

