"""Poster-friendly geographic IPP track figure.

Reads the dumped real-flight GNSS positions and per-step predicted impact points
(both in NED relative to the launch reference) and renders them on a satellite
basemap of Andoya. The rocket's ground track, the locus of predicted impact
points (coloured by time), and the actual splashdown are overlaid.

Inputs:  ../data/ipp_track.csv
         ../data/ipp_track_meta.csv

Output:  ../figures/poster_ipp_track.pdf

Dependency:
    pip install contextily

Run from this directory:
    python plot_poster_ipp_track.py
"""

from pathlib import Path

import contextily as cx
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

import poster_style as ps

ROOT = Path(__file__).resolve().parents[1]
TRACK_CSV = ROOT / "data" / "ipp_track.csv"
META_CSV = ROOT / "data" / "ipp_track_meta.csv"
OUT_PDF = ROOT / "figures" / "poster_ipp_track.pdf"

M_PER_DEG_LAT = 111_320.0


def load_meta(path):
    meta = {}
    arr = np.genfromtxt(path, delimiter=",", skip_header=1, dtype=str)
    for row in arr:
        meta[row[0]] = float(row[1])
    return meta


def ned_to_geo(x_n, x_e, lat0, lon0):
    """Flat-earth NED -> lat/lon. Good to ~10 m over a 30 km box at high latitude."""
    m_per_deg_lon = M_PER_DEG_LAT * np.cos(np.radians(lat0))
    lat = lat0 + x_n / M_PER_DEG_LAT
    lon = lon0 + x_e / m_per_deg_lon
    return lat, lon


def main():
    ps.apply()

    meta = load_meta(META_CSV)
    lat0, lon0 = meta["launch_lat"], meta["launch_lon"]
    impact_n, impact_e = meta["impact_n"], meta["impact_e"]

    arr = np.loadtxt(TRACK_CSV, delimiter=",", skiprows=1)
    t = arr[:, 0]
    rocket_n, rocket_e = arr[:, 1], arr[:, 2]
    pred_n, pred_e = arr[:, 3], arr[:, 4]

    rocket_lat, rocket_lon = ned_to_geo(rocket_n, rocket_e, lat0, lon0)
    pred_lat, pred_lon = ned_to_geo(pred_n, pred_e, lat0, lon0)
    impact_lat, impact_lon = ned_to_geo(impact_n, impact_e, lat0, lon0)

    fig, ax = plt.subplots(figsize=(ps.COLUMN_WIDTH_IN, 9.5))

    # Rocket ground track — thick warn-red line
    ax.plot(rocket_lon, rocket_lat, color=ps.WARN_RED, lw=ps.LW_PRIMARY,
            label="Rocket ground track", zorder=3)

    # IPP predictions — coloured by flight time so the convergence reads as a gradient
    sc = ax.scatter(pred_lon, pred_lat, c=t, cmap="viridis", s=70,
                    edgecolor="white", linewidth=0.6, zorder=4,
                    label="Predicted impact (per step)")

    # Actual splashdown — bullseye
    ax.scatter([impact_lon], [impact_lat], marker="*", s=600,
               color=ps.RESULT_GREEN, edgecolor="white", linewidth=1.4,
               zorder=5, label="Actual splashdown")

    # Launch site
    ax.scatter([lon0], [lat0], marker="^", s=300,
               color=ps.NTNU_BLUE, edgecolor="white", linewidth=1.4,
               zorder=5, label="Launch site")

    # Frame the area with a small margin in geo coords
    all_lats = np.concatenate([rocket_lat, pred_lat, [impact_lat, lat0]])
    all_lons = np.concatenate([rocket_lon, pred_lon, [impact_lon, lon0]])
    pad_lat = 0.02
    pad_lon = 0.04
    ax.set_xlim(all_lons.min() - pad_lon, all_lons.max() + pad_lon)
    ax.set_ylim(all_lats.min() - pad_lat, all_lats.max() + pad_lat)
    ax.set_aspect(1.0 / np.cos(np.radians(lat0)))

    # Satellite basemap (Esri World Imagery — no API key)
    cx.add_basemap(ax, source=cx.providers.Esri.WorldImagery,
                   crs="EPSG:4326", zoom="auto")

    # Time colorbar
    cbar = fig.colorbar(sc, ax=ax, fraction=0.035, pad=0.02)
    cbar.set_label("Flight time [s]")

    ax.set_xlabel("Longitude [deg]")
    ax.set_ylabel("Latitude [deg]")

    # Single legend above the map
    handles = [
        Line2D([0], [0], color=ps.WARN_RED, lw=ps.LW_PRIMARY,
               label="Rocket ground track"),
        Line2D([0], [0], marker="o", color="none", markerfacecolor="#3b528b",
               markersize=10, label="Predicted impact (per step)"),
        Line2D([0], [0], marker="*", color="none", markerfacecolor=ps.RESULT_GREEN,
               markeredgecolor="white", markersize=18, label="Actual splashdown"),
        Line2D([0], [0], marker="^", color="none", markerfacecolor=ps.NTNU_BLUE,
               markeredgecolor="white", markersize=14, label="Launch site"),
    ]
    fig.legend(handles=handles, loc="upper center", ncol=4,
               bbox_to_anchor=(0.5, 1.02), frameon=False,
               fontsize=ps.SIZE_LEGEND)

    fig.tight_layout(rect=(0, 0, 1, 0.95))
    OUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_PDF)
    print(f"saved {OUT_PDF}")
    print(f"  launch ref:   ({lat0:.4f}, {lon0:.4f})")
    print(f"  rocket NED bbox: N=[{rocket_n.min():.0f}, {rocket_n.max():.0f}]  "
          f"E=[{rocket_e.min():.0f}, {rocket_e.max():.0f}]")
    impact_dist_km = np.hypot(impact_n, impact_e) / 1000
    print(f"  impact at {impact_dist_km:.1f} km from launch ref")


if __name__ == "__main__":
    main()
