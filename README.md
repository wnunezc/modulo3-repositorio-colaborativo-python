# Repositorio colaborativo en Python

Proyecto del Modulo 3 para practicar GitHub, ramas, Pull Requests y colaboracion en un proyecto Python.

## Descripcion

El repositorio contiene tres modulos separados con funcionalidades diferentes:

- `modulos/matematicas.py`: funciones para operaciones matematicas.
- `modulos/cuento.py`: imprime un cuento con titulo, varios parrafos y moraleja. Permite cambiar el nombre del protagonista con `imprimir_cuento("Nombre")`.
- `modulos/saludos.py`: funcion reutilizada del Modulo 2 para imprimir un saludo.

El archivo `main.py` ejecuta las funciones principales de cada modulo.

## Estructura

```text
.
├── main.py
├── modulos/
│   ├── __init__.py
│   ├── cuento.py
│   ├── matematicas.py
│   └── saludos.py
├── CONTRIBUTING.md
└── README.md
```

## Uso

Para ejecutar el proyecto:

```bash
python main.py
```

Salida esperada:

```text
Hola, GitHub
Resultado de 1 + 1: 2
El equipo que aprendio Git
==========================

Habia una vez un equipo que aprendio Git colaborando en Python.
...
Moraleja: trabajar en equipo, con orden y revisiones, mejora el resultado de todos.
```

## Colaboracion

Cada integrante del equipo debe trabajar en una rama separada, subir sus cambios y crear un Pull Request hacia `main`.

Ejemplo:

```bash
git checkout -b nombre-de-la-rama
git add .
git commit -m "Descripcion del cambio"
git push -u origin nombre-de-la-rama
```

Luego se crea el Pull Request en GitHub y otro integrante revisa el cambio antes de combinarlo.
