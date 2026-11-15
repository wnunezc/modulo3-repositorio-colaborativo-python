"""
Punto de entrada: aquí se crean los objetos y se conectan entre sí
(inyección de dependencias). Es el ÚNICO archivo que conoce las clases concretas.
"""
from autenticacion import AutenticadorPin
from cajero import Cajero
from consola import Consola, LectorDatos
from historial import FormateadorHistorial
from menu import MenuCajero
from operaciones import ServicioOperaciones
from repositorio import RepositorioUsuariosMemoria, usuarios_de_ejemplo


def crear_cajero() -> Cajero:
    io = Consola()
    lector = LectorDatos(io)
    menu = MenuCajero(io, ServicioOperaciones(), lector, FormateadorHistorial())
    return Cajero(
        io=io,
        repositorio=RepositorioUsuariosMemoria(usuarios_de_ejemplo()),
        autenticador=AutenticadorPin(io),
        menu=menu,
        lector=lector,
    )


if __name__ == "__main__":
    crear_cajero().iniciar()
