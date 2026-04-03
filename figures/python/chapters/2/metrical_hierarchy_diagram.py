import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path


# Global style aligned with existing Python-generated figures
plt.rcParams.update(
    {
        "font.family": "serif",
        "font.size": 10,
        "axes.linewidth": 0.6,
        "xtick.major.width": 0.5,
        "ytick.major.width": 0.5,
    }
)


def main() -> None:
    fig, ax = plt.subplots(figsize=(11.5, 4.3))

    # Timeline spans four bars of 4/4 time.
    x_start, x_end = 0.0, 4.0
    row_y = {
        "phrase": 3.2,
        "downbeats": 2.35,
        "beats": 1.5,
        "subbeats": 0.65,
    }

    # Draw row baselines
    for y in row_y.values():
        ax.hlines(y, x_start, x_end, color="#9099a1", linewidth=0.8, zorder=1)

    # Phrase boundary: one 4-bar span
    phrase_h = 0.26
    phrase_rect = plt.Rectangle(
        (x_start, row_y["phrase"] - phrase_h / 2),
        x_end - x_start,
        phrase_h,
        facecolor="#d8ecff",
        edgecolor="#356a9a",
        linewidth=1.0,
        zorder=2,
    )
    ax.add_patch(phrase_rect)
    ax.text(
        2.0,
        row_y["phrase"],
        "4-bar phrase",
        ha="center",
        va="center",
        fontsize=9,
        fontweight="bold",
        color="#1f4e79",
        zorder=3,
    )

    # Downbeats at bar starts (plus end marker)
    downbeat_pos = np.arange(0, 5, 1)
    for i, x in enumerate(downbeat_pos):
        ax.vlines(
            x,
            row_y["downbeats"] - 0.22,
            row_y["downbeats"] + 0.22,
            color="#2563eb",
            linewidth=2.2 if i in (0, 4) else 1.8,
            zorder=3,
        )
        if i < 4:
            ax.text(
                x + 0.02,
                row_y["downbeats"] + 0.28,
                f"Bar {i + 1}",
                fontsize=8,
                color="#1e40af",
            )

    # Beats: quarter-note pulses (16 beats in 4 bars)
    beat_pos = np.arange(0, 4, 0.25)
    ax.scatter(
        beat_pos,
        np.full_like(beat_pos, row_y["beats"]),
        s=28,
        color="#0f766e",
        edgecolors="white",
        linewidths=0.5,
        zorder=4,
    )

    # Sub-beats: eighth-note divisions (32 positions)
    subbeat_pos = np.arange(0, 4.0001, 0.125)
    for x in subbeat_pos:
        ax.vlines(
            x,
            row_y["subbeats"] - 0.08,
            row_y["subbeats"] + 0.08,
            color="#a16207",
            linewidth=0.9,
            zorder=3,
        )

    # Highlight each bar region lightly to improve readability
    for i in range(4):
        if i % 2 == 0:
            ax.axvspan(i, i + 1, color="#f8fafc", zorder=0)

    # Hierarchy guides connecting levels at each bar boundary
    for x in downbeat_pos:
        ax.plot(
            [x, x],
            [row_y["phrase"] - 0.13, row_y["subbeats"] + 0.08],
            linestyle="--",
            linewidth=0.6,
            color="#9ca3af",
            alpha=0.8,
            zorder=1,
        )

    # Level labels
    ax.text(-0.18, row_y["phrase"], "Phrase level", ha="right", va="center", fontweight="bold")
    ax.text(-0.18, row_y["downbeats"], "Downbeats\n(bar lines)", ha="right", va="center", fontweight="bold")
    ax.text(-0.18, row_y["beats"], "Beats\n(quarter notes)", ha="right", va="center", fontweight="bold")
    ax.text(-0.18, row_y["subbeats"], "Sub-beats\n(eighth notes)", ha="right", va="center", fontweight="bold")

    # Beat numbers for first bar as reference
    for n, x in enumerate(np.arange(0, 1, 0.25), start=1):
        ax.text(x + 0.125, row_y["beats"] - 0.24, str(n), ha="center", va="center", fontsize=8, color="#065f46")

    ax.set_title(
        "Metrical Hierarchy in a Four-Bar Excerpt (4/4)",
        fontsize=11,
        fontweight="bold",
        pad=10,
    )
    ax.set_xlim(-0.55, 4.05)
    ax.set_ylim(0.2, 3.65)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    fig.tight_layout()

    out_dir = Path(__file__).resolve().parent.parent / "chapters" / "2"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_pdf = out_dir / "metrical_hierarchy_diagram.pdf"
    fig.savefig(out_pdf, dpi=300, bbox_inches="tight")
    fig.savefig(out_png, dpi=300, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved {out_pdf}")


if __name__ == "__main__":
    main()
