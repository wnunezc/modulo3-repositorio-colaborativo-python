"""
Modelos de datos compartidos por todo el cajero.
Son el "idioma común" del proyecto: no tienen lógica de negocio.
"""
from dataclasses import InitVar, dataclass, field
from enum import Enum


class TipoMovimiento(Enum):
    DEPOSITO = "Depósito"
    RETIRO = "Retiro"


@dataclass(frozen=True)
class Movimiento:
    """Un depósito o retiro ya realizado. Es inmutable (frozen)."""
    tipo: TipoMovimiento
    monto: float
    saldo_resultante: float


@dataclass
class Usuario:
    """Un cliente del cajero con su saldo y su historial de movimientos."""
    nombre: str
    pin: InitVar[str]
    saldo: float = 0.0
    movimientos: list[Movimiento] = field(default_factory=list)

    def __post_init__(self, pin: str) -> None:
        self.__pin = pin

    def pin_es_correcto(self, pin: str) -> bool:
        return self.__pin == pin
