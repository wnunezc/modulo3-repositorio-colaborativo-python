def sumar(numero_uno, numero_dos):
    return numero_uno + numero_dos


def restar(numero_uno, numero_dos):
    return numero_uno - numero_dos


def multiplicar(numero_uno, numero_dos):
    return numero_uno * numero_dos


def dividir(numero_uno, numero_dos):
    if numero_dos == 0:
        return "No se puede dividir entre cero"
    return numero_uno / numero_dos


def potencia(base, exponente):
    return base ** exponente


OPERACIONES = {
    "suma": sumar,
    "resta": restar,
    "multiplicacion": multiplicar,
    "division": dividir,
    "potencia": potencia,
}


def calcular(operacion, numero_uno, numero_dos):
    if operacion not in OPERACIONES:
        return "Operacion no valida"
    return OPERACIONES[operacion](numero_uno, numero_dos)


def listar_operaciones():
    return list(OPERACIONES.keys())
