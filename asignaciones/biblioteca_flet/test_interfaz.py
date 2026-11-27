"""Integración de controles Flet reales con los modelos de biblioteca."""

import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock

import flet as ft

from interfaz import AplicacionBiblioteca
from modelos import Biblioteca, DISPONIBLE, PRESTADO


class PaginaPrueba:
    def __init__(self):
        self.controls = []
        self.actualizaciones = 0
        self.window = SimpleNamespace(close=AsyncMock())

    def add(self, *controles):
        self.controls.extend(controles)

    def update(self):
        self.actualizaciones += 1


def textos(control):
    resultado = [control.value] if isinstance(control, ft.Text) else []
    for hijo in getattr(control, "controls", []):
        resultado.extend(textos(hijo))
    contenido = getattr(control, "content", None)
    if isinstance(contenido, ft.Control):
        resultado.extend(textos(contenido))
    return resultado


class PruebasInterfaz(unittest.TestCase):
    def setUp(self):
        self.page = PaginaPrueba()
        self.app = AplicacionBiblioteca(self.page)

    def registrar(self, vista, valores):
        for campo, valor in zip(vista.campos, valores):
            campo.value = valor
        vista.boton.on_click(None)

    def navegar(self, nombre):
        boton = next(b for b in self.app.navegacion if b.data == nombre)
        boton.on_click(SimpleNamespace(control=boton))

    def datos_base(self):
        self.registrar(self.app.libros, ("Rayuela", "Julio Cortázar", "111"))
        self.registrar(self.app.clientes, ("Ana", "Pérez", "8-123-456"))

    def seleccionar_prestamo(self):
        vista = self.app.prestamos
        vista.libro.value = "111"
        vista.cliente.value = "8-123-456"
        vista.cliente.on_select(None)

    def test_inicio_vacio_muestra_listas_y_no_permite_prestar(self):
        self.assertIs(self.app.contenido.content, self.app.libros)
        self.assertIn("Todavía no hay libros. Registra el primero usando el formulario.", textos(self.app.libros))
        self.navegar("Clientes")
        self.assertIn("Todavía no hay clientes. Registra el primero usando el formulario.", textos(self.app.clientes))
        self.navegar("Préstamos")
        self.assertTrue(self.app.prestamos.boton.disabled)
        self.assertTrue(self.app.prestamos.libro.disabled)
        self.assertTrue(self.app.prestamos.cliente.disabled)

    def test_listas_iniciales_muestran_registros_sin_nuevas_altas(self):
        biblioteca = Biblioteca()
        biblioteca.registrar_libro("Rayuela", "Julio Cortázar", "111")
        biblioteca.registrar_cliente("Ana", "Pérez", "8-123-456")
        app = AplicacionBiblioteca(PaginaPrueba(), biblioteca)
        self.assertIn("Rayuela", textos(app.libros))
        self.assertIn("Nombre: Ana", textos(app.clientes))
        self.assertEqual(len(biblioteca.libros), 1)
        self.assertEqual(len(biblioteca.clientes), 1)

    def test_registro_actualiza_lista_selector_y_limpia_formulario(self):
        self.registrar(self.app.libros, (" Rayuela ", " Julio Cortázar ", " 111 "))
        self.assertEqual(self.app.biblioteca.libros[0].estado, DISPONIBLE)
        self.assertIn("Rayuela", textos(self.app.libros))
        self.assertIn("Autor: Julio Cortázar", textos(self.app.libros))
        self.assertIn(DISPONIBLE, textos(self.app.libros))
        self.assertEqual(self.app.prestamos.libro.options[0].key, "111")
        self.assertTrue(all(c.value == "" for c in self.app.libros.campos))
        self.assertTrue(self.app.aviso.visible)
        self.assertGreater(self.page.actualizaciones, 0)

    def test_campos_obligatorios_muestran_error_y_conservan_formulario(self):
        for vista in (self.app.libros, self.app.clientes):
            with self.subTest(vista=vista):
                self.registrar(vista, ("Ana", " ", "111"))
                self.assertIn("Campos obligatorios faltantes", self.app.mensaje.value)
                self.assertEqual(vista.campos[0].value, "Ana")
        self.assertEqual(self.app.biblioteca.libros, [])
        self.assertEqual(self.app.biblioteca.clientes, [])

    def test_duplicados_no_agregan_registros_y_muestran_error(self):
        self.datos_base()
        for vista, valores in (
            (self.app.libros, ("Otro libro", "Otro autor", " 111 ")),
            (self.app.clientes, ("Luis", "Gómez", " 8-123-456 ")),
        ):
            self.registrar(vista, valores)
            self.assertIn("ya está registrad", self.app.mensaje.value)
            self.assertEqual(vista.campos[0].value, valores[0])
        self.assertEqual(len(self.app.biblioteca.libros), 1)
        self.assertEqual(len(self.app.biblioteca.clientes), 1)

    def test_cliente_se_muestra_completo_y_actualiza_selector(self):
        self.registrar(self.app.clientes, ("Ana", "Pérez", "8-123-456"))
        contenido = textos(self.app.clientes)
        self.assertIn("Nombre: Ana", contenido)
        self.assertIn("Apellido: Pérez", contenido)
        self.assertIn("Cédula/ID: 8-123-456", contenido)
        self.assertEqual(self.app.prestamos.cliente.options[0].key, "8-123-456")

    def test_prestamo_actualiza_inventario_asociacion_y_disponibles(self):
        self.datos_base()
        self.navegar("Préstamos")
        self.seleccionar_prestamo()
        self.assertFalse(self.app.prestamos.boton.disabled)
        self.app.prestamos.boton.on_click(None)
        prestamo = self.app.biblioteca.prestamo_de("111")
        self.assertEqual(prestamo.cliente.cedula, "8-123-456")
        self.assertEqual(prestamo.libro.estado, PRESTADO)
        self.assertIn("Cliente: Ana Pérez", textos(self.app.prestamos))
        self.assertEqual(self.app.prestamos.libro.options, [])
        self.assertIsNone(self.app.prestamos.libro.value)
        self.assertIsNone(self.app.prestamos.cliente.value)
        self.assertTrue(self.app.prestamos.boton.disabled)
        self.navegar("Libros")
        self.assertIn(PRESTADO, textos(self.app.libros))
        self.assertIn("Cliente: Ana Pérez", textos(self.app.libros))

    def test_seleccion_incompleta_no_modifica_el_modelo(self):
        self.datos_base()
        self.app.prestamos.libro.value = "111"
        self.app.prestamos.libro.on_select(None)
        self.assertTrue(self.app.prestamos.boton.disabled)
        self.app.prestamos.prestar(None)
        self.assertIn("Seleccione el libro y el cliente", self.app.mensaje.value)
        self.assertEqual(self.app.biblioteca.prestamos, [])
        self.assertEqual(self.app.biblioteca.libros[0].estado, DISPONIBLE)

    def test_seleccion_obsoleta_no_permite_segundo_prestamo(self):
        self.datos_base()
        self.registrar(self.app.libros, ("Ficciones", "Borges", "222"))
        self.seleccionar_prestamo()
        self.app.biblioteca.prestar("111", "8-123-456")
        self.app.prestamos.prestar(None)
        self.assertIn("no está disponible", self.app.mensaje.value)
        self.assertEqual(len(self.app.biblioteca.prestamos), 1)
        self.assertIsNone(self.app.prestamos.libro.value)
        self.assertEqual([o.key for o in self.app.prestamos.libro.options], ["222"])

    def test_navegacion_conserva_datos_y_oculta_mensajes_anteriores(self):
        self.datos_base()
        self.assertTrue(self.app.aviso.visible)
        for nombre in ("Clientes", "Préstamos", "Libros"):
            self.navegar(nombre)
            self.assertIs(self.app.contenido.content, self.app.vistas[nombre])
            self.assertEqual(self.app.titulo.value, nombre)
            self.assertFalse(self.app.aviso.visible)
        self.assertEqual(len(self.app.biblioteca.libros), 1)

    def test_nueva_aplicacion_comienza_sin_datos_de_la_anterior(self):
        self.datos_base()
        otra = AplicacionBiblioteca(PaginaPrueba())
        self.assertEqual(otra.biblioteca.libros, [])
        self.assertEqual(otra.biblioteca.clientes, [])


class PruebasSalida(unittest.IsolatedAsyncioTestCase):
    async def test_boton_salir_solicita_cierre_de_ventana(self):
        page = PaginaPrueba()
        app = AplicacionBiblioteca(page)
        await app.salida.on_click(None)
        page.window.close.assert_awaited_once()


if __name__ == "__main__":
    unittest.main()
