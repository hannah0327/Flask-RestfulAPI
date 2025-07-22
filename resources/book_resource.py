from datetime import datetime
from flask import request, Response
from flask_restful import Resource
from flask_apispec import doc, MethodResource, use_kwargs
from flask_apispec import marshal_with
from models.book_model import BookModel
from resources import api, docs, app
from services.book_service import BookService
from common.constants import LOGIN_SECRET
import jwt
from common.api_tools import token_required
from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

# 定義Token的Schema，用於驗證JWT token
class TokenSchema(Schema):
    token = fields.Str(required=True, description="JWT token for authentication")

# 定義書籍的Schema，用於驗證和序列化書籍數據 (用於 POST/PUT 請求主體)
class BookRequestSchema(Schema):
    name = fields.Str(required=True, description="Name of the book")
    author = fields.Str(required=True, description="Author of the book")
    publish_time = fields.DateTime(required=True, description="Publish time of the book")

# 定義單本書籍響應的Schema (用於 GET 單本書籍或列表中的單個元素)
class BookModelSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = BookModel
        load_instance = True
        include_fk = True

# 定義多本書籍列表響應的Schema (用於 GET 所有書籍)
class BookListResponseSchema(Schema):
    books = fields.List(fields.Nested(BookModelSchema), description="List of books")


# 帶有id的書籍資源：用於獲取、修改書籍資訊
class BookResource(MethodResource, Resource):
    @doc(description='Get book information', tags=['Book Request'])
    @marshal_with(BookModelSchema, code=200)
    def get(self, book_id: int):
        book_model = BookService().get_book_by_id(book_id)
        if book_model:
            return book_model, 200
        else:
            return {'error': f'Book not found for id: {book_id}'}, 404
        
    @doc(description='Update book information', tags=['Book Request'])  
    @marshal_with(BookModelSchema, code=200) 
    @use_kwargs(BookRequestSchema, location="json") # 解析請求的json數據 
    @use_kwargs(TokenSchema, location="headers") # 從 headers 獲取 token 的 Schema
    @token_required()
    def put(self, book_id: int, **kwargs):
        try:
            name = kwargs.get('name', None)
            author = kwargs.get('author', None)
            publish_time = kwargs.get('publish_time', None)
            book_model = BookModel(id=book_id, name=name, author=author, publish_time=publish_time)
            book_model = BookService().update_book(book_model)
            return book_model, 200 # marshal_with 會自動序列化 BookModel 實例
        except Exception as error:
            return {'error': f'{error}'}, 400
            

# 不帶有id的書籍資源：用於獲取所有書籍或新增書籍            
class BookListResource(MethodResource, Resource):
    @doc(description='Get all books', tags=['Book Request'])
    @marshal_with(BookModelSchema(many=True), code=200)
    def get(self):
        book_list = BookService().get_all_books()
        return book_list, 200
    
    @token_required()
    @doc(description='Create a new book', tags=['Book Request'])
    @marshal_with(BookModelSchema, code=201) # 新增成功通常返回 201 Created
    @use_kwargs(BookRequestSchema, location="json")
    @use_kwargs(TokenSchema, location="headers")
    def post(self, **kwargs):
        try:
            name = kwargs.get('name', None)
            author = kwargs.get('author', None)
            publish_time = kwargs.get('publish_time')
            book_model = BookModel(name=name, author=author, publish_time=publish_time)
            BookService().create_book(book_model)
            return book_model, 201
        except Exception as error:
            return {'error': f'{error}'}, 400

api.add_resource(BookResource, '/books/<int:book_id>')
api.add_resource(BookListResource, '/books')

docs.register(BookResource)
docs.register(BookListResource)

@app.route('/swagger.yaml')
def generate_swagger_yaml():
    yaml_doc = docs.spec.to_yaml()
    return Response(yaml_doc, mimetype='text/yaml')