# CLAUDE.md

## Project Overview

This is a LaTeX poster for the **27th ESA Symposium on European Rocket and Balloon Programmes and Related Research**.

**Title**: Real-Time Impact Point Prediction of Suborbital Rockets Using Kalman Filtering  
**Author**: Emil Killingberg Jensen  
**Affiliation**: Department of Engineering Cybernetics, NTNU. Supervisor: Kristoffer Gryte

The poster presents Emil's master's thesis work (May 2026) and is the third step in a research lineage:

1. **Gryte et al. (KriGry artikkel.pdf)** — Proof-of-concept: USV guided to live predicted impact point of an Andøya student rocket. Pre-launch ballistic IPP, guidance-state model.
2. **Meta (2025) (Admir meta thesis.pdf)** — INS-aided IPP in simulation using IMU/GNSS Kalman filtering.
3. **Jensen (2026) (Master_Thesis.pdf / this poster)** — Real-flight validation, sensor fusion (GNSS + IMU + barometer + magnetometer), Cartesian IPP EKF.

## Template Integrity

**Two posters are being produced from this shared template. The template must not be modified — only content changes are permitted.**

The following are template elements and must remain unchanged across both posters:
- `\documentclass`, `\usepackage`, and `\usetikzlibrary` lines
- `\usetheme{NTNU}` and all `\setbeamertemplate` / `\setbeamerfont` calls
- `\paperwidth` / `\paperheight` (33.1 × 46.8 in = A0)
- `\captionsetup` and caption numbering
- Font configuration (`\setmainfont` / `\setsansfont` with Arial)
- All `\definecolor` definitions (`ntnublue`, `resultgreen`, `warnred`, `softgray`, `darkgray`)
- The `\keymetric` command definition
- Column margin widths (`.052\textwidth` left gutter, `.01\textwidth` separator, `.039\textwidth` right gutter)

Content that **can and should** differ between the two posters:
- `\title`, `\author`, `\institute`
- Everything inside `\begin{frame} ... \end{frame}`

## Poster Structure

Single-file: `poster.tex`. Compiled with **XeLaTeX** (first line `% !TEX program = XeLaTeX`).

- Format: A0 portrait (33.1 × 46.8 in), beamerposter with NTNU theme
- Font: Arial (from `resources/fonts/`)
- Two columns:
  - **Left**: Motivation → Method (ESKF) → Method (Cartesian IPP) → Results (Navigation Filter)
  - **Right**: Results (Real-Flight IPP) → Challenges & Outlook → References

### Current figures (in `figures/`)

| File | Used at width | Content |
|------|--------------|---------|
| `poster_real_flight_rmse.pdf` | 0.80 col | Navigation filter comparison (GNSS position only vs. GNSS position+velocity); note: text refers to baro+mag improvement — mismatch to fix |
| `sim_vs_real_ipp_combined.pdf` | 0.90 col | Real-flight vs. simulation IPP error, 3 panels (horizontal, along-track, cross-track) |
| `poster_spin_limit.pdf` | 0.62 col | Magnetometer oscillations revealing ~113 rad/s peak spin rate |

## Framing

This poster presents the system and what it achieves — not a comparison or improvement story. Do not frame results as "X% improvement over baseline" or "reduced from A to B". Present what the system produces: actual error numbers, actual filter performance, actual flight behaviour.

## Writing Style

- Do not use dashes, colons, or semicolons to bind sentences together. Write separate, complete sentences instead.

## Build & Review Workflow

After every edit to `poster.tex`:

1. Compile: `xelatex poster.tex` (run twice if cross-references change)
2. Check the compile output for `Overfull \vbox` warnings — these mean content overflows the page
3. Read `poster.pdf` (page 1) and visually verify that all blocks are fully visible and nothing is clipped at the bottom of either column
4. If the right column overflows, reduce figure widths or trim text; if the left column has excess space, consider adding content (e.g. references, acknowledgements)

Requires XeLaTeX (not pdflatex).

## Symposium Requirements (ESA)

- **Max poster size**: 96 × 138 cm (W × H). A0 (84.1 × 118.9 cm) is compliant — do not resize.
- **Install by**: Monday 1 June 2026, 12:00 (early setup: Sunday 31 May 16:00–19:00)
- **Take down after**: Thursday 4 June 2026, 18:00
- **PICO pitch**: 2-minute oral intro + 1–2 viewgraphs. Upload via Dropbox ≥2 days before conference. Filename: `Jensen_<AbstractRef>_PICO`. PowerPoint preferred.
- **Registration deadline**: 17 May 2026 (separate from abstract acceptance)

## Figures Source

All thesis figures live in `C:/Source/Rocket-Catch/master_thesis/figures/`. Key files relevant to the poster:

- **Navigation comparison**: `nav_*_gnss_vs_gnss_barometer_magnetometer_comparison.pdf` (four flights)
- **IPP simulation per flight**: `ipp_sim_*_combined.pdf`
- **IPP combined overview**: `ipp_mc_combined_horizontal.pdf`, `ipp_model_comparison.pdf`
- **Real vs. sim IPP**: `sim_vs_real_ipp_combined.pdf`, `sim_vs_real_ipp_error.pdf`
- **Spin rate**: `real_spin_rate.pdf`
- **IMU channels/biases**: `real_imu_channels.pdf`, `real_imu_biases.pdf`

The Rocket-Catch codebase (`C:/Source/Rocket-Catch/`) generates these figures. See its CLAUDE.md for how to regenerate them. Available trajectories: 12_11_2024, 05_03_2025, 06_04_2025, 15_02_2025.

New poster-specific figures (tighter layout, no thesis-style titles) should be generated by adapting the analysis scripts in `C:/Source/Rocket-Catch/dev/src/analysis/`.

## Key Scientific Content

**Navigation**: Error-State Kalman Filter (ESKF) fusing GNSS, IMU, barometer, magnetometer. Adding baro + mag reduced coast-phase 3D RMSE from 42.36 m → 8.20 m on real flight.

**IPP model** (Cartesian EKF): state = [x, y, z, vx, vy, vz] in NED. Equations:
```
ṗ = v
v̇ = g − K_D(v − v_wind) + a_thrust
```
Avoids course-angle wrapping and ground-speed singularities near apogee. Initializes directly from ESKF covariance.

**Key result**: 84% average full-flight IPP RMSE reduction vs. guidance-state baseline; 45.3 m mean RMSE across four simulated trajectories (66–92% per trajectory).

**Limitation**: Peak spin rate ~113 rad/s during powered flight exceeds gyroscope range → IMU saturation. Fix: move IMU closer to spin axis, use higher-range gyroscope.

**Rocket**: Andøya Space Education Mongoose 98 (customized), 271 cm long, 10.3 cm diameter, carbon fiber, Pro98 motor. Mass ~19.6 kg at lift-off.
