"""Figure: server-side per-stage processing time per machine.

This is the fair device comparison: every quantity here is measured on the
backend and excludes the network path. Grouped bars on a logarithmic axis
because the stages span four orders of magnitude (queue handoffs at ~0.01 ms
versus BeatNet drain at tens of ms). Skip-BART inference is shown separately
in its own figure because it is three orders larger again.
"""

from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))
sys.path.append(str(Path(__file__).parent))

import _bench_data as bd  # noqa: E402
from figures.python.io import output_pdf_path, save_pdf  # noqa: E402
from figures.python.style import apply_style, apply_suptitle, get_figsize  # noqa: E402

STAGES = [
    ("server.beat.ingest_ms", "Beat\ningest"),
    ("server.beat.drain_ms", "Beat\ndrain"),
    ("server.skip.ingest_queue_ms", "Skip\nenqueue"),
    ("server.skip.drain_queue_ms", "Skip\ndequeue"),
]


def main() -> None:
    apply_style()
    runs = bd.load_runs()
    machines = [m for m in bd.active_machines() if runs.get(m.key)]

    fig, ax = plt.subplots(figsize=get_figsize(override=(11.5, 5.0)))

    n_groups = len(STAGES)
    n_mach = len(machines)
    width = 0.8 / max(n_mach, 1)
    x = np.arange(n_groups)

    for i, machine in enumerate(machines):
        means = []
        for metric, _ in STAGES:
            stats = bd.describe(bd.pooled_server(runs[machine.key], metric))
            means.append(stats.get("mean", 0.0))
        offset = (i - (n_mach - 1) / 2) * width
        bars = ax.bar(x + offset, means, width=width, color=machine.color,
                      edgecolor=machine.edge, linewidth=1.0,
                      label=machine.label.replace("\n", " "))
        for bar, value in zip(bars, means):
            ax.text(bar.get_x() + bar.get_width() / 2, value * 1.10,
                    f"{value:.2f}", ha="center", va="bottom", fontsize=7.4,
                    color="#334155")

    ax.set_yscale("log")
    ax.set_xticks(x)
    ax.set_xticklabels([label for _, label in STAGES], fontsize=9)
    ax.set_ylabel("Mean stage time (ms, log scale)")
    ax.grid(axis="y", which="both", color="#e2e8f0", linestyle=":", linewidth=0.6)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(fontsize=8, frameon=False, loc="upper right")

    apply_suptitle(fig, "Server-Side Per-Stage Processing Time")
    out_pdf = output_pdf_path(__file__, chapter=6)
    save_pdf(fig, out_pdf)
    print(f"Saved {out_pdf}")


if __name__ == "__main__":
    main()
