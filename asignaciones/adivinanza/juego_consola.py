"""
Juega UNA partida en consola: pide números y muestra las pistas.
Responsable: Marta Lorenzo
"""
from typing import Callable

from consola import LectorDatos
from interfaces import IEntradaSalida, IPartida
from modelos import Nivel, ResultadoIntento


class JuegoConsola:
    """Conecta la partida (lógica de A) con la pantalla.
    Recibe una 'fábrica' de partidas para crear una nueva en cada juego
    sin conocer la clase concreta (Inversión de Dependencias)."""

    # Un mensaje por resultado: agregar un resultado nuevo = agregar una línea (O de SOLID)
    PISTAS = {
        ResultadoIntento.SECRETO_ES_MAYOR: "⬆️  El número secreto es MAYOR que {numero}.",
        ResultadoIntento.SECRETO_ES_MENOR: "⬇️  El número secreto es MENOR que {numero}.",
        ResultadoIntento.CORRECTO: "🎉 ¡Correcto! Era el {numero}.",
    }

    def __init__(self, io: IEntradaSalida, lector: LectorDatos,
                 crear_partida: Callable[[Nivel], IPartida]):
        self._io = io
        self._lector = lector
        self._crear_partida = crear_partida

    def jugar(self, nivel: Nivel) -> bool:
        """Juega una partida completa. Devuelve True si ganaron."""
        partida = self._crear_partida(nivel)
        self._io.mostrar(f"\nPensé un número entre {nivel.minimo} y {nivel.maximo}. "
                         f"Tienen {partida.max_intentos} intentos.")

        while not partida.terminada:
            self._io.mostrar(f"\nIntento {partida.intentos_usados + 1} de {partida.max_intentos}")
            numero = self._lector.pedir_entero_en_rango(
                f"Ingresa un número entre {nivel.minimo} y {nivel.maximo}: ",
                nivel.minimo, nivel.maximo)
            resultado = partida.intentar(numero)
            self._io.mostrar(self.PISTAS[resultado].format(numero=numero))

        self._mostrar_final(partida)
        return partida.gano

    def _mostrar_final(self, partida: IPartida) -> None:
        if partida.gano:
            self._io.mostrar(f"Lo adivinaron en {partida.intentos_usados} intento(s).")
        else:
            self._io.mostrar(f"\n💀 Se acabaron los intentos. El número era {partida.secreto}.")
