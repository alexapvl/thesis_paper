from pathlib import Path
import sys

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from figures.python.components import directed_edge, flow_node, panel
from figures.python.io import output_pdf_path, save_pdf
from figures.python.palette import color
from figures.python.style import apply_style, apply_suptitle, get_figsize


def main() -> None:
    apply_style()
    fig, ax = plt.subplots(figsize=get_figsize(override=(14.4, 7.6)))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # Major panels
    panel(
        ax,
        0.06,
        0.14,
        0.54,
        0.70,
        "Browser Client",
        box_overrides={"facecolor": "#eff6ff", "edgecolor": color("audio_edge"), "linewidth": 1.1},
        title_overrides={"color": color("audio_edge")},
    )
    panel(
        ax,
        0.68,
        0.14,
        0.25,
        0.70,
        "Python Inference Server",
        box_overrides={"facecolor": "#f0fdf4", "edgecolor": color("ws_edge"), "linewidth": 1.1},
        title_overrides={"color": color("ws_edge")},
    )

    # Browser module nodes
    flow_node(ax, (0.13, 0.72), (0.13, 0.10), "Audio Input\n(Microphone/File)", fill_token="audio_fill", edge_token="audio_edge", bold=True, pad=0.01)
    flow_node(ax, (0.32, 0.72), (0.13, 0.10), "Web Audio API", fill_token="audio_fill", edge_token="audio_edge", bold=True, pad=0.01)
    flow_node(ax, (0.52, 0.72), (0.13, 0.10), "WebSocket\nClient", fill_token="ws_fill", edge_token="ws_edge", bold=True, pad=0.01)

    flow_node(ax, (0.13, 0.46), (0.13, 0.10), "React UI", fill_token="render_fill", edge_token="render_edge", pad=0.01)
    flow_node(ax, (0.32, 0.46), (0.13, 0.10), "Zustand\nState Layer", fill_token="store_fill", edge_token="store_edge", bold=True, pad=0.01)
    flow_node(ax, (0.52, 0.46), (0.13, 0.10), "R3F + Three.js\nRenderer", fill_token="render_fill", edge_token="render_edge", pad=0.01)

    # Server module nodes
    flow_node(ax, (0.735, 0.7), (0.11, 0.11), "Beat Tracker\n(PyTorch)", fill_token="ws_fill", edge_token="ws_edge", pad=0.01)
    flow_node(ax, (0.875, 0.7), (0.11, 0.11), "Skip-BART\n(PyTorch)", fill_token="ws_fill", edge_token="ws_edge", pad=0.01)
    flow_node(ax, (0.815, 0.38), (0.15, 0.10), "Streaming API\n(FastAPI)", fill_token="ws_fill", edge_token="ws_edge", bold=True, pad=0.01)

    # Browser internal edges
    directed_edge(ax, (0.20, 0.72), (0.245, 0.72), arrow_overrides={"color": color("audio_edge"), "linewidth": 1.2})
    directed_edge(
        ax,
        (0.36, 0.72),
        (0.445, 0.72),
        label="audio chunks",
        label_offset=(0.018, 0.026),
        arrow_overrides={"color": color("ws_edge"), "linewidth": 1.2},
        label_overrides={"fontsize": 5.5, "color": color("ws_edge")},
    )
    directed_edge(ax, (0.32, 0.67), (0.32, 0.52), arrow_overrides={"color": color("store_edge"), "linewidth": 1.2})
    directed_edge(ax, (0.2, 0.46), (0.245, 0.46), arrow_overrides={"color": color("store_edge"), "linewidth": 1.2})
    directed_edge(
        ax,
        (0.39, 0.46),
        (0.445, 0.46),
        label="lighting state",
        label_offset=(0.003, 0.022),
        arrow_overrides={"color": color("render_edge"), "linewidth": 1.2},
        label_overrides={"fontsize": 5.5, "color": color("render_edge")},
    )

    # Server internal edges
    directed_edge(ax, (0.735, 0.65), (0.79, 0.44), arrow_overrides={"color": color("ws_edge"), "linewidth": 1.2})
    directed_edge(ax, (0.875, 0.65), (0.83, 0.44), arrow_overrides={"color": color("ws_edge"), "linewidth": 1.2})

    # Cross-boundary WebSocket edges
    directed_edge(
        ax,
        (0.58, 0.67),
        (0.75, 0.44),
        label="upstream: raw PCM",
        label_offset=(-0.035, 0.07),
        arrow_overrides={"color": color("ws_edge"), "linewidth": 1.3, "connectionstyle": "arc3,rad=-0.12"},
        label_overrides={"fontsize": 7.8, "color": color("ws_edge")},
    )
    directed_edge(
        ax,
        (0.78, 0.33),
        (0.52, 0.66),
        label="downstream:\nbeat/tempo/hue/value",
        label_offset=(-0.15, 0.08),
        arrow_overrides={"color": color("ws_edge"), "linewidth": 1.3, "connectionstyle": "arc3,rad=-0.1"},
        label_overrides={"fontsize": 7.8, "color": color("ws_edge")},
    )
    directed_edge(
        ax,
        (0.52, 0.67),
        (0.34, 0.52),
        label="to shared state",
        label_offset=(-0.03, 0.035),
        arrow_overrides={"color": color("ws_edge"), "linewidth": 1.2, "connectionstyle": "arc3,rad=0.1"},
        label_overrides={"fontsize": 7.5, "color": color("ws_edge")},
    )

    # Boundary marker
    ax.plot([0.64, 0.64], [0.18, 0.86], linestyle="--", color=color("stroke_default"), linewidth=0.9)
    ax.text(0.64, 0.87, "Runtime Boundary", ha="center", va="bottom", fontsize=8, color=color("text_muted"))

    ax.text(
        0.33,
        0.20,
        "Client responsibilities: capture/playback, UI, 3D rendering",
        ha="center",
        va="center",
        fontsize=8,
        color=color("text_muted"),
    )
    ax.text(
        0.815,
        0.20,
        "Server responsibilities: beat tracking,\ngenerative inference",
        ha="center",
        va="center",
        fontsize=8,
        color=color("text_muted"),
    )

    apply_suptitle(fig, "High-Level Hybrid System Architecture")

    out_pdf = output_pdf_path(__file__, chapter=4)
    save_pdf(fig, out_pdf)
    print(f"Saved {out_pdf}")


if __name__ == "__main__":
    main()
