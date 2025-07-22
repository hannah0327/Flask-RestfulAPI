from functools import wraps
from flask import request
import jwt
from common.constants import LOGIN_SECRET

def token_required():
    def check_token(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # 檢查JWT token是否存在
            jwt_token = request.headers.get('token', None)
            if not jwt_token:
                return {'error': 'User unauthorized'}, 401
            try:
                user_info = jwt.decode(jwt_token, LOGIN_SECRET, algorithms='HS256')
                if not user_info or not user_info.get('username', None):
                    return {'error': 'User unauthorized'}, 401
            except Exception as error:
                return {'error': 'User unauthorized'}, 401
            
            result = f(*args, **kwargs)
            return result  
        
        return wrapper
    
    return check_token