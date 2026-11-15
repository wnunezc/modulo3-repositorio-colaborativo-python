"""
Generador del número secreto.
Responsable: Walter Nuñez
"""
import random

from interfaces import IGeneradorNumeros


class GeneradorAleatorio(IGeneradorNumeros):

    def generar(self, minimo: int, maximo: int) -> int:
        return random.randint(minimo, maximo)
