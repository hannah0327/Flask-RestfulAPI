from flask import request
from flask_restful import Resource
from flask_apispec import doc, MethodResource, use_kwargs
from services.user_service import UserService
from models.user_model import UserModel
from resources import api, docs
import jwt
from common.constants import LOGIN_SECRET
from flask_apispec import doc, MethodResource, use_kwargs
from flask_apispec import marshal_with
from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from datetime import datetime, timedelta, timezone

# 登入請求的 Schema
class LoginRequestSchema(Schema):
    username = fields.Str(required=True, description="User's username")
    password = fields.Str(required=True, description="User's password")

# 登入成功響應的 Schema
class LoginResponseSchema(Schema):
    id = fields.Int(dump_only=True, description="User ID") # dump_only=True 表示只用於輸出
    username = fields.Str(dump_only=True, description="User's username")
    token = fields.Str(dump_only=True, description="JWT authentication token")

# 定義用戶登錄資源
class LoginResource(MethodResource, Resource):
    @doc(description='User login to get JWT token', tags=['User Authentication'])
    @use_kwargs(LoginRequestSchema, location="json")
    @marshal_with(LoginResponseSchema, code=200)
    def post(self, **kwargs):
        try:
            # 從 kwargs 獲取由 @use_kwargs 解析的數據
            username = kwargs.get('username', None)
            password = kwargs.get('password', None)

            user_model = UserService().login(username, password)
            if user_model:
                payload = {
                    'id': user_model.id,
                    'username': user_model.username,
                    'exp': datetime.now(timezone.utc) + timedelta(hours=1) # Token 1 小時後過期
                }
                jwt_token = jwt.encode(payload, LOGIN_SECRET, algorithm='HS256')
                return {
                    'id': user_model.id,
                    'username': user_model.username,
                    'token': jwt_token
                }, 200
            else:
                return {'error': 'Invalid username or password'}, 401

        except Exception as error:
            return {'error': f'{error}'}, 400
        
api.add_resource(LoginResource, '/login')

docs.register(LoginResource)
       