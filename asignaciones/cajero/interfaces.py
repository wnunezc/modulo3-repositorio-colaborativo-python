"""
Contratos (clases abstractas) del sistema.

Principio de Inversión de Dependencias (D de SOLID): las clases dependen de
estas abstracciones, no de implementaciones concretas. Por eso operaciones.py
puede implementar IOperaciones y encajar sin cambiar el resto del cajero,
y las pruebas pueden usar implementaciones falsas (fakes).
"""
from abc import ABC, abstractmethod
from typing import Optional

from modelos import Movimiento, Usuario


class IOperaciones(ABC):
    """Operaciones bancarias. Se implementa en operaciones.py."""

    @abstractmethod
    def consultar_saldo(self, usuario: Usuario) -> float:
        """Devuelve el saldo actual del usuario. No modifica nada."""

    @abstractmethod
    def depositar(self, usuario: Usuario, monto: float) -> Movimiento:
        """Suma el monto al saldo, registra el movimiento y lo devuelve.
        Lanza MontoInvalidoError si monto <= 0."""

    @abstractmethod
    def retirar(self, usuario: Usuario, monto: float) -> Movimiento:
        """Resta el monto del saldo, registra el movimiento y lo devuelve.
        Lanza MontoInvalidoError si monto <= 0.
        Lanza SaldoInsuficienteError si monto > saldo (y NO cambia nada)."""


class IRepositorioUsuarios(ABC):
    """Dónde se guardan los usuarios (hoy en memoria, mañana podría ser un archivo)."""

    @abstractmethod
    def buscar(self, nombre: str) -> Optional[Usuario]:
        """Devuelve el usuario o None si no existe."""


class IAutenticador(ABC):
    """Cómo se verifica la identidad (hoy PIN, mañana podría ser otra cosa)."""

    @abstractmethod
    def autenticar(self, usuario: Usuario) -> bool:
        """True si el usuario demostró ser quien dice ser."""


class IEntradaSalida(ABC):
    """Leer y mostrar texto. Permite probar sin teclado ni pantalla."""

    @abstractmethod
    def leer(self, mensaje: str) -> str:
        """Muestra el mensaje y devuelve lo que escribe el usuario."""

    @abstractmethod
    def mostrar(self, mensaje: str) -> None:
        """Muestra un mensaje."""
