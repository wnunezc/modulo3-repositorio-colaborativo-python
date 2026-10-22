"""Funciones sencillas para analizar texto."""


def contar_palabras(texto):
    """Cuenta las palabras separadas por espacios en blanco."""
    return len(texto.split())


def contar_vocales(texto):
    """Cuenta las vocales, incluidas las acentuadas, sin distinguir mayúsculas."""
    vocales = "aeiouáéíóúü"
    return sum(caracter in vocales for caracter in texto.lower())
