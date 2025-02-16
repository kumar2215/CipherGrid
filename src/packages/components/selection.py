import flet as ft
from packages.problem_generation.generate import MathProblem
from packages.misc.difficulty import Difficulty

def difficulty_column(puzzle_params: dict):

    def on_change(event):
        puzzle_params.update({"difficulty": Difficulty[event.control.value]})

    return ft.Column(
        spacing=20,
        controls=[
            ft.Text("Select a difficulty:", size=20, weight=ft.FontWeight.W_500, color="black"),
            ft.RadioGroup(
                content=ft.Column(
                    spacing=10,
                    controls=[
                        ft.Radio(value=difficulty.name, label=difficulty.name.title()) for difficulty in Difficulty
                    ]
                ),
                on_change=on_change,
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

def base_column(puzzle_params: dict):

    def on_change(event):
        base = int(event.control.label)
        if base in puzzle_params["bases"]:
            puzzle_params["bases"].remove(base)
        else:
            puzzle_params["bases"].add(base)

    return ft.Column(
        spacing=20,
        controls=[
            ft.Text("Select bases:", size=20, weight=ft.FontWeight.W_500, color="black"),
            ft.Column(
                spacing=10,
                controls=[
                    ft.Checkbox(label=str(base), on_change=on_change)
                    for base in range(2, 11)
                ]
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

def selection_page(page: ft.Page, puzzle_params: dict) -> ft.View:

    def handle_click(event):
        page.close(invalid_selection_dlg) # NOQA

    invalid_selection_dlg = ft.AlertDialog(
        title=ft.Text("Invalid selection", text_align=ft.TextAlign.CENTER),
        content=ft.Text("Please select a difficulty, at least one topic, and at least one base."),
        actions=[ft.TextButton(text="OK", on_click=handle_click)],
        actions_alignment=ft.MainAxisAlignment.CENTER
    )

    progress_dlg = ft.AlertDialog(
        title=ft.Text("Generating puzzle...", text_align=ft.TextAlign.CENTER),
        content=ft.Row(
            controls=[
                ft.ProgressRing(width=50, height=50),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        actions=[],
        actions_alignment=ft.MainAxisAlignment.CENTER
    )

    def go_to_play(event):
        if all(puzzle_params.values()):
            page.open(progress_dlg) # NOQA
            page.go("/play")
        else:
            page.open(invalid_selection_dlg) # NOQA

    return ft.View(
        route="/select",
        spacing=20,
        bgcolor="#9effff",
        controls=[
            ft.Container(height=20),
            difficulty_column(puzzle_params),
            base_column(puzzle_params),
            ft.ElevatedButton(text="Start game", on_click=go_to_play),
        ],
        scroll=ft.ScrollMode.HIDDEN,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
