from fastapi import FastAPI
from routes import book_routes
from config.database import engine, Base


app = FastAPI(
    title="Book Inventory API",
    description="API for managing a book inventory system.",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

app.include_router(book_routes.router)
