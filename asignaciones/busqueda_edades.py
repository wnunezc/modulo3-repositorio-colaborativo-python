# ==========================================
# Asignación: Listas, diccionarios y condicionales
# Rama: listas-diccionarios-condicionales-marta
# Integrantes: Marta Lorenzo (Persona A), Walter (Persona B)
# ==========================================

# ---------- Persona A: lista de nombres ----------
nombres = ["Ana", "Luis", "Carlos", "María", "Sofía"]

# ---------- Persona A: diccionario de edades ----------
edades = {
    nombres[0]: 30,
    nombres[1]: 25,
    nombres[2]: 40,
    nombres[3]: 22,
    nombres[4]: 35
}

# ---------- Persona B: entrada del usuario ----------
nombre_ingresado = input("Ingresa un nombre: ").strip()

# ---------- Persona B: condicional ----------
if nombre_ingresado in edades:
    print(f"{nombre_ingresado} tiene {edades[nombre_ingresado]} años.")
else:
    print(f"{nombre_ingresado} no fue encontrado.")
