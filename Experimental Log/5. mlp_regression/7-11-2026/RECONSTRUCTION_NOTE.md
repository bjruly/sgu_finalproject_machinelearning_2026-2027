# Supplementary reconstructed snapshot

- Run date: 19-11-2026
- Feature set: v2 — PM2.5 hiện tại + lag + rolling
- This is a newly executed supplementary run, not an authentic recovered historical version.
- All model scores are newly calculated on the same five chronological expanding-window validation folds. The final test set was not used.
- Heavy row-level OOF prediction CSVs are omitted; fold metrics and figures are included.
- Dataset version: `beijing_air_quality_standardized.csv; ffill<=6h; lags=1/2/3/6/12/24; rolling=6/24; features=v2 (PM2.5 hiện tại + lag + rolling); supplementary run 19-11-2026`
- Runtime environment: Python 3.13.5, scikit-learn 1.8.0, pandas 2.2.3.
