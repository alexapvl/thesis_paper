THESIS_COLORS: dict[str, str] = {
    "text_primary": "#0f172a",
    "text_muted": "#334155",
    "stroke_default": "#475569",
    "panel_bg": "#f8fafc",
    "panel_border": "#334155",
    "audio_fill": "#dbeafe",
    "audio_edge": "#2563eb",
    "processing_fill": "#e0f2fe",
    "render_fill": "#f3e8ff",
    "render_edge": "#7c3aed",
    "ws_fill": "#dcfce7",
    "ws_edge": "#16a34a",
    "store_fill": "#ffedd5",
    "store_edge": "#f59e0b",
    "warn_fill": "#fff7ed",
    "warn_edge": "#fdba74",
    "danger_fill": "#fee2e2",
    "danger_edge": "#b91c1c",
}


def color(name: str, fallback: str | None = None) -> str:
    if fallback is not None:
        return THESIS_COLORS.get(name, fallback)
    if name not in THESIS_COLORS:
        raise KeyError(f"Unknown thesis color token: {name}")
    return THESIS_COLORS[name]
