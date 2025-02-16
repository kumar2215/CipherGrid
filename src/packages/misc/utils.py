import matplotlib
import matplotlib.pyplot as plt
from PIL import Image
from packages.puzzle_logic.puzzle_manager import PuzzleManager
import io
import base64
import multiprocessing

matplotlib.use("Agg")

def get_formatted_time_str(time_str: str) -> str:
    minutes, seconds = time_str.split(":")
    minutes = minutes.removeprefix("0")
    seconds = seconds.removeprefix("0")
    if minutes == "0": return f"{seconds.removeprefix('0')}s"
    return f"{minutes.removeprefix('0')}m {seconds.removeprefix('0')}s"

def get_time_from_str(time_str: str) -> int:
    minutes, seconds = time_str.split(" ")
    minutes = int(minutes.replace("m", ""))
    seconds = int(seconds.replace("s", ""))
    return minutes * 60 + seconds

def render_image(path: str, height: int, width: int) -> str:
    buf = io.BytesIO()
    img = Image.open(path)
    img = img.resize((width, height))
    img.save(buf, format="png")
    return base64.b64encode(buf.getvalue()).decode("utf-8")

def render_latex_to_image(latex_expr: str) -> str:
    fig, ax = plt.subplots(figsize=(1, 1))  # Adjust size as needed
    ax.axis("off")  # Hide axes
    ax.text(0.5, 0.5, latex_expr, fontsize=12, ha="center", va="center")
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight", pad_inches=0.01)
    plt.close(fig)
    buf.seek(0)

    # Crop image
    img = Image.open(buf)
    box = list(img.getbbox())
    h = box[3] - box[1]
    box[1] += (h // 4)
    box[3] -= (h // 4)
    img = img.crop(tuple(box)) # NOQA
    buf = io.BytesIO()
    img.save(buf, format="png")
    return base64.b64encode(buf.getvalue()).decode("utf-8")

def generate_puzzle(*args, timeout=5) -> PuzzleManager:
    while True:
        queue = multiprocessing.Queue()  # Create a queue for return value
        process = multiprocessing.Process(target=PuzzleManager, args=(*args, queue))
        process.start()
        process.join(timeout)

        if process.is_alive():
            print("Function timed out! Restarting...")
            process.terminate()
            process.join()
        else:
            if not queue.empty():
                return queue.get()
