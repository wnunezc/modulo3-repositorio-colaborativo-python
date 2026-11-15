"""
Entrada/salida por consola y lectura validada de datos.
Responsable: Marta Lorenzo
"""
from decimal import Decimal, InvalidOperation
from typing import Callable, TypeVar

from interfaces import IEntradaSalida

T = TypeVar("T")


class Consola(IEntradaSalida):
    """Implementación real: usa input() y print()."""

    def leer(self, mensaje: str) -> str:
        return input(mensaje).strip()

    def mostrar(self, mensaje: str) -> None:
        print(mensaje)


class LectorDatos:
    """Pide datos al usuario hasta que sean válidos.
    DRY: toda la lógica de 'repetir hasta que sea válido' vive en un solo método."""

    def __init__(self, io: IEntradaSalida):
        self._io = io

    def pedir_valido(self, mensaje: str, convertir: Callable[[str], T],
                     es_valido: Callable[[T], bool], error: str) -> T:
        while True:
            texto = self._io.leer(mensaje)
            try:
                valor = convertir(texto)
            except (ValueError, InvalidOperation):
                self._io.mostrar(f"❌ {error}")
                continue
            if es_valido(valor):
                return valor
            self._io.mostrar(f"❌ {error}")

    def pedir_monto(self, mensaje: str) -> Decimal:
        return self.pedir_valido(mensaje, Decimal,
                                 lambda m: not m.is_nan() and m > 0,
                                 "Ingresa un número mayor que 0.")

    def pedir_si_no(self, mensaje: str) -> bool:
        respuesta = self.pedir_valido(
            mensaje, lambda t: t.lower(),
            lambda r: r in ("s", "si", "sí", "n", "no"),
            "Responde 's' o 'n'.")
        return respuesta.startswith("s")
