"""Figure: end-to-end latency CDFs (beat and lighting) per machine.

Two panels share the cumulative-distribution view so the reader can read
"what fraction of updates arrived within X ms". The Mac curves rise steeply
(loopback path); the Windows curves are shifted right and have long tails
(real LAN through the SSH tunnel). This visualises the network-path confound:
the difference here is dominated by transport, not by the inference device.
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


def cdf(ax, values, label, color):
    if not values:
        return
    ordered = np.sort(np.asarray(values))
    y = np.arange(1, len(ordered) + 1) / len(ordered)
    ax.step(ordered, y, where="post", label=label, color=color, linewidth=1.6)


def main() -> None:
    apply_style()
    runs = bd.load_runs()
    machines = bd.active_machines()

    fig, axes = plt.subplots(1, 2, figsize=get_figsize(override=(12.6, 4.8)))
    panels = [
        ("beat.e2e_ms", "Beat update latency"),
        ("lighting.e2e_ms", "Lighting update latency"),
    ]

    for ax, (metric, title) in zip(axes, panels):
        for machine in machines:
            samples = bd.pooled_client(runs.get(machine.key, []), metric)
            cdf(ax, samples, machine.label.replace("\n", " "), machine.edge)
        ax.axhline(0.5, color="#cbd5e1", linestyle=":", linewidth=0.8)
        ax.axhline(0.95, color="#cbd5e1", linestyle=":", linewidth=0.8)
        ax.text(ax.get_xlim()[1], 0.5, " p50", fontsize=7.5, color="#94a3b8", va="center")
        ax.text(ax.get_xlim()[1], 0.95, " p95", fontsize=7.5, color="#94a3b8", va="center")
        ax.set_title(title, fontsize=10)
        ax.set_xlabel("Latency (ms)")
        ax.set_ylim(0, 1.02)
        ax.set_xscale("log")
        ax.grid(True, which="both", color="#e2e8f0", linestyle=":", linewidth=0.6)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    axes[0].set_ylabel("Cumulative fraction of updates")
    axes[0].legend(fontsize=8, loc="lower right", frameon=False)

    apply_suptitle(fig, "End-to-End Latency Distributions")
    out_pdf = output_pdf_path(__file__, chapter=6)
    save_pdf(fig, out_pdf)
    print(f"Saved {out_pdf}")


if __name__ == "__main__":
    main()
