import flet as ft
from packages.misc.difficulty import Difficulty
from packages.misc.utils import get_formatted_time_str, get_time_from_str

def completed_message_dialog(page: ft.Page, difficulty: Difficulty, time_txt: ft.Text) -> ft.AlertDialog:
    time_taken = get_formatted_time_str(time_txt.value)
    key = f"ciphergrid.best_times.{difficulty.name.lower()}"
    record_broken = False

    if page.client_storage.contains_key(key):
        best_time = page.client_storage.get(key)

        current_time = get_time_from_str(time_taken)
        best_time = get_time_from_str(best_time)

        if current_time < best_time:
            page.client_storage.set(key, time_taken)
            record_broken = True
    else:
        page.client_storage.set(key, time_taken)

    success_message = f"You have successfully completed the crossword puzzle in {time_taken}!"
    if record_broken:
        success_message += " You have broken your record!"

    return ft.AlertDialog(
        modal=True,
        title=ft.Text("Congratulations!", size=30, weight=ft.FontWeight.W_600, color="green"),
        content=ft.Text(success_message, size=20),
        actions=[
            ft.TextButton(
                text="Ok",
                on_click=lambda _: page.go("/"),
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=10),
                    bgcolor="green",
                    color="white",
                    overlay_color="lightgreen"
                )
            )
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER
    )
