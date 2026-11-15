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
from decimal import Decimal

from dinero import a_centavos, desde_centavos
from excepciones import MontoInvalidoError, SaldoInsuficienteError
from interfaces import IOperaciones
from modelos import Movimiento, TipoMovimiento, Usuario


class ServicioOperaciones(IOperaciones):

    def consultar_saldo(self, usuario: Usuario) -> Decimal:
        return usuario.saldo

    def depositar(self, usuario: Usuario, monto: Decimal) -> Movimiento:
        centavos = self._validar_monto(monto)
        nuevo_saldo = desde_centavos(a_centavos(usuario.saldo) + centavos)
        usuario.saldo = nuevo_saldo
        return self._registrar_movimiento(
            usuario, TipoMovimiento.DEPOSITO, desde_centavos(centavos))

    def retirar(self, usuario: Usuario, monto: Decimal) -> Movimiento:
        centavos = self._validar_monto(monto)
        saldo_centavos = a_centavos(usuario.saldo)
        if centavos > saldo_centavos:
            raise SaldoInsuficienteError(
                f"Saldo insuficiente. Tienes ${usuario.saldo:,.2f}.")
        nuevo_saldo = desde_centavos(saldo_centavos - centavos)
        usuario.saldo = nuevo_saldo
        return self._registrar_movimiento(
            usuario, TipoMovimiento.RETIRO, desde_centavos(centavos))

    @staticmethod
    def _validar_monto(monto: Decimal) -> int:
        centavos = a_centavos(monto)
        if centavos <= 0:
            raise MontoInvalidoError("El monto debe ser mayor que 0 y finito.")
        return centavos

    @staticmethod
    def _registrar_movimiento(usuario: Usuario, tipo: TipoMovimiento,
                              monto: Decimal) -> Movimiento:
        movimiento = Movimiento(tipo, monto, usuario.saldo)
        usuario.movimientos.append(movimiento)
        return movimiento
