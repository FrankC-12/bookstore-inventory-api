from sqlalchemy.orm import Session
from models.book_model import BookModel
from schemas.book_schema import BookCreate, BookUpdate, BookResponse
from fastapi import HTTPException, status
from typing import List, Optional
from config.database import get_db

def get_all_books(db: Session, skip: int = 0, limit: int = 100) -> List[BookResponse]:
    """
    Retorno todos los libros en la base de datos con paginacion.
    """
    books = db.query(BookModel).offset(skip).limit(limit).all()
    return books

def get_book_by_id(db: Session, book_id: int) -> Optional[BookResponse]:
    """
    Retorna un libro por su ID.
    """
    book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book

def get_books_by_category(db: Session, category: str) -> List[BookResponse]:
    """
    Retorna libros por categoria.
    """
    books = db.query(BookModel).filter(BookModel.category == category).all()
    if not books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No books found in this category")
    return books

def get_books_below_stock(db: Session, stock_quantity: int) -> List[BookResponse]:
    """
    Retorna libros con stock por debajo de una cantidad especifica.
    """
    books = db.query(BookModel).filter(BookModel.stock_quantity < stock_quantity).all()
    if not books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No books found below this stock quantity")
    return books

def create_book(db: Session, book: BookCreate) -> BookResponse:
    """
    Crea un nuevo libro en la base de datos.
    """
    db_book = BookModel(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def update_book(db: Session, book_id: int, book: BookUpdate) -> BookResponse:
    """
    Actualiza un libro existente en la base de datos.
    """
    db_book = get_book_by_id(db, book_id)
    if not db_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    for key, value in book.model_dump().items():
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int) -> None:
    """
    Elimina un libro de la base de datos.
    """
    db_book = get_book_by_id(db, book_id)
    if not db_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    db.delete(db_book)
    db.commit()

