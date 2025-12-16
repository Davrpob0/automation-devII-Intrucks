# Escribe tu solución aquí
import re

def es_palindromo(texto: str) -> bool:
    """
    Retorna True si 'texto' es un palíndromo, ignorando:
    - espacios
    - signos de puntuación
    - mayúsculas/minúsculas

    Considera únicamente caracteres alfanuméricos (letras y números).
    """
    if texto is None:
        return False

    normalizado = re.sub(r"[^A-Za-z0-9]", "", texto).lower()
    return normalizado == normalizado[::-1]


if __name__ == "__main__":
    texto = input("Escribe el texto a evaluar: ").strip()

    if not texto:
        print("Entrada vacía. No hay nada para evaluar.")
    else:
        print(es_palindromo(texto))