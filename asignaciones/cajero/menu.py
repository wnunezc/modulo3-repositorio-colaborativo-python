"""
Menú principal del cajero (while + if/elif/else).
Responsable: Marta Lorenzo
"""
from dataclasses import dataclass
from typing import Callable

from consola import LectorDatos
from excepciones import CajeroError
from historial import FormateadorHistorial, formatear_dinero
from interfaces import IEntradaSalida, IOperaciones
from modelos import Usuario


@dataclass(frozen=True)
class OpcionMenu:
    clave: str
    texto: str
    accion: Callable[[Usuario], None]


class MenuCajero:
    """Abierto/Cerrado (O de SOLID): para agregar una opción nueva solo se
    agrega un OpcionMenu en _crear_opciones(); el ciclo no se toca."""

    CLAVE_SALIR = "5"

    def __init__(self, io: IEntradaSalida, operaciones: IOperaciones,
                 lector: LectorDatos, formateador: FormateadorHistorial):
        self._io = io
        self._operaciones = operaciones
        self._lector = lector
        self._formateador = formateador
        self._opciones = {op.clave: op for op in self._crear_opciones()}

    def _crear_opciones(self) -> list[OpcionMenu]:
        return [
            OpcionMenu("1", "Consultar saldo", self._consultar),
            OpcionMenu("2", "Depositar dinero", self._depositar),
            OpcionMenu("3", "Retirar dinero", self._retirar),
            OpcionMenu("4", "Ver historial", self._ver_historial),
        ]

    # ---------- ciclo principal ----------
    def ejecutar(self, usuario: Usuario) -> None:
        opcion = ""
        while opcion != self.CLAVE_SALIR:
            self._mostrar_menu()
            opcion = self._io.leer("Selecciona una opción: ")

            if opcion == self.CLAVE_SALIR:
                self._io.mostrar(f"👋 Hasta luego, {usuario.nombre}.")
            elif opcion in self._opciones:
                self._ejecutar_accion(self._opciones[opcion], usuario)
            else:
                self._io.mostrar(f"❌ Opción no válida. Elige del 1 al {self.CLAVE_SALIR}.")

    def _mostrar_menu(self) -> None:
        self._io.mostrar("\n--- MENÚ ---")
        for op in self._opciones.values():
            self._io.mostrar(f"{op.clave}. {op.texto}")
        self._io.mostrar(f"{self.CLAVE_SALIR}. Salir")

    def _ejecutar_accion(self, opcion: OpcionMenu, usuario: Usuario) -> None:
        """Único lugar donde se manejan los errores de las operaciones (DRY)."""
        try:
            opcion.accion(usuario)
        except CajeroError as error:
            self._io.mostrar(f"❌ {error}")

    # ---------- acciones ----------
    def _consultar(self, usuario: Usuario) -> None:
        saldo = self._operaciones.consultar_saldo(usuario)
        self._io.mostrar(f"💵 Tu saldo actual es: {formatear_dinero(saldo)}")

    def _depositar(self, usuario: Usuario) -> None:
        monto = self._lector.pedir_monto("Monto a depositar: $")
        mov = self._operaciones.depositar(usuario, monto)
        self._io.mostrar(f"✅ Depositaste {formatear_dinero(mov.monto)}. "
                         f"Nuevo saldo: {formatear_dinero(mov.saldo_resultante)}")

    def _retirar(self, usuario: Usuario) -> None:
        monto = self._lector.pedir_monto("Monto a retirar: $")
        mov = self._operaciones.retirar(usuario, monto)
        self._io.mostrar(f"✅ Retiraste {formatear_dinero(mov.monto)}. "
                         f"Nuevo saldo: {formatear_dinero(mov.saldo_resultante)}")

    def _ver_historial(self, usuario: Usuario) -> None:
        for linea in self._formateador.formatear(usuario):
            self._io.mostrar(linea)
