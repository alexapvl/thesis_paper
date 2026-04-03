import matplotlib.pyplot as plt
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
    rows = [
        (
            "Spectral",
            "Centroid, bandwidth,\nflux, rolloff, contrast",
            "Brightness, timbral shape,\nonset/transient change",
        ),
        (
            "Cepstral",
            "MFCCs (typically 13-20\ncoefficients)",
            "Spectral envelope /\ntimbre summary",
        ),
        (
            "Temporal",
            "Zero-crossing rate,\nRMS energy, onset strength",
            "Noisiness/percussiveness,\nloudness, event salience",
        ),
        (
            "Tonal",
            "Chroma (STFT/CQT/CENS)",
            "Harmonic content,\nchord/key tendencies",
        ),
    ]

    fig, ax = plt.subplots(figsize=(11.2, 3.8))
    ax.axis("off")

    col_labels = ["Feature Category", "Representative Features", "Musical Quality Captured"]
    col_widths = [0.18, 0.42, 0.40]
    table = ax.table(
        cellText=rows,
        colLabels=col_labels,
        colLoc="center",
        cellLoc="left",
        colWidths=col_widths,
        loc="center",
    )

    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 2.1)

    # Header styling
    for j in range(len(col_labels)):
        cell = table[(0, j)]
        cell.set_facecolor("#d9e6f2")
        cell.set_text_props(weight="bold", ha="center", va="center")
        cell.set_edgecolor("#7f8c8d")
        cell.set_linewidth(0.8)

    # Body styling
    row_shades = ["#f8fbff", "#eef5fb"]
    n_rows = len(rows)
    n_cols = len(col_labels)
    for i in range(1, n_rows + 1):
        for j in range(n_cols):
            cell = table[(i, j)]
            cell.set_facecolor(row_shades[(i - 1) % 2])
            cell.set_edgecolor("#a0a7ad")
            cell.set_linewidth(0.6)
            if j == 0:
                cell.set_text_props(weight="bold", ha="center")
            else:
                cell.set_text_props(ha="left")

    ax.set_title(
        "Summary of Core Audio Feature Categories in MIR",
        fontsize=11,
        fontweight="bold",
        pad=10,
    )

    fig.tight_layout()

    out_dir = Path(__file__).resolve().parent.parent
    out_pdf = out_dir / "audio_feature_summary.pdf"
    fig.savefig(out_pdf, dpi=300, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved {out_pdf}")


if __name__ == "__main__":
    main()
