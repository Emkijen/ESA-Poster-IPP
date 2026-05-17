# To-Do

## Poster layout (from review 2026-05-17)

Suggested order of attack: title-gap `\keymetric` fix first (biggest visual win, also
helps column balance), then column balance, then the two figure regenerations (those
need the Rocket-Catch analysis scripts).

- [ ] **Fill the empty band below the title.** Large white gap between the affiliation line and the first blocks makes the title float. The template's `\keymetric` command is defined but unused — add 2-3 metric boxes here (e.g. "45.3 m sim RMSE", "real-flight validated", "113 rad/s peak spin"). Highest-impact quick win.
- [ ] **Balance the columns.** Left column ends short at the simulation plots while the right column runs to References. Options: move References to the left, add an Acknowledgements block, or enlarge the diagram/sim figure.
- [ ] **Clean up the simulation plots (`poster_sim_1x3.pdf`).** Four overlapping translucent 3-sigma bands wash into an indistinct tan blur, and bands extend well past the y-axis range. Plot fewer bands, use a single aggregate envelope, or clip the y-axis so median lines stay readable at poster distance.
- [ ] **Improve the Andøya map (`poster_ipp_track.pdf`).** At 0.38 column width the purple IPP-prediction dots are hard to read against dark satellite imagery. Use a brighter marker or a larger/tighter crop.

## Poster content

- [ ] **Trim repeated sensor-saturation mentions.** The saturation point appears in the Andøya block, Real Flight IPP Error block, Discussion, and Simulation Performance. Keep the Discussion as the definitive statement and trim the others.
- [x] **Add contact information** — added `emilkj@stud.ntnu.no` and `kristoffer.gryte@ntnu.no` under the affiliation line.
- [x] **Fix navigation figure/text mismatch** — resolved by removing the stale navigation-comparison figure from the current poster layout.

## Project housekeeping

- [ ] **Update the figure table in `CLAUDE.md`.** It lists `poster_real_flight_rmse.pdf`, `sim_vs_real_ipp_combined.pdf`, `poster_spin_limit.pdf`, but the poster now uses `poster_sim_1x3.pdf`, `poster_ipp_track.pdf`, `poster_ipp_error.pdf`, `poster_spin_rate.pdf`.

## Symposium logistics (ESA deadlines)

- [x] **Register for symposium by 17 May 2026** — already registered.
- [ ] **Prepare 1–2 viewgraphs for 2-minute PICO pitch** — PowerPoint preferred (PDF/Keynote also accepted). Upload via Dropbox link at least 2 days before the conference. Filename format: `Jensen_AB01_PICO` (surname + abstract reference + PICO).
- [ ] **Install poster by Monday 1 June 2026, 12:00** — early setup possible Sunday 31 May 16:00–19:00. Do not take down before Thursday 4 June 18:00.

## Thesis

- [ ] **Update reference [3]** once the master's thesis is submitted and has a final title — it currently points to an unfinished draft.

## Poster figures

- [x] **Render the geographic IPP track plot.** `figures/poster_ipp_track.pdf` is rendered and used in the Andøya Test Flight block.
