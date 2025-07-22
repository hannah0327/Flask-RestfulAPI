from flask import request
from flask_restful import Resource
from services.user_service import UserService
from models.user_model import UserModel
from resources import api
import jwt
from common.constants import LOGIN_SECRET

# 定義用戶登錄資源
class LoginResource(Resource):
    def post(self):
        try:
            request_json = request.json
            if request_json:
                username = request_json.get('username', None)
                password = request_json.get('password', None)
                user_model = UserService().login(username, password)
                if user_model:
                    user_json = user_model.serialize()
                    jwt_token = jwt.encode(user_json, LOGIN_SECRET, algorithm='HS256')
                    user_json['token'] = jwt_token
                    return user_json
                else:
                    return {'error': 'Invalid username or password'}, 401
            else:
                return {'error': 'Please provide login info as a json'}, 400
        except Exception as error:
            return {'error': f'{error}'}, 400
        
api.add_resource(LoginResource, '/login')
       