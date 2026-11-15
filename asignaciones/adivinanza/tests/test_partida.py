import unittest
from unittest.mock import patch

from configuracion import MAX_INTENTOS, NIVELES
from excepciones import NumeroFueraDeRangoError, PartidaTerminadaError
from generador import GeneradorAleatorio
from modelos import ResultadoIntento
from partida import Partida


class GeneradorFijo:
    def __init__(self, secreto):
        self.secreto = secreto
        self.rango = None

    def generar(self, minimo, maximo):
        self.rango = (minimo, maximo)
        return self.secreto


class PruebasPartida(unittest.TestCase):
    def setUp(self):
        self.generador = GeneradorFijo(7)
        self.partida = Partida(NIVELES[1], self.generador, MAX_INTENTOS)

    def test_pistas_acierto_y_fin(self):
        self.assertEqual(self.generador.rango, (1, 20))
        self.assertEqual(self.partida.intentar(3), ResultadoIntento.SECRETO_ES_MAYOR)
        self.assertEqual(self.partida.intentar(9), ResultadoIntento.SECRETO_ES_MENOR)
        self.assertEqual(self.partida.intentar(7), ResultadoIntento.CORRECTO)
        self.assertTrue(self.partida.gano)
        self.assertTrue(self.partida.terminada)
        self.assertEqual(self.partida.intentos_usados, 3)
        self.assertEqual(self.partida.intentos_restantes, 2)
        with self.assertRaises(PartidaTerminadaError):
            self.partida.intentar(7)

    def test_cinco_fallos_terminan_la_partida(self):
        for numero in (1, 2, 3, 4, 5):
            self.partida.intentar(numero)
        self.assertFalse(self.partida.gano)
        self.assertTrue(self.partida.terminada)
        self.assertEqual(self.partida.intentos_usados, 5)
        self.assertEqual(self.partida.intentos_restantes, 0)
        self.assertEqual(self.partida.secreto, 7)
        with self.assertRaises(PartidaTerminadaError):
            self.partida.intentar(7)

    def test_fuera_de_rango_no_gasta_intento(self):
        for numero in (0, 21):
            with self.assertRaises(NumeroFueraDeRangoError):
                self.partida.intentar(numero)
        self.assertEqual(self.partida.intentos_usados, 0)
        self.assertFalse(self.partida.terminada)

    def test_generador_usa_limites_inclusivos_de_cada_nivel(self):
        for nivel in NIVELES:
            with self.subTest(nivel=nivel.nombre):
                with patch("generador.random.randint", return_value=nivel.maximo) as randint:
                    secreto = GeneradorAleatorio().generar(nivel.minimo, nivel.maximo)
                randint.assert_called_once_with(nivel.minimo, nivel.maximo)
                self.assertEqual(secreto, nivel.maximo)


if __name__ == "__main__":
    unittest.main()
