from pathlib import Path
import sys

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from figures.python.io import output_pdf_path, save_pdf
from figures.python.palette import color
from figures.python.style import apply_style, apply_suptitle, get_figsize


def label_layout(label: str, width: float) -> tuple[str, float]:
    compact = {
        "WebSocket transport": "WebSocket\ntransport",
        "State/render update": "State/render\nupdate",
    }
    display = compact.get(label, label)
    if width <= 8:
        return display, 7.0
    if width <= 10:
        return display, 7.2
    return display, 8.0


def main() -> None:
    apply_style()
    fig, ax = plt.subplots(figsize=get_figsize(override=(12.6, 5.2)))

    # Approximate budget ranges in milliseconds (illustrative for architecture discussion)
    segments = [
        ("Browser audio latency", 30, color("audio_fill"), color("audio_edge")),
        ("WebSocket transport", 8, color("ws_fill"), color("ws_edge")),
        ("Backend inference", 42, color("processing_fill"), color("stroke_default")),
        ("State/render update", 10, color("render_fill"), color("render_edge")),
    ]

    start = 0.0
    y = 0.58
    h = 0.22

    for label, width, fill, edge in segments:
        label_text, label_fontsize = label_layout(label, width)
        ax.barh(
            [y],
            [width],
            left=[start],
            height=h,
            color=fill,
            edgecolor=edge,
            linewidth=1.0,
        )
        ax.text(
            start + width / 2,
            y,
            f"{label_text}\n{width:.0f} ms",
            ha="center",
            va="center",
            fontsize=label_fontsize,
            color=color("text_primary"),
        )
        start += width

    total = start

    # Reference lines
    target = 100
    ax.axvline(target, color=color("danger_edge"), linestyle="--", linewidth=1.2)
    ax.text(target + 1.2, y + 0.18, "Target threshold (100 ms)", fontsize=8.0, color=color("danger_edge"), va="center")

    ax.axvline(total, color=color("ws_edge"), linestyle="-.", linewidth=1.2)
    ax.text(total - 1.2, y - 0.18, f"Estimated total (~{total:.0f} ms)", fontsize=8.0, color=color("ws_edge"), va="center", ha="right")

    # Highlight synchronous perception zone
    ax.axvspan(0, target, color="#ecfdf5", alpha=0.35, zorder=0)
    ax.text(50, 0.20, "Synchronous perception zone (<100 ms)", ha="center", va="center", fontsize=8.2, color=color("text_muted"))
    ax.text(50, 0.12, "Above this threshold, delay becomes more noticeable", ha="center", va="center", fontsize=7.7, color=color("text_muted"))

    # Axis formatting
    ax.set_xlim(0, 125)
    ax.set_ylim(0, 1)
    ax.set_yticks([])
    ax.set_xlabel("Latency (ms)")
    ax.grid(axis="x", color="#cbd5e1", linestyle=":", linewidth=0.8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)

    apply_suptitle(fig, "Latency-Budget Breakdown")

    out_pdf = output_pdf_path(__file__, chapter=4)
    save_pdf(fig, out_pdf)
    print(f"Saved {out_pdf}")


if __name__ == "__main__":
    main()
