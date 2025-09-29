from fastapi import APIRouter, Depends, status
from config.database import get_db
from models.book_model import BookModel
from schemas.book_schema import Book, BookCreate, BookUpdate, BookCalculatorPrice, BookCalculatePrice
from sqlalchemy.orm import Session
import services.book_services as book_services
from schemas.exchange_schema import ExchangeRequest, ExchangeResponse
from services.exchange_services import convert_currency_service

router = APIRouter(
    prefix="/books",
    tags=["Books"]
)


@router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo libro en la base de datos.
    """
    return book_services.create_book(db, book)

@router.get("/", response_model=list[Book])
def read_books(skip: int = 1, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retorna todos los libros en la base de datos con paginacion.
    """
    return book_services.get_all_books(db, skip=skip, limit=limit)

@router.get("/{book_id}", response_model=Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    """
    Retorna un libro por su ID.
    """
    return book_services.get_book_by_id(db, book_id)

@router.get("/category/{category}", response_model=list[Book])
def read_books_by_category(category: str, db: Session = Depends(get_db)):
    """
    Retorna libros por categoria.
    """
    return book_services.get_books_by_category(db, category)

@router.get("/stock/below/{stock_quantity}", response_model=list[Book])
def read_books_below_stock(stock_quantity: int, db: Session = Depends(get_db)):
    """
    Retorna libros con stock por debajo de una cantidad especifica.
    """
    return book_services.get_books_below_stock(db, stock_quantity)

@router.put("/{book_id}", response_model=Book)
def update_book_endpoint(book_id: int, book: BookUpdate, db: Session = Depends(get_db)):
    """
    Actualiza parcialmente un libro.
    Solo los campos enviados se modificarán.
    Los demás campos permanecen como están en la base de datos.
    """
    return book_services.update_book(db, book_id, book)

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """
    Elimina un libro de la base de datos.
    """
    book_services.delete_book(db, book_id)
    return None

@router.post("/healthcheck/api/exchange-rate", response_model=ExchangeResponse)
def healthcheck_exchange_rate(request: ExchangeRequest):
    """
    Endpoint que llama al servicio para convertir monedas usando FastForex.
    """
    result = convert_currency_service(
        amount=request.amount,
        from_currency=request.from_currency,
        to_currency=request.to_currency
    )
    return result


@router.post("/books/{book_id}/calculate-price", response_model=BookCalculatePrice)
def calculate_price(book_id: int, request: BookCalculatorPrice, db: Session = Depends(get_db)):
    """
    Endpoint para calcular el precio de un libro en otra moneda aplicando margen.
    """
    result = book_services.calculate_book_price(
        db=db,
        book_id=book_id,
        to_currency=request.to_currency  # por ejemplo "COP"
    )
    return result



