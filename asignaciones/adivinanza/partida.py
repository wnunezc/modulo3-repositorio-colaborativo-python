"""
Reglas de una partida: número secreto, pistas y límite de intentos (Extensión 1).
Responsable: Walter Nuñez — PENDIENTE DE IMPLEMENTAR

Implementa IPartida (ver interfaces.py). Reglas:
  - Nada de print() ni input(): eso lo hace JuegoConsola (SRP).
  - Recibe el generador por el constructor (no uses random aquí): así en las
    pruebas se puede pasar un generador falso que siempre devuelva, por ejemplo, 7.
  - Un número fuera de rango lanza NumeroFueraDeRangoError y NO cuenta como intento.
  - Intentar después de terminar lanza PartidaTerminadaError.
"""
from excepciones import NumeroFueraDeRangoError, PartidaTerminadaError  # noqa: F401
from interfaces import IGeneradorNumeros, IPartida
from modelos import Nivel, ResultadoIntento  # noqa: F401


class Partida(IPartida):

    def __init__(self, nivel: Nivel, generador: IGeneradorNumeros, max_intentos: int):
        # TODO: guardar nivel y max_intentos, generar el secreto con
        #           generador.generar(nivel.minimo, nivel.maximo),
        #           e iniciar intentos_usados en 0 y gano en False.
        raise NotImplementedError("Pendiente de implementar")

    def intentar(self, numero: int) -> ResultadoIntento:
        # TODO:
        #   1. si terminada -> raise PartidaTerminadaError("La partida ya terminó.")
        #   2. si el nivel no contiene el número -> raise NumeroFueraDeRangoError(...)
        #   3. sumar 1 a intentos_usados
        #   4. devolver SECRETO_ES_MAYOR, SECRETO_ES_MENOR o CORRECTO (y marcar gano)
        raise NotImplementedError("Pendiente de implementar")

    @property
    def intentos_usados(self) -> int:
        raise NotImplementedError("Pendiente de implementar")

    @property
    def intentos_restantes(self) -> int:
        # TODO: max_intentos - intentos_usados
        raise NotImplementedError("Pendiente de implementar")

    @property
    def max_intentos(self) -> int:
        raise NotImplementedError("Pendiente de implementar")

    @property
    def gano(self) -> bool:
        raise NotImplementedError("Pendiente de implementar")

    @property
    def terminada(self) -> bool:
        # TODO: True si gano o si intentos_restantes == 0
        raise NotImplementedError("Pendiente de implementar")

    @property
    def secreto(self) -> int:
        raise NotImplementedError("Pendiente de implementar")
