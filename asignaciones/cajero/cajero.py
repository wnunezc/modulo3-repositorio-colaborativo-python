"""
Orquesta las sesiones: varios usuarios pueden usar el cajero uno tras otro.
Responsable: Marta Lorenzo
"""
from typing import Optional

from consola import LectorDatos
from interfaces import IAutenticador, IEntradaSalida, IRepositorioUsuarios
from menu import MenuCajero
from modelos import Usuario


class Cajero:

    def __init__(self, io: IEntradaSalida, repositorio: IRepositorioUsuarios,
                 autenticador: IAutenticador, menu: MenuCajero, lector: LectorDatos):
        self._io = io
        self._repositorio = repositorio
        self._autenticador = autenticador
        self._menu = menu
        self._lector = lector

    def iniciar(self) -> None:
        self._io.mostrar("💰 Bienvenido a tu Cajero Automático")
        continuar = True
        while continuar:
            usuario = self._iniciar_sesion()
            if usuario is not None:
                self._menu.ejecutar(usuario)
            continuar = self._lector.pedir_si_no("\n¿Otro usuario desea usar el cajero? (s/n): ")
        self._io.mostrar("🏧 Cajero apagado. ¡Gracias!")

    def _iniciar_sesion(self) -> Optional[Usuario]:
        nombre = self._io.leer("\n👤 Usuario: ")
        usuario = self._repositorio.buscar(nombre)
        if usuario is None:
            self._io.mostrar("❌ Usuario no encontrado.")
            return None
        if self._autenticador.autenticar(usuario):
            return usuario
        return None
