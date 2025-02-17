import flet as ft
from src.components.grid import grid_component
from src.components.hints import hints_component
from src.components.home import home_page
from src.components.selection import selection_page
from src.components.instructions import instructions_page
from src.components.best_times import best_times_page
from src.components.navigation_bar import app_navigation_bar
from src.misc.utils import generate_puzzle
from src.misc.time_tracker import Timer
import multiprocessing
import time

if __name__ == "__main__":
    multiprocessing.freeze_support()

    def main(page: ft.Page):

        puzzle_params = {}

        def route_change(event: ft.RouteChangeEvent):
            page.views.clear()
            page.views.append(home_page(page))

            if page.route == "/select":
                puzzle_params["difficulty"] = None
                puzzle_params["bases"] = set()
                page.views.append(selection_page(page, puzzle_params))

            elif page.route == "/instructions":
                page.views.append(instructions_page(page))

            elif page.route == "/best_times":
                page.views.append(best_times_page(page))

            elif page.route == "/play":
                time_txt = ft.Text("", size=20, weight=ft.FontWeight.W_600)

                def refresh_time():
                    nonlocal time_txt, timer, page
                    if timer.start_time is None:
                        timer.start_time = time.time()
                    time_txt.value = time.strftime("%M:%S",
                                                   time.gmtime(timer.prev_time + time.time() - timer.start_time))
                    page.update()

                timer = Timer(interval_s=1, callback=refresh_time)
                puzzle_manager = generate_puzzle(*list(puzzle_params.values()))

                page.views.append(
                    ft.View(
                        route="/play",
                        controls=[
                            ft.Container(height=20),
                            grid_component(page, puzzle_manager, time_txt, timer),
                            hints_component(puzzle_manager.hints),
                            app_navigation_bar(page, timer)
                        ],
                        bgcolor="white",
                        padding=20,
                        scroll=ft.ScrollMode.HIDDEN,
                        vertical_alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                )

            page.update()

        def view_pop(event: ft.ViewPopEvent):
            page.views.pop()
            top_view = page.views[-1]
            page.go(top_view.route)

        page.on_route_change = route_change
        page.on_view_pop = view_pop
        page.go(page.route)

    ft.app(target=main)
