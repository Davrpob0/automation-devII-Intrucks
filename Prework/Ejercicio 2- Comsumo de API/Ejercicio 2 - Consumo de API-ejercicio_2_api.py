# Escribe tu solución aquí
from __future__ import annotations

from typing import Any, Dict, List
import requests


USERS_URL = "https://jsonplaceholder.typicode.com/users"


def obtener_usuarios_limpios(url: str = USERS_URL, timeout_seg: int = 8) -> List[Dict[str, str]]:
    """
    Hace GET a la API de usuarios y devuelve una lista de dicts con:
    - name
    - email
    - city

    Maneja:
    - Timeout
    - Errores HTTP (4xx/5xx)
    - Errores de red
    - JSON inválido

    Lanza RuntimeError con un mensaje claro en caso de fallo.
    """
    try:
        resp = requests.get(url, timeout=timeout_seg)
        resp.raise_for_status() 

        data: Any = resp.json()
        if not isinstance(data, list):
            raise RuntimeError("Respuesta inesperada: se esperaba una lista de usuarios.")

        resultado: List[Dict[str, str]] = []
        for u in data:
            if not isinstance(u, dict):
                continue

            name = str(u.get("name", "")).strip()
            email = str(u.get("email", "")).strip()

            address = u.get("address") or {}
            city = ""
            if isinstance(address, dict):
                city = str(address.get("city", "")).strip()

            # Limpieza mínima: solo agregamos si hay valores razonables
            resultado.append(
                {
                    "name": name,
                    "email": email,
                    "city": city,
                }
            )

        return resultado

    except requests.exceptions.Timeout as e:
        raise RuntimeError(f"Timeout al consultar la API (>{timeout_seg}s).") from e
    except requests.exceptions.HTTPError as e:
        status = e.response.status_code if e.response is not None else "desconocido"
        raise RuntimeError(f"Error HTTP al consultar la API. Status: {status}.") from e
    except requests.exceptions.RequestException as e:
        # Cubre problemas de red/DNS/conexión, etc.
        raise RuntimeError(f"Error de red al consultar la API: {e}") from e
    except ValueError as e:
        # Error parseando JSON
        raise RuntimeError("La respuesta no es JSON válido.") from e


if __name__ == "__main__":
    try:
        # usuarios = obtener_usuarios_limpios(url="https://jsonplaceholder.typicode.com/usersxxxx")
        # usuarios = obtener_usuarios_limpios(timeout_seg=(2, 0.05))
        usuarios = obtener_usuarios_limpios()
        for u in usuarios:
            print(f"{u['name']} | {u['email']} | {u['city']}")
    except RuntimeError as err:
        print(f"Fallo: {err}")
