import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

adult_url = "https://raw.githubusercontent.com/MICA-MNI/ENIGMA/master/enigmatoolbox/datasets/summary_statistics/adhdadult_case-controls_CortThick.csv"
adult = pd.read_csv(adult_url)

def fdr_bh(pvals):
    pvals = np.asarray(pvals)
    n = len(pvals)
    order = np.argsort(pvals)
    ranked = pvals[order]
    adjusted = ranked * n / np.arange(1, n + 1)
    adjusted = np.minimum.accumulate(adjusted[::-1])[::-1]
    adjusted = np.clip(adjusted, 0, 1)
    result = np.empty(n)
    result[order] = adjusted
    return result

adult["fdr_q"] = fdr_bh(adult["pobs"])
n_uncorrected = (adult["pobs"] < 0.05).sum()
n_fdr = (adult["fdr_q"] < 0.05).sum()
print(f"Regions p<0.05 uncorrected: {n_uncorrected} / {len(adult)}")
print(f"Regions surviving FDR q<0.05: {n_fdr} / {len(adult)}")

top10 = adult.reindex(adult.d_icv.abs().sort_values(ascending=False).index).head(10)
colors = ["#d62728" if p < 0.05 else "#1f77b4" for p in top10["pobs"]]

plt.figure(figsize=(8, 5))
plt.barh(top10["Structure"], top10["d_icv"], color=colors)
plt.axvline(0, color="grey", linewidth=0.5)
plt.xlabel("Cohen's d")
plt.title("Top 10 brain regions by effect size (adult ADHD vs. controls)")
plt.gca().invert_yaxis()
red = plt.Line2D([0], [0], color="#d62728", lw=6, label="p < 0.05 (uncorrected)")
blue = plt.Line2D([0], [0], color="#1f77b4", lw=6, label="not significant")
plt.legend(handles=[red, blue], loc="lower right")
plt.tight_layout()
plt.savefig("plot.png")
print("Saved plot.png")
