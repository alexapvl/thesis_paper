from pathlib import Path
import sys

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from figures.python.io import output_pdf_path, save_pdf
from figures.python.style import apply_style


def main() -> None:
    apply_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), gridspec_kw={"wspace": 0.20})
    fig.patch.set_facecolor("white")

    # ---------------- Panel A: Shared emotional space (schematic MDS) ----------------
    ax1.set_title("Shared Emotional Space (MDS)", fontsize=11, fontweight="bold", pad=10)
    ax1.set_xlim(-1.5, 1.5)
    ax1.set_ylim(-1.5, 1.5)
    ax1.set_xticks([-1.5, -0.75, 0, 0.75, 1.5])
    ax1.set_yticks([-1.5, -0.75, 0, 0.75, 1.5])
    ax1.grid(True, color="#d1d5db", alpha=0.3, linewidth=0.7)
    ax1.axhline(0, color="#9ca3af", linewidth=0.8)
    ax1.axvline(0, color="#9ca3af", linewidth=0.8)

    ax1.text(-1.48, -1.68, "Sad", ha="left", va="top", fontsize=9, fontweight="bold", fontstyle="italic")
    ax1.text(1.48, -1.68, "Happy", ha="right", va="top", fontsize=9, fontweight="bold", fontstyle="italic")
    ax1.text(-1.85, -1.48, "Weak", ha="right", va="bottom", fontsize=9, rotation=90, fontweight="bold", fontstyle="italic")
    ax1.text(-1.85, 1.48, "Strong", ha="right", va="top", fontsize=9, rotation=90, fontweight="bold", fontstyle="italic")
    ax1.set_xlabel("Dimension 1: Valence", fontweight="bold")
    ax1.set_ylabel("Dimension 2: Potency", fontweight="bold")

    # Colour stimuli (schematic clusters)
    colour_points = [
        ("#facc15", 1.10, 1.15),  # vivid yellow
        ("#f97316", 0.95, 1.00),  # saturated orange
        ("#fb923c", 0.78, 0.85),  # warm orange
        ("#fef08a", 0.40, 0.65),  # light yellow pastel
        ("#fde68a", 0.20, 0.52),  # pastel yellow
        ("#93c5fd", 0.10, 0.40),  # light pastel blue
        ("#1f2937", -1.10, -1.15),  # dark grey
        ("#334155", -0.95, -1.00),  # blue-grey
        ("#1e3a8a", -1.00, -0.85),  # dark navy blue
        ("#475569", -0.75, -0.95),  # muted dark grey-blue
        ("#7f1d1d", 0.65, -0.82),  # dark red (sad but strong)
    ]
    for hex_color, x, y in colour_points:
        ax1.scatter(x, y, s=95, marker="o", color=hex_color, edgecolor="#111827", linewidth=0.5, zorder=3)

    # 18 musical selections: tempo(shape) + mode(fill) + composer(edge color)
    tempo_shape = {"slow": "o", "medium": "s", "fast": "^"}
    mode_filled = {"major": True, "minor": False}
    composer_edge = {"Bach": "#111827", "Mozart": "#4b5563", "Brahms": "#9ca3af"}

    base_pos = {
        ("fast", "major"): (1.0, 0.95),
        ("fast", "minor"): (0.55, 0.35),
        ("medium", "major"): (0.40, 0.45),
        ("medium", "minor"): (-0.15, -0.10),
        ("slow", "major"): (-0.10, 0.15),
        ("slow", "minor"): (-0.95, -1.00),
    }
    composer_offsets = {"Bach": (-0.09, 0.04), "Mozart": (0.00, -0.04), "Brahms": (0.09, 0.03)}

    for tempo in ["slow", "medium", "fast"]:
        for mode in ["major", "minor"]:
            bx, by = base_pos[(tempo, mode)]
            for comp in ["Bach", "Mozart", "Brahms"]:
                ox, oy = composer_offsets[comp]
                x, y = bx + ox, by + oy
                face = "#111827" if mode_filled[mode] else "white"
                ax1.scatter(
                    x,
                    y,
                    s=60,
                    marker=tempo_shape[tempo],
                    facecolor=face,
                    edgecolor=composer_edge[comp],
                    linewidth=1.0,
                    zorder=4,
                )

    corr_text = (
        "Emotion-colour correlations:\n"
        "happy/sad r = .97\n"
        "lively/dreary r = .99\n"
        "strong/weak r = .96\n"
        "angry/calm r = .89"
    )
    ax1.text(
        -1.42,
        1.35,
        corr_text,
        ha="left",
        va="top",
        fontsize=7.6,
        bbox=dict(boxstyle="round,pad=0.28", facecolor="white", edgecolor="#9ca3af", alpha=0.95),
    )

    legend_tempo_mode = [
        Line2D([0], [0], marker="o", color="none", markerfacecolor="#111827", markeredgecolor="#111827", markersize=6, label="Slow major"),
        Line2D([0], [0], marker="o", color="none", markerfacecolor="white", markeredgecolor="#111827", markersize=6, label="Slow minor"),
        Line2D([0], [0], marker="s", color="none", markerfacecolor="#111827", markeredgecolor="#111827", markersize=6, label="Medium major"),
        Line2D([0], [0], marker="s", color="none", markerfacecolor="white", markeredgecolor="#111827", markersize=6, label="Medium minor"),
        Line2D([0], [0], marker="^", color="none", markerfacecolor="#111827", markeredgecolor="#111827", markersize=6, label="Fast major"),
        Line2D([0], [0], marker="^", color="none", markerfacecolor="white", markeredgecolor="#111827", markersize=6, label="Fast minor"),
    ]
    lg1 = ax1.legend(handles=legend_tempo_mode, loc="lower right", fontsize=6.8, frameon=True, framealpha=0.95, title="Music (tempo/mode)")
    lg1.get_title().set_fontsize(7)
    ax1.add_artist(lg1)

    legend_composer = [
        Line2D([0], [0], marker="o", color="none", markerfacecolor="white", markeredgecolor="#111827", markersize=6, label="Bach edge"),
        Line2D([0], [0], marker="o", color="none", markerfacecolor="white", markeredgecolor="#4b5563", markersize=6, label="Mozart edge"),
        Line2D([0], [0], marker="o", color="none", markerfacecolor="white", markeredgecolor="#9ca3af", markersize=6, label="Brahms edge"),
    ]
    lg2 = ax1.legend(handles=legend_composer, loc="lower left", fontsize=6.8, frameon=True, framealpha=0.95, title="Composer (optional)")
    lg2.get_title().set_fontsize(7)

    ax1.text(-1.47, 1.47, "(A)", fontsize=12, fontweight="bold", ha="left", va="top")

    # ---------------- Panel B: Example mappings ----------------
    ax2.set_title("Example Music-Colour Mappings", fontsize=11, fontweight="bold", pad=10)
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.axis("off")

    y_top = 0.72
    y_bot = 0.32

    ax2.text(0.07, y_top, "Fast / Major", ha="left", va="center", fontsize=11, fontweight="bold", color="#b45309")
    ax2.text(0.07, y_bot, "Slow / Minor", ha="left", va="center", fontsize=11, fontweight="bold", color="#334155")
    ax2.annotate("", xy=(0.45, y_top), xytext=(0.33, y_top), arrowprops=dict(arrowstyle="-|>", lw=1.3, color="#6b7280"))
    ax2.annotate("", xy=(0.45, y_bot), xytext=(0.33, y_bot), arrowprops=dict(arrowstyle="-|>", lw=1.3, color="#6b7280"))

    warm = ["#facc15", "#f97316", "#84cc16", "#fef08a", "#ea580c"]
    cool = ["#334155", "#64748b", "#1f2937", "#1e3a8a", "#475569"]

    sw_w, sw_h, sw_gap = 0.085, 0.10, 0.018
    x_start = 0.47
    for i, c in enumerate(warm):
        ax2.add_patch(Rectangle((x_start + i * (sw_w + sw_gap), y_top - sw_h / 2), sw_w, sw_h, facecolor=c, edgecolor="#111827", linewidth=0.6))
    for i, c in enumerate(cool):
        ax2.add_patch(Rectangle((x_start + i * (sw_w + sw_gap), y_bot - sw_h / 2), sw_w, sw_h, facecolor=c, edgecolor="#111827", linewidth=0.6))

    ax2.text(0.70, y_top - 0.10, "Saturated · Light · Warm", ha="center", va="top", fontsize=8.4, color="#7c2d12")
    ax2.text(0.70, y_bot - 0.10, "Desaturated · Dark · Cool", ha="center", va="top", fontsize=8.4, color="#1f2937")
    ax2.text(0.40, 0.52, "↕ emotional contrast", ha="center", va="center", fontsize=8, color="#6b7280", rotation=90)

    ax2.text(0.01, 0.98, "(B)", fontsize=12, fontweight="bold", ha="left", va="top")

    # Shared title + subcaption
    fig.suptitle("Music-Colour Associations Mediated by Emotion", fontsize=14, fontweight="bold", y=0.985)
    fig.text(
        0.5,
        0.00,
        "Adapted from Palmer et al. (2013). PNAS, 110(22), 8836-8841. "
        "MDS positions are schematic approximations consistent with reported findings.",
        ha="center",
        va="bottom",
        fontsize=8,
        color="#6b7280",
    )

    out_pdf = output_pdf_path(__file__, chapter=2)
    save_pdf(fig, out_pdf)
    print(f"Saved {out_pdf}")


if __name__ == "__main__":
    main()
