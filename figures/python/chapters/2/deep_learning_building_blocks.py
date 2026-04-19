from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, Rectangle

ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from figures.python.io import output_pdf_path, save_pdf
from figures.python.style import apply_style


def draw_cnn(ax):
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)

    # Input spectrogram-like tile
    t = np.linspace(0, 1, 80)
    f = np.linspace(0, 1, 56)
    T, F = np.meshgrid(t, f)
    spec = (
        0.6 * np.exp(-((F - (0.30 + 0.08 * np.sin(2 * np.pi * T))) ** 2) / 0.015)
        + 0.5 * np.exp(-((F - (0.62 + 0.06 * np.cos(2 * np.pi * 0.8 * T))) ** 2) / 0.02)
    )
    ax.imshow(spec, extent=[0.04, 0.36, 0.18, 0.84], cmap="magma", origin="lower", aspect="auto")
    ax.text(0.20, 0.08, "Log-mel\nspectrogram", ha="center", va="center", fontsize=7)

    ax.annotate("", xy=(0.46, 0.51), xytext=(0.37, 0.51),
                arrowprops=dict(arrowstyle="->", lw=1.0, color="#0f172a"))

    # Conv/Pool feature map stack
    for i, x in enumerate([0.50, 0.61, 0.71]):
        w = 0.11 if i < 2 else 0.09
        h = 0.50 - i * 0.07
        y = 0.26 + i * 0.035
        rect = Rectangle((x, y), w, h, facecolor="#dbeafe", edgecolor="#1d4ed8", linewidth=0.85)
        ax.add_patch(rect)
    ax.text(0.66, 0.12, "Conv\n+ Pool", ha="center", va="center", fontsize=7)

    ax.annotate("", xy=(0.87, 0.51), xytext=(0.81, 0.51),
                arrowprops=dict(arrowstyle="->", lw=1.0, color="#0f172a"))
    emb = Rectangle((0.88, 0.40), 0.08, 0.22, facecolor="#d1fae5", edgecolor="#059669", linewidth=0.9)
    ax.add_patch(emb)
    ax.text(0.92, 0.34, "Feature\nembedding", ha="center", va="top", fontsize=6.7)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)


def draw_rnn(ax):
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)

    xs = np.linspace(0.12, 0.88, 5)
    y = 0.50

    # Inputs
    for i, x in enumerate(xs):
        inp = Rectangle((x - 0.04, 0.78), 0.08, 0.10, facecolor="#fef3c7", edgecolor="#d97706", linewidth=0.8)
        ax.add_patch(inp)
        ax.text(x, 0.83, f"x{i+1}", ha="center", va="center", fontsize=6.7)
        ax.annotate("", xy=(x, y + 0.09), xytext=(x, 0.78),
                    arrowprops=dict(arrowstyle="->", lw=0.9, color="#334155"))

    for i, x in enumerate(xs):
        c = plt.Circle((x, y), 0.09, facecolor="#e0f2fe", edgecolor="#0284c7", linewidth=1.0)
        ax.add_patch(c)
        ax.text(x, y, f"h{i+1}", ha="center", va="center", fontsize=6.8)
        if i < len(xs) - 1:
            # Left-to-right recurrent flow.
            ax.annotate(
                "",
                xy=(xs[i + 1] - 0.085, y),
                xytext=(x + 0.085, y),
                arrowprops=dict(arrowstyle="-|>", lw=1.0, color="#0f172a"),
            )

    # Output probabilities
    for i, x in enumerate(xs):
        out = Rectangle((x - 0.04, 0.12), 0.08, 0.10, facecolor="#dcfce7", edgecolor="#16a34a", linewidth=0.8)
        ax.add_patch(out)
        ax.text(x, 0.17, f"y{i+1}", ha="center", va="center", fontsize=6.7)
        ax.annotate("", xy=(x, 0.22), xytext=(x, y - 0.09),
                    arrowprops=dict(arrowstyle="->", lw=0.9, color="#334155"))
    ax.text(0.5, 0.05, "Unrolled LSTM over time steps", ha="center", va="center", fontsize=7.2)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)


def draw_crnn(ax):
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)

    # CNN front-end stack
    for i, x in enumerate([0.06, 0.15, 0.24]):
        rect = Rectangle((x, 0.24 + i * 0.03), 0.10, 0.48 - i * 0.07,
                         facecolor="#dcfce7", edgecolor="#16a34a", linewidth=0.85)
        ax.add_patch(rect)
    ax.text(0.20, 0.12, "CNN front-end", ha="center", va="center", fontsize=7.0)

    # Flatten to temporal sequence
    seq = Rectangle((0.39, 0.40), 0.12, 0.22, facecolor="#fef3c7", edgecolor="#d97706", linewidth=0.85)
    ax.add_patch(seq)
    ax.text(0.45, 0.51, "T x F", ha="center", va="center", fontsize=7)
    ax.text(0.45, 0.33, "reshape", ha="center", va="center", fontsize=6.5)
    # Keep CNN -> reshape and reshape -> RNN as separate, non-overlapping links.
    ax.annotate(
        "",
        xy=(0.39, 0.56),
        xytext=(0.34, 0.56),
        arrowprops=dict(arrowstyle="-|>", lw=1.0, color="#0f172a"),
    )
    ax.annotate(
        "",
        xy=(0.55, 0.50),
        xytext=(0.51, 0.50),
        arrowprops=dict(arrowstyle="-|>", lw=1.0, color="#0f172a"),
    )

    # BiLSTM/GRU back-end (right)
    xs = np.linspace(0.62, 0.92, 3)
    for i, x in enumerate(xs):
        c = plt.Circle((x, 0.52), 0.07, facecolor="#e0f2fe", edgecolor="#0284c7", linewidth=1.0)
        ax.add_patch(c)
        ax.text(x, 0.52, f"h{i+1}", ha="center", va="center", fontsize=6.8)
        if i < len(xs) - 1:
            ax.annotate(
                "",
                xy=(xs[i + 1] - 0.065, 0.52),
                xytext=(x + 0.065, 0.52),
                arrowprops=dict(arrowstyle="-|>", lw=1.0, color="#0f172a"),
            )
    ax.text(0.78, 0.12, "RNN back-end", ha="center", va="center", fontsize=7.0)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)


