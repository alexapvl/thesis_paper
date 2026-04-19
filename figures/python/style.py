from __future__ import annotations

from typing import Any

import matplotlib.pyplot as plt


BASE_STYLE: dict[str, Any] = {
    "font.family": "serif",
    "font.size": 10,
    "axes.linewidth": 0.6,
    "xtick.major.width": 0.5,
    "ytick.major.width": 0.5,
}

TITLE_STYLE: dict[str, Any] = {
    "fontsize": 14,
    "fontweight": "bold",
    "y": 0.98,
}

FIGSIZE_PRESETS: dict[str, tuple[float, float]] = {
    "standard": (12.0, 4.8),
    "wide": (14.5, 7.8),
    "tall": (11.5, 8.5),
}

BOX_STYLE_DEFAULTS: dict[str, Any] = {
    "boxstyle": "round,pad=0.02,rounding_size=0.02",
    "linewidth": 1.0,
    "edgecolor": "#334155",
    "facecolor": "#f8fafc",
}

ARROW_STYLE_DEFAULTS: dict[str, Any] = {
    "arrowstyle": "-|>",
    "mutation_scale": 12,
    "linewidth": 1.0,
    "color": "#475569",
}

LABEL_STYLE_DEFAULTS: dict[str, Any] = {
    "fontsize": 8.5,
    "color": "#0f172a",
}


def _merge(base: dict[str, Any], overrides: dict[str, Any] | None) -> dict[str, Any]:
    if not overrides:
        return dict(base)
    merged = dict(base)
    merged.update(overrides)
    return merged


def apply_style(overrides: dict[str, Any] | None = None) -> dict[str, Any]:
    style = _merge(BASE_STYLE, overrides)
    plt.rcParams.update(style)
    return style


def get_figsize(preset: str = "standard", override: tuple[float, float] | None = None) -> tuple[float, float]:
    if override is not None:
        return override
    return FIGSIZE_PRESETS.get(preset, FIGSIZE_PRESETS["standard"])


def apply_suptitle(fig: plt.Figure, text: str, overrides: dict[str, Any] | None = None) -> None:
    fig.suptitle(text, **_merge(TITLE_STYLE, overrides))
