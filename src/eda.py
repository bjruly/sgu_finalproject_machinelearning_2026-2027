"""Reproduce additional raw-data EDA used by the report: ACF, log plots and wind."""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from src.data_loader import PROJECT_ROOT, load_data


def eda_tables(data, max_lag=48):
    if max_lag < 1:
        raise ValueError("max_lag must be positive.")
    data = data.sort_values(["station", "datetime"]).copy()
    if data.duplicated(["station", "datetime"]).any():
        raise ValueError("Duplicate station-hour keys.")
    gaps = data.groupby("station").datetime.diff().dropna()
    if not gaps.eq(pd.Timedelta(hours=1)).all():
        raise ValueError("ACF requires continuous hourly rows; retain missing measurements.")
    acf_rows = []
    for station, part in data.groupby("station", sort=True):
        series = part["PM2.5"]
        for lag in range(1, max_lag + 1):
            aligned = pd.concat([series, series.shift(lag)], axis=1).dropna()
            acf_rows.append({"station": station, "lag_hours": lag,
                             "correlation": series.autocorr(lag), "n_pairs": len(aligned)})
    by_station = pd.DataFrame(acf_rows)
    acf = by_station.groupby("lag_hours").agg(
        mean_station_correlation=("correlation", "mean"),
        std_station_correlation=("correlation", "std"),
        n_stations=("correlation", "count"), n_pairs=("n_pairs", "sum"),
    ).reset_index()
    wind = data.groupby("wd", observed=True)["PM2.5"].agg(
        n="count", mean_pm25="mean", median_pm25="median").reset_index()
    wind = wind.sort_values("mean_pm25", ascending=False)
    bins = [-np.inf, .5, 1, 2, 3, 5, np.inf]
    labels = ["<=0.5", "(0.5,1]", "(1,2]", "(2,3]", "(3,5]", ">5"]
    speed = data.assign(wind_speed_group=pd.cut(data.WSPM, bins, labels=labels, right=True))
    speed = speed.groupby("wind_speed_group", observed=True)["PM2.5"].agg(
        n="count", mean_pm25="mean", median_pm25="median").reset_index()
    return {"pm25_acf_by_station": by_station, "pm25_acf": acf,
            "pm25_by_wind_direction": wind, "pm25_by_wind_speed": speed}


def export_eda(data, output_dir=None):
    import matplotlib.pyplot as plt

    output_dir = Path(output_dir or PROJECT_ROOT / "outputs" / "eda")
    tables_dir, figures_dir = output_dir / "tables", output_dir / "figures"
    tables_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)
    tables = eda_tables(data)
    for name, table in tables.items():
        table.to_csv(tables_dir / f"{name}.csv", index=False, encoding="utf-8-sig")
    values = data["PM2.5"].dropna().to_numpy()
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    axes[0].hist(values, bins=80)
    axes[0].set(xlabel="PM2.5 (µg/m³)", ylabel="Observed measurements", title="Raw PM2.5: linear scale")
    axes[1].hist(values[values > 0], bins=np.geomspace(values[values > 0].min(), values.max(), 60))
    axes[1].set_xscale("log")
    axes[1].set(xlabel="PM2.5 (µg/m³; log scale)", title="Positive raw PM2.5")
    fig.tight_layout()
    fig.savefig(figures_dir / "pm25_distribution_linear_log.png", dpi=150)
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(10, 4))
    acf = tables["pm25_acf"]
    colors = ["#e18a35" if k in {1, 2, 3, 6, 12, 24} else "#39798e" for k in acf.lag_hours]
    ax.bar(acf.lag_hours, acf.mean_station_correlation, color=colors)
    ax.set(xlabel="Lag (hours)", ylabel="Mean station Pearson correlation", title="Raw PM2.5 autocorrelation")
    fig.tight_layout()
    fig.savefig(figures_dir / "pm25_autocorrelation.png", dpi=150)
    plt.close(fig)
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    tables["pm25_by_wind_direction"].plot.bar(x="wd", y="mean_pm25", ax=axes[0], legend=False)
    tables["pm25_by_wind_speed"].plot.bar(x="wind_speed_group", y="mean_pm25", ax=axes[1], legend=False)
    for ax in axes:
        ax.set_ylabel("Mean observed PM2.5 (µg/m³)")
    axes[0].set_title("Wind direction")
    axes[1].set_title("Wind speed (m/s), right-closed groups")
    fig.tight_layout()
    fig.savefig(figures_dir / "pm25_wind_relationships.png", dpi=150)
    plt.close(fig)
    return tables


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    tables = export_eda(load_data(), args.output_dir)
    print(tables["pm25_acf"].query("lag_hours in [1,2,3,6,12,24]").to_string(index=False))
    print("Raw-data EDA exported; source measurements and targets were not imputed.")


if __name__ == "__main__":
    main()

