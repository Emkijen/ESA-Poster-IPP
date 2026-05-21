"""Poster simulation IPP error figure: 1x3 panels (horizontal | along | cross).

All four simulated trajectories are pooled into one set of 4 x 100 = 400 Monte
Carlo realisations. Each panel shows the median IPP error and the empirical
5th-95th percentile band across the pool -- the centre and the spread of the
actual error, i.e. the same quantity. (The real-flight figure instead shows the
filter's covariance, which is the right thing for a single flight; the
simulation is an ensemble, so its natural band is the ensemble spread.)

The Rocket-Catch repo is used only to load the Monte Carlo NPZ files and the
ground-truth trajectory velocity (for the along/cross-track rotation). Its data
loaders use repo-root-relative paths, so this script chdir's there.

Output: ../figures/poster_sim_1x3.pdf
Run:    python plot_poster_sim.py   (from anywhere)
"""

import os
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
OUT_PDF = ROOT / "figures" / "poster_sim_1x3.pdf"

sys.path.insert(0, str(SCRIPT_DIR))
import poster_style as ps

ROCKET_CATCH = Path("C:/Source/Rocket-Catch")
MC_DIR = ROCKET_CATCH / "dev" / "data" / "sim" / "ipp_data" / "mc_wind"

# Rocket-Catch's loaders read data via paths relative to the repo root.
os.chdir(ROCKET_CATCH)
sys.path.append(str(ROCKET_CATCH))
sys.path.append(str(ROCKET_CATCH / "dev"))
from src.simulation.fetch_data import SimData

DATES = ["12_11_2024", "06_04_2025", "05_03_2025", "15_02_2025"]
SIGMA = 1.5
N = 100
P_LOW, P_HIGH = 5, 95


def load_mc(date):
    path = MC_DIR / f"{date}_gnss_baro_mag_sigma{SIGMA:.2f}_N{N}.npz"
    with np.load(path, allow_pickle=True) as d:
        return {k: d[k] for k in d.files}


def trajectory_errors(date):
    """Per-realisation [N, T] horizontal/along/cross error for one trajectory."""
    d = load_mc(date)
    t = d["prediction_times"]
    tx, ty = float(d["true_impact"][0]), float(d["true_impact"][1])

    eN = d["impact_x"] - tx
    eE = d["impact_y"] - ty
    err_h = np.sqrt(eN ** 2 + eE ** 2)

    sd = SimData(date, verbose=False)
    sd._import_sim_data()
    gt_vN = np.interp(t, sd.t_sim, sd.vx_gt)
    gt_vE = np.interp(t, sd.t_sim, sd.vy_gt)
    speed = np.sqrt(gt_vN ** 2 + gt_vE ** 2)
    speed = np.where(speed < 1e-6, 1.0, speed)
    uN, uE = gt_vN / speed, gt_vE / speed

    err_a = np.abs(eN * uN + eE * uE)
    err_c = np.abs(-eN * uE + eE * uN)
    return t, err_h, err_a, err_c


def main():
    t_ref = None
    pools = {"h": [], "a": [], "c": []}

    for date in DATES:
        t, err_h, err_a, err_c = trajectory_errors(date)
        if t_ref is None:
            t_ref = t

        def to_ref(arr):
            if np.array_equal(t, t_ref):
                return arr
            return np.vstack([np.interp(t_ref, t, row) for row in arr])

        pools["h"].append(to_ref(err_h))
        pools["a"].append(to_ref(err_a))
        pools["c"].append(to_ref(err_c))

    # Pool all 4 x 100 realisations: median line + empirical 5-95 percentile
    # band (the middle 90% of runs).
    pooled = {k: np.vstack(v) for k, v in pools.items()}  # each [400, T]
    med = {k: np.median(pooled[k], axis=0) for k in pooled}
    lo = {k: np.percentile(pooled[k], P_LOW, axis=0) for k in pooled}
    hi = {k: np.percentile(pooled[k], P_HIGH, axis=0) for k in pooled}

    ps.apply()
    fig, axes = plt.subplots(1, 3, figsize=(ps.COLUMN_WIDTH_IN, 6.0),
                             sharex=True, sharey=True)
    panels = [(axes[0], "Horizontal", "h"), (axes[1], "Along-track", "a"),
              (axes[2], "Cross-track", "c")]
    # Burn-phase spread reaches ~650 m; clip at 300 m so the median convergence
    # and the post-burnout band stay readable.
    y_top = 300.0
    for ax, title, k in panels:
        ax.fill_between(t_ref, lo[k], hi[k], color="grey", alpha=0.35, linewidth=0)
        ax.plot(t_ref, med[k], color=ps.NTNU_BLUE, lw=ps.LW_PRIMARY, label="Median")
        ax.set_xlim(0, t_ref[-1])
        ax.set_ylim(0, y_top)
        ax.set_title(title, fontsize=ps.SIZE_LABEL, pad=4)
        ax.grid(True)
    axes[0].set_ylabel("Error [m]")
    fig.supxlabel("Time [s]", fontsize=ps.SIZE_LABEL)

    band_patch = mpatches.Patch(color="grey", alpha=0.35,
                                label=f"{P_LOW}th–{P_HIGH}th percentile")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles + [band_patch], labels + [band_patch.get_label()],
               loc="upper center", ncol=2, bbox_to_anchor=(0.5, 1.03),
               frameon=False, fontsize=ps.SIZE_LEGEND)

    fig.tight_layout(rect=(0, 0, 1, 0.94))
    OUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_PDF)
    print(f"saved {OUT_PDF}  (pooled {len(DATES) * N} realisations)")
    for label, k in [("horizontal", "h"), ("along", "a"), ("cross", "c")]:
        print(f"  {label:11s} median peak={med[k].max():8.1f}  "
              f"p95 peak={hi[k].max():8.1f}  median final={med[k][-1]:7.1f}  "
              f"p95 final={hi[k][-1]:7.1f}")


if __name__ == "__main__":
    main()
