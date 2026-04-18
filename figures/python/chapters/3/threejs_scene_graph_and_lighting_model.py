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


def draw_box(ax, center, size, text, fc="#f8fafc", ec="#334155", fontsize=9.2, bold=False):
    cx, cy = center
    w, h = size
    box = FancyBboxPatch(
        (cx - w / 2, cy - h / 2),
        w,
        h,
        boxstyle="round,pad=0.02,rounding_size=0.03",
        linewidth=1.0,
        facecolor=fc, 
        edgecolor=ec,
        zorder=3,
    )
    ax.add_patch(box)
    ax.text(
        cx,
        cy,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
        fontweight="bold" if bold else "normal",
        color="#0f172a",
        zorder=4,
    )


def arrow(ax, p0, p1, text=None, y_offset=0.0, shrink_b=10, curve=0.0):
    arr = FancyArrowPatch(
        p0,
        p1,
        arrowstyle="-|>",
        mutation_scale=12,
        linewidth=1.0,
        color="#475569",
        shrinkB=shrink_b,
        connectionstyle=f"arc3,rad={curve}",
        zorder=2,
    )
    ax.add_patch(arr)
    if text:
        mx = 0.5 * (p0[0] + p1[0])
        my = 0.5 * (p0[1] + p1[1]) + y_offset
        ax.text(mx, my, text, ha="center", va="center", fontsize=8.2, color="#334155")


def spotlight_annotation(ax, anchor_xy, lines, x_shift, y_shift=0.06):
    x, y = anchor_xy
    tx = x + x_shift
    ty = y + y_shift
    ax.text(
        tx,
        ty,
        lines,
        ha="center",
        va="center",
        fontsize=7.6,
        bbox=dict(boxstyle="round,pad=0.22", fc="#fff7ed", ec="#fdba74", lw=0.8),
        zorder=5,
    )
    arrow(ax, (tx, ty - 0.035), (x, y + 0.01))


def main() -> None:
    fig, ax = plt.subplots(figsize=(13.8, 8.0))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # Core graph
    scene = (0.5, 0.9)
    lights = (0.2, 0.72)
    camera = (0.47, 0.72)
    meshes = (0.8, 0.72)

    spot = (0.06, 0.5)
    point = (0.20, 0.5)
    target = (0.34, 0.5)

    floor = (0.66, 0.5)
    truss = (0.80, 0.5)
    fixtures = (0.94, 0.5)

    renderer = (0.5, 0.16)
    frame = (0.83, 0.16)

    draw_box(ax, scene, (0.14, 0.08), "Scene", fc="#dbeafe", ec="#1d4ed8", bold=True, fontsize=10.5)
    draw_box(ax, camera, (0.17, 0.085), "PerspectiveCamera", fc="#f1f5f9")
    draw_box(ax, lights, (0.12, 0.08), "Lights", fc="#fef3c7")
    draw_box(ax, meshes, (0.12, 0.08), "Meshes", fc="#e2e8f0")

    draw_box(ax, spot, (0.07, 0.085), "SpotLight", fc="#ffedd5", ec="#ea580c", bold=True)
    draw_box(ax, point, (0.07, 0.08), "PointLight", fc="#ffedd5", ec="#f59e0b")
    draw_box(ax, target, (0.07, 0.08), "SpotTarget", fc="#ffedd5", ec="#f59e0b")

    draw_box(ax, floor, (0.07, 0.08), "Floor Mesh", fc="#f8fafc")
    draw_box(ax, truss, (0.07, 0.08), "Truss Mesh", fc="#f8fafc")
    draw_box(ax, fixtures, (0.07, 0.08), "Fixture Mesh\nGroup", fc="#f8fafc")

    draw_box(ax, renderer, (0.2, 0.085), "WebGLRenderer", fc="#dcfce7", ec="#166534", bold=True)
    draw_box(ax, frame, (0.16, 0.08), "Rendered Frame", fc="#f0fdf4", ec="#16a34a")

    arrow(ax, (scene[0] - 0.02, scene[1] - 0.045), (camera[0] - 0.04, camera[1] + 0.05))
    arrow(ax, (scene[0], scene[1] - 0.045), (lights[0], lights[1] + 0.05))
    arrow(ax, (scene[0], scene[1] - 0.045), (meshes[0], meshes[1] + 0.05))

    arrow(ax, (lights[0] - 0.005, lights[1] - 0.045), (spot[0], spot[1] + 0.045), shrink_b=20)
    arrow(ax, (lights[0], lights[1] - 0.045), (point[0], point[1] + 0.045))
    arrow(ax, (lights[0] + 0.005, lights[1] - 0.045), (target[0], target[1] + 0.045), shrink_b=20)

    arrow(ax, (meshes[0] - 0.005, meshes[1] - 0.045), (floor[0], floor[1] + 0.045), shrink_b=20)
    arrow(ax, (meshes[0] + 0.005, meshes[1] - 0.045), (truss[0], truss[1] + 0.045))
    arrow(ax, (meshes[0], meshes[1] - 0.045), (fixtures[0], fixtures[1] + 0.05), shrink_b=20)

    arrow(
        ax,
        (scene[0] + 0.08, scene[1] - 0.045),
        (renderer[0] + 0.07, renderer[1] + 0.058),
        y_offset=0.02,
        curve=-0.12,
    )
    arrow(
        ax,
        (camera[0] - 0.04, camera[1] - 0.05),
        (renderer[0] - 0.11, renderer[1] + 0.052),
        curve=0.12,
    )
    arrow(ax, (renderer[0] + 0.11, renderer[1]), (frame[0] - 0.09, frame[1]), text="render()", y_offset=0.03)

    spotlight_annotation(
        ax,
        spot,
        "SpotLight controls\n"
        "color -> hue token\n"
        "intensity -> value token\n"
        "angle -> beam width\n"
        "penumbra -> edge softness\n"
        "target -> direction",
        x_shift=0.0,
        y_shift=-0.15,
    )

    fig.suptitle("Three.js Scene Graph and Lighting Model", fontsize=14, fontweight="bold", y=0.98)

    out_dir = Path(__file__).resolve().parents[3] / "chapters" / "3"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_pdf = out_dir / "threejs_scene_graph_and_lighting_model.pdf"
    fig.savefig(out_pdf, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {out_pdf}")


if __name__ == "__main__":
    main()
