import flet as ft
from packages.misc.time_tracker import Timer

def app_navigation_bar(page: ft.Page, timer: Timer) -> ft.NavigationBar:

    def resume(func):
        timer.start()
        func()

    def pause(func):
        timer.stop()
        func()

    RETURN_TO_HOME_DLG = ft.AlertDialog(
        modal=True,
        title=ft.Text("Return home", size=27, weight=ft.FontWeight.W_500, color="#b4b4b4"),
        content=ft.Text("Quit current game and return to home?", size=20),
        actions=[
            ft.TextButton(text="Yes", on_click=lambda _: page.go("/")),
            ft.TextButton(text="No", on_click=lambda _: resume(lambda: page.close(RETURN_TO_HOME_DLG))) # NOQA
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )

    SELECT_AGAIN_DLG = ft.AlertDialog(
        modal=True,
        title=ft.Text("Reconfigure puzzle", size=27, weight=ft.FontWeight.W_500, color="#b4b4b4"),
        content=ft.Text("Quit current game and select different puzzle parameters?", size=20),
        actions=[
            ft.TextButton(text="Yes", on_click=lambda _: page.go("/select")),
            ft.TextButton(text="No", on_click=lambda _: resume(lambda: page.close(SELECT_AGAIN_DLG))) # NOQA
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )

    def on_change(event):
        if event.control.selected_index == 0:
            pause(lambda: page.open(RETURN_TO_HOME_DLG)) # NOQA
        elif event.control.selected_index == 1:
            pause(lambda: page.open(SELECT_AGAIN_DLG)) # NOQA

    return ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(label="Home", icon=ft.Icons.HOME), # NOQA
            ft.NavigationBarDestination(label="Select", icon=ft.Icons.ARROW_OUTWARD) # NOQA
        ],
        on_change=on_change
    )
