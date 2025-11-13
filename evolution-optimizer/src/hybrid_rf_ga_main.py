import numpy as np
from data_synthesis import generate_synthetic_dataset, get_variable_bounds
from models.random_forest_feature_importance import train_rf, permutation_importance_oob
from optimizers.hybrid_ga import HybridGA
from plotting_hybrid import (
    plot_feature_importance,
    plot_top2_scatter,
    plot_partial_dependence_grid,
)

def main():
    print("Hybrid RF + GA Optimization (Synthetic Synthesis Data)")
    # 1. Data
    X, y, scaler_X = generate_synthetic_dataset()
    bounds = get_variable_bounds()

    # 2. Train RF
    rf, baseline_oob_err = train_rf(X, y)
    print(f"Baseline OOB proxy error: {baseline_oob_err:.6f}")

    # 3. Permutation importance
    importances, ranking = permutation_importance_oob(rf, X, y, baseline_oob_err)
    print("\nFeature importance (Δ error, higher = more impact):")
    for rank_pos, var_idx in enumerate(ranking):
        print(f"Rank {rank_pos+1}: Var {var_idx}  ΔOOB≈ {importances[var_idx]:.6f}")

    # Plots: feature importance and top-2 scatter
    fi_path = plot_feature_importance(importances, ranking, out_path="output/rf_feature_importance.png")
    print(f"Feature importance plot: {fi_path}")
    top2 = ranking[:2] if len(ranking) >= 2 else ranking[:1]
    if len(top2) == 2:
        sc_path = plot_top2_scatter(X, y, top2, out_path="output/top2_feature_scatter.png")
        print(f"Top-2 feature scatter: {sc_path}")

    # 4. Mutation weights (positive shift & ReLU)
    pos_importances = np.maximum(importances, 0)
    if pos_importances.sum() == 0:
        weights = np.ones_like(pos_importances) / len(pos_importances)
    else:
        weights = pos_importances / pos_importances.sum()

    # 5. Optional: adjust bounds (wider for important vars)
    adjusted_bounds = []
    widen_factor = 0.15
    for i, (lo, hi) in enumerate(bounds):
        span = hi - lo
        expand = widen_factor * weights[i]
        new_lo = max(0.0, lo - span * expand)
        new_hi = min(1.0, hi + span * expand)
        adjusted_bounds.append((new_lo, new_hi))

    # 6. GA using RF as surrogate fitness
    ga = HybridGA(
        population_size=60,
        generations=160,
        base_mutation_rate=0.05,
        crossover_rate=0.75,
        elitism=3,
        variable_mutation_weights=weights
    )
    result = ga.run(model=rf, bounds=adjusted_bounds)

    best = result["best_solution"]
    predicted_yield = result["best_fitness"]

    print("\nOptimized parameter vector (scaled 0-1):")
    print([f"{v:.4f}" for v in best])
    print(f"Predicted yield (RF): {predicted_yield:.4f}")

    # 7. Simple progress plot
    try:
        import matplotlib.pyplot as plt
        import os
        os.makedirs("output", exist_ok=True)
        plt.figure(figsize=(6,4))
        plt.plot(result["history"], marker='o')
        plt.xlabel("Generation")
        plt.ylabel("Best predicted yield")
        plt.title("GA Progress (RF surrogate)")
        plt.grid(alpha=0.3)
        out_path = "output/hybrid_ga_progress.png"
        plt.tight_layout()
        plt.savefig(out_path, dpi=120)
        plt.close()
        print(f"Progress plot saved: {out_path}")

        # Partial dependence on top important variables (mark GA best)
        X_ref = np.median(X, axis=0)
        topk = ranking[:4] if len(ranking) >= 4 else ranking
        pd_path = plot_partial_dependence_grid(rf, X_ref, list(topk), best=best,
                                               out_path="output/partial_dependence.png")
        print(f"Partial dependence plot: {pd_path}")
    except Exception as e:
        print(f"Plot skipped: {e}")

    # 8. Report importance again
    print("\nFeature importance ranking (index => importance):")
    print(list(zip(range(len(importances)), importances)))

if __name__ == "__main__":
    main()