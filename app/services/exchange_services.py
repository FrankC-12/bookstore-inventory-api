import requests
from fastapi import HTTPException
from datetime import datetime
from schemas.exchange_schema import ExchangeResponse

API_KEY = "66448d3913-e10c16681c-t3dc5s"  # Mejor usar .env en producción

def convert_currency_service(amount: float, from_currency: str, to_currency: str) -> ExchangeResponse:
    """
    Servicio que convierte un monto de una moneda a otra usando FastForex
    y devuelve un diccionario listo para la respuesta del endpoint.
    """
    url = f"https://api.fastforex.io/fetch-one?from={from_currency}&to={to_currency}&api_key={API_KEY}"

    try:
        response = requests.get(url)
        data = response.json()
    except Exception:
        raise HTTPException(status_code=500, detail="Error al conectar con FastForex")

    if response.status_code != 200 or "result" not in data or to_currency not in data["result"]:
        raise HTTPException(status_code=500, detail="Error al obtener tasa de conversión")

    exchange_rate = data["result"][to_currency]

    converted_amount = round(amount * exchange_rate, 2)

    return {
        "amount": amount,
        "from_currency": from_currency,
        "to_currency": to_currency,
        "exchange_rate": 0.90,
        "converted_amount": converted_amount,
        "calculation_timestamp": datetime.utcnow()
    }
