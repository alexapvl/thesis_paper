from pathlib import Path
import sys

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from figures.python.components import directed_edge, rounded_box
from figures.python.io import output_pdf_path, save_pdf
from figures.python.palette import color
from figures.python.style import apply_style, apply_suptitle, get_figsize


def stage(ax, center, size, title, subtitle, fill_token, edge_token):
    rounded_box(
        ax,
        center,
        size,
        subtitle,
        box_overrides={
            "boxstyle": "round,pad=0.012,rounding_size=0.02",
            "facecolor": color(fill_token),
            "edgecolor": color(edge_token),
            "linewidth": 1.0,
        },
        text_overrides={"fontsize": 8.1},
    )
    ax.text(
        center[0],
        center[1] + size[1] * 0.34,
        title,
        ha="center",
        va="center",
        fontsize=8.6,
        fontweight="bold",
        color=color("text_primary"),
    )


def main() -> None:
    apply_style()
    fig, ax = plt.subplots(figsize=get_figsize(override=(15.0, 5.2)))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    y = 0.57
    w, h = 0.15, 0.26
    x_positions = [0.095, 0.29, 0.485, 0.68, 0.875]

    stage(
        ax,
        (x_positions[0], y),
        (w, h),
        "Stage 1",
        "Audio Input\nMicrophone or File\n(in browser)",
        "audio_fill",
        "audio_edge",
    )
    stage(
        ax,
        (x_positions[1], y),
        (w, h),
        "Stage 2",
        "Web Audio Processing\nPlayback + Analysis\n+ AudioWorklet",
        "audio_fill",
        "audio_edge",
    )
    stage(
        ax,
        (x_positions[2], y),
        (w, h),
        "Stage 3",
        "WebSocket Transport\nUpstream raw PCM\nDownstream controls",
        "ws_fill",
        "ws_edge",
    )
    stage(
        ax,
        (x_positions[3], y),
        (w, h),
        "Stage 4",
        "Backend Inference\nBeat Tracker +\nSkip-BART (Python)",
        "ws_fill",
        "ws_edge",
    )
    stage(
        ax,
        (x_positions[4], y),
        (w, h),
        "Stage 5",
        "State + Rendering\nZustand + React UI\n+ R3F scene updates",
        "render_fill",
        "render_edge",
    )

    # Forward flow (centerline for 1->2 and 3->4 only)
    directed_edge(
        ax,
        (x_positions[0] + w / 2, y),
        (x_positions[1] - w / 2, y),
        arrow_overrides={"color": color("stroke_default"), "linewidth": 1.25},
    )
    directed_edge(
        ax,
        (x_positions[2] + w / 2, y),
        (x_positions[3] - w / 2, y),
        arrow_overrides={"color": color("stroke_default"), "linewidth": 1.25},
    )

    # Labels for key payloads
    directed_edge(
        ax,
        (x_positions[1], 0.73),
        (x_positions[2], 0.73),
        label="raw PCM chunks",
        label_offset=(0.0, 0.05),
        arrow_overrides={"color": color("audio_edge"), "linewidth": 1.1, "connectionstyle": "arc3,rad=-0.12"},
        label_overrides={"fontsize": 7.7, "color": color("audio_edge")},
    )
    directed_edge(
        ax,
        (x_positions[3], 0.73),
        (x_positions[4], 0.73),
        label="beat + lighting parameters",
        label_offset=(0.0, 0.05),
        arrow_overrides={"color": color("ws_edge"), "linewidth": 1.1, "connectionstyle": "arc3,rad=-0.12"},
        label_overrides={"fontsize": 7.7, "color": color("ws_edge")},
    )

    # Loop-back control relation
    directed_edge(
        ax,
        (x_positions[4], 0.37),
        (x_positions[1], 0.37),
        label="user controls influence playback/rendering context",
        label_offset=(0.0, -0.045),
        arrow_overrides={"color": color("store_edge"), "linewidth": 1.0, "connectionstyle": "arc3,rad=-0.12"},
        label_overrides={"fontsize": 7.5, "color": color("store_edge")},
    )

    ax.text(0.5, 0.18, "Single continuous real-time pipeline from audio capture to scene update", ha="center", va="center", fontsize=8.2, color=color("text_muted"))

    apply_suptitle(fig, "End-to-End Runtime Pipeline")

    out_pdf = output_pdf_path(__file__, chapter=4)
    save_pdf(fig, out_pdf)
    print(f"Saved {out_pdf}")


if __name__ == "__main__":
    main()
