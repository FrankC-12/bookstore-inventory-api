from sqlalchemy.orm import Session
from models.book_model import BookModel
from schemas.book_schema import BookCreate, BookUpdate, Book
from fastapi import HTTPException, status
from typing import List, Optional
from config.database import get_db
import requests
from datetime import datetime
from services.exchange_services import convert_currency_service as convert_currency
from models.book_model import BookModel


def get_all_books(db: Session, skip: int = 1, limit: int = 100) -> List[Book]:
    """
    Retorno todos los libros en la base de datos con paginacion.
    """
    real_offset = (max(skip - 1, 0)) * limit
    books = db.query(BookModel).offset(real_offset).limit(limit).all()
    return books

def get_book_by_id(db: Session, book_id: int) -> Optional[Book]:
    """
    Retorna un libro por su ID.
    """
    book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book

def get_books_by_category(db: Session, category: str) -> List[Book]:
    """
    Retorna libros por categoria.
    """
    books = db.query(BookModel).filter(BookModel.category == category).all()
    if not books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No books found in this category")
    return books

def get_books_below_stock(db: Session, stock_quantity: int) -> List[Book]:
    """
    Retorna libros con stock por debajo de una cantidad especifica.
    """
    books = db.query(BookModel).filter(BookModel.stock_quantity < stock_quantity).all()
    if not books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No books found below this stock quantity")
    return books

def create_book(db: Session, book: BookCreate) -> Book:
    """
    Crea un nuevo libro en la base de datos.
    """
    db_book = BookModel(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def update_book(db: Session, book_id: int, book_update: BookUpdate) -> BookModel:
    db_book = get_book_by_id(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    # Solo actualiza los campos enviados
    for key, value in book_update.model_dump(exclude_unset=True).items():
        setattr(db_book, key, value)

    # Actualiza fecha de modificación automáticamente
    db_book.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(db_book)  # Trae todo tal cual está en la DB

    return db_book  # Devuelve el objeto completo, con cambios aplicados

def delete_book(db: Session, book_id: int) -> None:
    """
    Elimina un libro de la base de datos.
    """
    db_book = get_book_by_id(db, book_id)
    if not db_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    db.delete(db_book)
    db.commit()


def calculate_book_price(db: Session, book_id: int, to_currency: str = "EUR", margin_percentage: float = 40.0):
    """
    1. Toma el cost_usd del libro
    2. Obtiene tasa de cambio actual USD → moneda local usando API gratuita
    3. Aplica margen de ganancia del 40%
    4. Actualiza selling_price_local en la base de datos
    5. Retorna el cálculo detallado
    """
    # 1. Obtener el libro
    book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    # 2. Convertir costo del libro a la moneda local
    conversion = convert_currency(amount=book.cost_usd, from_currency="USD", to_currency=to_currency)

    # 3. Aplicar margen del 40% y redondear a 2 decimales
    cost_usd = round(book.cost_usd, 2)
    cost_local = round(conversion["converted_amount"], 2)
    exchange_rate = round(conversion["exchange_rate"], 2)
    selling_price = round(cost_local * (1 + margin_percentage / 100), 2)

    # 4. Actualizar el precio de venta en la base de datos
    book.selling_price_local = selling_price
    db.commit()
    db.refresh(book)

    # 5. Construir respuesta detallada
    result = {
        "id": book.id,
        "cost_usd": cost_usd,
        "exchange_rate": exchange_rate,
        "cost_local": cost_local,
        "margin_percentage": round(margin_percentage, 2),
        "selling_price": selling_price,
        "currency": to_currency,
        "calculation_timestamp": conversion["calculation_timestamp"]
    }

    return result




