"""
Modelos de datos compartidos por todo el cajero.
Son el "idioma común" del proyecto: no tienen lógica de negocio.
"""
from dataclasses import dataclass, field
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
    pin: str = field(repr=False)          # repr=False: el PIN no sale al imprimir
    saldo: float = 0.0
    movimientos: list[Movimiento] = field(default_factory=list)

    def pin_es_correcto(self, pin: str) -> bool:
        return self.pin == pin
