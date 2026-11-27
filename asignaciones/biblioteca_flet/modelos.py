"""
modelos.py
Módulo de datos del Sistema de Control de Biblioteca.

Contiene las clases Libro y Cliente, y la clase Biblioteca, que gestiona en
memoria las listas de libros, clientes y las asociaciones de préstamo.
Los datos se conservan mientras la aplicación está abierta (sesión).

Este módulo no depende de Flet: toda la lógica y las validaciones viven aquí,
y la interfaz (main.py) solo se encarga de mostrar los datos y los mensajes.
"""

from dataclasses import dataclass
from datetime import datetime

DISPONIBLE = "Disponible"
PRESTADO = "Prestado"


class ErrorBiblioteca(Exception):
    """Error de validación que se muestra al usuario en la interfaz."""


@dataclass
class Libro:
    titulo: str
    autor: str
    isbn: str  # identificador único
    estado: str = DISPONIBLE

    @property
    def disponible(self) -> bool:
        return self.estado == DISPONIBLE


@dataclass
class Cliente:
    nombre: str
    apellido: str
    cedula: str  # identificador único

    @property
    def nombre_completo(self) -> str:
        return f"{self.nombre} {self.apellido}"


@dataclass
class Prestamo:
    """Asociación entre un libro y el cliente que lo tiene."""
    libro: Libro
    cliente: Cliente
    fecha: datetime


def _limpiar(texto) -> str:
    """Quita espacios al inicio y al final; convierte None en cadena vacía."""
    return (texto or "").strip()


class Biblioteca:
    """Gestiona libros, clientes y préstamos durante la sesión."""

    def __init__(self):
        self.libros: list[Libro] = []
        self.clientes: list[Cliente] = []
        self.prestamos: list[Prestamo] = []  # préstamos activos

    # ------------------------------------------------------------------
    # 1. Gestión de libros
    # ------------------------------------------------------------------
    def buscar_libro(self, isbn: str) -> Libro | None:
        isbn = _limpiar(isbn)
        return next((l for l in self.libros if l.isbn == isbn), None)

    def registrar_libro(self, titulo: str, autor: str, isbn: str) -> Libro:
        titulo, autor, isbn = _limpiar(titulo), _limpiar(autor), _limpiar(isbn)

        # ¿Todos los campos obligatorios tienen datos?
        faltantes = [nombre for nombre, valor in
                     (("Título", titulo), ("Autor", autor), ("ISBN", isbn)) if not valor]
        if faltantes:
            raise ErrorBiblioteca("Campos obligatorios faltantes: " + ", ".join(faltantes))

        # ¿El ISBN ya existe en la lista de libros?
        if self.buscar_libro(isbn):
            raise ErrorBiblioteca(f"El ISBN {isbn} ya está registrado.")

        # Crear libro con estado inicial «Disponible» y agregarlo a la lista
        libro = Libro(titulo=titulo, autor=autor, isbn=isbn)
        self.libros.append(libro)
        return libro

    def libros_disponibles(self) -> list[Libro]:
        return [l for l in self.libros if l.disponible]

    # ------------------------------------------------------------------
    # 2. Gestión de clientes
    # ------------------------------------------------------------------
    def buscar_cliente(self, cedula: str) -> Cliente | None:
        cedula = _limpiar(cedula)
        return next((c for c in self.clientes if c.cedula == cedula), None)

    def registrar_cliente(self, nombre: str, apellido: str, cedula: str) -> Cliente:
        nombre, apellido, cedula = _limpiar(nombre), _limpiar(apellido), _limpiar(cedula)

        faltantes = [n for n, v in
                     (("Nombre", nombre), ("Apellido", apellido), ("Cédula/ID", cedula)) if not v]
        if faltantes:
            raise ErrorBiblioteca("Campos obligatorios faltantes: " + ", ".join(faltantes))

        if self.buscar_cliente(cedula):
            raise ErrorBiblioteca(f"La Cédula/ID {cedula} ya está registrada.")

        cliente = Cliente(nombre=nombre, apellido=apellido, cedula=cedula)
        self.clientes.append(cliente)
        return cliente

    # ------------------------------------------------------------------
    # 3. Préstamo y devolución
    # ------------------------------------------------------------------
    def puede_prestar(self) -> bool:
        """¿Hay libros disponibles y clientes registrados?"""
        return bool(self.libros_disponibles()) and bool(self.clientes)

    def prestar(self, isbn: str | None, cedula: str | None) -> Prestamo:
        if not self.puede_prestar():
            raise ErrorBiblioteca(
                "Faltan libros disponibles o clientes registrados para realizar el préstamo.")

        # ¿Se seleccionaron libro y cliente?
        if not _limpiar(isbn) or not _limpiar(cedula):
            raise ErrorBiblioteca("Seleccione el libro y el cliente.")

        libro = self.buscar_libro(isbn)
        cliente = self.buscar_cliente(cedula)
        if libro is None:
            raise ErrorBiblioteca("El libro seleccionado no existe.")
        if cliente is None:
            raise ErrorBiblioteca("El cliente seleccionado no existe.")

        # Validación: solo se prestan libros «Disponible»
        if not libro.disponible:
            raise ErrorBiblioteca(f"El libro «{libro.titulo}» no está disponible.")

        # Asociar libro con cliente y cambiar estado a «Prestado»
        libro.estado = PRESTADO
        prestamo = Prestamo(libro=libro, cliente=cliente, fecha=datetime.now())
        self.prestamos.append(prestamo)
        return prestamo

    def prestamo_de(self, isbn: str) -> Prestamo | None:
        """Devuelve el préstamo activo de un libro (quién lo tiene)."""
        isbn = _limpiar(isbn)
        return next((p for p in self.prestamos if p.libro.isbn == isbn), None)

    def devolver(self, isbn: str) -> Libro:
        """Opcional avanzado: devolver un libro prestado."""
        prestamo = self.prestamo_de(isbn)
        if prestamo is None:
            raise ErrorBiblioteca("Ese libro no tiene un préstamo activo.")
        prestamo.libro.estado = DISPONIBLE
        self.prestamos.remove(prestamo)
        return prestamo.libro
