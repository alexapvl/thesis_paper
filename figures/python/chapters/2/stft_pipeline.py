import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from figures.python.io import output_pdf_path, save_pdf
from figures.python.style import apply_style


def main() -> None:
    apply_style()

    fig = plt.figure(figsize=(14, 3.2))
    gs = gridspec.GridSpec(
        1,
        4,
        width_ratios=[1, 1, 1, 1.15],
        wspace=0.28,
        left=0.03,
        right=0.97,
        bottom=0.18,
        top=0.82,
    )

    # Synthesise a simple signal (two tones + chirp).
    sr = 4000
    dur = 0.25
    t = np.linspace(0, dur, int(sr * dur), endpoint=False)
    sig = (
        0.6 * np.sin(2 * np.pi * 220 * t)
        + 0.4 * np.sin(2 * np.pi * 550 * t)
        + 0.3 * np.sin(2 * np.pi * (100 + 600 * t / dur) * t)
    )

    # (1) Raw waveform.
    ax1 = fig.add_subplot(gs[0])
    ax1.plot(t * 1000, sig, color="#2b6cb0", linewidth=0.7)
    ax1.set_xlabel("Time (ms)")
    ax1.set_ylabel("Amplitude")
    ax1.set_title("(1) Raw waveform", fontsize=9, fontweight="bold", pad=6)
    ax1.set_xlim(0, dur * 1000)
    ax1.set_yticks([])

    # (2) Windowing.
    win_len = 128
    hop = 64
    n_wins = 5
    ax2 = fig.add_subplot(gs[1])
    ax2.plot(t * 1000, sig, color="#a0aec0", linewidth=0.5)
    colours = plt.cm.Set2(np.linspace(0, 0.6, n_wins))
    for i in range(n_wins):
        start = i * hop
        end = start + win_len
        if end > len(sig):
            break
        seg_t = t[start:end] * 1000
        window = np.hanning(win_len)
        seg_y = sig[start:end] * window
        ax2.fill_between(seg_t, seg_y, alpha=0.25, color=colours[i])
        ax2.plot(seg_t, seg_y, linewidth=0.7, color=colours[i])
    ax2.set_xlabel("Time (ms)")
    ax2.set_title("(2) Windowing", fontsize=9, fontweight="bold", pad=6)
    ax2.set_xlim(0, dur * 1000)
    ax2.set_yticks([])

    # (3) FFT of one window.
    frame_idx = 2
    start_sample = frame_idx * hop
    frame = sig[start_sample : start_sample + win_len] * np.hanning(win_len)
    spectrum = np.abs(np.fft.rfft(frame))
    freqs = np.fft.rfftfreq(win_len, d=1 / sr)
    ax3 = fig.add_subplot(gs[2])
    ax3.plot(freqs, 20 * np.log10(spectrum + 1e-8), color="#d53f8c", linewidth=0.8)
    ax3.set_xlabel("Frequency (Hz)")
    ax3.set_ylabel("Magnitude (dB)")
    ax3.set_title("(3) FFT per window", fontsize=9, fontweight="bold", pad=6)
    ax3.set_xlim(0, sr / 2)

    # (4) Spectrogram.
    ax4 = fig.add_subplot(gs[3])
    n_frames = (len(sig) - win_len) // hop + 1
    spec = np.zeros((win_len // 2 + 1, n_frames))
    for i in range(n_frames):
        s = i * hop
        frame = sig[s : s + win_len] * np.hanning(win_len)
        spec[:, i] = np.abs(np.fft.rfft(frame))
    spec_db = 20 * np.log10(spec + 1e-8)

    time_axis = np.arange(n_frames) * hop / sr * 1000
    freq_axis = np.fft.rfftfreq(win_len, d=1 / sr)
    im = ax4.pcolormesh(time_axis, freq_axis, spec_db, shading="gouraud", cmap="magma")
    ax4.set_xlabel("Time (ms)")
    ax4.set_ylabel("Frequency (Hz)")
    ax4.set_title("(4) Spectrogram", fontsize=9, fontweight="bold", pad=6)
    cb = fig.colorbar(im, ax=ax4, pad=0.03, aspect=20)
    cb.set_label("dB", fontsize=8)

    out_pdf = output_pdf_path(__file__, chapter=2)
    save_pdf(fig, out_pdf)
    print(f"Saved {out_pdf}")


if __name__ == "__main__":
    main()
