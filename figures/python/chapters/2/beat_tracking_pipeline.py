from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch, Rectangle

ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from figures.python.io import output_pdf_path, save_pdf
from figures.python.style import apply_style


BEAT_POS = np.array([0.10, 0.30, 0.50, 0.70, 0.90], dtype=float)
DOWNBEAT_POS = np.array([0.10, 0.90], dtype=float)


def _gaussian_pulse(t: np.ndarray, center: float, width: float) -> np.ndarray:
    return np.exp(-0.5 * ((t - center) / width) ** 2)


def _onset_envelope(t: np.ndarray) -> np.ndarray:
    env = np.zeros_like(t)
    for b in BEAT_POS:
        amp = 1.0 if np.any(np.isclose(b, DOWNBEAT_POS)) else 0.68
        env += amp * _gaussian_pulse(t, b, width=0.010)
    return env


def draw_waveform(ax):
    t = np.linspace(0, 1, 1800)
    env = _onset_envelope(t)

    # Build a representative "beat-driven" waveform: tonal bed + transient onsets.
    carrier = 0.11 * np.sin(2 * np.pi * 7.0 * t) + 0.07 * np.sin(2 * np.pi * 13.0 * t + 0.4)
    transients = env * np.sin(2 * np.pi * 52.0 * t)
    y = carrier + 0.75 * transients
    y /= np.max(np.abs(y)) + 1e-12

    ax.plot(t, y, color="#2563eb", linewidth=1.15)
    ax.axhline(0, color="#94a3b8", linewidth=0.5)
    for b in BEAT_POS:
        col = "#059669" if np.any(np.isclose(b, DOWNBEAT_POS)) else "#94a3b8"
        ax.axvline(b, color=col, linewidth=0.8, alpha=0.7)
    ax.set_xlim(0, 1)
    ax.set_ylim(-1.05, 1.05)
    ax.set_xticks([])
    ax.set_yticks([])


def draw_spectrogram(ax):
    time = np.linspace(0, 1, 220)
    freq = np.linspace(0, 1, 96)
    T, F = np.meshgrid(time, freq)

    # Harmonic beds + percussive vertical bursts at beat positions.
    img = 0.30 * np.exp(-((F - 0.22) ** 2) / 0.010) + 0.22 * np.exp(-((F - 0.58) ** 2) / 0.018)
    for b in BEAT_POS:
        strength = 0.70 if np.any(np.isclose(b, DOWNBEAT_POS)) else 0.46
        vertical = np.exp(-((T - b) ** 2) / 0.0009)
        img += strength * vertical * (0.65 + 0.35 * (1 - F))

    # Gentle texture for realism without random noise mismatch between runs.
    img += 0.03 * (np.sin(2 * np.pi * 3.0 * T) ** 2) * (0.3 + 0.7 * F)
    ax.imshow(img, origin="lower", aspect="auto", cmap="magma", extent=[0, 1, 0, 1])
    ax.set_xticks([])
    ax.set_yticks([])


def draw_activations(ax):
    t = np.linspace(0, 1, 1200)
    env = _onset_envelope(t)

    # Correlation-style activation extraction (matched filtering idea).
    # Inspired by cross-correlation usage for alignment discussions:
    # https://stackoverflow.com/questions/41606185/audio-waveform-matching
    k_t = np.linspace(-0.05, 0.05, 121)
    beat_kernel = np.exp(-0.5 * (k_t / 0.010) ** 2)
    beat_curve = np.correlate(env, beat_kernel, mode="same")
    beat_curve = 0.08 + 0.78 * beat_curve / (np.max(beat_curve) + 1e-12)

    downbeat_env = np.zeros_like(t)
    for d in DOWNBEAT_POS:
        downbeat_env += _gaussian_pulse(t, d, width=0.012)
    downbeat_kernel = np.exp(-0.5 * (k_t / 0.012) ** 2)
    downbeat_curve = np.correlate(downbeat_env, downbeat_kernel, mode="same")
    downbeat_curve = 0.05 + 0.62 * downbeat_curve / (np.max(downbeat_curve) + 1e-12)

    ax.plot(t, beat_curve, color="#dc2626", linewidth=1.3, label="Beat")
    ax.plot(t, downbeat_curve, color="#0f766e", linewidth=1.2, linestyle="--", label="Downbeat")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 0.9)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.legend(
        loc="lower center",
        bbox_to_anchor=(0.5, 1.02),
        ncol=2,
        fontsize=6.2,
        frameon=False,
        handlelength=1.8,
        columnspacing=1.0,
    )


