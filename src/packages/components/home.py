import flet as ft
from packages.misc.utils import render_image

def home_page(page: ft.Page) -> ft.View:
    return ft.View(
        route="/",
        spacing=20,
        bgcolor="#9effff",
        controls=[
            ft.Container(height=20),
            ft.Image(src_base64=render_image("assets/icon.png", 100, 250), fit=ft.ImageFit.CONTAIN),
            ft.Image(
                src_base64=render_image("assets/homepage_icon.png", 400, 400),
                fit=ft.ImageFit.CONTAIN
            ),
            ft.ElevatedButton(text="Start new game", on_click=lambda _: page.go("/select")),
            ft.ElevatedButton(text="View best times", on_click=lambda _: page.go("/best_times")),
            ft.ElevatedButton(text="How to play", on_click=lambda _: page.go("/instructions"))
        ],
        scroll=ft.ScrollMode.HIDDEN,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
