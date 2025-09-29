# Etapa 1: construir la app
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --prefix=/install -r requirements.txt

# Copiar todo el contenido de app al WORKDIR
COPY ./app/. ./

# Etapa 2: imagen final ligera
FROM python:3.12-slim

WORKDIR /app

# Copiar dependencias desde builder
COPY --from=builder /install /usr/local
COPY --from=builder /app /app

EXPOSE 8000

# Comando por defecto para ejecutar la app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