def draw_postprocessed_beats(ax):
    ax.hlines(0.25, 0.05, 0.95, color="#64748b", linewidth=1.0)
    for x in BEAT_POS:
        ax.vlines(x, 0.15, 0.35, color="#1d4ed8", linewidth=1.4)
    for x in DOWNBEAT_POS:
        ax.vlines(x, 0.12, 0.38, color="#059669", linewidth=2.2)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 0.45)
    ax.set_xticks([])
    ax.set_yticks([])
    beat_handle = Line2D([0], [0], color="#1d4ed8", lw=1.6, label="Beat markers")
    downbeat_handle = Line2D([0], [0], color="#059669", lw=2.2, label="Downbeats")
    ax.legend(
        handles=[beat_handle, downbeat_handle],
        loc="lower center",
        bbox_to_anchor=(0.5, 1.02),
        ncol=2,
        fontsize=6.2,
        frameon=False,
        handlelength=1.8,
        columnspacing=1.0,
    )


def main() -> None:
    apply_style()
    fig = plt.figure(figsize=(14.5, 4.8))
    gs = fig.add_gridspec(1, 4, left=0.04, right=0.98, bottom=0.16, top=0.76, wspace=0.24)

    blocks = [
        {"label": "Audio Waveform", "drawer": draw_waveform},
        {"label": "Mel Spectrogram", "drawer": draw_spectrogram},
        {"label": "Neural Network\n(Beat/Downbeat Activations)", "drawer": draw_activations},
        {"label": "Post-Processing\n(Final Beat Positions)", "drawer": draw_postprocessed_beats},
    ]

    axes = []
    for i, block in enumerate(blocks):
        panel = fig.add_subplot(gs[0, i])
        panel.set_facecolor("#f8fafc")
        panel.set_xticks([])
        panel.set_yticks([])
        for spine in panel.spines.values():
            spine.set_color("#475569")
            spine.set_linewidth(1.0)

        # Add an inner plotting area to mimic "small visual inside each block"
        inner = panel.inset_axes([0.08, 0.08, 0.84, 0.72], facecolor="white")
        block["drawer"](inner)
        for spine in inner.spines.values():
            spine.set_color("#94a3b8")
            spine.set_linewidth(0.6)

        panel.set_title(block["label"], fontsize=10, fontweight="bold", pad=12, color="#1f2937")
        axes.append(panel)

    # Draw arrows between panels in figure coordinates
    for i in range(len(axes) - 1):
        left = axes[i].get_position()
        right = axes[i + 1].get_position()
        start = (left.x1 + 0.008, (left.y0 + left.y1) / 2)
        end = (right.x0 - 0.008, (right.y0 + right.y1) / 2)
        arrow = FancyArrowPatch(
            start,
            end,
            transform=fig.transFigure,
            arrowstyle="-|>",
            mutation_scale=14,
            linewidth=1.1,
            color="#334155",
        )
        fig.add_artist(arrow)

    fig.suptitle("Beat Tracking Pipeline", fontsize=14, fontweight="bold", y=0.93)

    out_pdf = output_pdf_path(__file__, chapter=2)
    save_pdf(fig, out_pdf)
    print(f"Saved {out_pdf}")


if __name__ == "__main__":
    main()
