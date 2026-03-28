import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

import librosa
import librosa.display


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


def make_demo_signal(sr: int = 22050, duration: float = 3.5) -> np.ndarray:
    """Synthesize a musically varied signal to compare frequency scales."""
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)

    # Low harmonic bed
    low = 0.35 * np.sin(2 * np.pi * 110 * t)
    low += 0.20 * np.sin(2 * np.pi * 220 * t)
    low += 0.15 * np.sin(2 * np.pi * 330 * t)

    # Mid/high content with light modulation
    high = 0.10 * np.sin(2 * np.pi * 1400 * t + 0.6 * np.sin(2 * np.pi * 2.0 * t))
    high += 0.08 * np.sin(2 * np.pi * 2800 * t)

    # Sweep to add changing energy distribution
    f0, f1 = 300.0, 5200.0
    k = (f1 - f0) / duration
    chirp = 0.12 * np.sin(2 * np.pi * (f0 * t + 0.5 * k * t**2))

    y = low + high + chirp
    y /= np.max(np.abs(y)) + 1e-10
    return y


def main() -> None:
    sr = 22050
    n_fft = 2048
    hop_length = 256
    n_mels = 128

    y = make_demo_signal(sr=sr)

    # Linear-frequency spectrogram (STFT magnitude in dB)
    stft = librosa.stft(y, n_fft=n_fft, hop_length=hop_length, window="hann")
    stft_db = librosa.amplitude_to_db(np.abs(stft), ref=np.max)

    # Mel spectrogram (power in dB)
    mel = librosa.feature.melspectrogram(
        y=y, sr=sr, n_fft=n_fft, hop_length=hop_length, n_mels=n_mels
    )
    mel_db = librosa.power_to_db(mel, ref=np.max)

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.2), constrained_layout=True)

    img_lin = librosa.display.specshow(
        stft_db,
        sr=sr,
        hop_length=hop_length,
        x_axis="time",
        y_axis="linear",
        cmap="magma",
        ax=axes[0],
    )
    axes[0].set_title("(a) Linear spectrogram", fontsize=10, fontweight="bold", pad=6)
    axes[0].set_xlabel("Time (s)")
    axes[0].set_ylabel("Frequency (Hz)")

    img_mel = librosa.display.specshow(
        mel_db,
        sr=sr,
        hop_length=hop_length,
        x_axis="time",
        y_axis="mel",
        cmap="magma",
        ax=axes[1],
    )
    axes[1].set_title("(b) Mel spectrogram", fontsize=10, fontweight="bold", pad=6)
    axes[1].set_xlabel("Time (s)")
    axes[1].set_ylabel("Mel frequency")

    # Annotate mel-axis resolution behavior
    x_pos = librosa.get_duration(y=y, sr=sr) * 0.97
    axes[1].annotate(
        "More bins / finer detail\nat low frequencies",
        xy=(x_pos, 500),
        xytext=(x_pos * 0.58, 1300),
        arrowprops=dict(arrowstyle="->", lw=0.8, color="white"),
        color="white",
        fontsize=8,
        ha="right",
        va="center",
        bbox=dict(boxstyle="round,pad=0.2", fc=(0, 0, 0, 0.35), ec="none"),
    )
    axes[1].annotate(
        "Fewer bins / coarser detail\nat high frequencies",
        xy=(x_pos, 7000),
        xytext=(x_pos * 0.58, 9000),
        arrowprops=dict(arrowstyle="->", lw=0.8, color="white"),
        color="white",
        fontsize=8,
        ha="right",
        va="center",
        bbox=dict(boxstyle="round,pad=0.2", fc=(0, 0, 0, 0.35), ec="none"),
    )

    cbar = fig.colorbar(img_mel, ax=axes, shrink=0.92, pad=0.02)
    cbar.set_label("Magnitude (dB)")

    out_dir = Path(__file__).resolve().parent.parent
    out_pdf = out_dir / "linear_vs_mel_spectrogram.pdf"
    fig.savefig(out_pdf, dpi=300, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved {out_pdf}")

if __name__ == "__main__":
    main()
