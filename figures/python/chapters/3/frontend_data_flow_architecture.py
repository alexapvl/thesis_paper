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


def node(ax, center, size, text, fill_token, edge_token, bold=False):
    rounded_box(
        ax,
        center,
        size,
        text,
        box_overrides={
            "boxstyle": "round,pad=0.008,rounding_size=0.02",
            "facecolor": color(fill_token),
            "edgecolor": color(edge_token),
            "linewidth": 1.0,
        },
        text_overrides={"fontweight": "bold" if bold else "normal"},
    )


def main() -> None:
    apply_style()
    fig, ax = plt.subplots(figsize=get_figsize(override=(14.6, 8.0)))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # Nodes
    mic = (0.21, 0.85)
    file_in = (0.4, 0.85)
    web_audio = (0.3, 0.7)

    speakers = (0.1, 0.55)
    analyser = (0.3, 0.55)
    worklet = (0.5, 0.55)

    ws_up = (0.74, 0.8)
    ws_down = (0.74, 0.62)
    store = (0.54, 0.40)

    react_ui = (0.32, 0.22)
    r3f_loop = (0.54, 0.22)
    three_scene = (0.79, 0.22)
    py_server = (0.90, 0.71)

    # Draw nodes
    node(ax, mic, (0.16, 0.09), "Microphone\n(getUserMedia)", "audio_fill", "audio_edge", bold=True)
    node(ax, file_in, (0.16, 0.09), "Audio File\n(decodeAudioData)", "audio_fill", "audio_edge", bold=True)
    node(ax, web_audio, (0.20, 0.10), "Web Audio API", "audio_fill", "audio_edge", bold=True)

    node(ax, speakers, (0.18, 0.085), "AudioDestinationNode\n(Speakers)", "audio_fill", "audio_edge")
    node(ax, analyser, (0.18, 0.085), "AnalyserNode", "audio_fill", "audio_edge")
    node(ax, worklet, (0.18, 0.085), "AudioWorkletNode", "audio_fill", "audio_edge")

    node(ax, ws_up, (0.16, 0.085), "WebSocket\n(upstream)", "ws_fill", "ws_edge")
    node(ax, ws_down, (0.16, 0.085), "WebSocket\n(downstream)", "ws_fill", "ws_edge")
    node(ax, py_server, (0.1, 0.105), "Python Server\nBeat + Skip-BART", "ws_fill", "ws_edge", bold=True)

    node(ax, store, (0.2, 0.095), "Zustand Store", "store_fill", "store_edge", bold=True)
    node(ax, react_ui, (0.15, 0.095), "React UI\ncomponents", "render_fill", "render_edge")
    node(ax, r3f_loop, (0.15, 0.095), "R3F useFrame\nloop", "render_fill", "render_edge")
    node(ax, three_scene, (0.15, 0.095), "Three.js Scene\n(SpotLights)", "render_fill", "render_edge")

    # Audio path
    directed_edge(ax, (0.21, 0.805), (0.26, 0.76), arrow_overrides={"color": color("audio_edge"), "linewidth": 1.2})
    directed_edge(ax, (0.40, 0.805), (0.34, 0.76), arrow_overrides={"color": color("audio_edge"), "linewidth": 1.2})
    directed_edge(ax, (0.24, 0.65), (0.13, 0.61), arrow_overrides={"color": color("audio_edge"), "linewidth": 1.2})
    directed_edge(ax, (0.30, 0.65), (0.30, 0.6), arrow_overrides={"color": color("audio_edge"), "linewidth": 1.2})
    directed_edge(ax, (0.36, 0.65), (0.47, 0.61), arrow_overrides={"color": color("audio_edge"), "linewidth": 1.2})

    # Analysis + websocket
    directed_edge(
        ax,
        (0.30, 0.507),
        (0.33, 0.275),
        label="FFT data",
        label_offset=(-0.035, 0.005),
        arrow_overrides={"color": color("audio_edge"), "linewidth": 1.2},
        label_overrides={"fontsize": 7.5, "color": color("audio_edge")},
    )
    directed_edge(
        ax,
        (0.55, 0.58),
        (0.65, 0.80),
        label="raw PCM chunks",
        label_offset=(-0.09, 0.015),
        arrow_overrides={"color": color("ws_edge"), "linewidth": 1.2, "connectionstyle": "arc3,rad=-0.5"},
        label_overrides={"fontsize": 7.5, "color": color("ws_edge")},
    )
    directed_edge(ax, 
        (0.82, 0.80), 
        (0.9, 0.77), 
        arrow_overrides={"color": color("ws_edge"), "linewidth": 1.2, "connectionstyle": "arc3,rad=-0.5"},
    )
    
    directed_edge(
        ax,
        (0.9, 0.67),
        (0.829, 0.62),
        label="beat, tempo, hue, value",
        label_offset=(0.06, -0.05),
        arrow_overrides={"color": color("ws_edge"), "linewidth": 1.2, "connectionstyle": "arc3,rad=-0.5"},
        label_overrides={"fontsize": 7.5, "color": color("ws_edge")},
    )
    directed_edge(ax, 
        (0.7, 0.58), 
        (0.65, 0.42), 
        arrow_overrides={"color": color("ws_edge"), "linewidth": 1.2, "connectionstyle": "arc3,rad=-0.5"},
    )

    # Store/render path
    directed_edge(ax, (0.44, 0.40), (0.41, 0.22), arrow_overrides={"color": color("render_edge"), "linewidth": 1.2, "connectionstyle": "arc3,rad=-0.5"},)
    directed_edge(
        ax,
        (0.54, 0.35),
        (0.54, 0.27),
        label="lighting state",
        label_offset=(0.035, 0.0),
        arrow_overrides={"color": color("render_edge"), "linewidth": 1.2},
        label_overrides={"fontsize": 7.5, "color": color("render_edge")},
    )
    directed_edge(
        ax,
        (0.62, 0.22),
        (0.705, 0.22),
        label="scene updates",
        label_offset=(0, 0.018),
        arrow_overrides={"color": color("render_edge"), "linewidth": 1.2},
        label_overrides={"fontsize": 7.5, "color": color("render_edge")},
    )
    directed_edge(
        ax,
        (0.37, 0.24),
        (0.43, 0.42),
        label="user settings",
        label_offset=(-0.01, 0.1),
        arrow_overrides={"color": color("store_edge"), "linewidth": 1.2, "connectionstyle": "arc3,rad=-0.5"},
        label_overrides={"fontsize": 7.5, "color": color("store_edge")},
    )

    # Legend labels
    ax.text(0.07, 0.93, "Audio path", color=color("audio_edge"), fontsize=8.7, fontweight="bold")
    ax.text(0.8, 0.93, "WebSocket path", color=color("ws_edge"), fontsize=8.7, fontweight="bold")
    ax.text(0.55, 0.47, "State layer", color=color("store_edge"), fontsize=8.7, fontweight="bold")
    ax.text(0.39, 0.09, "Rendering path", color=color("render_edge"), fontsize=8.7, fontweight="bold")

    apply_suptitle(fig, "Frontend Data Flow Architecture")

    out_pdf = output_pdf_path(__file__, chapter=3)
    save_pdf(fig, out_pdf)
    print(f"Saved {out_pdf}")


if __name__ == "__main__":
    main()
