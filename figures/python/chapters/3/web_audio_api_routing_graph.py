from pathlib import Path
import sys

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from figures.python.components import directed_edge, flow_node
from figures.python.io import output_pdf_path, save_pdf
from figures.python.palette import color
from figures.python.style import apply_style, apply_suptitle


def link(
    ax,
    p0,
    p1,
    color="#475569",
    label=None,
    offset=0.0,
    shrink_a=6,
    shrink_b=10,
    curve=0.0,
    label_dx=0.0,
):
    directed_edge(
        ax,
        p0,
        p1,
        label=label,
        label_offset=(label_dx, offset),
        arrow_overrides={
            "color": color,
            "shrinkA": shrink_a,
            "shrinkB": shrink_b,
            "connectionstyle": f"arc3,rad={curve}",
        },
    )


def main() -> None:
    apply_style()
    fig, ax = plt.subplots(figsize=(15.6, 7.6))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # Input paths
    mic = (0.08, 0.73)
    gum = (0.25, 0.73)
    file_in = (0.08, 0.48)
    decode = (0.25, 0.48)

    # Shared chain
    gain = (0.42, 0.605)
    analyser = (0.58, 0.605)
    worklet = (0.74, 0.605)
    destination = (0.90, 0.605)

    # Side outputs
    react_ui = (0.45, 0.245)
    websocket = (0.62, 0.245)
    python_server = (0.91, 0.245)

    flow_node(ax, mic, (0.11, 0.09), "Microphone", facecolor="#dbeafe", bold=True)
    flow_node(ax, gum, (0.17, 0.1), "getUserMedia()\nMediaStreamAudioSourceNode", facecolor="#dbeafe", fontsize=8.3)

    flow_node(ax, file_in, (0.11, 0.09), "Audio File", facecolor="#dbeafe", bold=True)
    flow_node(ax, decode, (0.17, 0.1), "decodeAudioData()\nAudioBufferSourceNode", facecolor="#dbeafe", fontsize=8.3)

    flow_node(ax, gain, (0.11, 0.09), "GainNode", facecolor="#e0f2fe")
    flow_node(ax, analyser, (0.12, 0.09), "AnalyserNode", facecolor="#e0f2fe", bold=True)
    flow_node(ax, worklet, (0.12, 0.09), "AudioWorkletNode", facecolor="#e0f2fe", bold=True)
    flow_node(ax, destination, (0.15, 0.09), "AudioDestinationNode\n(Speakers)", facecolor="#e0f2fe", fontsize=8.0)

    flow_node(ax, react_ui, (0.13, 0.1), "React UI\nwaveform/spectrum", facecolor="#dcfce7", edgecolor="#15803d")
    flow_node(ax, websocket, (0.13, 0.1), "WebSocket\nupstream", facecolor="#dcfce7", edgecolor="#15803d")
    flow_node(ax, python_server, (0.15, 0.1), "Python Server\nbeat + Skip-BART", facecolor="#dcfce7", edgecolor="#15803d")

    # Main links
    link(ax, (mic[0] + 0.055, mic[1]), (gum[0] - 0.085, gum[1]), color="#2563eb")
    link(ax, (file_in[0] + 0.055, file_in[1]), (decode[0] - 0.085, decode[1]), color="#2563eb")
    link(ax, (gum[0] + 0.085, gum[1] - 0.01), (gain[0] - 0.055, gain[1] + 0.03), color="#2563eb", curve=-0.05)
    link(ax, (decode[0] + 0.085, decode[1] + 0.01), (gain[0] - 0.055, gain[1] - 0.03), color="#2563eb", curve=0.05)

    link(ax, (gain[0] + 0.055, gain[1]), (analyser[0] - 0.06, analyser[1]))
    link(ax, (analyser[0] + 0.06, analyser[1]), (worklet[0] - 0.06, worklet[1]))
    link(ax, (worklet[0] + 0.06, worklet[1]), (destination[0] - 0.075, destination[1]))

    # Side links
    link(
        ax,
        (analyser[0], analyser[1] - 0.045),
        (react_ui[0], react_ui[1] + 0.055),
        color="#16a34a",
        label="frequency + time-domain data",
        offset=0.05,
        label_dx=-0.05,
    )
    link(
        ax,
        (worklet[0], worklet[1] - 0.045),
        (websocket[0], websocket[1] + 0.055),
        color="#16a34a",
        label="raw PCM chunks",
        offset=0.05,
        label_dx=0.07,
    )
    link(
        ax,
        (websocket[0] + 0.065, websocket[1]),
        (python_server[0] - 0.08, python_server[1]),
        color="#16a34a",
        label="WebSocket stream",
        offset=0.075,
    )

    ax.text(0.03, 0.84, "Input Path A", fontsize=8.5, color="#1d4ed8", fontweight="bold")
    ax.text(0.03, 0.59, "Input Path B", fontsize=8.5, color=color("text_muted"), fontweight="bold")
    ax.text(0.36, 0.74, "Shared processing chain", fontsize=8.6, color=color("text_muted"), fontweight="bold")
    ax.text(0.54, 0.105, "Analysis + transport outputs", fontsize=8.6, color=color("ws_edge"), fontweight="bold")

    apply_suptitle(fig, "Web Audio API Routing Graph for the Application")

    out_pdf = output_pdf_path(__file__, chapter=3)
    save_pdf(fig, out_pdf)
    print(f"Saved {out_pdf}")


if __name__ == "__main__":
    main()
