"""Vistas de Flet y coordinación de las operaciones de biblioteca."""

from collections.abc import Callable, Sequence

import flet as ft

from modelos import Biblioteca, Cliente, ErrorBiblioteca, Libro

TINTA = "#27304B"
GRIS = "#677286"
BORDE = "#DBE1E8"
VERDE = "#1F6D60"


def panel(titulo: str, controles: list[ft.Control], columnas: int) -> ft.Container:
    return ft.Container(
        content=ft.Column(
            [ft.Text(titulo, size=20, weight=ft.FontWeight.W_600), *controles],
            spacing=18,
        ),
        bgcolor="#FFFFFF",
        border=ft.Border.all(1, BORDE),
        border_radius=12,
        padding=24,
        col={"xs": 12, "md": columnas},
    )


class VistaRegistro(ft.Column):
    """Formulario y listado compartidos por los registros de libros y clientes."""

    def __init__(
        self,
        titulo: str,
        etiquetas: Sequence[str],
        accion: Callable[..., object],
        ejecutar: Callable,
        mensaje_exito: str,
        texto_vacio: str,
    ):
        super().__init__(spacing=20)
        self.accion = accion
        self.ejecutar = ejecutar
        self.mensaje_exito = mensaje_exito
        self.texto_vacio = texto_vacio
        self.campos = [ft.TextField(label=etiqueta) for etiqueta in etiquetas]
        self.campos[-1].on_submit = self.registrar
        self.boton = ft.Button(
            content=f"Registrar {titulo.lower()}",
            icon=ft.Icons.ADD,
            on_click=self.registrar,
        )
        self.total = ft.Text(color=GRIS)
        self.lista = ft.Column(spacing=12)
        self.controls = [
            ft.ResponsiveRow(
                [
                    panel(f"Nuevo {titulo.lower()}", [
                        ft.Text("Todos los campos son obligatorios.", color=GRIS),
                        *self.campos,
                        self.boton,
                    ], 4),
                    panel("Inventario" if titulo == "Libro" else "Clientes registrados", [
                        self.total, self.lista,
                    ], 8),
                ],
                spacing=20,
                run_spacing=20,
                vertical_alignment=ft.CrossAxisAlignment.START,
            )
        ]

    def registrar(self, _evento):
        self.ejecutar(
            lambda: self.accion(*(campo.value for campo in self.campos)),
            self.limpiar,
            self.mensaje_exito,
        )

    def limpiar(self):
        for campo in self.campos:
            campo.value = ""

    def mostrar(self, filas: list[ft.Control]):
        self.total.value = f"Registros: {len(filas)}"
        self.lista.controls = filas or [ft.Text(self.texto_vacio, color=GRIS)]


