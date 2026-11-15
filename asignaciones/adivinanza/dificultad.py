"""
Selección del nivel de dificultad (Extensión 3).
Responsable: Marta Lorenzo
"""
from consola import LectorDatos
from interfaces import IEntradaSalida
from modelos import Nivel


class SelectorDificultad:
    """Solo muestra los niveles y devuelve el elegido (SRP).
    Abierto/Cerrado: para agregar un nivel se agrega en configuracion.py;
    esta clase no cambia."""

    def __init__(self, io: IEntradaSalida, lector: LectorDatos, niveles: list[Nivel]):
        self._io = io
        self._lector = lector
        self._niveles = niveles

    def elegir(self) -> Nivel:
        self._io.mostrar("\nElige la dificultad:")
        numero = 1
        for nivel in self._niveles:
            self._io.mostrar(f"  {numero}. {nivel}")
            numero += 1

        opcion = self._lector.pedir_entero_en_rango(
            f"Opción (1-{len(self._niveles)}): ", 1, len(self._niveles))
        nivel = self._niveles[opcion - 1]
        self._io.mostrar(f"Nivel {nivel.nombre} seleccionado.")
        return nivel
