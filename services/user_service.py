from models.user_model import UserModel
from sqlalchemy import select
from resources import db

class UserService:
    def login(self, username: str, password: str):
        query = select(UserModel).where(UserModel.username == username)
        user_model = db.session.scalar(query)
        if user_model and user_model.password == password:
            return user_model
        else:
            return None