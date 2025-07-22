from models.book_model import BookModel
from resources import db
from sqlalchemy import select, asc

class BookService:
    def get_book_by_id(self, book_id: int):
        return BookModel.query.get(book_id)
    
    def get_all_books(self):
        query = select(BookModel).order_by(asc(BookModel.name))
        return db.session.scalars(query).all()
    
    def get_book_by_name(self, book_name: str):
        query = select(BookModel).where(BookModel.name == book_name)
        return db.session.scalar(query)

    def create_book(self, book_model: BookModel):
        exist_book = self.get_book_by_name(book_model.name)
        if exist_book:
            raise Exception(f'Book with name {book_model.name} already exists.')
        db.session.add(book_model)
        db.session.commit()
        return book_model
    
    def update_book(self, book_model: BookModel):
        exist_book = self.get_book_by_id(book_model.id)
        if not exist_book:
            raise  Exception(f'Book with name {book_model.id} does not exist.')
        if exist_book.name:
            exist_book.name = book_model.name
        if exist_book.author:
            exist_book.author = book_model.author
        if exist_book.publish_time:
            exist_book.publish_time = book_model.publish_time
        db.session.commit()
        return exist_book