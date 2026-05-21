# To-Do

## Poster layout (from review 2026-05-17)

Suggested order of attack: decide what content fills the free space (mostly left
column), then the two figure regenerations (those need the Rocket-Catch analysis
scripts).

- [x] **Reclaim the empty band below the title.** Added `\vspace*{-6cm}` after `\begin{frame}` to pull the columns up under the title (decided against `\keymetric` metric boxes — prefer substantive content over a layout patch). Reclaimed space is now a free band at the bottom of both columns.
- [x] **Cartesian-formulation rationale — decided against.** Briefly added a "why Cartesian" paragraph to IPP Architecture, then removed it. The poster states the other methods without justifying them, so singling out one choice for a rationale is inconsistent, and space is tight.
- [x] **Add the IMU saturation fix to Discussion.** Placed at the start of the second (full-width) paragraph: "Mounting the IMU closer to the spin axis or using a higher-range gyroscope would reduce the saturation." Not in the first paragraph (its height is fine-tuned to the spin plot) and not claiming it eliminates saturation, only reduces it.
- [x] **Rebuilt the architecture diagram.** Replaced the single-tier "Onboard algorithm" diagram with a two-tier thesis-style diagram (thesis Figure 3.1 minus the BTE block): top tier Rocket / Impact Point Prediction System / ASV, dashed zoom into the onboard container holding Navigation ESKF, IPP EKF, and Rocket and environment models. Word arrow labels, ASV naming, wrapped in `\resizebox{0.97\columnwidth}` so it cannot exceed column width. Moved from Research Objective into the IPP Architecture block.
- [ ] **Fill remaining left-column space.** ~10 cm still free below Simulation Performance. Reviewed the text for terse spots that could be expanded — concluded the text is already appropriately concise and should not be padded (restating what the plots show, or adding non-load-bearing setup detail, would make it worse). This is a figure problem: enlarge the sim figure (see figure task below), or leave the space as breathing room.
- [x] **Regenerated the simulation figure (`poster_sim_1x3.pdf`).** New `scripts/plot_poster_sim.py` pools all four trajectories' 4x100 = 400 Monte Carlo realisations and plots the median error line + an empirical 5-95th percentile band per panel. Chose the empirical percentile band over the filter's 3-sigma covariance: the line is a median (a central value), so pairing it with a covariance tail-bound was a scale mismatch (the median can never approach a 3-sigma bound). The percentile band is the spread of the same quantity as the line. The real-flight figure keeps its 3-sigma covariance — correct there, since it is a single flight, not an ensemble. Taller figure also fills the previously empty left-column space. The script chdir's to the Rocket-Catch root because its loaders use repo-root-relative paths.
- [x] **Andøya map — kept the original.** Explored alternatives (light `CartoDB.Positron` basemap with `viridis`; dark satellite with `spring`; dark satellite with `autumn`). Emil disliked all of them and decided the original `Esri.WorldImagery` + `plasma` was best, so the map is back to the original `cmap="plasma"`, `s=90`, white edges, white-underlay impact crosshair.

## Poster content

- [ ] **Trim repeated sensor-saturation mentions.** The saturation point appears in the Andøya block, Real Flight IPP Error block, Discussion, and Simulation Performance. Keep the Discussion as the definitive statement and trim the others.
- [x] **Add contact information** — added `emilkj@stud.ntnu.no` and `kristoffer.gryte@ntnu.no` under the affiliation line.
- [x] **Fix navigation figure/text mismatch** — resolved by removing the stale navigation-comparison figure from the current poster layout.

## Project housekeeping

- [x] **Updated the figure table in `CLAUDE.md`.** Replaced the stale entries with the four current poster figures (`poster_ipp_track.pdf`, `poster_ipp_error.pdf`, `poster_sim_1x3.pdf`, `poster_spin_rate.pdf`), each with its width, location and content. Also updated the column-structure description and added a note that `plot_poster_sim.py` chdir's to the Rocket-Catch root.

## Symposium logistics (ESA deadlines)

- [x] **Register for symposium by 17 May 2026** — already registered.
- [ ] **Prepare 1–2 viewgraphs for 2-minute PICO pitch** — PowerPoint preferred (PDF/Keynote also accepted). Upload via Dropbox link at least 2 days before the conference. Filename format: `Jensen_AB01_PICO` (surname + abstract reference + PICO).
- [ ] **Install poster by Monday 1 June 2026, 12:00** — early setup possible Sunday 31 May 16:00–19:00. Do not take down before Thursday 4 June 18:00.

## Thesis

- [ ] **Update reference [3]** once the master's thesis is submitted and has a final title — it currently points to an unfinished draft.

## Poster figures

- [x] **Render the geographic IPP track plot.** `figures/poster_ipp_track.pdf` is rendered and used in the Andøya Test Flight block.
