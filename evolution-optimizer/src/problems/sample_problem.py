import numpy as np
import math

def scherrer_equation(K, lambda_val, B, theta):
    """Scherrer equation: D = (K * lambda) / (B * cos(theta))"""
    cos_t = math.cos(theta)
    if B <= 0 or abs(cos_t) < 1e-12:
        return np.nan
    return (K * lambda_val) / (B * cos_t)

def generate_synthetic_scherrer_data(num_points=20, noise_level=0.05):
    """
    Generate synthetic XRD-like data for Scherrer equation fitting.
    Returns:
        theta_data: array of Bragg angles (radians)
        D_measured: array of "measured" crystallite sizes with noise
        true_params: dict with true values of K, lambda, B used to generate data
    """
    # True underlying parameters
    true_K = 0.9
    true_lambda = 1.54  # Å (Cu Kα)
    true_B = 0.015      # radians (FWHM)
    
    # Generate theta values (typical XRD range: 10-80 degrees)
    theta_deg = np.linspace(10, 80, num_points)
    theta_data = np.radians(theta_deg)
    
    # Calculate "true" D values using Scherrer equation
    D_true = np.array([scherrer_equation(true_K, true_lambda, true_B, t) 
                       for t in theta_data])
    
    # Add measurement noise
    noise = np.random.normal(0, noise_level * np.mean(D_true), num_points)
    D_measured = D_true + noise
    
    true_params = {
        'K': true_K,
        'lambda': true_lambda,
        'B': true_B
    }
    
    return theta_data, D_measured, true_params

def evaluate_solution(solution):
    """
    Fitness function for genetic algorithm.
    solution = [K, lambda, B]
    Returns: Mean squared error between predicted and measured D values.
    Lower is better (minimization problem).
    """
    K, lambda_val, B = solution
    
    # Generate or load synthetic data (cached globally to avoid regeneration)
    if not hasattr(evaluate_solution, 'cached_data'):
        theta_data, D_measured, true_params = generate_synthetic_scherrer_data()
        evaluate_solution.cached_data = (theta_data, D_measured, true_params)
    
    theta_data, D_measured, true_params = evaluate_solution.cached_data
    
    # Predict D for each theta using candidate parameters
    D_predicted = np.array([scherrer_equation(K, lambda_val, B, t) 
                           for t in theta_data])
    
    # Calculate mean squared error
    mse = np.mean((D_predicted - D_measured) ** 2)
    
    return mse

def get_problem_bounds():
    """Return reasonable bounds for [K, lambda, B]"""
    return [
        (0.5, 1.2),      # K (shape factor)
        (1.0, 2.0),      # lambda (Å)
        (0.005, 0.05)    # B (radians)
    ]

def plot_fit_comparison(best_solution):
    """
    Plot the fitted Scherrer curve vs measured data.
    best_solution = [K, lambda, B] from genetic algorithm
    """
    import matplotlib.pyplot as plt
    
    theta_data, D_measured, true_params = evaluate_solution.cached_data
    K_fit, lambda_fit, B_fit = best_solution
    
    # Generate fine theta grid for smooth curves
    theta_fine = np.linspace(theta_data[0], theta_data[-1], 200)
    
    # True curve
    D_true_fine = [scherrer_equation(true_params['K'], true_params['lambda'], 
                                     true_params['B'], t) for t in theta_fine]
    
    # Fitted curve
    D_fit_fine = [scherrer_equation(K_fit, lambda_fit, B_fit, t) 
                  for t in theta_fine]
    
    plt.figure(figsize=(8, 5))
    plt.scatter(np.degrees(theta_data), D_measured, 
                label='Measured data (with noise)', alpha=0.6, s=50)
    plt.plot(np.degrees(theta_fine), D_true_fine, 
             label=f'True: K={true_params["K"]:.2f}, λ={true_params["lambda"]:.2f}, B={true_params["B"]:.4f}',
             linestyle='--', linewidth=2)
    plt.plot(np.degrees(theta_fine), D_fit_fine, 
             label=f'GA Fit: K={K_fit:.2f}, λ={lambda_fit:.2f}, B={B_fit:.4f}',
             linewidth=2)
    
    plt.xlabel('2θ (degrees)')
    plt.ylabel('Crystallite Size D (Å)')
    plt.title('Scherrer Equation: GA Fit vs True Parameters')
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    
    import os
    os.makedirs("output", exist_ok=True)
    out_path = "output/scherrer_fit_comparison.png"
    plt.savefig(out_path, dpi=120)
    plt.close()
    
    return out_path