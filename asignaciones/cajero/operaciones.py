"""
Operaciones bancarias y registro de movimientos.
Responsable: Walter Nuñez — PENDIENTE DE IMPLEMENTAR

Implementa IOperaciones (ver interfaces.py). Reglas:
  - No uses print() ni input(): eso lo hace el menú (SRP).
  - Si algo está mal, LANZA la excepción; el menú la atrapa y muestra el mensaje.
  - Cada depósito/retiro exitoso se agrega a usuario.movimientos y se devuelve.
  - Usa un método privado para validar el monto y otro para registrar el
    movimiento, así depositar() y retirar() no repiten código (DRY).
"""
from excepciones import MontoInvalidoError, SaldoInsuficienteError  # noqa: F401
from interfaces import IOperaciones
from modelos import Movimiento, TipoMovimiento, Usuario  # noqa: F401


class ServicioOperaciones(IOperaciones):

    def consultar_saldo(self, usuario: Usuario) -> float:
        # TODO: devolver el saldo del usuario
        raise NotImplementedError("Pendiente de implementar")

    def depositar(self, usuario: Usuario, monto: float) -> Movimiento:
        # TODO:
        #   1. validar monto > 0, si no: raise MontoInvalidoError("El monto debe ser mayor que 0.")
        #   2. sumar al saldo
        #   3. crear Movimiento(TipoMovimiento.DEPOSITO, monto, usuario.saldo)
        #   4. agregarlo a usuario.movimientos y devolverlo
        raise NotImplementedError("Pendiente de implementar")

    def retirar(self, usuario: Usuario, monto: float) -> Movimiento:
        # TODO:
        #   1. validar monto > 0 (mismo método privado que depositar)
        #   2. si monto > saldo: raise SaldoInsuficienteError(f"Saldo insuficiente. Tienes ${...}")
        #      y NO modificar nada
        #   3. restar del saldo, crear Movimiento(TipoMovimiento.RETIRO, ...),
        #      agregarlo a usuario.movimientos y devolverlo
        raise NotImplementedError("Pendiente de implementar")
