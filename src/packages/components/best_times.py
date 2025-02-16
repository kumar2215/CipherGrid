import flet as ft
from packages.misc.difficulty import Difficulty, DIFFICULTY_TO_COLOR

def best_times_page(page: ft.Page) -> ft.View:

    best_times = {}
    for difficulty in Difficulty:
        key = f"ciphergrid.best_times.{difficulty.name.lower()}"
        if page.client_storage.contains_key(key):
            best_times[difficulty] = page.client_storage.get(key)
        else:
            best_times[difficulty] = "No best time yet"

    return ft.View(
        route="/best_times",
        spacing=20,
        bgcolor="#9effff",
        controls=[
            ft.Container(height=20),
            ft.Text("Your Best Times", size=30, weight=ft.FontWeight.W_400, color="#b4b4b4"),
            ft.Column(
                spacing=10,
                controls=[
                    ft.Row(
                        spacing=10,
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Text(f"{difficulty.name.title()}:", size=20, color=DIFFICULTY_TO_COLOR[difficulty],
                                    weight=ft.FontWeight.W_600),
                            ft.Text(best_times[difficulty], size=20, weight=ft.FontWeight.W_500)
                        ]
                    )
                    for difficulty in Difficulty
                ]
            ),
            ft.ElevatedButton(text="Back to home", on_click=lambda _: page.go("/"))
        ],
        scroll=ft.ScrollMode.HIDDEN,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
