import os
import numpy as np
import matplotlib.pyplot as plt

"ploting utilities for hybrid evolution + random forest optimizer"

def _ensure_dir(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)

def plot_feature_importance(importances, ranking, out_path="output/rf_feature_importance.png"):
    "plot feature importance as bar chart"
    _ensure_dir(out_path)
    idx_sorted = ranking  # already descending
    vals = importances[idx_sorted]
    labels = [f"X{j}" for j in idx_sorted]

    plt.figure(figsize=(8, 5))
    bars = plt.bar(range(len(vals)), vals, color="#4C78A8", edgecolor="black", alpha=0.9)
    plt.xticks(range(len(vals)), labels, rotation=0)
    plt.ylabel("Δ error (permute − baseline)")
    plt.title("Permutation-based Feature Importance (higher is more important)")
    for i, b in enumerate(bars):
        plt.text(b.get_x() + b.get_width()/2, b.get_height(), f"{vals[i]:.3f}",
                 ha="center", va="bottom", fontsize=8)
    plt.tight_layout()
    plt.savefig(out_path, dpi=140)
    plt.close()
    return out_path

def plot_top2_scatter(X, y, top2_idx, out_path="output/top2_feature_scatter.png"):
    "scatter plot of dataset on top-2 important features"
    _ensure_dir(out_path)
    i, j = top2_idx
    plt.figure(figsize=(6.5, 5.5))
    sc = plt.scatter(X[:, i], X[:, j], c=y, cmap="viridis", s=28, edgecolors="k", linewidths=0.2)
    plt.xlabel(f"X{i} (scaled)")
    plt.ylabel(f"X{j} (scaled)")
    plt.title("Dataset scatter on top-2 important features")
    cb = plt.colorbar(sc)
    cb.set_label("Target (y)")
    plt.grid(alpha=0.25)
    plt.tight_layout()
    plt.savefig(out_path, dpi=140)
    plt.close()
    return out_path

def plot_partial_dependence_grid(rf, X_ref, feature_indices, best=None,
                                 n_points=200, out_path="output/partial_dependence.png"):
    """
    Simple 1D partial dependence: vary 1 feature in [0,1], fix others to X_ref.
    feature_indices: list of feature ids (e.g., top 4).
    best: optional best vector (to mark vertical line).
    """
    _ensure_dir(out_path)
    k = len(feature_indices)
    rows = int(np.ceil(k / 2))
    cols = 2 if k > 1 else 1
    plt.figure(figsize=(6.5*cols/2, 3.4*rows))

    grid = np.linspace(0, 1, n_points)
    for idx, feat in enumerate(feature_indices):
        plt.subplot(rows, cols, idx + 1)
        Xp = np.repeat(X_ref[None, :], n_points, axis=0)
        Xp[:, feat] = grid
        yp = rf.predict(Xp)
        plt.plot(grid, yp, color="#F58518", lw=2)
        if best is not None:
            xval = np.clip(best[feat], 0, 1)
            plt.axvline(xval, color="#43AA8B", ls="--", lw=1.5, label="GA best")
            plt.legend(frameon=False, fontsize=8)
        plt.xlabel(f"X{feat} (scaled)")
        plt.ylabel("Predicted y")
        plt.title(f"Partial dependence: X{feat}")
        plt.grid(alpha=0.25)

    plt.tight_layout()
    plt.savefig(out_path, dpi=140)
    plt.close()
    return out_path