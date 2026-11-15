"""
Formato del historial de movimientos.
Responsable: Marta Lorenzo
"""
from decimal import Decimal

from modelos import Usuario


def formatear_dinero(monto: Decimal) -> str:
    """Único lugar donde se da formato al dinero (DRY)."""
    return f"${monto:,.2f}"


class FormateadorHistorial:
    """Solo convierte movimientos en texto; no imprime ni modifica nada (SRP)."""

    def formatear(self, usuario: Usuario) -> list[str]:
        if not usuario.movimientos:
            return ["📭 Aún no tienes movimientos."]

        lineas = [f"📜 Historial de {usuario.nombre}"]
        numero = 1
        for mov in usuario.movimientos:
            lineas.append(f"  {numero}. {mov.tipo.value:<9} "
                          f"{formatear_dinero(mov.monto):>12}   "
                          f"Saldo: {formatear_dinero(mov.saldo_resultante)}")
            numero += 1
        lineas.append(f"  Total de movimientos: {len(usuario.movimientos)}")
        return lineas