def draw_transformer(ax):
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)

    # Pre-norm transformer block representation
    ln1 = Rectangle((0.10, 0.72), 0.80, 0.09, facecolor="#e2e8f0", edgecolor="#64748b", linewidth=0.85)
    mha = Rectangle((0.10, 0.58), 0.80, 0.10, facecolor="#ede9fe", edgecolor="#7c3aed", linewidth=0.95)
    add1 = Rectangle((0.10, 0.46), 0.80, 0.08, facecolor="#f8fafc", edgecolor="#334155", linewidth=0.8)
    ln2 = Rectangle((0.10, 0.33), 0.80, 0.09, facecolor="#e2e8f0", edgecolor="#64748b", linewidth=0.85)
    ffn = Rectangle((0.10, 0.19), 0.80, 0.10, facecolor="#fee2e2", edgecolor="#dc2626", linewidth=0.95)
    add2 = Rectangle((0.10, 0.07), 0.80, 0.08, facecolor="#f8fafc", edgecolor="#334155", linewidth=0.8)
    for p in [ln1, mha, add1, ln2, ffn, add2]:
        ax.add_patch(p)

    ax.text(0.50, 0.765, "LayerNorm", ha="center", va="center", fontsize=7)
    ax.text(0.50, 0.63, "Multi-Head Self-Attention", ha="center", va="center", fontsize=7)
    ax.text(0.50, 0.50, "Add + Residual", ha="center", va="center", fontsize=7)
    ax.text(0.50, 0.375, "LayerNorm", ha="center", va="center", fontsize=7)
    ax.text(0.50, 0.24, "Position-wise Feed-Forward", ha="center", va="center", fontsize=7)
    ax.text(0.50, 0.11, "Add + Residual", ha="center", va="center", fontsize=7)

    # Vertical flow arrows
    for y1, y2 in [(0.72, 0.68), (0.58, 0.54), (0.46, 0.42), (0.33, 0.29), (0.19, 0.15)]:
        ax.annotate("", xy=(0.50, y2), xytext=(0.50, y1),
                    arrowprops=dict(arrowstyle="->", lw=0.85, color="#334155"))
    ax.text(0.50, 0.01, "Encoder block (pre-norm)", ha="center", va="bottom", fontsize=7.0)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)


def main() -> None:
    apply_style()
    fig = plt.figure(figsize=(15.0, 5.2))
    gs = fig.add_gridspec(1, 4, left=0.03, right=0.97, bottom=0.14, top=0.82, wspace=0.20)

    panels = [
        ("(1) CNN", draw_cnn, "#eff6ff"),
        ("(2) RNN / LSTM", draw_rnn, "#f0f9ff"),
        ("(3) CRNN", draw_crnn, "#f0fdf4"),
        ("(4) Transformer", draw_transformer, "#faf5ff"),
    ]

    axes = []
    for i, (title, drawer, bg) in enumerate(panels):
        ax = fig.add_subplot(gs[0, i])
        ax.set_facecolor(bg)
        for spine in ax.spines.values():
            spine.set_color("#475569")
            spine.set_linewidth(0.95)
        drawer(ax)
        ax.set_title(title, fontsize=10, fontweight="bold", pad=10)
        axes.append(ax)

    # Flow arrows showing increasing architectural complexity
    for i in range(len(axes) - 1):
        left = axes[i].get_position()
        right = axes[i + 1].get_position()
        start = (left.x1 + 0.008, (left.y0 + left.y1) / 2)
        end = (right.x0 - 0.008, (right.y0 + right.y1) / 2)
        fig.add_artist(
            FancyArrowPatch(
                start,
                end,
                transform=fig.transFigure,
                arrowstyle="-|>",
                mutation_scale=14,
                linewidth=1.2,
                color="#334155",
            )
        )

    fig.suptitle("Deep Learning Building Blocks for Audio Analysis", fontsize=14, fontweight="bold", y=0.93)

    out_pdf = output_pdf_path(__file__, chapter=2)
    save_pdf(fig, out_pdf)
    print(f"Saved {out_pdf}")


if __name__ == "__main__":
    main()
