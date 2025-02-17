import flet as ft
from src.puzzle_logic.crossword import Orientation
from src.misc.utils import render_latex_to_image

def get_column_hints(hints: list[str]):
    return ft.Row(
        spacing=10,
        controls=[
            ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Image(
                        src_base64=render_latex_to_image(hint),
                        fit=ft.ImageFit.CONTAIN,
                    )
                    for hint in hints
                ]
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        scroll=ft.ScrollMode.HIDDEN
    )

def hints_component(hints: dict):
    hints_for_top_to_bottom = []
    hints_for_left_to_right = []

    for hint in hints:
        latex_str, orientation = hints[hint]
        if orientation == Orientation.TOP_TO_BOTTOM:
            hints_for_top_to_bottom.append(latex_str)
        else:
            hints_for_left_to_right.append(latex_str)

    return ft.Column(
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Text("Hints for columns:", size=20, weight=ft.FontWeight.W_500, color="blue"),
            get_column_hints(hints_for_top_to_bottom),
            ft.Text("Hints for rows:", size=20, weight=ft.FontWeight.W_500, color="blue"),
            get_column_hints(hints_for_left_to_right)
        ]
    )
