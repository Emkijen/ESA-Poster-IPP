# To-Do

## Poster content

- [x] **Add contact information** — added `emilkj@stud.ntnu.no` and `kristoffer.gryte@ntnu.no` under the affiliation line.
- [ ] **Fix navigation figure/text mismatch** — `poster_real_flight_rmse.pdf` shows *GNSS position only* vs *GNSS position + velocity* (the joint update), but the ESKF block text says barometer and magnetometer aiding drove the 42.36 → 8.20 m improvement. Either swap the figure for the correct baro+mag comparison (`nav_*_gnss_vs_gnss_barometer_magnetometer_comparison.pdf` from Rocket-Catch) or correct the text to match the figure.

## Symposium logistics (ESA deadlines)

- [x] **Register for symposium by 17 May 2026** — already registered.
- [ ] **Prepare 1–2 viewgraphs for 2-minute PICO pitch** — PowerPoint preferred (PDF/Keynote also accepted). Upload via Dropbox link at least 2 days before the conference. Filename format: `Jensen_AB01_PICO` (surname + abstract reference + PICO).
- [ ] **Install poster by Monday 1 June 2026, 12:00** — early setup possible Sunday 31 May 16:00–19:00. Do not take down before Thursday 4 June 18:00.

## Thesis

- [ ] **Update reference [3]** once the master's thesis is submitted and has a final title — it currently points to an unfinished draft.

## Poster figures

- [ ] **Render the geographic IPP track plot.** Data is already staged at `data/ipp_track.csv` and `data/ipp_track_meta.csv`. Run `pip install contextily` once, then `python scripts/plot_poster_ipp_track.py` produces `figures/poster_ipp_track.pdf` (rocket ground track + per-step predicted impacts coloured by flight time + actual splashdown bullseye, all on Esri satellite tiles). Then decide layout — likely replaces the 1×3 error figure in the Real-Flight Validation block.
