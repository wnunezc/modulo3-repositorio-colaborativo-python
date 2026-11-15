"""
Marcador de partidas ganadas y jugadas.
Responsable: Marta Lorenzo
"""


class Marcador:
    """Lleva la cuenta de partidas (variables acumulativas) y nada más (SRP)."""

    def __init__(self):
        self._jugadas = 0
        self._ganadas = 0

    def registrar(self, gano: bool) -> None:
        self._jugadas += 1
        if gano:
            self._ganadas += 1

    @property
    def jugadas(self) -> int:
        return self._jugadas

    @property
    def ganadas(self) -> int:
        return self._ganadas

    def resumen(self) -> str:
        return f"📊 Marcador: {self._ganadas} ganada(s) de {self._jugadas} partida(s)."
