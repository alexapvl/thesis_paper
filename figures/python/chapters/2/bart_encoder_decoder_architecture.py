from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle


plt.rcParams.update(
    {
        "font.family": "serif",
        "font.size": 10,
        "axes.linewidth": 0.6,
        "xtick.major.width": 0.5,
        "ytick.major.width": 0.5,
    }
)


@dataclass
class Box:
    x: float
    y: float
    w: float
    h: float

    @property
    def cx(self) -> float:
        return self.x + self.w / 2

    @property
    def top(self) -> float:
        return self.y + self.h

    @property
    def bottom(self) -> float:
        return self.y

    @property
    def right(self) -> float:
        return self.x + self.w

    @property
    def left(self) -> float:
        return self.x


def draw_token_strip(ax, box: Box, labels, face, edge, title, title_above=True):
    n = len(labels)
    gap = box.w * 0.02
    token_w = (box.w - gap * (n - 1)) / n
    for i, label in enumerate(labels):
        tx = box.x + i * (token_w + gap)
        rect = Rectangle((tx, box.y), token_w, box.h, facecolor=face, edgecolor=edge, linewidth=0.9)
        ax.add_patch(rect)
        ax.text(tx + token_w / 2, box.y + box.h / 2, label, ha="center", va="center", fontsize=7)
    if title_above:
        ax.text(box.cx, box.top + 0.015, title, ha="center", va="bottom", fontsize=8.3, fontweight="bold")
    else:
        ax.text(box.cx, box.bottom - 0.018, title, ha="center", va="top", fontsize=8.3, fontweight="bold")


def draw_stack(ax, box: Box, n_layers, face, edge, layer_text, stack_label, label_gap=0.028):
    offset = 0.010
    for i in range(n_layers):
        rect = Rectangle(
            (box.x + i * offset, box.y + i * offset),
            box.w,
            box.h,
            facecolor=face,
            edgecolor=edge,
            linewidth=1.0,
            alpha=0.95,
        )
        ax.add_patch(rect)

    cx = box.cx + (n_layers - 1) * offset / 2
    cy = box.y + box.h / 2 + (n_layers - 1) * offset / 2
    ax.text(cx, cy, layer_text, ha="center", va="center", fontsize=8)
    ax.text(cx, box.bottom - label_gap, stack_label, ha="center", va="top", fontsize=8)
    return Box(box.x + (n_layers - 1) * offset, box.y + (n_layers - 1) * offset, box.w, box.h)


def arrow(ax, start, end, color="#334155", dashed=False):
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=13,
            linewidth=1.1 if not dashed else 1.0,
            linestyle="--" if dashed else "-",
            color=color,
        )
    )


def main() -> None:
    fig, ax = plt.subplots(figsize=(14.8, 5.2))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # Layout model: derive most coordinates from a few anchors.
    stack_y = 0.36
    stack_w = 0.19
    stack_h = 0.31
    token_h = 0.07
    bottom_gap = 0.16
    top_gap = 0.14

    encoder_stack_base = Box(0.10, stack_y, stack_w, stack_h)
    decoder_stack_base = Box(0.60, stack_y, stack_w, stack_h)
    encoder_tokens = Box(0.05, stack_y - bottom_gap - token_h, 0.36, token_h)
    decoder_tokens_in = Box(0.60, stack_y - bottom_gap - token_h, 0.30, token_h)
    decoder_tokens_out = Box(0.60, stack_y + stack_h + top_gap, 0.30, token_h)

    ax.text(
        0.5,
        0.965,
        "BART Encoder-Decoder Architecture (Denoising Sequence-to-Sequence)",
        ha="center",
        va="top",
        fontsize=13.5,
        fontweight="bold",
    )

    draw_token_strip(
        ax,
        encoder_tokens,
        ["The", "[MASK]", "lights", "are", "vivid"],
        face="#fef3c7",
        edge="#d97706",
        title="Corrupted Input Tokens",
        title_above=False,
    )
    draw_token_strip(
        ax,
        decoder_tokens_in,
        ["<s>", "The", "stage", "lights", "..."],
        face="#e0f2fe",
        edge="#0284c7",
        title="Shifted Decoder Input",
        title_above=False,
    )
    draw_token_strip(
        ax,
        decoder_tokens_out,
        ["The", "stage", "lights", "are", "</s>"],
        face="#dcfce7",
        edge="#16a34a",
        title="Reconstructed Output Tokens",
        title_above=False,
    )

    encoder_front = draw_stack(
        ax,
        encoder_stack_base,
        n_layers=4,
        face="#dbeafe",
        edge="#1d4ed8",
        layer_text="Self-Attention\n(bidirectional)",
        stack_label="Bidirectional Encoder Layers",
        label_gap=0.022,
    )
    decoder_front = draw_stack(
        ax,
        decoder_stack_base,
        n_layers=4,
        face="#ede9fe",
        edge="#7c3aed",
        layer_text="Masked Self-Attention\n+ Cross-Attention",
        stack_label="Autoregressive Decoder Layers",
        label_gap=0.040,
    )

    # Main centered vertical data-flow arrows
    arrow(ax, (encoder_front.cx, encoder_tokens.top), (encoder_front.cx, encoder_front.bottom - 0.08))
    arrow(ax, (decoder_front.cx, decoder_tokens_in.top), (decoder_front.cx, decoder_front.bottom - 0.08))
    arrow(ax, (decoder_front.cx, decoder_front.top), (decoder_front.cx, decoder_tokens_out.bottom - 0.033))

    # Cross-attention links
    y_levels = [decoder_front.bottom + 0.08, decoder_front.bottom + 0.16, decoder_front.bottom + 0.24]
    for y in y_levels:
        arrow(ax, (encoder_front.right, y), (decoder_front.left - 0.03, y), dashed=True, color="#475569")
    ax.text((encoder_front.right + decoder_front.left) / 2, y_levels[-1] + 0.02, "Cross-attention", ha="center", va="bottom", fontsize=8, color="#475569")

    # Causal decoding cue + tiny legend for special tokens.
    y_causal = 0.035
    arrow(ax, (decoder_tokens_in.left + 0.07, y_causal), (decoder_tokens_in.right - 0.07, y_causal), color="#7c3aed")
    ax.text(decoder_tokens_in.cx, y_causal - 0.018, "Causal decoding (left -> right)", ha="center", va="top", fontsize=7.1, color="#6d28d9")

    out_dir = Path(__file__).resolve().parent.parent / "chapters" / "2"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_pdf = out_dir / "bart_encoder_decoder_architecture.pdf"
    fig.savefig(out_pdf, dpi=300)
    plt.close(fig)
    print(f"Saved {out_pdf}")


if __name__ == "__main__":
    main()
