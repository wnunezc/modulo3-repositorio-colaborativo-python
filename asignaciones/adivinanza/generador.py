"""
Generador del número secreto.
Responsable: Walter Nuñez — PENDIENTE DE IMPLEMENTAR
"""
import random  # noqa: F401

from interfaces import IGeneradorNumeros


class GeneradorAleatorio(IGeneradorNumeros):

    def generar(self, minimo: int, maximo: int) -> int:
        # TODO: devolver un número aleatorio entre minimo y maximo (incluidos).
        #           Pista: random.randint
        raise NotImplementedError("Pendiente de implementar")
