from modulos.cuento import imprimir_cuento
from modulos.matematicas import sumar
from modulos.saludos import saludar


def main():
    saludar()
    print("Resultado de 1 + 1:", sumar(1, 1))
    imprimir_cuento()


if __name__ == "__main__":
    main()
