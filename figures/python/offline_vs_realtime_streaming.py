from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch, Rectangle


plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 10,
        "axes.linewidth": 0.7,
    }
)


def make_wave(n=1400):
    rng = np.random.default_rng(7)
    x = np.linspace(0, 1, n)
    y = (
        0.55 * np.sin(2 * np.pi * 2.4 * x + 0.4)
        + 0.25 * np.sin(2 * np.pi * 7.0 * x)
        + 0.08 * rng.normal(size=n)
    )
    y = 0.28 * y / (np.max(np.abs(y)) + 1e-12)
    return x, y


def add_box(ax, x, y, w, h, text, fc="#ffffff", ec="#111827", fs=9.5):
    rect = Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec, linewidth=0.8, zorder=4)
    ax.add_patch(rect)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, zorder=5)
    return rect


def main():
    fig, axes = plt.subplots(2, 1, figsize=(14, 7), gridspec_kw={"hspace": 0.36})
    fig.patch.set_facecolor("white")

    xw, yw = make_wave()
    x_left, x_right = 0.08, 0.92
    x_plot = x_left + (x_right - x_left) * xw

    # -------------------- (A) OFFLINE --------------------
    ax = axes[0]
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.90, 0.95)
    ax.axis("off")

    ax.text(0.015, 0.78, "OFFLINE", rotation=90, ha="center", va="center", fontsize=13, fontweight="bold", color="#4b6b8a")
    ax.text(0.03, 0.90, "(A)", ha="left", va="top", fontsize=12, fontweight="bold")

    y_off_center = 0.30
    y_off = y_off_center + yw
    ax.fill_between(x_plot, y_off_center, y_off, color="#bfdbfe", alpha=0.95, zorder=2, linewidth=0)
    ax.plot(x_plot, y_off, color="#1d4ed8", linewidth=1.0, zorder=3)
    y_off_peak = float(np.max(y_off))
    y_anno_top = y_off_peak + 0.30  # >=15% axes-height clearance above waveform peak
    ax.text(
        0.46,
        y_anno_top + 0.1,
        "Entire signal available at once",
        ha="left",
        va="bottom",
        fontsize=9,
        style="italic",
        color="#374151",
        bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="none", alpha=0.95),
    )

    # processing chain
    pbox = add_box(ax, 0.36, -0.20, 0.18, 0.13, "Process( x[0...N] )", fc="#f8fafc")
    obox = add_box(ax, 0.66, -0.20, 0.17, 0.13, "Output y[0...N]", fc="#f8fafc")

    ax.add_patch(FancyArrowPatch((0.22, -0.135), (0.36, -0.135), arrowstyle="-|>", mutation_scale=13, linewidth=1.1, color="#111827"))
    ax.add_patch(FancyArrowPatch((0.54, -0.135), (0.66, -0.135), arrowstyle="-|>", mutation_scale=13, linewidth=1.1, color="#111827"))

    ax.text(
        0.49,
        y_anno_top - 0.08,
        "No causal constraint - future samples accessible.",
        ha="left",
        va="bottom",
        fontsize=8.8,
        color="#4b5563",
        bbox=dict(boxstyle="round,pad=0.16", fc="white", ec="none", alpha=0.95),
    )
    add_box(
        ax,
        0.81,
        -0.75,
        0.1,
        0.5,
        "Latency:\nentire signal\nduration.",
        fc="#f9fafb",
        ec="#6b7280",
        fs=8.5,
    )

    # -------------------- (B) REAL-TIME --------------------
    ax = axes[1]
    ax.set_xlim(0, 1)
    ax.set_ylim(-1.00, 1.02)
    ax.axis("off")

    ax.text(0.015, 0.74, "REAL-TIME", rotation=90, ha="center", va="center", fontsize=13, fontweight="bold", color="#c96a4a")
    ax.text(0.03, 0.96, "(B)", ha="left", va="top", fontsize=12, fontweight="bold")

    y_rt_center = 0.42
    y_rt = y_rt_center + yw
    y_rt_peak = float(np.max(y_rt))

    # block structure (full-width so visual span matches offline row)
    n_blocks = 4
    block_w = (x_right - x_left) / n_blocks
    block_x = [x_left + i * block_w for i in range(n_blocks)]
    shades = ["#fed7cc", "#fdbaa8", "#fb9f82", "#f9825e"]

    # Causal regions and current time marker after Block 3
    n0_x = block_x[0] + 3 * block_w
    ax.add_patch(Rectangle((x_left, 0.12), n0_x - x_left, 0.56, facecolor="#dcfce7", edgecolor="none", alpha=0.18, zorder=0))
    ax.add_patch(Rectangle((n0_x, 0.12), x_right - n0_x, 0.56, facecolor="#fee2e2", edgecolor="none", alpha=0.22, zorder=0))
    ax.plot([n0_x, n0_x], [0.12, 0.70], linestyle="--", color="#dc2626", linewidth=1.0, zorder=1)
    block_label_y = 0.82
    y_rt_note = y_rt_peak + 0.15
    ax.text(
        n0_x - 0.1,
        y_rt_note + 0.37,
        "Future - inaccessible",
        ha="left",
        va="bottom",
        fontsize=8.8,
        color="#374151",
        bbox=dict(boxstyle="round,pad=0.16", fc="white", ec="none", alpha=0.95),
    )
    ax.text(
        n0_x - 0.07,
        y_rt_note + 0.2,
        "(causal constraint)",
        ha="left",
        va="bottom",
        fontsize=8.2,
        color="#4b5563",
        bbox=dict(boxstyle="round,pad=0.14", fc="white", ec="none", alpha=0.95),
    )

    # waveform split into blocks
    for i in range(n_blocks):
        bx0 = block_x[i]
        bx1 = bx0 + block_w
        m = (x_plot >= bx0) & (x_plot <= bx1)
        ax.fill_between(x_plot[m], y_rt_center, y_rt[m], color=shades[i], alpha=0.85, linewidth=0, zorder=2)
        ax.plot(x_plot[m], y_rt[m], color="#9a3412", linewidth=0.95, zorder=3)
        ax.text((bx0 + bx1) / 2, block_label_y, f"Block {i+1}", ha="center", va="bottom", fontsize=8.6)
        if i > 0:
            ax.plot([bx0, bx0], [0.12, 0.70], linestyle=(0, (3, 3)), color="#9ca3af", linewidth=0.8, zorder=1)
    ax.text(0.935, block_label_y, "...", ha="left", va="bottom", fontsize=11, color="#6b7280")

    # block width annotation
    ax.annotate("", xy=(block_x[0], 0.10), xytext=(block_x[0] + block_w, 0.10), arrowprops=dict(arrowstyle="<->", lw=1.0, color="#374151"))
    ax.text(block_x[0], 0, "M samples", ha="left", va="top", fontsize=8.3, color="#374151")

    add_box(
        ax,
        0.81,
        -0.65,
        0.1,
        0.7,
        "Latency:\nT = M / Fₛ\n(e.g., M=512,\nFₛ=44100 ->\nT ≈ 11.6 ms).",
        fc="#f9fafb",
        ec="#6b7280",
        fs=8.2,
    )

    # shared notes and separators
    fig.suptitle("Offline Batch vs. Real-Time Streaming Audio Processing", fontsize=14, fontweight="bold", y=0.985)
    fig.add_artist(Line2D([0.06, 0.97], [0.505, 0.505], transform=fig.transFigure, color="#d1d5db", linewidth=0.8))

    out_dir = Path(__file__).resolve().parent.parent / "chapters" / "2"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_pdf = out_dir / "offline_vs_realtime_streaming.pdf"
    fig.savefig(out_pdf, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {out_pdf}")


if __name__ == "__main__":
    main()
