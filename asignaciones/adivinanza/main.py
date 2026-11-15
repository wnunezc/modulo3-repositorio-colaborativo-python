"""
Punto de entrada: crea los objetos y los conecta (inyección de dependencias).
Es el ÚNICO archivo que conoce las clases concretas.
"""
from aplicacion import AplicacionAdivina
from configuracion import MAX_INTENTOS, NIVELES
from consola import Consola, LectorDatos
from dificultad import SelectorDificultad
from generador import GeneradorAleatorio
from juego_consola import JuegoConsola
from marcador import Marcador
from modelos import Nivel
from partida import Partida


def crear_aplicacion() -> AplicacionAdivina:
    io = Consola()
    lector = LectorDatos(io)
    generador = GeneradorAleatorio()

    def crear_partida(nivel: Nivel) -> Partida:
        return Partida(nivel, generador, MAX_INTENTOS)

    return AplicacionAdivina(
        io=io,
        lector=lector,
        selector=SelectorDificultad(io, lector, NIVELES),
        juego=JuegoConsola(io, lector, crear_partida),
        marcador=Marcador(),
    )


if __name__ == "__main__":
    crear_aplicacion().iniciar()