class VistaPrestamos(ft.Column):
    """Selección de registros existentes y confirmación de un préstamo."""

    def __init__(self, biblioteca: Biblioteca, ejecutar: Callable, actualizar: Callable):
        super().__init__(spacing=20)
        self.biblioteca = biblioteca
        self.ejecutar = ejecutar
        self.actualizar = actualizar
        self.libro = ft.Dropdown(label="Libro disponible", on_select=self.seleccionar)
        self.cliente = ft.Dropdown(label="Cliente registrado", on_select=self.seleccionar)
        self.ayuda = ft.Text(color=GRIS)
        self.boton = ft.Button(
            content="Confirmar préstamo",
            icon=ft.Icons.BOOKMARK_ADD_OUTLINED,
            on_click=self.prestar,
            disabled=True,
        )
        self.lista = ft.Column(spacing=12)
        self.controls = [
            ft.ResponsiveRow(
                [
                    panel("Realizar préstamo", [
                        self.ayuda, self.libro, self.cliente, self.boton,
                    ], 5),
                    panel("Préstamos activos", [self.lista], 7),
                ],
                spacing=20,
                run_spacing=20,
                vertical_alignment=ft.CrossAxisAlignment.START,
            )
        ]

    def seleccionar(self, _evento):
        self.boton.disabled = not (self.libro.value and self.cliente.value)
        self.actualizar()

    def prestar(self, _evento):
        self.ejecutar(
            lambda: self.biblioteca.prestar(self.libro.value, self.cliente.value),
            self.limpiar,
            "Préstamo registrado. El libro ahora está Prestado.",
        )

    def limpiar(self):
        self.libro.value = None
        self.cliente.value = None

    def refrescar(self):
        disponibles = self.biblioteca.libros_disponibles()
        clientes = self.biblioteca.clientes
        self.libro.options = [
            ft.DropdownOption(key=libro.isbn, text=f"{libro.titulo} · ISBN {libro.isbn}")
            for libro in disponibles
        ]
        self.cliente.options = [
            ft.DropdownOption(key=cliente.cedula, text=f"{cliente.nombre_completo} · {cliente.cedula}")
            for cliente in clientes
        ]
        if self.libro.value not in {libro.isbn for libro in disponibles}:
            self.libro.value = None
        if self.cliente.value not in {cliente.cedula for cliente in clientes}:
            self.cliente.value = None
        self.libro.disabled = not disponibles
        self.cliente.disabled = not clientes
        self.boton.disabled = not (self.libro.value and self.cliente.value)
        if not disponibles and not clientes:
            self.ayuda.value = "Registra un libro y un cliente en sus secciones para comenzar."
        elif not disponibles:
            self.ayuda.value = "No hay libros disponibles para prestar."
        elif not clientes:
            self.ayuda.value = "Registra un cliente en la sección Clientes para realizar un préstamo."
        else:
            self.ayuda.value = "Selecciona un libro disponible y el cliente que lo recibirá."
        self.lista.controls = [
            ft.Container(
                ft.Column([
                    ft.Text(prestamo.libro.titulo, weight=ft.FontWeight.W_600),
                    ft.Text(f"ISBN: {prestamo.libro.isbn}", color=GRIS),
                    ft.Text(f"Cliente: {prestamo.cliente.nombre_completo}"),
                    ft.Text(f"Cédula/ID: {prestamo.cliente.cedula}", color=GRIS),
                ], spacing=4),
                padding=16,
                border=ft.Border.all(1, BORDE),
                border_radius=8,
            )
            for prestamo in self.biblioteca.prestamos
        ] or [ft.Text("Todavía no hay préstamos activos.", color=GRIS)]


