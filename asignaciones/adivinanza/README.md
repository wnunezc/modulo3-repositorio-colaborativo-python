# 🎲 Adivina el número (POO, DRY y SOLID)

El programa genera un número secreto y los jugadores intentan adivinarlo con pistas de "mayor" o "menor".

- **Extensión 1:** máximo 5 intentos antes de perder.
- **Extensión 2:** al final pregunta si quieren jugar otra vez (con marcador).
- **Extensión 3:** niveles Fácil (1–10), Medio (1–20) y Difícil (1–50).

## Cómo ejecutar
Desde la raíz del repositorio:
```bash
python3 asignaciones/adivinanza/main.py
```

El juego valida las entradas, muestra pistas después de cada intento y termina
al acertar o agotar cinco intentos. Al finalizar permite jugar otra vez y
actualiza el marcador.

## Pruebas
Desde `asignaciones/adivinanza/`:
```bash
python -m unittest discover -s tests -v
```

## Reparto
| Archivo | Responsable |
|---|---|
| `modelos.py`, `excepciones.py`, `configuracion.py`, `interfaces.py` | Marta Lorenzo — contratos compartidos |
| `consola.py`, `dificultad.py`, `marcador.py`, `juego_consola.py`, `aplicacion.py`, `main.py` | Marta Lorenzo |
| `partida.py`, `generador.py`, `tests/` | Walter Nuñez |

## Diseño
- **POO:** cada responsabilidad es una clase (`Partida`, `SelectorDificultad`, `Marcador`, `JuegoConsola`...).
- **DRY:** reglas en `configuracion.py`; validación de entradas en `LectorDatos.pedir_valido()`.
- **SOLID:** las clases dependen de las interfaces de `interfaces.py` y reciben sus dependencias por el constructor; las piezas concretas solo se conectan en `main.py`.
