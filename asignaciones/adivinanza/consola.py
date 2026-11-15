"""
Entrada/salida por consola y lectura validada de datos.
Responsable: Marta Lorenzo
"""
from typing import Callable, TypeVar

from interfaces import IEntradaSalida

T = TypeVar("T")


class Consola(IEntradaSalida):
    """Implementación real: el ÚNICO lugar con input() y print()."""

    def leer(self, mensaje: str) -> str:
        return input(mensaje).strip()

    def mostrar(self, mensaje: str) -> None:
        print(mensaje)


class LectorDatos:
    """Pide datos hasta que sean válidos.
    DRY: el ciclo 'repetir hasta que sea válido' está escrito una sola vez."""

    def __init__(self, io: IEntradaSalida):
        self._io = io

    def pedir_valido(self, mensaje: str, convertir: Callable[[str], T],
                     es_valido: Callable[[T], bool], error: str) -> T:
        while True:
            texto = self._io.leer(mensaje)
            try:
                valor = convertir(texto)
            except ValueError:
                self._io.mostrar(error)
                continue
            if es_valido(valor):
                return valor
            self._io.mostrar(error)

    def pedir_entero_en_rango(self, mensaje: str, minimo: int, maximo: int) -> int:
        return self.pedir_valido(mensaje, int, lambda n: minimo <= n <= maximo,
                                 f"Ingresa un número entero entre {minimo} y {maximo}.")

    def pedir_si_no(self, mensaje: str) -> bool:
        respuesta = self.pedir_valido(
            mensaje, lambda t: t.lower(),
            lambda r: r in ("s", "si", "sí", "n", "no"),
            "Responde 's' o 'n'.")
        return respuesta.startswith("s")
