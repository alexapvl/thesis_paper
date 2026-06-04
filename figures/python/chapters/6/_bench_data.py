"""Shared loader for the Evaluation chapter benchmark CSVs.

The benchmark tool (apps/web) exports two CSVs per run: a ``_summary`` file
with per-metric aggregate statistics and a ``_raw`` file with every sample.
Both carry a ``# key=value`` metadata header. This module parses those files,
groups the runs per machine (keyed on the authoritative ``device`` field, not
the editable config label), and exposes pooled samples plus per-run summary
statistics for the figure scripts.

A single ``MACHINES`` table drives every figure and table, so adding a third
configuration later (e.g. a university GPU) is a one-line change here and it
flows into all plots automatically.
"""

from __future__ import annotations

import csv
import statistics
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
DATA_DIR = ROOT / "figures" / "data" / "chapters" / "6"


@dataclass(frozen=True)
class Machine:
    key: str  # internal id
    label: str  # short label for axes/legends
    device_prefix: str  # matches the CSV `device` field
    color: str  # plot fill
    edge: str  # plot edge
    active: bool = True  # set False to reserve a slot without data


# Order here is the order used in every figure and table.
MACHINES: list[Machine] = [
    Machine("mps", "Mac M1 Pro\n(MPS)", "mps", "#dbeafe", "#2563eb"),
    Machine("cuda", "Win. RTX 2070S\n(CUDA, LAN)", "cuda", "#dcfce7", "#16a34a"),
    # Reserved third configuration (university GPU). Flip active=True and drop
    # the matching CSVs into figures/data/chapters/6/ to include it everywhere.
    Machine("third", "University GPU\n(planned)", "__none__", "#f1f5f9", "#94a3b8", active=False),
]


@dataclass
class RunData:
    name: str
    meta: dict[str, str]
    summary: dict[str, dict[str, float]]  # metric -> {mean,p50,p95,...}
    server_samples: dict[str, list[float]] = field(default_factory=dict)
    client_samples: dict[str, list[float]] = field(default_factory=dict)


def _read_with_header(path: Path) -> tuple[dict[str, str], str, list[str]]:
    meta: dict[str, str] = {}
    header: str | None = None
    body: list[str] = []
    with path.open() as handle:
        for line in handle:
            if line.startswith("# "):
                key, value = line[2:].rstrip("\n").split("=", 1)
                meta[key] = value
            elif line.startswith("metric,") or line.startswith("t_ms,"):
                header = line.strip()
            elif line.strip() and header is not None:
                body.append(line)
    if header is None:
        raise ValueError(f"no data header found in {path}")
    return meta, header, body


def _load_summary(path: Path) -> tuple[dict[str, str], dict[str, dict[str, float]]]:
    meta, header, body = _read_with_header(path)
    rows = csv.DictReader(body, fieldnames=header.split(","))
    summary: dict[str, dict[str, float]] = {}
    for row in rows:
        metric = row["metric"]
        summary[metric] = {
            k: float(row[k])
            for k in ("mean", "p50", "p95", "p99", "min", "max", "stddev", "n")
            if row.get(k) not in (None, "")
        }
    return meta, summary


def _load_raw(path: Path) -> tuple[dict[str, list[float]], dict[str, list[float]]]:
    meta, header, body = _read_with_header(path)
    warmup = float(meta.get("warmup_ms", "0"))
    rows = csv.DictReader(body, fieldnames=header.split(","))
    server: dict[str, list[float]] = {}
    client: dict[str, list[float]] = {}
    for row in rows:
        metric = row["metric"]
        value = float(row["value"])
        stamp = row["t_ms"].strip()
        if not stamp:  # backend stage sample (no client clock)
            server.setdefault(metric, []).append(value)
        elif float(stamp) >= warmup:  # client sample, past warmup
            client.setdefault(metric, []).append(value)
    return server, client


def load_runs() -> dict[str, list[RunData]]:
    """Return {machine_key: [RunData, ...]} for every active machine."""
    by_device: dict[str, list[RunData]] = {}
    for summary_path in sorted(DATA_DIR.glob("*_summary.csv")):
        meta, summary = _load_summary(summary_path)
        raw_path = Path(str(summary_path).replace("_summary.csv", "_raw.csv"))
        server, client = _load_raw(raw_path) if raw_path.exists() else ({}, {})
        run = RunData(summary_path.name, meta, summary, server, client)
        device = meta.get("device", "")
        key = "cuda" if device.startswith("cuda") else "mps" if device == "mps" else device
        by_device.setdefault(key, []).append(run)
    return by_device


def active_machines() -> list[Machine]:
    return [m for m in MACHINES if m.active]


def pooled_server(runs: list[RunData], metric: str) -> list[float]:
    out: list[float] = []
    for run in runs:
        out.extend(run.server_samples.get(metric, []))
    return out


def pooled_client(runs: list[RunData], metric: str) -> list[float]:
    out: list[float] = []
    for run in runs:
        out.extend(run.client_samples.get(metric, []))
    return out


def summary_stat(runs: list[RunData], metric: str, stat: str) -> float | None:
    """Average a summary statistic (e.g. 'p50') across runs for one metric."""
    vals = [r.summary[metric][stat] for r in runs if metric in r.summary]
    return statistics.mean(vals) if vals else None


def describe(values: list[float]) -> dict[str, float]:
    if not values:
        return {"n": 0}
    ordered = sorted(values)
    n = len(ordered)
    quant = lambda q: ordered[min(n - 1, int(q * n))]
    return {
        "n": n,
        "mean": sum(ordered) / n,
        "sd": statistics.pstdev(ordered) if n > 1 else 0.0,
        "min": ordered[0],
        "p50": quant(0.5),
        "p95": quant(0.95),
        "max": ordered[-1],
    }
