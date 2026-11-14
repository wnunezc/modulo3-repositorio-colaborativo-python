"""
Múltiples usuarios guardados en memoria.
Responsable: Marta Lorenzo
"""
from typing import Iterable, Optional

from interfaces import IRepositorioUsuarios
from modelos import Usuario


class RepositorioUsuariosMemoria(IRepositorioUsuarios):

    def __init__(self, usuarios: Iterable[Usuario]):
        # La clave es el nombre normalizado: "  MARTA " encuentra a "Marta"
        self._usuarios = {self._normalizar(u.nombre): u for u in usuarios}

    @staticmethod
    def _normalizar(nombre: str) -> str:
        return nombre.strip().lower()

    def buscar(self, nombre: str) -> Optional[Usuario]:
        return self._usuarios.get(self._normalizar(nombre))


def usuarios_de_ejemplo() -> list[Usuario]:
    return [
        Usuario("Marta", "1234", 1000.0),
        Usuario("Carlos", "5678", 500.0),
        Usuario("Ana", "0000", 2500.0),
    ]
