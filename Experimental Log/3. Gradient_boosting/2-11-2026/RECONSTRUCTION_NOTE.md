# Supplementary reconstructed snapshot

- Run date: 19-11-2026
- Feature set: v1 — PM2.5 hiện tại
- This is a newly executed supplementary run, not an authentic recovered historical version.
- Validation uses the same five expanding-window chronological folds. The final test set was not used for tuning or evaluation.
- Row-level OOF prediction CSV was omitted to keep the repository size manageable; fold metrics and figures are included.
- Dataset version: `beijing_air_quality_standardized.csv; ffill<=6h; lags=1/2/3/6/12/24; rolling=6/24; features=v1 (Chỉ PM2.5 hiện tại); supplementary run 19-11-2026`
- Runtime environment: Python 3.13.5, scikit-learn 1.8.0, pandas 2.2.3.
