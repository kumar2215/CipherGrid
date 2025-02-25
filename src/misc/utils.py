import matplotlib
import matplotlib.pyplot as plt
from PIL import Image
from src.puzzle_logic.puzzle_manager import PuzzleManager
import io
import base64

matplotlib.use("Agg")

def get_formatted_time_str(time_str: str) -> str:
    minutes, seconds = time_str.split(":")
    minutes = minutes.removeprefix("0")
    seconds = seconds.removeprefix("0")
    if minutes == "0": return f"{seconds.removeprefix('0')}s"
    return f"{minutes.removeprefix('0')}m {seconds.removeprefix('0')}s"

def get_time_from_str(time_str: str) -> int:
    if "m" not in time_str:
        return int(time_str.replace("s", ""))
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

def generate_puzzle(*args) -> PuzzleManager:
    return PuzzleManager(*args)
