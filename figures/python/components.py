from __future__ import annotations

from typing import Any

from matplotlib.axes import Axes
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

from .palette import color
from .style import ARROW_STYLE_DEFAULTS, BOX_STYLE_DEFAULTS, LABEL_STYLE_DEFAULTS


def rounded_box(
    ax: Axes,
    center: tuple[float, float],
    size: tuple[float, float],
    text: str,
    *,
    box_overrides: dict[str, Any] | None = None,
    text_overrides: dict[str, Any] | None = None,
) -> FancyBboxPatch:
    cx, cy = center
    w, h = size
    box_style = dict(BOX_STYLE_DEFAULTS)
    if box_overrides:
        box_style.update(box_overrides)
    text_style = {"ha": "center", "va": "center", **LABEL_STYLE_DEFAULTS}
    if text_overrides:
        text_style.update(text_overrides)

    patch = FancyBboxPatch((cx - w / 2, cy - h / 2), w, h, zorder=3, **box_style)
    ax.add_patch(patch)
    ax.text(cx, cy, text, zorder=4, **text_style)
    return patch


def panel(
    ax: Axes,
    x: float,
    y: float,
    w: float,
    h: float,
    title: str,
    *,
    box_overrides: dict[str, Any] | None = None,
    title_overrides: dict[str, Any] | None = None,
) -> FancyBboxPatch:
    panel_style = {
        **BOX_STYLE_DEFAULTS,
        "facecolor": color("panel_bg"),
        "edgecolor": color("panel_border"),
        "linewidth": 1.2,
    }
    if box_overrides:
        panel_style.update(box_overrides)
    patch = FancyBboxPatch((x, y), w, h, zorder=1, **panel_style)
    ax.add_patch(patch)
    title_style = {"ha": "center", "va": "bottom", "fontsize": 11, "fontweight": "bold", "color": color("text_primary")}
    if title_overrides:
        title_style.update(title_overrides)
    ax.text(x + w / 2, y + h + 0.03, title, **title_style)
    return patch


def directed_edge(
    ax: Axes,
    p0: tuple[float, float],
    p1: tuple[float, float],
    *,
    label: str | None = None,
    label_offset: tuple[float, float] = (0.0, 0.0),
    arrow_overrides: dict[str, Any] | None = None,
    label_overrides: dict[str, Any] | None = None,
) -> FancyArrowPatch:
    arrow_style = dict(ARROW_STYLE_DEFAULTS)
    if arrow_overrides:
        arrow_style.update(arrow_overrides)
    arr = FancyArrowPatch(p0, p1, zorder=2, **arrow_style)
    ax.add_patch(arr)

    if label:
        mx = 0.5 * (p0[0] + p1[0]) + label_offset[0]
        my = 0.5 * (p0[1] + p1[1]) + label_offset[1]
        text_style = {"ha": "center", "va": "center", "fontsize": 7.8, "color": arrow_style.get("color", color("stroke_default"))}
        if label_overrides:
            text_style.update(label_overrides)
        ax.text(mx, my, label, **text_style)
    return arr


def flow_node(
    ax: Axes,
    center: tuple[float, float],
    size: tuple[float, float],
    text: str,
    *,
    fill_token: str | None = None,
    edge_token: str | None = None,
    facecolor: str | None = None,
    edgecolor: str | None = None,
    bold: bool = False,
    fontsize: float = 8.5,
    linewidth: float = 1.0,
    pad: float = 0.008,
    rounding_size: float = 0.02,
) -> FancyBboxPatch:
    resolved_face = facecolor if facecolor is not None else color(fill_token or "panel_bg")
    resolved_edge = edgecolor if edgecolor is not None else color(edge_token or "panel_border")
    return rounded_box(
        ax,
        center,
        size,
        text,
        box_overrides={
            "boxstyle": f"round,pad={pad},rounding_size={rounding_size}",
            "facecolor": resolved_face,
            "edgecolor": resolved_edge,
            "linewidth": linewidth,
        },
        text_overrides={
            "fontsize": fontsize,
            "fontweight": "bold" if bold else "normal",
            "color": color("text_primary"),
        },
    )
