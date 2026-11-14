# 🏧 Cajero automático (POO, DRY y SOLID)

Simulación en consola de un cajero automático. El menú se mantiene activo hasta que el usuario decide salir.

- Consultar saldo, depositar y retirar (sin permitir saldo negativo).
- **PIN:** antes de entrar al menú hay que ingresar el PIN correcto (máximo 3 intentos).
- **Registro de movimientos:** cada depósito y retiro se guarda en una lista.
- **Ver historial:** muestra los movimientos registrados.
- **Múltiples usuarios:** cada uno con su PIN, saldo e historial.

## Cómo ejecutar
Desde la raíz del repositorio:
```bash
python3 asignaciones/cajero/main.py
```

## Usuarios de prueba
| Usuario | PIN | Saldo inicial |
|---|---|---|
| marta | 1234 | $1,000.00 |
| carlos | 5678 | $500.00 |
| ana | 0000 | $2,500.00 |

## Reparto
| Archivos | Responsable |
|---|---|
| `modelos.py`, `excepciones.py`, `interfaces.py`, `consola.py`, `repositorio.py`, `autenticacion.py`, `historial.py`, `menu.py`, `cajero.py`, `main.py` | Marta Lorenzo |
| `operaciones.py`, pruebas unitarias en `tests/` | Walter Nuñez |

## Diseño
- **POO:** cada responsabilidad es una clase (`Usuario`, `AutenticadorPin`, `MenuCajero`, `FormateadorHistorial`, `Cajero`...).
- **DRY:** la validación de entradas está en `LectorDatos.pedir_valido()`, el formato del dinero en `formatear_dinero()` y el manejo de errores del menú en un solo lugar.
- **SOLID:** las clases dependen de los contratos de `interfaces.py` y reciben sus dependencias por el constructor; las piezas concretas solo se conectan en `main.py`. Para agregar una opción al menú basta con agregar un `OpcionMenu`.
