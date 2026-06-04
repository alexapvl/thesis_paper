"""Figure: Skip-BART inference-time distribution per machine.

Headline result of the chapter. Each point is one whole-window inference
(OpenL3 embed + Skip-BART decode) pooled across the three runs of a machine.
The box shows the quartiles; the jittered points show every sample. The two
distributions overlap heavily, which is the visual evidence that the GPU
backend barely changes lighting-generation time.
"""

from pathlib import Path
import random
import sys

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))
sys.path.append(str(Path(__file__).parent))

import _bench_data as bd  # noqa: E402
from figures.python.io import output_pdf_path, save_pdf  # noqa: E402
from figures.python.style import apply_style, apply_suptitle, get_figsize  # noqa: E402


def main() -> None:
    apply_style()
    random.seed(7)
    runs = bd.load_runs()
    machines = bd.active_machines()

    fig, ax = plt.subplots(figsize=get_figsize(override=(11.0, 5.4)))

    positions = list(range(1, len(machines) + 1))
    box_data = []
    for machine in machines:
        samples = bd.pooled_server(runs.get(machine.key, []), "server.skip.inference_ms")
        box_data.append([s / 1000.0 for s in samples])  # ms -> s

    bp = ax.boxplot(
        box_data,
        positions=positions,
        widths=0.5,
        patch_artist=True,
        showfliers=False,
        medianprops={"color": "#0f172a", "linewidth": 1.4},
        whiskerprops={"color": "#475569"},
        capprops={"color": "#475569"},
    )
    for patch, machine in zip(bp["boxes"], machines):
        patch.set_facecolor(machine.color)
        patch.set_edgecolor(machine.edge)
        patch.set_linewidth(1.2)

    for pos, samples, machine in zip(positions, box_data, machines):
        if not samples:
            ax.text(pos, 0.5, "no data\n(reserved)", ha="center", va="center",
                    fontsize=8.5, color="#94a3b8", transform=ax.get_xaxis_transform())
            continue
        jitter = [pos + random.uniform(-0.12, 0.12) for _ in samples]
        ax.scatter(jitter, samples, s=18, color=machine.edge, alpha=0.55,
                   edgecolors="white", linewidths=0.4, zorder=3)
        mean_s = sum(samples) / len(samples)
        ax.scatter([pos], [mean_s], marker="D", s=42, color="#b91c1c", zorder=4)
        ax.text(pos + 0.30, mean_s, f"mean {mean_s:.1f}s", fontsize=8.2,
                color="#b91c1c", va="center")

    ax.set_xticks(positions)
    ax.set_xticklabels([m.label for m in machines], fontsize=9)
    ax.set_ylabel("Inference time per window (s)")
    ax.set_ylim(0, max((max(d) for d in box_data if d), default=1) * 1.12)
    ax.grid(axis="y", color="#cbd5e1", linestyle=":", linewidth=0.8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    apply_suptitle(fig, "Skip-BART Inference Time per Window")
    out_pdf = output_pdf_path(__file__, chapter=6)
    save_pdf(fig, out_pdf)
    print(f"Saved {out_pdf}")


if __name__ == "__main__":
    main()
