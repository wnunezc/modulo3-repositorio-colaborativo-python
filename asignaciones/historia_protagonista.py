# ==========================================
# Asignación: Estructura lineal simple
# Integrantes: Marta Lorenzo (Persona A), Walter (Persona B)
# ==========================================

nombre = input("¿Cuál es tu nombre? ")
edad = input("¿Cuántos años tienes? ")
ciudad = input("¿En qué ciudad vives? ")

profesion = input("¿A qué te dedicas? ")
pasatiempo = input("¿Cuál es tu pasatiempo favorito? ")
comida = input("¿Cuál es tu comida favorita? ")

# ---------- BLOQUE 3 (Persona B): desarrollo ----------
problema = input("¿Qué problema inesperado encontró el protagonista? ")
acompanante = input("¿Quién le ayudó a superarlo? ")
solucion = input("¿Cómo resolvieron el problema? ")
aprendizaje = input("¿Qué aprendió de esa experiencia? ")

# ---------- SALIDA ----------
print()
print(f"¡Hola, {nombre}! Tienes {edad} años y vives en {ciudad}.")
print()
print("=== LA HISTORIA DEL PROTAGONISTA ===")

# Inicio (Persona A)
print(f"{nombre} era una persona de {edad} años que vivía en {ciudad}.")
print(f"Trabajaba como {profesion} y en su tiempo libre le encantaba {pasatiempo}.")
print(f"Cada fin de semana celebraba comiendo {comida}.")

# Nudo y desenlace (Persona B)
print(f"Un día apareció un problema inesperado: {problema}.")
print(f"Aunque al principio no sabía qué hacer, {acompanante} le ofreció ayuda.")
print(f"Juntos encontraron una solución: {solucion}.")
print(f"Después de superar el reto, {nombre} regresó a su vida en {ciudad}.")
print(f"Desde entonces, conservó una lección: {aprendizaje}.")
