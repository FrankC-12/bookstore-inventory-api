# Bookstore Inventory API

API para la gestión de inventario de libros, construida con **FastAPI** y **SQLite**, dockerizada para facilitar su ejecución en cualquier entorno.

---

## Requisitos previos

Antes de ejecutar el proyecto, asegúrate de tener:

- **Python 3.12** (solo si deseas ejecutar sin Docker)
- **Docker** y **Docker Compose** (recomendado para desarrollo y producción)
- Navegador web o cliente HTTP (como **Postman** o **curl**) para probar los endpoints

---

## Instalación y ejecución

# Clono el repositorio

```bash
git clone https://github.com/tu-usuario/bookstore-inventory-api.git
cd bookstore-inventory-api

---

# Instalación y ejecución

- docker-compose up --build


# Acceder a la API
http://localhost:8000

# Si lo ejecutas sin docker
python -m venv env
source env/bin/activate  # Linux/macOS
env\Scripts\activate     # Windows

# Instalar las dependencias
pip install -r requirements.txt

#Ejecutar
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Ejemplo de endpoints
GET /books/

[
  {
    "id": 1,
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "isbn": "9780743273565",
    "cost_usd": 10.99,
    "selling_price_local": 15.99,
    "stock_quantity": 100,
    "category": "Fiction",
    "supplier_country": "USA",
    "created_at": "1925-04-10T00:00:00",
    "updated_at": "2024-01-01T12:00:00"
  }
]

#Crar un libro nuevo
POST /books/
Content-Type: application/json

{
  "title": "1984",
  "author": "George Orwell",
  "isbn": "9780451524935",
  "cost_usd": 12.5,
  "selling_price_local": 18.0,
  "stock_quantity": 50,
  "category": "Dystopian",
  "supplier_country": "UK"
}



