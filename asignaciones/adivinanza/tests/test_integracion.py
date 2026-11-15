import unittest

from aplicacion import AplicacionAdivina
from configuracion import MAX_INTENTOS, NIVELES
from consola import LectorDatos
from dificultad import SelectorDificultad
from juego_consola import JuegoConsola
from marcador import Marcador
from partida import Partida


class EntradaSalidaFalsa:
    def __init__(self, entradas):
        self.entradas = iter(entradas)
        self.mensajes = []

    def leer(self, mensaje):
        return next(self.entradas)

    def mostrar(self, mensaje):
        self.mensajes.append(mensaje)


class GeneradorFijo:
    def generar(self, minimo, maximo):
        return 7


class PruebasIntegracion(unittest.TestCase):
    def crear_aplicacion(self, entradas):
        io = EntradaSalidaFalsa(entradas)
        lector = LectorDatos(io)
        marcador = Marcador()
        juego = JuegoConsola(
            io, lector, lambda nivel: Partida(nivel, GeneradorFijo(), MAX_INTENTOS))
        aplicacion = AplicacionAdivina(
            io, lector, SelectorDificultad(io, lector, NIVELES), juego, marcador)
        return aplicacion, io, marcador

    def test_repeticion_victoria_derrota_y_marcador(self):
        aplicacion, io, marcador = self.crear_aplicacion(
            ["2", "7", "s", "1", "8", "8", "8", "8", "8", "n"])
        aplicacion.iniciar()
        self.assertEqual(marcador.jugadas, 2)
        self.assertEqual(marcador.ganadas, 1)
        self.assertTrue(any("¡Correcto!" in texto for texto in io.mensajes))
        self.assertTrue(any("Se acabaron los intentos" in texto
                            for texto in io.mensajes))

    def test_entradas_invalidas_se_repiten(self):
        aplicacion, io, marcador = self.crear_aplicacion(
            ["x", "0", "2", "21", "7", "n"])
        aplicacion.iniciar()
        self.assertEqual(marcador.jugadas, 1)
        self.assertEqual(marcador.ganadas, 1)
        self.assertTrue(any("entre 1 y 3" in texto for texto in io.mensajes))
        self.assertTrue(any("entre 1 y 20" in texto for texto in io.mensajes))


if __name__ == "__main__":
    unittest.main()
