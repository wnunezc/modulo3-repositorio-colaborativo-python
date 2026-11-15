"""
Sistema de PIN con intentos limitados.
Responsable: Marta Lorenzo
"""
from interfaces import IAutenticador, IEntradaSalida
from modelos import Usuario


class AutenticadorPin(IAutenticador):

    def __init__(self, io: IEntradaSalida, max_intentos: int = 3):
        self._io = io
        self._max_intentos = max_intentos

    def autenticar(self, usuario: Usuario) -> bool:
        intentos = 0
        while intentos < self._max_intentos:
            pin = self._io.leer("🔒 Ingresa tu PIN: ")
            if usuario.pin_es_correcto(pin):
                self._io.mostrar(f"🔓 Acceso concedido. ¡Hola, {usuario.nombre}!")
                return True
            intentos += 1
            restantes = self._max_intentos - intentos
            if restantes > 0:
                self._io.mostrar(f"❌ PIN incorrecto. Te quedan {restantes} intento(s).")
        self._io.mostrar("⛔ Demasiados intentos fallidos. Acceso bloqueado.")
        return False
