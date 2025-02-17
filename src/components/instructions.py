import flet as ft

def instructions_page(page: ft.Page) -> ft.View:
    return ft.View(
        route="/instructions",
        spacing=20,
        bgcolor="#9effff",
        controls=[
            ft.Container(height=20),
            ft.Text("How To Play:", size=30, weight=ft.FontWeight.W_500, color="#b4b4b4"),
            ft.Text(
                "This is a math puzzle game where you have to fill in the grid with numbers. "
                "Each row and column has a hint that tells you the number in that row or column. "
                "The hints are in the form of math problems. "
                "You can choose the difficulty level and the number bases to use in the puzzle. ",
                size=20
            ),
            ft.Text("Steps to solve the hint:", size=20, weight=ft.FontWeight.W_500, color="#b4b4b4"),
            ft.Text("1. Solve for the capital letter in the form the solution to the problem is given in.", size=20),
            ft.Text("2. Convert that number into the base specified in the hint.", size=20),
            ft.Text("3. Fill in the grid with the number you got from the conversion.", size=20),
            ft.Markdown(
                "Learn more about base conversion "
                "[here](https://byjus.com/gate/conversion-of-bases-to-other-bases-notes/).",
                on_tap_link=lambda e: page.launch_url(e.data)
            ),
            ft.ElevatedButton(text="Back to home", on_click=lambda _: page.go("/")),
        ],
        scroll=ft.ScrollMode.HIDDEN,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
