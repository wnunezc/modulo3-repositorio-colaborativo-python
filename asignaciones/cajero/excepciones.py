"""
Errores del dominio del cajero.
Las operaciones LANZAN estas excepciones; el menú las ATRAPA y muestra el mensaje.
Así la lógica de negocio no imprime nada (SRP).
"""


class CajeroError(Exception):
    """Error base: el menú atrapa cualquier CajeroError en un solo lugar (DRY)."""


class MontoInvalidoError(CajeroError):
    """El monto es menor o igual a 0."""


class SaldoInsuficienteError(CajeroError):
    """Se intenta retirar más de lo que hay en el saldo."""
