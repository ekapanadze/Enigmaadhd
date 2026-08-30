import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

adult_url = "https://raw.githubusercontent.com/MICA-MNI/ENIGMA/master/enigmatoolbox/datasets/summary_statistics/adhdadult_case-controls_CortThick.csv"
adolescent_url = "https://raw.githubusercontent.com/MICA-MNI/ENIGMA/master/enigmatoolbox/datasets/summary_statistics/adhdadolescent_case-controls_CortThick.csv"

adult = pd.read_csv(adult_url)
adolescent = pd.read_csv(adolescent_url)

merged = adult[["Structure", "d_icv"]].merge(
    adolescent[["Structure", "d_icv"]],
    on="Structure",
    suffixes=("_adult", "_adolescent")
)

merged["diff"] = merged["d_icv_adult"] - merged["d_icv_adolescent"]
merged["abs_diff"] = merged["diff"].abs()

correlation = merged["d_icv_adult"].corr(merged["d_icv_adolescent"])
print(f"Correlation between adult and adolescent effect sizes: {correlation:.2f}")

print("\nTop 5 regions where adult vs adolescent effects diverge most:")
print(merged.sort_values("abs_diff", ascending=False)[["Structure", "d_icv_adult", "d_icv_adolescent", "diff"]].head())

lims = [-0.35, 0.35]

# static version (kept as fallback / for the analysis script reference)
plt.figure(figsize=(6, 6))
plt.scatter(merged["d_icv_adolescent"], merged["d_icv_adult"], alpha=0.7)
plt.axhline(0, color="grey", linewidth=0.5)
plt.axvline(0, color="grey", linewidth=0.5)
plt.plot(lims, lims, linestyle="--", color="red", linewidth=1, label="equal effect line")
plt.xlabel("Adolescent Cohen's d")
plt.ylabel("Adult Cohen's d")
plt.title("ADHD cortical thickness effects: adolescent vs adult")
plt.legend()
plt.tight_layout()
plt.savefig("age_comparison.png")
print("\nSaved age_comparison.png")

# interactive version
hover = [
    f"{s}<br>Adult d: {a:.3f}<br>Adolescent d: {b:.3f}"
    for s, a, b in zip(merged["Structure"], merged["d_icv_adult"], merged["d_icv_adolescent"])
]

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=merged["d_icv_adolescent"], y=merged["d_icv_adult"],
    mode="markers", marker=dict(size=8, color="#1f77b4", opacity=0.7),
    hovertext=hover, hoverinfo="text", name="brain region"
))
fig.add_trace(go.Scatter(
    x=lims, y=lims, mode="lines",
    line=dict(color="red", dash="dash", width=1),
    name="equal effect line"
))
fig.update_layout(
    title=f"ADHD cortical thickness effects: adolescent vs adult (r = {correlation:.2f})",
    xaxis_title="Adolescent Cohen's d",
    yaxis_title="Adult Cohen's d",
    template="plotly_white",
    height=500,
)
fig.write_html("age_comparison_interactive.html", include_plotlyjs="cdn")
print("Saved age_comparison_interactive.html")
