# Guia de colaboracion

Este repositorio esta preparado para que cada integrante trabaje en una rama propia y envie un Pull Request.

## Pasos sugeridos

1. Clonar el repositorio.
2. Crear una rama nueva con un nombre claro, por ejemplo:

```bash
git checkout -b mejora-matematicas
```

3. Modificar o agregar codigo en el modulo correspondiente.
4. Probar el proyecto:

```bash
python main.py
```

5. Guardar los cambios:

```bash
git add .
git commit -m "Descripcion breve del cambio"
git push -u origin nombre-de-la-rama
```

6. Crear un Pull Request hacia la rama `main`.
7. Pedir revision de otro companero antes de combinar.

## Ideas para los companeros

- Mejorar `modulos/matematicas.py` con resta, multiplicacion o division.
- Ampliar `modulos/cuento.py` con una historia mas larga.
- Crear un nuevo modulo con funciones de texto, listas o conversiones.
