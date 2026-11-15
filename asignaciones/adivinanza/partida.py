"""
Reglas de una partida: número secreto, pistas y límite de intentos (Extensión 1).
Responsable: Walter Nuñez

Implementa IPartida (ver interfaces.py). Reglas:
  - Nada de print() ni input(): eso lo hace JuegoConsola (SRP).
  - Recibe el generador por el constructor (no uses random aquí): así en las
    pruebas se puede pasar un generador falso que siempre devuelva, por ejemplo, 7.
  - Un número fuera de rango lanza NumeroFueraDeRangoError y NO cuenta como intento.
  - Intentar después de terminar lanza PartidaTerminadaError.
"""
from excepciones import NumeroFueraDeRangoError, PartidaTerminadaError
from interfaces import IGeneradorNumeros, IPartida
from modelos import Nivel, ResultadoIntento


class Partida(IPartida):

    def __init__(self, nivel: Nivel, generador: IGeneradorNumeros, max_intentos: int):
        self.__nivel = nivel
        self.__max_intentos = max_intentos
        self.__secreto = generador.generar(nivel.minimo, nivel.maximo)
        self.__intentos_usados = 0
        self.__gano = False

    def intentar(self, numero: int) -> ResultadoIntento:
        if self.terminada:
            raise PartidaTerminadaError("La partida ya terminó.")
        if not self.__nivel.contiene(numero):
            raise NumeroFueraDeRangoError(
                f"El número debe estar entre {self.__nivel.minimo} y {self.__nivel.maximo}.")

        self.__intentos_usados += 1
        if numero < self.__secreto:
            return ResultadoIntento.SECRETO_ES_MAYOR
        if numero > self.__secreto:
            return ResultadoIntento.SECRETO_ES_MENOR
        self.__gano = True
        return ResultadoIntento.CORRECTO

    @property
    def intentos_usados(self) -> int:
        return self.__intentos_usados

    @property
    def intentos_restantes(self) -> int:
        return self.__max_intentos - self.__intentos_usados

    @property
    def max_intentos(self) -> int:
        return self.__max_intentos

    @property
    def gano(self) -> bool:
        return self.__gano

    @property
    def terminada(self) -> bool:
        return self.__gano or self.intentos_restantes == 0

    @property
    def secreto(self) -> int:
        return self.__secreto
