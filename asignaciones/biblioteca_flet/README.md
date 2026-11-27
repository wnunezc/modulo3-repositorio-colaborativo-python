# Sistema de Control de Biblioteca con Flet

Proyecto final de Programación de Computadoras III.

**Estudiantes:** Marta Lorenzo y Walter Nuñez.

Aplicación de escritorio para registrar libros y clientes y gestionar préstamos. Los datos se conservan únicamente durante la sesión: al cerrar el proceso y abrir una nueva ejecución, las listas comienzan vacías.

## Requisitos

- Windows y Python 3.10 o superior. Desarrollo y pruebas realizados con Python 3.13.
- Flet 1.1.4 con el componente de escritorio, declarado en `requirements.txt`.
- Acceso a Internet para instalar las dependencias y descargar el cliente de escritorio de Flet en el primer arranque. No hay autenticación ni servicios de base de datos en esta aplicación.

## Instalación y ejecución en PowerShell

Desde la raíz del repositorio:

```powershell
Set-Location .\asignaciones\biblioteca_flet
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

Para ejecuciones posteriores, desde la misma carpeta:

```powershell
.\.venv\Scripts\python.exe main.py
```

No es necesario activar el entorno virtual ni cambiar la política de ejecución de PowerShell. El `main.py` de la raíz del repositorio corresponde a ejercicios anteriores y no inicia esta biblioteca.

## Uso

1. **Libros:** consultar el inventario inicial y registrar un libro con Título, Autor e ISBN. Los tres campos son obligatorios; el ISBN debe ser único. El libro se crea con estado **Disponible**.
2. **Clientes:** consultar los clientes registrados y agregar un cliente con Nombre, Apellido y Cédula/ID. Los tres campos son obligatorios; la cédula debe ser única.
3. **Préstamos:** seleccionar un libro disponible y un cliente existente y pulsar **Confirmar préstamo**. La aplicación registra la asociación y cambia el estado del libro a **Prestado**. El libro deja de aparecer entre los disponibles; el inventario muestra su estado actualizado y el cliente que lo tiene.
4. **Salir:** cerrar la ventana de la aplicación. También se puede usar el cierre habitual de Windows.

La navegación conserva los datos dentro de la misma ejecución. Las listas se muestran sin necesidad de registrar nuevos elementos. Los registros y préstamos refrescan los controles de Flet mediante `page.update()`.

Los campos vacíos, identificadores duplicados y selecciones inválidas producen mensajes de validación. Ante un registro rechazado se conserva el contenido del formulario para corregirlo. El préstamo se habilita cuando hay selecciones válidas y vuelve a comprobarse en el modelo al confirmar.

## Organización y responsabilidades

| Archivo | Responsabilidad |
|---|---|
| `modelos.py` | Clases `Libro`, `Cliente`, `Prestamo` y `Biblioteca`; datos y validaciones de negocio aportados por Marta. |
| `interfaz.py` | Formularios, listas, selección de préstamos, navegación y coordinación con el modelo. |
| `main.py` | Configuración de la ventana e inicio de Flet. |
| `test_modelos.py` | Diez pruebas originales de la lógica. |
| `test_interfaz.py` | Pruebas de integración entre controles de Flet y modelos, con una página de prueba. |
| `requirements.txt` | Versión de Flet utilizada y componente de escritorio. |

La interfaz compone tres vistas y recibe una única instancia de `Biblioteca`. `VistaRegistro` comparte el comportamiento de los dos formularios mediante operaciones inyectadas; `VistaPrestamos` concentra la selección y confirmación de préstamos. `AplicacionBiblioteca` coordina navegación, mensajes y refresco. El dominio no importa Flet y la interfaz utiliza sus métodos en vez de duplicar sus validaciones.

## Pruebas

Desde `asignaciones/biblioteca_flet/`:

```powershell
.\.venv\Scripts\python.exe -B -m unittest -v
.\.venv\Scripts\python.exe -m pip check
```

Las pruebas no abren ventanas. Cubren registros, campos obligatorios, duplicados, listas iniciales, selectores, préstamo, selecciones incompletas u obsoletas, actualización del inventario, navegación, aislamiento entre ejecuciones y solicitud de cierre. La salida se prueba con una ventana simulada; estas pruebas no sustituyen una revisión visual completa.

### Verificación disponible

- Las diez pruebas originales del modelo y las doce nuevas de integración fueron aprobadas durante el desarrollo.
- En Windows se verificó el arranque real, la presentación inicial y el mensaje de rechazo de un registro vacío.
- La prueba manual completa de registro, selección, préstamo, desplazamiento y cierre de la ventana quedó pendiente; la comprobación automatizada de esos controles sí está incluida.

## Alcance

- Tres secciones principales, datos en memoria y comportamiento reactivo, conforme al challenge.
- No se utiliza MySQL, SQLite, JSON ni persistencia entre ejecuciones.
- La devolución de libros es opcional en el enunciado. `Biblioteca.devolver()` ya existe y tiene una prueba original; esta entrega no añade controles de devolución.
- El diseño se adapta en una o dos columnas al ancho disponible; la ventana tiene un mínimo de 760 × 600 y permite desplazamiento vertical.

## Referencias técnicas

- [Controles de Flet](https://flet.dev/docs/controls/).
- [Dropdown y selección de registros](https://flet.dev/docs/controls/dropdown/).
- [Column y organización vertical](https://flet.dev/docs/controls/column/).
- [Paquete oficial de Flet](https://pypi.org/project/flet/1.1.4/).
