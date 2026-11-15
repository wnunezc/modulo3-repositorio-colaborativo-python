"""Conversión exacta entre importes decimales y centavos enteros."""
import sys
from decimal import Decimal, InvalidOperation
from typing import Union

from excepciones import MontoInvalidoError


_LIMITE_DIGITOS = getattr(sys, "get_int_max_str_digits", lambda: 4300)() or 4300


def a_centavos(valor: Union[Decimal, int, float]) -> int:
    if isinstance(valor, bool) or not isinstance(valor, (Decimal, int, float)):
        raise MontoInvalidoError("El monto debe ser mayor que 0 y finito.")
    try:
        importe = Decimal(str(valor))
    except (InvalidOperation, ValueError) as error:
        raise MontoInvalidoError("El monto debe ser mayor que 0 y finito.") from error
    if not importe.is_finite():
        raise MontoInvalidoError("El monto debe ser mayor que 0 y finito.")

    signo, digitos, exponente = importe.as_tuple()
    texto = "".join(str(digito) for digito in digitos)
    escala = exponente + 2
    if escala < 0:
        sobrantes = -escala
        if any(digito != 0 for digito in digitos[-sobrantes:]):
            raise MontoInvalidoError("El monto debe tener como máximo dos decimales.")
        texto = texto[:-sobrantes] or "0"
    else:
        if len(texto) + escala > _LIMITE_DIGITOS:
            raise MontoInvalidoError("El monto excede el tamaño admitido.")
        texto += "0" * escala
    if len(texto) > _LIMITE_DIGITOS:
        raise MontoInvalidoError("El monto excede el tamaño admitido.")
    centavos = int(texto)
    return -centavos if signo else centavos


def desde_centavos(centavos: int) -> Decimal:
    try:
        texto = str(abs(centavos))
    except ValueError as error:
        raise MontoInvalidoError("El monto excede el tamaño admitido.") from error
    if len(texto) > _LIMITE_DIGITOS:
        raise MontoInvalidoError("El monto excede el tamaño admitido.")
    texto = texto.zfill(3)
    signo = "-" if centavos < 0 else ""
    return Decimal(f"{signo}{texto[:-2]}.{texto[-2:]}")
