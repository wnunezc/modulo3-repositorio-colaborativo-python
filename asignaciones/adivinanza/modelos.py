"""
Modelos compartidos por todo el juego: el "idioma común" del proyecto.
"""
from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class Nivel:
    """Un nivel de dificultad con su rango (ambos extremos incluidos)."""
    nombre: str
    minimo: int
    maximo: int

    def contiene(self, numero: int) -> bool:
        return self.minimo <= numero <= self.maximo

    def __str__(self) -> str:
        return f"{self.nombre} ({self.minimo}-{self.maximo})"


class ResultadoIntento(Enum):
    """Lo que responde la partida después de cada intento."""
    SECRETO_ES_MAYOR = "mayor"
    SECRETO_ES_MENOR = "menor"
    CORRECTO = "correcto"