class AplicacionBiblioteca:
    """Conecta las vistas a una única biblioteca durante la sesión de Flet."""

    def __init__(self, page: ft.Page, biblioteca: Biblioteca | None = None):
        self.page = page
        self.biblioteca = biblioteca if biblioteca is not None else Biblioteca()
        self.mensaje = ft.Text()
        self.aviso = ft.Container(self.mensaje, padding=14, border_radius=8, visible=False)
        self.libros = VistaRegistro(
            "Libro", ("Título", "Autor", "ISBN"),
            self.biblioteca.registrar_libro, self.ejecutar,
            "Libro registrado. Su estado inicial es Disponible.",
            "Todavía no hay libros. Registra el primero usando el formulario.",
        )
        self.clientes = VistaRegistro(
            "Cliente", ("Nombre", "Apellido", "Cédula/ID"),
            self.biblioteca.registrar_cliente, self.ejecutar,
            "Cliente registrado.",
            "Todavía no hay clientes. Registra el primero usando el formulario.",
        )
        self.prestamos = VistaPrestamos(self.biblioteca, self.ejecutar, page.update)
        self.vistas = {"Libros": self.libros, "Clientes": self.clientes, "Préstamos": self.prestamos}
        self.titulo = ft.Text("Libros", size=28, weight=ft.FontWeight.W_600, color=TINTA)
        self.contenido = ft.Container(content=self.libros)
        self.navegacion = [
            ft.OutlinedButton(content=nombre, on_click=self.navegar, data=nombre)
            for nombre in self.vistas
        ]
        self.salida = ft.TextButton(content="Salir", icon=ft.Icons.LOGOUT, on_click=self.salir)
        self.refrescar()
        self.marcar_seccion("Libros")
        page.add(ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.LOCAL_LIBRARY_OUTLINED, size=34, color=TINTA),
                ft.Text("Biblioteca", font_family="Georgia", size=36, color=TINTA),
            ]),
            ft.Text("Registro y circulación de libros", color=GRIS, size=16),
            ft.Row([*self.navegacion, self.salida], spacing=12, wrap=True),
            ft.Divider(color=BORDE),
            self.titulo,
            self.aviso,
            self.contenido,
            ft.Text("Estudiantes: Marta Lorenzo y Walter Nuñez", size=12, color=GRIS),
        ], spacing=18, scroll=ft.ScrollMode.AUTO, expand=True))

    def marcar_seccion(self, nombre: str):
        for boton in self.navegacion:
            boton.style = ft.ButtonStyle(
                bgcolor=TINTA if boton.data == nombre else "#FFFFFF",
                color="#FFFFFF" if boton.data == nombre else TINTA,
            )

    def navegar(self, evento):
        nombre = evento.control.data
        self.titulo.value = nombre
        self.contenido.content = self.vistas[nombre]
        self.aviso.visible = False
        self.marcar_seccion(nombre)
        self.refrescar()
        self.page.update()

    def ejecutar(self, accion: Callable, al_exito: Callable, mensaje: str):
        try:
            accion()
        except ErrorBiblioteca as error:
            self.mensaje.value = str(error)
            self.mensaje.color = "#8B2531"
            self.aviso.bgcolor = "#FCEBEC"
        else:
            al_exito()
            self.mensaje.value = mensaje
            self.mensaje.color = VERDE
            self.aviso.bgcolor = "#E7F3ED"
        self.refrescar()
        self.aviso.visible = True
        self.page.update()

    def refrescar(self):
        self.libros.mostrar([self.fila_libro(libro) for libro in self.biblioteca.libros])
        self.clientes.mostrar([self.fila_cliente(cliente) for cliente in self.biblioteca.clientes])
        self.prestamos.refrescar()

    def fila_libro(self, libro: Libro) -> ft.Control:
        prestamo = self.biblioteca.prestamo_de(libro.isbn)
        detalles = [
            ft.Text(libro.titulo, size=18, weight=ft.FontWeight.W_600),
            ft.Text(f"Autor: {libro.autor}", color=GRIS),
            ft.Text(f"ISBN: {libro.isbn}", color=GRIS),
        ]
        if prestamo:
            detalles.append(ft.Text(f"Cliente: {prestamo.cliente.nombre_completo}"))
        return ft.Container(
            ft.Row([
                ft.Column(detalles, spacing=4, expand=True),
                ft.Container(
                    ft.Text(libro.estado, color=VERDE if libro.disponible else "#8A5A18"),
                    bgcolor="#E7F3ED" if libro.disponible else "#FFF2D9",
                    border_radius=6,
                    padding=10,
                ),
            ], vertical_alignment=ft.CrossAxisAlignment.START),
            padding=16,
            border=ft.Border.all(1, BORDE),
            border_radius=8,
        )

    @staticmethod
    def fila_cliente(cliente: Cliente) -> ft.Control:
        return ft.Container(
            ft.Column([
                ft.Text(f"Nombre: {cliente.nombre}", size=18, weight=ft.FontWeight.W_600),
                ft.Text(f"Apellido: {cliente.apellido}"),
                ft.Text(f"Cédula/ID: {cliente.cedula}", color=GRIS),
            ], spacing=4),
            padding=16,
            border=ft.Border.all(1, BORDE),
            border_radius=8,
        )

    async def salir(self, _evento):
        await self.page.window.close()
