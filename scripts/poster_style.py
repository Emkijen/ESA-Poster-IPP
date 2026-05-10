"""Shared figure style for the ESA poster.

All poster figures import this module, call :func:`apply`, and set their
figure width to :data:`COLUMN_WIDTH_IN`. With this convention matplotlib
points equal the points printed on the A0 sheet (no LaTeX rescaling),
so size choices map directly to "what the viewer sees from 2 m".

A0 portrait, beamerposter ``scale=1.15`` rendered sizes (reference):
    body text     ~13 pt
    block title   ~17 pt
    caption       ~11.5 pt
    title         ~28 pt

Figure sizes here sit slightly above poster body so figures lead the eye
from distance without dwarfing surrounding prose.
"""

from __future__ import annotations

import matplotlib.pyplot as plt

# Colors — keep in lockstep with \definecolor in poster.tex
NTNU_BLUE = "#00509E"
RESULT_GREEN = "#00843D"
WARN_RED = "#C64632"
SOFT_GRAY = "#EEF2F5"
DARK_GRAY = "#232834"

# Inches of one figure included at width=0.95\columnwidth.
# Column body = .45 * paperwidth = .45 * 33.1 in;  0.95 of that = 14.15 in.
COLUMN_WIDTH_IN = 14.15

# Inches for a half-width figure (e.g. the spin plot if placed beside text).
HALF_COLUMN_IN = 0.50 * COLUMN_WIDTH_IN

# Rendered point sizes (these print at this size on A0 because we save at
# target width and LaTeX does not rescale).
SIZE_BODY = 19
SIZE_LABEL = 21
SIZE_TICK = 17
SIZE_LEGEND = 19
SIZE_ANNOTATION = 24

# Line weights tuned for 2 m readability.
LW_PRIMARY = 3.0
LW_SECONDARY = 2.0
LW_REFERENCE = 1.6


def apply() -> None:
    """Set matplotlib rcParams for poster-consistent rendering."""
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
        "font.size": SIZE_BODY,
        "axes.labelsize": SIZE_LABEL,
        "axes.titlesize": SIZE_LABEL,
        "xtick.labelsize": SIZE_TICK,
        "ytick.labelsize": SIZE_TICK,
        "legend.fontsize": SIZE_LEGEND,
        "legend.framealpha": 0.95,
        "legend.edgecolor": "0.7",
        "axes.linewidth": 1.2,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.edgecolor": DARK_GRAY,
        "axes.labelcolor": DARK_GRAY,
        "xtick.color": DARK_GRAY,
        "ytick.color": DARK_GRAY,
        "grid.alpha": 0.30,
        "grid.linewidth": 0.7,
        "savefig.bbox": "tight",
        "pdf.fonttype": 42,  # embed Type 42 fonts so text is selectable in PDF
    })
