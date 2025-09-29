from fastapi import FastAPI


app = FastAPI(
    title="Book Inventory API",
    description="API for managing a book inventory system.",
    version="1.0.0"
)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Book Inventory API!"}
