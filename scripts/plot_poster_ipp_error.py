"""Poster-friendly IPP error figure: 1x3 panels (horizontal | along | cross).

Each panel shares a common y-axis capped at Y_CAP m so the post-burn-out
convergence is visible without the burn-phase spike compressing the scale.
The burn-phase window is shaded and any real-flight peak that exceeds Y_CAP
is annotated with an off-scale arrow.

Inputs:  ../data/ipp_sim.csv
         ../data/ipp_real.csv

Output:  ../figures/poster_ipp_error.pdf

Run from this directory:
    python plot_poster_ipp_error.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

import poster_style as ps

ROOT = Path(__file__).resolve().parents[1]
SIM_CSV = ROOT / "data" / "ipp_sim.csv"
REAL_CSV = ROOT / "data" / "ipp_real.csv"
OUT_PDF = ROOT / "figures" / "poster_ipp_error.pdf"

BURN_END = 10.0  # s — approximate motor burn-out window
Y_CAP = 1500.0   # m — common y-axis cap across panels


def load(csv_path):
    arr = np.loadtxt(csv_path, delimiter=",", skiprows=1)
    return {
        "t": arr[:, 0],
        "e_h": arr[:, 1],
        "sigma_h": arr[:, 2],
        "e_along": np.abs(arr[:, 3]),
        "sigma_along": arr[:, 4],
        "e_cross": np.abs(arr[:, 5]),
        "sigma_cross": arr[:, 6],
    }


def _draw_traces(ax, sim, real, key_e, key_sig):
    for d, color in [(real, ps.WARN_RED), (sim, ps.NTNU_BLUE)]:
        ax.fill_between(d["t"], 0, 3 * d[key_sig], color=color, alpha=0.18, linewidth=0)
    ax.plot(real["t"], real[key_e], color=ps.WARN_RED, lw=ps.LW_PRIMARY, label="Real flight")
    ax.plot(sim["t"], sim[key_e], color=ps.NTNU_BLUE, lw=ps.LW_PRIMARY, label="Simulation reference")


def _annotate_peak(ax, real, key_e, ymax):
    peak_idx = int(np.nanargmax(real[key_e]))
    peak_v = float(real[key_e][peak_idx])
    if peak_v <= ymax * 1.02:
        return
    peak_t = float(real["t"][peak_idx])
    ax.annotate(
        f"peak\n{peak_v / 1000:.1f} km",
        xy=(peak_t, ymax * 0.98),
        xytext=(peak_t + 12, ymax * 0.78),
        fontsize=ps.SIZE_LEGEND, color=ps.DARK_GRAY,
        ha="left", va="top",
        arrowprops=dict(arrowstyle="->", color=ps.DARK_GRAY, lw=1.6,
                        shrinkA=2, shrinkB=2),
    )


def main():
    ps.apply()

    sim = load(SIM_CSV)
    real = load(REAL_CSV)

    fig, axes = plt.subplots(
        1, 3,
        figsize=(ps.COLUMN_WIDTH_IN, 4.0),
        sharex=True, sharey=True,
    )

    panels = [
        (axes[0], "e_h", "sigma_h", "Horizontal"),
        (axes[1], "e_along", "sigma_along", "Along-track"),
        (axes[2], "e_cross", "sigma_cross", "Cross-track"),
    ]

    t_max = max(sim["t"][-1], real["t"][-1])

    for ax, ke, ks, title in panels:
        ax.axvspan(0, BURN_END, color=ps.WARN_RED, alpha=0.10, linewidth=0)
        _draw_traces(ax, sim, real, ke, ks)
        ax.set_xlim(0, t_max)
        ax.set_ylim(0, Y_CAP)
        ax.set_title(title, fontsize=ps.SIZE_LABEL, pad=4)
        ax.set_xlabel("Time [s]")
        ax.grid(True)
        _annotate_peak(ax, real, ke, Y_CAP)

    axes[0].set_ylabel("Error [m]")

    # Single legend above the row of panels
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels,
               loc="upper center", ncol=2,
               bbox_to_anchor=(0.5, 1.02),
               frameon=False, fontsize=ps.SIZE_LEGEND)

    fig.tight_layout(rect=(0, 0, 1, 0.93))
    OUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_PDF)
    print(f"saved {OUT_PDF}")

    for label, d in [("Real", real), ("Sim", sim)]:
        for k in ("e_h", "e_along", "e_cross"):
            e = d[k]
            print(f"  {label:<5s} {k:8s}  median={np.median(e):6.1f}  "
                  f"max={e.max():7.1f}  RMS={np.sqrt((e ** 2).mean()):6.1f}")


if __name__ == "__main__":
    main()
