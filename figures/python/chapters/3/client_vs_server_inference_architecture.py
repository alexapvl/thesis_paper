from pathlib import Path
import sys

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from figures.python.components import directed_edge, panel, rounded_box
from figures.python.io import output_pdf_path, save_pdf
from figures.python.palette import color
from figures.python.style import apply_style, apply_suptitle, get_figsize


def main() -> None:
    apply_style()
    fig, ax = plt.subplots(figsize=get_figsize(override=(14.4, 7.2)))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # Left panel: client-side
    panel(ax, 0.05, 0.12, 0.4, 0.72, "Client-Side")
    rounded_box(
        ax,
        (0.17, 0.725),
        (0.10, 0.09),
        "Web Audio API",
        box_overrides={"boxstyle": "round,pad=0.015,rounding_size=0.015", "facecolor": color("audio_fill"), "edgecolor": color("audio_edge"), "linewidth": 0.9},
        text_overrides={"fontsize": 8.4, "fontweight": "bold", "color": color("text_primary")},
    )
    rounded_box(
        ax,
        (0.345, 0.725),
        (0.10, 0.09),
        "Three.js",
        box_overrides={"boxstyle": "round,pad=0.015,rounding_size=0.015", "facecolor": color("audio_fill"), "edgecolor": color("audio_edge"), "linewidth": 0.9},
        text_overrides={"fontsize": 8.4, "fontweight": "bold", "color": color("text_primary")},
    )
    rounded_box(
        ax,
        (0.25, 0.57),
        (0.25, 0.1),
        "ONNX.js / TF.js inference\n(Beat + Skip-BART)",
        box_overrides={"boxstyle": "round,pad=0.015,rounding_size=0.015", "facecolor": color("danger_fill"), "edgecolor": color("danger_edge"), "linewidth": 0.9},
        text_overrides={"fontsize": 8.4, "color": color("text_primary")},
    )
    rounded_box(
        ax,
        (0.25, 0.40),
        (0.25, 0.1),
        "Post-processing in browser\n(DBN / particle filters / RSTC)",
        box_overrides={"boxstyle": "round,pad=0.015,rounding_size=0.015", "facecolor": color("danger_fill"), "edgecolor": color("danger_edge"), "linewidth": 0.9},
        text_overrides={"fontsize": 8.4, "color": color("text_primary")},
    )

    directed_edge(ax, (0.17, 0.68), (0.20, 0.635))
    directed_edge(ax, (0.25, 0.52), (0.25, 0.465))
    directed_edge(
        ax,
        (0.39, 0.42),
        (0.41, 0.75),
        label="lighting params",
        label_offset=(0.040, 0.012),
        arrow_overrides={"color": color("stroke_default"), "connectionstyle": "arc3,rad=0.5"},
        label_overrides={"fontsize": 7.8, "color": color("stroke_default")},
    )

    ax.text(
        0.25,
        0.2,
        "Limitations: memory constraints (240M params),\nno CUDA, conversion required,\npost-processing rewrite needed",
        ha="center",
        va="center",
        fontsize=7.8,
        color=color("text_muted"),
        bbox=dict(boxstyle="round,pad=0.22", fc="#fee2e2", ec="#b91c1c", lw=0.8),
    )

    # Right panel: hybrid (chosen)
    panel(ax, 0.55, 0.12, 0.4, 0.72, "Hybrid (Chosen)")
    panel(
        ax,
        0.58,
        0.53,
        0.34,
        0.27,
        "Browser",
        box_overrides={
            "facecolor": "#eff6ff",
            "edgecolor": color("audio_edge"),
            "linewidth": 1.0,
            "boxstyle": "round,pad=0.02,rounding_size=0.015",
        },
        title_overrides={"fontsize": 8.6, "color": color("audio_edge")},
    )
    rounded_box(
        ax,
        (0.675, 0.73),
        (0.1, 0.08),
        "Web Audio API",
        box_overrides={"boxstyle": "round,pad=0.015,rounding_size=0.015", "facecolor": color("audio_fill"), "edgecolor": color("audio_edge"), "linewidth": 0.9},
        text_overrides={"fontsize": 8.4, "color": color("text_primary")},
    )
    rounded_box(
        ax,
        (0.825, 0.73),
        (0.12, 0.08),
        "React + Three.js",
        box_overrides={"boxstyle": "round,pad=0.015,rounding_size=0.015", "facecolor": color("audio_fill"), "edgecolor": color("audio_edge"), "linewidth": 0.9},
        text_overrides={"fontsize": 8.4, "color": color("text_primary")},
    )
    rounded_box(
        ax,
        (0.755, 0.60),
        (0.14, 0.08),
        "Zustand Store",
        box_overrides={"boxstyle": "round,pad=0.015,rounding_size=0.015", "facecolor": color("audio_fill"), "edgecolor": color("audio_edge"), "linewidth": 0.9},
        text_overrides={"fontsize": 8.4, "color": color("text_primary")},
    )

    panel(
        ax,
        0.58,
        0.24,
        0.34,
        0.20,
        "Python Server",
        box_overrides={
            "facecolor": "#f0fdf4",
            "edgecolor": color("ws_edge"),
            "linewidth": 1.0,
            "boxstyle": "round,pad=0.02,rounding_size=0.015",
        },
        title_overrides={"fontsize": 8.6, "color": color("ws_edge")},
    )
    rounded_box(
        ax,
        (0.65, 0.305),
        (0.08, 0.09),
        "PyTorch\nBeat Tracker",
        box_overrides={"boxstyle": "round,pad=0.015,rounding_size=0.015", "facecolor": color("ws_fill"), "edgecolor": color("ws_edge"), "linewidth": 0.9},
        text_overrides={"fontsize": 8.4, "color": color("text_primary")},
    )
    rounded_box(
        ax,
        (0.85, 0.305),
        (0.08, 0.09),
        "PyTorch\nSkip-BART",
        box_overrides={"boxstyle": "round,pad=0.015,rounding_size=0.015", "facecolor": color("ws_fill"), "edgecolor": color("ws_edge"), "linewidth": 0.9},
        text_overrides={"fontsize": 8.4, "color": color("text_primary")},
    )

    directed_edge(
        ax,
        (0.7, 0.56),
        (0.667, 0.365),
        label="audio chunks (upstream)",
        label_offset=(-0.01, -0.03),
        arrow_overrides={"color": color("ws_edge")},
        label_overrides={"fontsize": 7.8, "color": color("ws_edge")},
    )
    directed_edge(
        ax,
        (0.84, 0.35),
        (0.80, 0.545),
        label="beat + hue/value (downstream)",
        label_offset=(0.003, -0.055),
        arrow_overrides={"color": color("ws_edge")},
        label_overrides={"fontsize": 7.8, "color": color("ws_edge")},
    )
    directed_edge(
        ax,
        (0.71, 0.305),
        (0.79, 0.305),
        label="WebSocket",
        label_offset=(0.0, 0.025),
        arrow_overrides={"color": color("ws_edge"), "linewidth": 1.1},
        label_overrides={"fontsize": 7.8, "color": color("ws_edge")},
    )
    

    ax.text(
        0.75,
        0.145,
        "Advantages: native PyTorch, CUDA GPU,\noriginal model weights, no conversion",
        ha="center",
        va="center",
        fontsize=7.8,
        color=color("text_muted"),
        bbox=dict(boxstyle="round,pad=0.22", fc="#ecfdf5", ec="#86efac", lw=0.8),
    )

    apply_suptitle(fig, "Client-Side vs. Server-Side Inference Architecture")

    out_pdf = output_pdf_path(__file__, chapter=3)
    save_pdf(fig, out_pdf)
    print(f"Saved {out_pdf}")


if __name__ == "__main__":
    main()
