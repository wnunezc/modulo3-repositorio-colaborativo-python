"""
Ciclo general: elegir nivel, jugar, marcador y jugar otra vez (Extensión 2).
Responsable: Marta Lorenzo
"""
from consola import LectorDatos
from dificultad import SelectorDificultad
from interfaces import IEntradaSalida
from juego_consola import JuegoConsola
from marcador import Marcador


class AplicacionAdivina:

    def __init__(self, io: IEntradaSalida, lector: LectorDatos,
                 selector: SelectorDificultad, juego: JuegoConsola, marcador: Marcador):
        self._io = io
        self._lector = lector
        self._selector = selector
        self._juego = juego
        self._marcador = marcador

    def iniciar(self) -> None:
        self._io.mostrar("🎲 === ADIVINA EL NÚMERO ===")
        otra_vez = True
        while otra_vez:
            nivel = self._selector.elegir()
            gano = self._juego.jugar(nivel)
            self._marcador.registrar(gano)
            self._io.mostrar(self._marcador.resumen())
            otra_vez = self._lector.pedir_si_no("\n¿Quieren jugar otra vez? (s/n): ")
        self._io.mostrar("👋 ¡Gracias por jugar!")
