"""
Contratos (clases abstractas) del sistema.

Inversión de Dependencias (D de SOLID): las clases dependen de estas
abstracciones, no de implementaciones concretas. Así partida.py y generador.py implementan
IPartida e IGeneradorNumeros y encajan sin cambiar el resto del juego,
y las pruebas pueden usar versiones falsas (fakes).
"""
from abc import ABC, abstractmethod

from modelos import ResultadoIntento


class IGeneradorNumeros(ABC):
    """Fuente del número secreto. Se implementa en generador.py."""

    @abstractmethod
    def generar(self, minimo: int, maximo: int) -> int:
        """Devuelve un entero entre minimo y maximo (ambos incluidos)."""


class IPartida(ABC):
    """Reglas de UNA partida. Se implementa en partida.py.
    No lee teclado ni imprime: solo lógica."""

    @abstractmethod
    def intentar(self, numero: int) -> ResultadoIntento:
        """Registra un intento y dice si el secreto es mayor, menor o si acertó.
        Lanza PartidaTerminadaError si la partida ya terminó.
        Lanza NumeroFueraDeRangoError si el número no está en el rango del nivel
        (en ese caso NO cuenta como intento)."""

    @property
    @abstractmethod
    def intentos_usados(self) -> int:
        """Cuántos intentos válidos se han hecho."""

    @property
    @abstractmethod
    def intentos_restantes(self) -> int:
        """Cuántos intentos quedan."""

    @property
    @abstractmethod
    def max_intentos(self) -> int:
        """Límite de intentos de la partida."""

    @property
    @abstractmethod
    def gano(self) -> bool:
        """True si ya se adivinó el número."""

    @property
    @abstractmethod
    def terminada(self) -> bool:
        """True si ganaron o si se acabaron los intentos."""

    @property
    @abstractmethod
    def secreto(self) -> int:
        """El número secreto (la consola solo lo muestra al terminar)."""


class IEntradaSalida(ABC):
    """Leer y mostrar texto. Permite probar sin teclado ni pantalla."""

    @abstractmethod
    def leer(self, mensaje: str) -> str:
        """Muestra el mensaje y devuelve lo que escribe el usuario."""

    @abstractmethod
    def mostrar(self, mensaje: str) -> None:
        """Muestra un mensaje."""
