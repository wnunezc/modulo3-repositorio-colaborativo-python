import unittest

from excepciones import MontoInvalidoError, SaldoInsuficienteError
from modelos import TipoMovimiento, Usuario
from operaciones import ServicioOperaciones


class PruebasOperaciones(unittest.TestCase):
    def setUp(self):
        self.usuario = Usuario("Marta", "1234", 1000.0)
        self.servicio = ServicioOperaciones()

    def test_consulta_deposito_retiro_e_historial(self):
        self.assertEqual(self.servicio.consultar_saldo(self.usuario), 1000.0)
        deposito = self.servicio.depositar(self.usuario, 200.0)
        retiro = self.servicio.retirar(self.usuario, 100.0)
        self.assertEqual(self.usuario.saldo, 1100.0)
        self.assertEqual(deposito.tipo, TipoMovimiento.DEPOSITO)
        self.assertEqual(deposito.saldo_resultante, 1200.0)
        self.assertEqual(retiro.tipo, TipoMovimiento.RETIRO)
        self.assertEqual(retiro.saldo_resultante, 1100.0)
        self.assertEqual(self.usuario.movimientos, [deposito, retiro])

    def test_retiro_del_saldo_exacto_deja_cero(self):
        movimiento = self.servicio.retirar(self.usuario, 1000.0)
        self.assertEqual(self.usuario.saldo, 0.0)
        self.assertEqual(movimiento.saldo_resultante, 0.0)

    def test_saldo_insuficiente_no_cambia_estado(self):
        with self.assertRaises(SaldoInsuficienteError):
            self.servicio.retirar(self.usuario, 1000.01)
        self.assertEqual(self.usuario.saldo, 1000.0)
        self.assertEqual(self.usuario.movimientos, [])

    def test_montos_invalidos_no_cambian_estado(self):
        for monto in (0, -1, float("nan"), float("inf"), float("-inf"), True):
            for operacion in (self.servicio.depositar, self.servicio.retirar):
                with self.subTest(monto=monto, operacion=operacion.__name__):
                    with self.assertRaises(MontoInvalidoError):
                        operacion(self.usuario, monto)
        self.assertEqual(self.usuario.saldo, 1000.0)
        self.assertEqual(self.usuario.movimientos, [])

    def test_usuarios_conservan_saldos_e_historiales_independientes(self):
        otro = Usuario("Ana", "0000", 2500.0)
        self.servicio.depositar(self.usuario, 20.0)
        self.servicio.retirar(otro, 50.0)
        self.assertEqual(self.usuario.saldo, 1020.0)
        self.assertEqual(otro.saldo, 2450.0)
        self.assertEqual(len(self.usuario.movimientos), 1)
        self.assertEqual(len(otro.movimientos), 1)
        self.assertEqual(self.usuario.movimientos[0].tipo, TipoMovimiento.DEPOSITO)
        self.assertEqual(otro.movimientos[0].tipo, TipoMovimiento.RETIRO)

    def test_pin_se_comprueba_sin_exponerlo(self):
        self.assertTrue(self.usuario.pin_es_correcto("1234"))
        self.assertFalse(self.usuario.pin_es_correcto("0000"))
        self.assertFalse(hasattr(self.usuario, "pin"))
        self.assertNotIn("1234", repr(self.usuario))


if __name__ == "__main__":
    unittest.main()
