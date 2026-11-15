"""
Operaciones bancarias y registro de movimientos.
Responsable: Walter Nuñez

Implementa IOperaciones (ver interfaces.py). Reglas:
  - No uses print() ni input(): eso lo hace el menú (SRP).
  - Si algo está mal, LANZA la excepción; el menú la atrapa y muestra el mensaje.
  - Cada depósito/retiro exitoso se agrega a usuario.movimientos y se devuelve.
  - Usa un método privado para validar el monto y otro para registrar el
    movimiento, así depositar() y retirar() no repiten código (DRY).
"""
import math

from excepciones import MontoInvalidoError, SaldoInsuficienteError
from interfaces import IOperaciones
from modelos import Movimiento, TipoMovimiento, Usuario


class ServicioOperaciones(IOperaciones):

    def consultar_saldo(self, usuario: Usuario) -> float:
        return usuario.saldo

    def depositar(self, usuario: Usuario, monto: float) -> Movimiento:
        self._validar_monto(monto)
        usuario.saldo += monto
        return self._registrar_movimiento(usuario, TipoMovimiento.DEPOSITO, monto)

    def retirar(self, usuario: Usuario, monto: float) -> Movimiento:
        self._validar_monto(monto)
        if monto > usuario.saldo:
            raise SaldoInsuficienteError(
                f"Saldo insuficiente. Tienes ${usuario.saldo:,.2f}.")
        usuario.saldo -= monto
        return self._registrar_movimiento(usuario, TipoMovimiento.RETIRO, monto)

    @staticmethod
    def _validar_monto(monto: float) -> None:
        if (isinstance(monto, bool) or not isinstance(monto, (int, float))
                or not math.isfinite(monto) or monto <= 0):
            raise MontoInvalidoError("El monto debe ser mayor que 0 y finito.")

    @staticmethod
    def _registrar_movimiento(usuario: Usuario, tipo: TipoMovimiento,
                              monto: float) -> Movimiento:
        movimiento = Movimiento(tipo, monto, usuario.saldo)
        usuario.movimientos.append(movimiento)
        return movimiento
