from modulos.cuento import imprimir_cuento
from modulos.matematicas import calcular, listar_operaciones
from modulos.saludos import saludar


def main():
    saludar()
    print("Operaciones disponibles:", ", ".join(listar_operaciones()))
    print("Resultado de 1 + 1:", calcular("suma", 1, 1))
    print("Resultado de 5 - 2:", calcular("resta", 5, 2))
    print("Resultado de 3 * 4:", calcular("multiplicacion", 3, 4))
    print("Resultado de 10 / 2:", calcular("division", 10, 2))
    print("Resultado de 2 ** 3:", calcular("potencia", 2, 3))
    imprimir_cuento()


if __name__ == "__main__":
    main()
