from __future__ import annotations

from pathlib import Path

from matplotlib.figure import Figure


def output_pdf_path(script_path: str | Path, chapter: int | str, stem: str | None = None) -> Path:
    script = Path(script_path).resolve()
    repo_root = script.parents[4]
    out_dir = repo_root / "figures" / "chapters" / str(chapter)
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir / f"{stem or script.stem}.pdf"


def save_pdf(
    fig: Figure,
    output_path: str | Path,
    *,
    dpi: int = 300,
    bbox_inches: str = "tight",
    close: bool = True,
) -> Path:
    out_path = Path(output_path)
    fig.savefig(out_path, dpi=dpi, bbox_inches=bbox_inches)
    if close:
        import matplotlib.pyplot as plt

        plt.close(fig)
    return out_path
