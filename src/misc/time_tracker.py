import flet as ft
import time
import threading
from interval_timer import IntervalTimer

class Timer(ft.Container):
    def __init__(self, interval_s=1, callback=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.interval_s = interval_s
        self.callback = callback
        self.start_time = None
        self.prev_time = 0
        self.active = False
        self.th = None

    def did_mount(self):
        self.start()

    def start(self):
        self.active = True
        self.start_time = time.time()
        self.th = threading.Thread(target=self.tick, daemon=True)
        self.th.start()

    def stop(self):
        self.active = False
        self.prev_time += time.time() - self.start_time
        self.th.join()

    def tick(self):
        for _ in IntervalTimer(self.interval_s):
            if not self.active:
                break
            try:
                self.callback()
            except Exception as e:
                print(e)

    def build(self):
        return ft.Container(margin=0, padding=0)

    def will_unmount(self):
        self.stop()
        super().will_unmount()
