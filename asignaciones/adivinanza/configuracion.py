"""
Valores del juego en un solo lugar (DRY): si cambian las reglas,
solo se modifica este archivo.
"""
from modelos import Nivel

MAX_INTENTOS = 5

NIVELES = [
    Nivel("Fácil", 1, 10),
    Nivel("Medio", 1, 20),
    Nivel("Difícil", 1, 50),
]
