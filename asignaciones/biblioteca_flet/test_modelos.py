"""
Pruebas unitarias de la lógica de la biblioteca (sin interfaz).
Ejecutar:  python -m unittest -v
"""

import unittest

from modelos import Biblioteca, ErrorBiblioteca, DISPONIBLE, PRESTADO


class PruebasBiblioteca(unittest.TestCase):
    def setUp(self):
        self.b = Biblioteca()

    # --- Libros ---
    def test_libro_nuevo_queda_disponible(self):
        libro = self.b.registrar_libro("Rayuela", "Julio Cortázar", "111")
        self.assertEqual(libro.estado, DISPONIBLE)
        self.assertEqual(len(self.b.libros), 1)

    def test_libro_con_campos_vacios_falla(self):
        with self.assertRaises(ErrorBiblioteca):
            self.b.registrar_libro("Rayuela", "  ", "111")

    def test_isbn_duplicado_falla(self):
        self.b.registrar_libro("Rayuela", "Julio Cortázar", "111")
        with self.assertRaises(ErrorBiblioteca):
            self.b.registrar_libro("Otro", "Otro autor", " 111 ")

    # --- Clientes ---
    def test_registrar_cliente(self):
        c = self.b.registrar_cliente("Ana", "Pérez", "8-123-456")
        self.assertEqual(c.nombre_completo, "Ana Pérez")

    def test_cedula_duplicada_falla(self):
        self.b.registrar_cliente("Ana", "Pérez", "8-123-456")
        with self.assertRaises(ErrorBiblioteca):
            self.b.registrar_cliente("Luis", "Gómez", "8-123-456")

    # --- Préstamos ---
    def _datos_base(self):
        self.b.registrar_libro("Rayuela", "Julio Cortázar", "111")
        self.b.registrar_cliente("Ana", "Pérez", "8-123-456")

    def test_prestamo_cambia_estado_y_asocia_cliente(self):
        self._datos_base()
        p = self.b.prestar("111", "8-123-456")
        self.assertEqual(p.libro.estado, PRESTADO)
        self.assertEqual(self.b.prestamo_de("111").cliente.cedula, "8-123-456")

    def test_no_se_presta_libro_prestado(self):
        self._datos_base()
        self.b.registrar_libro("Ficciones", "J. L. Borges", "222")
        self.b.prestar("111", "8-123-456")
        with self.assertRaises(ErrorBiblioteca):
            self.b.prestar("111", "8-123-456")

    def test_prestamo_sin_seleccion_falla(self):
        self._datos_base()
        with self.assertRaises(ErrorBiblioteca):
            self.b.prestar(None, "8-123-456")

    def test_prestamo_sin_clientes_falla(self):
        self.b.registrar_libro("Rayuela", "Julio Cortázar", "111")
        self.assertFalse(self.b.puede_prestar())
        with self.assertRaises(ErrorBiblioteca):
            self.b.prestar("111", "8-123-456")

    def test_devolucion_vuelve_a_disponible(self):
        self._datos_base()
        self.b.prestar("111", "8-123-456")
        libro = self.b.devolver("111")
        self.assertEqual(libro.estado, DISPONIBLE)
        self.assertEqual(self.b.prestamos, [])


if __name__ == "__main__":
    unittest.main()
