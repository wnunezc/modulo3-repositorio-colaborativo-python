"""
Errores del juego.
La lógica (Partida) LANZA estas excepciones; la consola nunca debería
provocarlas porque valida antes, pero quedan como protección.
"""


class JuegoError(Exception):
    """Error base del juego."""


class NumeroFueraDeRangoError(JuegoError):
    """El número intentado no está dentro del rango del nivel."""


class PartidaTerminadaError(JuegoError):
    """Se intentó jugar en una partida que ya terminó."""
