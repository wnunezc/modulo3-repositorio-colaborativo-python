import unittest
from decimal import Decimal

from autenticacion import AutenticadorPin
from cajero import Cajero
from consola import LectorDatos
from historial import FormateadorHistorial
from menu import MenuCajero
from operaciones import ServicioOperaciones
from repositorio import RepositorioUsuariosMemoria, usuarios_de_ejemplo


class EntradaSalidaFalsa:
    def __init__(self, entradas):
        self.entradas = iter(entradas)
        self.mensajes = []

    def leer(self, mensaje):
        return next(self.entradas)

    def mostrar(self, mensaje):
        self.mensajes.append(mensaje)


class PruebasIntegracion(unittest.TestCase):
    def crear_cajero(self, entradas):
        io = EntradaSalidaFalsa(entradas)
        lector = LectorDatos(io)
        repositorio = RepositorioUsuariosMemoria(usuarios_de_ejemplo())
        menu = MenuCajero(io, ServicioOperaciones(), lector, FormateadorHistorial())
        cajero = Cajero(io, repositorio, AutenticadorPin(io), menu, lector)
        return cajero, io, repositorio

    def test_menu_saldo_deposito_retiro_historial_y_salida(self):
        cajero, io, repositorio = self.crear_cajero(
            ["marta", "1234", "1", "2", "200", "3", "50", "4", "5", "n"])
        cajero.iniciar()
        usuario = repositorio.buscar("MARTA")
        self.assertEqual(usuario.saldo, 1150.0)
        self.assertEqual(len(usuario.movimientos), 2)
        self.assertTrue(any("$1,000.00" in texto for texto in io.mensajes))
        self.assertTrue(any("Total de movimientos: 2" in texto
                            for texto in io.mensajes))
        self.assertTrue(any("Cajero apagado" in texto for texto in io.mensajes))

    def test_tres_pines_incorrectos_y_cambio_de_usuario(self):
        cajero, io, repositorio = self.crear_cajero(
            ["marta", "0", "0", "0", "s", "ana", "0000", "2", "25", "5", "n"])
        cajero.iniciar()
        self.assertTrue(any("Demasiados intentos fallidos" in texto
                            for texto in io.mensajes))
        self.assertEqual(repositorio.buscar("marta").saldo, 1000.0)
        self.assertEqual(repositorio.buscar("ana").saldo, 2525.0)

    def test_entrada_invalida_no_registra_movimiento(self):
        cajero, io, repositorio = self.crear_cajero(
            ["marta", "1234", "2", "abc", "inf", "5", "n"])
        cajero.iniciar()
        usuario = repositorio.buscar("marta")
        self.assertEqual(usuario.saldo, 1000.0)
        self.assertEqual(usuario.movimientos, [])
        self.assertTrue(any("mayor que 0" in texto for texto in io.mensajes))
        self.assertTrue(any("finito" in texto for texto in io.mensajes))

    def test_centavos_por_consola_y_retiro_exacto(self):
        cajero, io, repositorio = self.crear_cajero(
            ["marta", "1234", "2", "0.10", "2", "0.20", "3", "0.30", "5", "n"])
        cajero.iniciar()
        usuario = repositorio.buscar("marta")
        self.assertEqual(usuario.saldo, Decimal("1000.00"))
        self.assertEqual(usuario.movimientos[-1].saldo_resultante, Decimal("1000.00"))
        self.assertTrue(any("Nuevo saldo: $1,000.00" in texto for texto in io.mensajes))


if __name__ == "__main__":
    unittest.main()
