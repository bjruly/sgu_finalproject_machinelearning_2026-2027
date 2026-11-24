# -*- coding: utf-8 -*-
"""Vẽ các hình bổ sung của báo cáo cuối kỳ từ các CSV đã lưu trong outputs/ (không huấn luyện lại mô hình).

Chạy: python scripts/make_report_figures.py. Kết quả: outputs/report_figures/*.png.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import pandas as pd, numpy as np

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
R = str(ROOT) + "/"
O = str(ROOT / "outputs" / "report_figures") + "/"
Path(O).mkdir(parents=True, exist_ok=True)
plt.rcParams["font.family"] = "DejaVu Sans"
BLUE, ORANGE, GREY, GREEN, RED = "#1f77b4", "#ff7f0e", "#6b6b6b", "#2ca02c", "#d62728"
A = R + "outputs/experiments/final_test/analysis/"
MODELS = [("Persistence", "Persistence", GREY, "o"), ("Linear Regression", "Linear Regression", GREEN, "s"), ("Random Forest - tuned", "Random Forest tinh chỉnh", BLUE, "D"),
          ("Gradient Boosting - tuned", "Gradient Boosting tinh chỉnh", ORANGE, "^"), ("MLP - tuned", "MLP tinh chỉnh", RED, "v")]
vn = lambda v, d=2: f"{v:.{d}f}".replace(".", ",")


def save(fig, name):
    fig.savefig(O + name, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def box(ax, x, y, w, h, text, fc="#eaf2fa", ec=BLUE, fs=8, bold=False):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0.02,rounding_size=0.06", fc=fc, ec=ec, lw=1.3))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, fontweight="bold" if bold else "normal")


def arrow(ax, x1, y1, x2, y2):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=11, color=GREY))


# ------------------------------------------------ 1. Random Forest and Gradient Boosting
fig, ax = plt.subplots(figsize=(8.4, 5.0)); ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
ax.text(0.05, 5.75, "Random Forest (các cây độc lập, lấy trung bình)", fontsize=9.5, fontweight="bold", color=BLUE)
box(ax, 1.0, 4.45, 1.7, 0.9, "Dữ liệu train\n79 cột", fs=8)
for k, (lab, y) in enumerate([("Cây 1", 5.05), ("Cây 2", 4.45), ("... Cây 50", 3.85)]):
    box(ax, 4.0, y, 2.3, 0.5, lab + ": mẫu bootstrap,\n70% đặc trưng mỗi lần tách", fs=7)
    arrow(ax, 1.85, 4.45, 2.8, y); arrow(ax, 5.15, y, 6.5, 4.45)
box(ax, 7.2, 4.45, 1.5, 0.9, "Trung bình\n50 dự báo", fs=8)
arrow(ax, 7.95, 4.45, 8.6, 4.45)
box(ax, 9.2, 4.45, 1.0, 0.7, "ŷ", fs=11, bold=True)
ax.text(5.0, 3.15, "Cấu hình tinh chỉnh: 50 cây; mỗi lá có ít nhất 20 mẫu; max_features = 0,7; độ sâu không giới hạn", ha="center", fontsize=7.6, color=GREY)
ax.plot([0.05, 9.95], [2.75, 2.75], color="#cccccc", lw=0.8)
ax.text(0.05, 2.4, "Gradient Boosting, HistGradientBoostingRegressor (các cây nối tiếp, mỗi cây sửa sai của các cây trước)", fontsize=9.5, fontweight="bold", color=ORANGE)
box(ax, 1.0, 1.35, 1.7, 0.9, "Dự báo\nban đầu F0", ec=ORANGE, fc="#fff3e6", fs=8)
xs = [3.2, 5.1, 7.0]
labs = ["Cây 1" + chr(10) + "học phần dư", "Cây 2" + chr(10) + "học phần dư mới", "... tối đa" + chr(10) + "100 cây"]
for x, lab in zip(xs, labs):
    box(ax, x, 1.35, 1.6, 0.9, lab, ec=ORANGE, fc="#fff3e6", fs=7.4)
arrow(ax, 1.85, 1.35, 2.4, 1.35); arrow(ax, 4.0, 1.35, 4.3, 1.35); arrow(ax, 5.9, 1.35, 6.2, 1.35); arrow(ax, 7.8, 1.35, 8.55, 1.35)
box(ax, 9.2, 1.35, 1.0, 0.7, "ŷ", ec=ORANGE, fc="#fff3e6", fs=11, bold=True)
ax.text(5.0, 0.35, "ŷ = F0 + 0,069 × (tổng các cây, tối đa 100 cây); mỗi cây tối đa 127 lá, mỗi lá ít nhất 200 mẫu, phạt L2 = 1,0",
        ha="center", fontsize=7.6, color=GREY)
save(fig, "fig_trees.png")

# ------------------------------------------------ 2. by station
st = pd.read_csv(A + "final_test_error_by_station.csv", encoding="utf-8-sig")
piv = st.pivot(index="station", columns="model", values="rmse")
piv = piv.loc[piv["Random Forest - tuned"].sort_values().index]
fig, ax = plt.subplots(figsize=(8.2, 4.6)); y = np.arange(len(piv))
for k, name, c, mk in MODELS:
    ax.scatter(piv[k], y, color=c, marker=mk, s=26, label=name, zorder=3)
ax.set_yticks(y); ax.set_yticklabels(piv.index); ax.set_xlabel("RMSE test (µg/m³)")
ax.grid(axis="x", alpha=0.25); ax.spines[["top", "right"]].set_visible(False)
ax.legend(fontsize=7.6, frameon=False, loc="lower right")
save(fig, "fig_station.png")

# ------------------------------------------------ 3. month and season
mo = pd.read_csv(A + "final_test_error_by_month.csv", encoding="utf-8-sig")
se = pd.read_csv(A + "final_test_error_by_season.csv", encoding="utf-8-sig")
fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 3.8), gridspec_kw={"width_ratios": [2.2, 1]})
pm = mo.pivot(index="month", columns="model", values="rmse")
x = np.arange(len(pm))
for k, name, c, mk in MODELS:
    a1.plot(x, pm[k], color=c, marker=mk, ms=4, lw=1.4, label=name)
a1.set_xticks(x); a1.set_xticklabels([m[5:] + "/" + m[:4] for m in pm.index], fontsize=8)
a1.set_ylabel("RMSE test (µg/m³)"); a1.set_xlabel("Tháng (nhãn)"); a1.grid(axis="y", alpha=0.25); a1.spines[["top", "right"]].set_visible(False)
a1.legend(fontsize=7, frameon=False, loc="upper left")
ps = se.pivot(index="season", columns="model", values="rmse")
xs = np.arange(len(ps)); bw = 0.16
for i, (k, name, c, mk) in enumerate(MODELS):
    a2.bar(xs + (i - 2) * bw, ps[k], bw, color=c)
a2.set_xticks(xs); a2.set_xticklabels(["Thu" if s == "Autumn" else "Đông" for s in ps.index])
a2.set_xlabel("Mùa"); a2.grid(axis="y", alpha=0.25); a2.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
save(fig, "fig_month_season.png")

# ------------------------------------------------ 4. predicted vs actual and residuals (Random Forest)
pr = pd.read_csv(A + "final_test_predictions.csv", encoding="utf-8-sig")
yt, yp = pr["y_true"].values, pr["pred_random_forest_tuned"].values
fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 3.9))
hb = a1.hexbin(yt, yp, gridsize=60, bins="log", cmap="Blues", mincnt=1, extent=(0, 700, 0, 700))
a1.plot([0, 700], [0, 700], color=RED, lw=1.1, ls="--")
a1.set_xlim(0, 700); a1.set_ylim(0, 700); a1.set_xlabel("PM2.5 thực tế (µg/m³)"); a1.set_ylabel("PM2.5 dự đoán (µg/m³)")
cb = fig.colorbar(hb, ax=a1, fraction=0.046, pad=0.03); cb.set_label("số mẫu (thang log)", fontsize=8)
res = yt - yp
a2.hist(np.clip(res, -150, 150), bins=75, color=BLUE)
a2.axvline(0, color=RED, ls="--", lw=1.1)
a2.set_xlabel("Phần dư = thực tế − dự đoán (µg/m³)"); a2.set_ylabel("Số mẫu")
a2.text(0.97, 0.95, f"trung bình {vn(res.mean())}\nđộ lệch chuẩn {vn(res.std())}\n(trục cắt ở ±150)", transform=a2.transAxes, ha="right", va="top", fontsize=8)
for a in (a1, a2):
    a.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
save(fig, "fig_pred_resid.png")

# ------------------------------------------------ 5. worst case window
pr["err"] = (pr["y_true"] - pr["pred_random_forest_tuned"]).abs()
i = pr["err"].idxmax()
stn, t0 = pr.loc[i, "station"], pd.to_datetime(pr.loc[i, "target_datetime"])
w = pr[(pr["station"] == stn)].copy(); w["tt"] = pd.to_datetime(w["target_datetime"])
w = w[(w["tt"] >= t0 - pd.Timedelta(hours=48)) & (w["tt"] <= t0 + pd.Timedelta(hours=48))]
cols = {"Persistence": "pred_baseline_persistence", "Linear Regression": "pred_baseline_linreg", "Random Forest - tuned": "pred_random_forest_tuned",
        "Gradient Boosting - tuned": "pred_gradient_boosting_tuned", "MLP - tuned": "pred_mlp_tuned"}
fig, (a1, a2) = plt.subplots(2, 1, figsize=(9, 5.0), sharex=True, gridspec_kw={"height_ratios": [2.2, 1]})
a1.plot(w["tt"], w["y_true"], color="black", lw=1.8, label="Thực tế")
for k, name, c, mk in MODELS:
    a1.plot(w["tt"], w[cols[k]], color=c, lw=1.0, alpha=0.85, label=name)
a1.axvline(t0, color=GREY, ls=":", lw=1)
a1.set_ylabel("PM2.5 (µg/m³)"); a1.legend(fontsize=7, frameon=False, ncol=3, loc="lower left", bbox_to_anchor=(0, 1.0))
a2.plot(w["tt"], w["y_true"] - w[cols["Random Forest - tuned"]], color=BLUE, lw=1.2)
a2.axhline(0, color="black", lw=0.8); a2.axvline(t0, color=GREY, ls=":", lw=1)
a2.set_ylabel("Phần dư RF (µg/m³)"); a2.set_xlabel(f"Thời điểm nhãn, trạm {stn} (đường chấm: sai số lớn nhất của Random Forest)")
for a in (a1, a2):
    a.spines[["top", "right"]].set_visible(False); a.grid(alpha=0.2)
fig.autofmt_xdate(rotation=20)
fig.tight_layout()
save(fig, "fig_worst.png")
print("worst:", stn, t0, pr.loc[i, "y_true"], pr.loc[i, "pred_random_forest_tuned"])

# ------------------------------------------------ 6. MLP loss curves
lc = pd.read_csv(R + "outputs/experiments/validation_diagnostics/mlp_loss_curves.csv", encoding="utf-8-sig")
fig, axs = plt.subplots(1, 2, figsize=(9, 3.4))
seedc = {7: BLUE, 42: ORANGE, 2026: GREEN}
for a, f in zip(axs, (1, 2)):
    d = lc[(lc["fold"] == f) & (lc["diagnostic"] == "seed_stability")]
    for sd, g in d.groupby("seed"):
        a.plot(g["epoch"], g["loss_scaled_target"], color=seedc[sd], lw=1.3, label=f"seed {sd} (tối đa 40 epoch)")
    e = lc[(lc["fold"] == f) & (lc["diagnostic"] == "epoch_limit_check")]
    a.plot(e["epoch"], e["loss_scaled_target"], color="black", lw=1.0, ls="--", label="thử giới hạn 100 epoch (seed 42)")
    a.axvline(40, color=GREY, ls=":", lw=1)
    a.set_title(f"Fold {f}", fontsize=10); a.set_xlabel("Epoch"); a.spines[["top", "right"]].set_visible(False); a.grid(alpha=0.2)
    a.legend(fontsize=7, frameon=False, loc="upper right")
axs[0].set_ylabel("Loss huấn luyện (nhãn đã chuẩn hóa)")
fig.tight_layout()
save(fig, "fig_mlp_loss.png")

# ------------------------------------------------ 7. paired bootstrap CI
pu = pd.read_csv(A + "paired_model_uncertainty.csv", encoding="utf-8-sig")
short = {"Persistence": "Persistence", "Linear Regression": "Linear Regression", "Gradient Boosting - tuned": "Gradient Boosting", "MLP - tuned": "MLP"}
fig, ax = plt.subplots(figsize=(8, 2.9))
yy = np.arange(len(pu))[::-1]
for yv, (_, r) in zip(yy, pu.iterrows()):
    inc = r["ci_95_low"] <= 0 <= r["ci_95_high"]
    c = GREY if inc else BLUE
    ax.plot([r["ci_95_low"], r["ci_95_high"]], [yv, yv], color=c, lw=2.2)
    ax.scatter([r["rmse_difference_a_minus_b"]], [yv], color=c, s=28, zorder=3)
    ax.text(r["ci_95_high"] + 0.06, yv, f"{vn(r['rmse_difference_a_minus_b'])} [{vn(r['ci_95_low'])}; {vn(r['ci_95_high'])}]", va="center", fontsize=7.6)
ax.axvline(0, color="black", lw=0.9)
ax.set_yticks(yy); ax.set_yticklabels([f"RF − {short[m]}" for m in pu["model_b"]])
ax.set_xlim(-3.3, 1.7); ax.set_xlabel("Chênh lệch RMSE test của Random Forest so với mô hình còn lại (µg/m³; âm là RF tốt hơn)")
ax.spines[["top", "right"]].set_visible(False); ax.grid(axis="x", alpha=0.25)
save(fig, "fig_bootstrap.png")
print("done")
