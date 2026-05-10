"""Poster-friendly spin-rate figure: gyro vs magnetometer-spectrogram.

Reads the staged real-flight IMU and magnetometer CSVs from ../data/ and
renders a single-panel time-series intended to be readable from 2 m on A0.

Output: ../figures/poster_spin_rate.pdf

Run from this directory:
    python plot_poster_spin_rate.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter, spectrogram

import poster_style as ps

ROOT = Path(__file__).resolve().parents[1]
IMU_CSV = ROOT / "data" / "imu.csv"
MAG_CSV = ROOT / "data" / "mag.csv"
OUT_PDF = ROOT / "figures" / "poster_spin_rate.pdf"

GYRO_CEILING = 40.0  # rad/s (LSM9DS1 +-2000 dps configured)


def mag_ridge(t_mag, B_nav, fs, fmin=0.5, fmax=30.0, nperseg=512, noverlap=480):
    """Peak-frequency ridge from transverse magnetic-field PSD with sub-bin
    parabolic interpolation for sub-bin frequency resolution."""
    B_y = B_nav[:, 1] - np.mean(B_nav[:, 1])
    B_z = B_nav[:, 2] - np.mean(B_nav[:, 2])
    f, t_s, S_y = spectrogram(B_y, fs=fs, window="hann", nperseg=nperseg, noverlap=noverlap)
    _, _, S_z = spectrogram(B_z, fs=fs, window="hann", nperseg=nperseg, noverlap=noverlap)
    S = S_y + S_z

    mask = (f >= fmin) & (f <= fmax)
    f_band = f[mask]
    S_band = S[mask, :]
    idx = np.argmax(S_band, axis=0)
    cols = np.arange(S_band.shape[1])

    eps = 1e-20
    logS = np.log(S_band + eps)
    i_mid = np.clip(idx, 1, len(f_band) - 2)
    a = logS[i_mid - 1, cols]
    b = logS[i_mid, cols]
    c = logS[i_mid + 1, cols]
    denom = a - 2 * b + c
    denom = np.where(np.abs(denom) < 1e-12, 1e-12, denom)
    delta = np.clip(0.5 * (a - c) / denom, -0.5, 0.5)
    df = f_band[1] - f_band[0]
    f_peak = f_band[i_mid] + delta * df
    bad = ~np.isfinite(f_peak) | (idx == 0) | (idx == len(f_band) - 1)
    f_peak[bad] = f_band[idx[bad]]

    return t_s + t_mag[0], f_peak


def main():
    ps.apply()

    imu = np.loadtxt(IMU_CSV, delimiter=",", skiprows=1)
    mag = np.loadtxt(MAG_CSV, delimiter=",", skiprows=1)

    t_imu = imu[:, 0]
    wx = imu[:, 4]  # rad/s, gyro spin-axis

    t_mag = mag[:, 0]
    B_nav = mag[:, 1:4]
    fs_mag = 1.0 / np.median(np.diff(t_mag))

    t_spec, f_peak = mag_ridge(t_mag, B_nav, fs_mag)
    omega_mag = 2 * np.pi * f_peak
    omega_smooth = savgol_filter(omega_mag, window_length=21, polyorder=2)

    # Half column width — placed beside text in the Challenges block.
    fig, ax = plt.subplots(figsize=(ps.HALF_COLUMN_IN, 3.6))

    ax.axhline(GYRO_CEILING, color=ps.WARN_RED, lw=ps.LW_REFERENCE, ls="--",
               alpha=0.75, zorder=1)
    ax.text(50, GYRO_CEILING + 1, f"{GYRO_CEILING:.0f} rad/s ceiling",
            color=ps.WARN_RED, fontsize=ps.SIZE_LEGEND, ha="center", va="bottom")

    ax.plot(t_spec, omega_smooth, color=ps.NTNU_BLUE, lw=ps.LW_PRIMARY,
            label="Magnetometer")
    ax.plot(t_imu, np.abs(wx), color=ps.WARN_RED, lw=ps.LW_SECONDARY, alpha=0.95,
            label="Gyroscope")

    peak_idx = int(np.nanargmax(omega_smooth))
    peak_t = t_spec[peak_idx]
    peak_w = float(omega_smooth[peak_idx])
    ax.annotate(
        f"peak {peak_w:.0f} rad/s",
        xy=(peak_t, peak_w), xytext=(peak_t + 12, peak_w + 8),
        fontsize=ps.SIZE_LEGEND, color=ps.NTNU_BLUE,
        ha="left", va="bottom",
        arrowprops=dict(arrowstyle="->", color=ps.NTNU_BLUE, lw=1.6,
                        shrinkA=2, shrinkB=2),
    )

    ax.set_xlim(0, 105)
    ax.set_ylim(0, max(135, peak_w * 1.2))
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Angular rate [rad/s]")
    ax.grid(True)

    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles, labels,
               loc="upper center", ncol=2,
               bbox_to_anchor=(0.5, 1.02),
               frameon=False, fontsize=ps.SIZE_LEGEND)

    fig.tight_layout(rect=(0, 0, 1, 0.93))
    OUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_PDF)
    print(f"saved {OUT_PDF}")
    print(f"  peak mag-derived spin rate: {peak_w:.1f} rad/s at t={peak_t:.1f} s")


if __name__ == "__main__":
    main()
