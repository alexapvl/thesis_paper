from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


plt.rcParams.update(
    {
        "font.family": "serif",
        "font.size": 10,
        "axes.linewidth": 0.6,
    }
)


def node(ax, xy, w, h, text, fc, ec="#334155", fs=8.6, bold=False):
    x, y = xy
    patch = FancyBboxPatch(
        (x - w / 2, y - h / 2),
        w,
        h,
        boxstyle="round,pad=0.008,rounding_size=0.02",
        linewidth=1.0,
        edgecolor=ec,
        facecolor=fc,
        zorder=3,
    )
    ax.add_patch(patch)
    ax.text(
        x,
        y,
        text,
        ha="center",
        va="center",
        fontsize=fs,
        fontweight="bold" if bold else "normal",
        color="#0f172a",
        zorder=4,
    )


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
    arr = FancyArrowPatch(
        p0,
        p1,
        arrowstyle="-|>",
        mutation_scale=12,
        linewidth=1.0,
        color=color,
        shrinkA=shrink_a,
        shrinkB=shrink_b,
        connectionstyle=f"arc3,rad={curve}",
        zorder=2,
    )
    ax.add_patch(arr)
    if label:
        mx = 0.5 * (p0[0] + p1[0])
        my = 0.5 * (p0[1] + p1[1]) + offset
        ax.text(mx + label_dx, my, label, ha="center", va="center", fontsize=7.8, color=color)


def main() -> None:
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

    node(ax, mic, 0.11, 0.09, "Microphone", fc="#dbeafe", bold=True)
    node(ax, gum, 0.17, 0.1, "getUserMedia()\nMediaStreamAudioSourceNode", fc="#dbeafe", fs=8.3)

    node(ax, file_in, 0.11, 0.09, "Audio File", fc="#dbeafe", bold=True)
    node(ax, decode, 0.17, 0.1, "decodeAudioData()\nAudioBufferSourceNode", fc="#dbeafe", fs=8.3)

    node(ax, gain, 0.11, 0.09, "GainNode", fc="#e0f2fe")
    node(ax, analyser, 0.12, 0.09, "AnalyserNode", fc="#e0f2fe", bold=True)
    node(ax, worklet, 0.12, 0.09, "AudioWorkletNode", fc="#e0f2fe", bold=True)
    node(ax, destination, 0.15, 0.09, "AudioDestinationNode\n(Speakers)", fc="#e0f2fe", fs=8.0)

    node(ax, react_ui, 0.13, 0.1, "React UI\nwaveform/spectrum", fc="#dcfce7", ec="#15803d")
    node(ax, websocket, 0.13, 0.1, "WebSocket\nupstream", fc="#dcfce7", ec="#15803d")
    node(ax, python_server, 0.15, 0.1, "Python Server\nbeat + Skip-BART", fc="#dcfce7", ec="#15803d")

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
    ax.text(0.03, 0.59, "Input Path B", fontsize=8.5, color="#1d4ed8", fontweight="bold")
    ax.text(0.36, 0.74, "Shared processing chain", fontsize=8.6, color="#334155", fontweight="bold")
    ax.text(0.54, 0.105, "Analysis + transport outputs", fontsize=8.6, color="#15803d", fontweight="bold")

    fig.suptitle("Web Audio API Routing Graph for the Application", fontsize=14, fontweight="bold", y=0.98)

    out_dir = Path(__file__).resolve().parents[3] / "chapters" / "3"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_pdf = out_dir / "web_audio_api_routing_graph.pdf"
    fig.savefig(out_pdf, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {out_pdf}")


if __name__ == "__main__":
    main()
