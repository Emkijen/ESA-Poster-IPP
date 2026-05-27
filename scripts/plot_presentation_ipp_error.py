"""Presentation-format real-flight IPP error figure.

Layout: horizontal error full-width on top, along-track and cross-track
side-by-side on the bottom. Single trace (real flight with August-5 wind
profile) + 3-sigma covariance band.

Styling matches the master thesis figures (Computer Modern serif, LaTeX
rendering, small fonts) so it blends with the other thesis-derived plots
in the bundle. Output is written to the Kristoffer presentation folder
and does NOT touch master_thesis/figures/.

Inputs:  ../data/ipp_real.csv

Output:  C:/Source/Kristoffer_presentation/real_flight_ipp_error_1plus2.pdf

Run from this directory:
    python plot_presentation_ipp_error.py
"""

import sys
from pathlib import Path

import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np

# Pull thesis matplotlib style from the Rocket-Catch repo (read-only import).
ROCKET_CATCH_ROOT = Path(r"C:/Source/Rocket-Catch")
sys.path.insert(0, str(ROCKET_CATCH_ROOT))
sys.path.insert(0, str(ROCKET_CATCH_ROOT / "dev"))
from src.utils.thesis_style import apply_style, figsize_grid  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
REAL_CSV = ROOT / "data" / "ipp_real.csv"
OUT_PDF = Path(r"C:/Source/Kristoffer_presentation/real_flight_ipp_error_1plus2_v2.pdf")

Y_CAP = 1500.0  # m


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


def _draw(ax, t, e, sigma, color, label):
    ax.fill_between(t, 0, 3 * sigma, color=color, alpha=0.18)
    ax.plot(t, e, color=color, lw=1.4, label=label)


def main():
    apply_style()
    real = load(REAL_CSV)
    t_max = float(real["t"][-1])

    color = "tab:blue"

    fig = plt.figure(figsize=figsize_grid(2, 2, cell_aspect=0.7))
    gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.35, wspace=0.28)

    ax_h = fig.add_subplot(gs[0, :])
    ax_a = fig.add_subplot(gs[1, 0])
    ax_c = fig.add_subplot(gs[1, 1], sharex=ax_a)

    _draw(ax_h, real["t"], real["e_h"], real["sigma_h"], color, "Real flight")
    _draw(ax_a, real["t"], real["e_along"], real["sigma_along"], color, "Real flight")
    _draw(ax_c, real["t"], real["e_cross"], real["sigma_cross"], color, "Real flight")

    for ax, ylabel in [
        (ax_h, "Horizontal error [m]"),
        (ax_a, "Along-track error [m]"),
        (ax_c, "Cross-track error [m]"),
    ]:
        ax.set_xlabel("Time [s]")
        ax.set_ylabel(ylabel)
        ax.set_xlim(0, t_max)
        ax.set_ylim(0, Y_CAP)
    ax_h.legend()

    OUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_PDF, bbox_inches="tight")
    print(f"saved {OUT_PDF}")

    for k in ("e_h", "e_along", "e_cross"):
        e = real[k]
        print(f"  {k:8s}  median={np.median(e):6.1f}  "
              f"max={e.max():7.1f}  RMS={np.sqrt((e ** 2).mean()):6.1f}")


if __name__ == "__main__":
    main()
