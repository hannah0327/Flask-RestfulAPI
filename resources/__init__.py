from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from apispec import APISpec
from flask_apispec import FlaskApiSpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_restful_swagger import swagger

app = Flask(__name__)
api = swagger.docs(Api(app), apiVersion='0.1')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:test@127.0.0.1/restful_db'
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Flask Restful API project',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'
})
db = SQLAlchemy(app)
docs = FlaskApiSpec(app)

from . import book_resource
from . import user_resource
