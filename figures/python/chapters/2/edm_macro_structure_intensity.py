from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from figures.python.io import output_pdf_path, save_pdf
from figures.python.style import apply_style


def smooth_signal(y: np.ndarray, window: int = 21) -> np.ndarray:
    """Simple moving-average smoothing with odd window length."""
    if window % 2 == 0:
        window += 1
    kernel = np.ones(window, dtype=float) / window
    y_pad = np.pad(y, (window // 2, window // 2), mode="edge")
    return np.convolve(y_pad, kernel, mode="valid")


def main() -> None:
    apply_style()
    # Relative section lengths (arbitrary timeline units)
    sections = [
        ("Intro", 14, "#dbeafe"),
        ("Build-up 1", 10, "#fee2e2"),
        ("Drop 1", 14, "#dcfce7"),
        ("Breakdown", 12, "#f3e8ff"),
        ("Build-up 2", 10, "#fecaca"),
        ("Drop 2", 16, "#bbf7d0"),
        ("Outro", 10, "#e2e8f0"),
    ]

    fig, ax = plt.subplots(figsize=(12.0, 4.6))

    # Draw section bands
    x0 = 0.0
    centers = []
    boundaries = [0.0]
    total_len = sum(length for _, length, _ in sections)
    for label, length, color in sections:
        rect = Rectangle(
            (x0, 0.0),
            length,
            1.0,
            facecolor=color,
            edgecolor="#94a3b8",
            linewidth=0.8,
            alpha=0.85,
            zorder=0,
        )
        ax.add_patch(rect)
        centers.append((x0 + length / 2.0, label))
        x0 += length
        boundaries.append(x0)

    # Construct an intensity profile with dips/peaks per section
    x_points = np.array([0, 8, 14, 22, 28, 36, 44, 50, 58, 66, 72, 80, 86], dtype=float)
    y_points = np.array([0.22, 0.34, 0.42, 0.72, 0.86, 0.56, 0.18, 0.44, 0.95, 0.90, 0.60, 0.35, 0.18], dtype=float)

    x = np.linspace(0, total_len, 1000)
    y = np.interp(x, x_points, y_points)
    y = smooth_signal(y, window=35)

    # Intensity area + curve
    ax.fill_between(x, 0, y, color="#f59e0b", alpha=0.18, zorder=1)
    ax.plot(x, y, color="#d97706", linewidth=2.2, zorder=2, label="Relative intensity")

    # Vertical separators at section boundaries
    for b in boundaries:
        ax.axvline(b, color="#64748b", linewidth=0.7, linestyle="--", alpha=0.65, zorder=1)

    # Section labels
    for cx, label in centers:
        ax.text(cx, 1.03, label, ha="center", va="bottom", fontsize=8.5, fontweight="bold", color="#1f2937")

    # Annotate key structural moments
    ax.annotate(
        "Drop 1 peak",
        xy=(26, np.interp(26, x, y)),
        xytext=(16, 0.95),
        arrowprops=dict(arrowstyle="->", lw=0.8, color="#92400e"),
        fontsize=8,
        color="#92400e",
    )
    ax.annotate(
        "Breakdown dip",
        xy=(45, np.interp(45, x, y)),
        xytext=(38, 0.36),
        arrowprops=dict(arrowstyle="->", lw=0.8, color="#92400e"),
        fontsize=8,
        color="#92400e",
    )
    ax.annotate(
        "Drop 2 peak",
        xy=(59, np.interp(59, x, y)),
        xytext=(63, 0.98),
        arrowprops=dict(arrowstyle="->", lw=0.8, color="#92400e"),
        fontsize=8,
        color="#92400e",
    )

    ax.set_xlim(0, total_len)
    ax.set_ylim(0, 1.12)
    ax.set_xlabel("Track timeline (relative duration)")
    ax.set_ylabel("Relative energy / intensity")
    ax.set_xticks([])
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.grid(axis="y", color="#cbd5e1", linewidth=0.5, alpha=0.6)

    ax.set_title(
        "Typical EDM Macro-Structure and Intensity Curve",
        fontsize=11,
        fontweight="bold",
        pad=12,
    )

    fig.tight_layout()

    out_pdf = output_pdf_path(__file__, chapter=2)
    save_pdf(fig, out_pdf)

    print(f"Saved {out_pdf}")


if __name__ == "__main__":
    main()
