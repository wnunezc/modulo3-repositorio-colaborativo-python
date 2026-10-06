"""Modulo para imprimir un cuento corto sobre trabajo en equipo."""

TITULO = "El equipo que aprendio Git"

PARRAFOS = [
    "Habia una vez un equipo que aprendio Git colaborando en Python.",
    "Al principio, cada integrante guardaba su codigo en una carpeta distinta "
    "y nadie sabia cual era la version correcta.",
    "Un dia, {protagonista} propuso crear un repositorio en GitHub. "
    "Cada companero trabajaria en su propia rama y enviaria un Pull Request.",
    "Las revisiones de codigo ayudaron a encontrar errores antes de que llegaran "
    "a la rama main, y todos aprendieron algo nuevo de los demas.",
    "Desde entonces, el equipo nunca volvio a perder una linea de codigo.",
]

MORALEJA = "Moraleja: trabajar en equipo, con orden y revisiones, mejora el resultado de todos."


def obtener_cuento(protagonista="Marta"):
    """Devuelve el cuento completo como texto, con el protagonista indicado."""
    lineas = [TITULO, "=" * len(TITULO), ""]
    for parrafo in PARRAFOS:
        lineas.append(parrafo.format(protagonista=protagonista))
        lineas.append("")
    lineas.append(MORALEJA)
    return "\n".join(lineas)


def imprimir_cuento(protagonista="Marta"):
    """Imprime el cuento en pantalla."""
    print(obtener_cuento(protagonista))
