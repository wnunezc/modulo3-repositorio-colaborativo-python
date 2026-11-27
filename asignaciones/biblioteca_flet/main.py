"""Entrada de la aplicación de escritorio de la biblioteca."""

import flet as ft

from interfaz import AplicacionBiblioteca


def main(page: ft.Page):
    page.title = "Biblioteca | Marta Lorenzo y Walter Nuñez"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(font_family="Segoe UI", color_scheme_seed="#27304B")
    page.bgcolor = "#F1F4F8"
    page.padding = 24
    page.window.width = 1180
    page.window.height = 820
    page.window.min_width = 760
    page.window.min_height = 600
    AplicacionBiblioteca(page)


if __name__ == "__main__":
    ft.run(main)
