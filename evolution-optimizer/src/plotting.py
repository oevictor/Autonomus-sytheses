import os
import matplotlib.pyplot as plt
import math
import numpy as np

def plot_history(history, maximize, out_dir="output", filename="optimization_progress.png"):
    os.makedirs(out_dir, exist_ok=True)
    gens = list(range(len(history)))
    plt.figure(figsize=(6,4))
    label = "Best D"
    plt.plot(gens, history, marker='o')
    plt.xlabel("Generation")
    plt.ylabel(label)
    plt.title("Optimization Progress (maximize D)" if maximize else "Optimization Progress (minimize D)")
    plt.grid(True, alpha=0.3)
    out_path = os.path.join(out_dir, filename)
    plt.tight_layout()
    plt.savefig(out_path, dpi=120)
    plt.close()
    return out_path

def scherrer_D(K, lam, B, theta):
    c = math.cos(theta)
    if B <= 0 or abs(c) < 1e-12:
        return np.nan
    return (K * lam) / (B * c)

def plot_scherrer_fit(initial_params, best_params, out_dir="output"):
    """
    initial_params: (K, lam, B, theta) from user
    best_params: (K, lam, B, theta) optimized
    Produces:
      1) D vs theta (vary theta, fixed K, lam, B) initial vs best
      2) D vs B (vary B, fixed K, lam, theta) initial vs best
      3) Bar chart comparing parameter values initial vs best
    Returns list of file paths.
    """
    os.makedirs(out_dir, exist_ok=True)
    K0, lam0, B0, th0 = initial_params
    K1, lam1, B1, th1 = best_params

    # 1) D vs theta
    theta_range = np.linspace(0.01, (math.pi/2) - 0.01, 300)
    D_theta_initial = [scherrer_D(K0, lam0, B0, t) for t in theta_range]
    D_theta_best = [scherrer_D(K1, lam1, B1, t) for t in theta_range]

    plt.figure(figsize=(6,4))
    plt.plot(np.degrees(theta_range), D_theta_initial, label="Initial params", alpha=0.8)
    plt.plot(np.degrees(theta_range), D_theta_best, label="Optimized params", alpha=0.8)
    plt.axvline(math.degrees(th0), color='gray', ls='--', label="Initial θ")
    plt.axvline(math.degrees(th1), color='black', ls=':', label="Optimized θ")
    plt.xlabel("Theta (degrees)")
    plt.ylabel("D (Å)")
    plt.title("Scherrer: D vs Theta")
    plt.legend()
    plt.grid(alpha=0.3)
    path1 = os.path.join(out_dir, "scherrer_D_vs_theta.png")
    plt.tight_layout()
    plt.savefig(path1, dpi=120)
    plt.close()

    # 2) D vs B
    B_range = np.linspace(max(0.0005, min(B0, B1)*0.2), max(B0, B1)*2.0, 300)
    D_B_initial = [scherrer_D(K0, lam0, b, th0) for b in B_range]
    D_B_best = [scherrer_D(K1, lam1, b, th1) for b in B_range]

    plt.figure(figsize=(6,4))
    plt.plot(B_range, D_B_initial, label="Initial params", alpha=0.8)
    plt.plot(B_range, D_B_best, label="Optimized params", alpha=0.8)
    plt.axvline(B0, color='gray', ls='--', label="Initial B")
    plt.axvline(B1, color='black', ls=':', label="Optimized B")
    plt.xlabel("B (radians)")
    plt.ylabel("D (Å)")
    plt.title("Scherrer: D vs Peak Width B")
    plt.legend()
    plt.grid(alpha=0.3)
    path2 = os.path.join(out_dir, "scherrer_D_vs_B.png")
    plt.tight_layout()
    plt.savefig(path2, dpi=120)
    plt.close()

    # 3) Parameter comparison
    labels = ["K", "λ", "B", "θ(deg)"]
    initial_vals = [K0, lam0, B0, math.degrees(th0)]
    best_vals = [K1, lam1, B1, math.degrees(th1)]
    x = np.arange(len(labels))
    width = 0.35

    plt.figure(figsize=(6,4))
    plt.bar(x - width/2, initial_vals, width, label="Initial")
    plt.bar(x + width/2, best_vals, width, label="Optimized")
    plt.xticks(x, labels)
    plt.ylabel("Value")
    plt.title("Parameter Fit Comparison")
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    path3 = os.path.join(out_dir, "scherrer_parameter_fit.png")
    plt.tight_layout()
    plt.savefig(path3, dpi=120)
    plt.close()

    return [path1, path2, path3]