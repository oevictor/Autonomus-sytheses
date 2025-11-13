import numpy as np
from sklearn.preprocessing import MinMaxScaler

def generate_synthetic_dataset(n_samples=400, noise=0.02, random_state=42):
    rng = np.random.default_rng(random_state)
    # 9 synthesis variables (X)
    X = rng.uniform(0, 1, size=(n_samples, 9))
    # Hidden nonlinear relationship (choose a few dominant vars)
    y = (
        3.5 * X[:, 0]**0.7 +
        2.2 * np.sin(2 * np.pi * X[:, 3]) +
        1.8 * X[:, 5]**2 -
        1.2 * X[:, 2] * X[:, 6] +
        0.9 * np.sqrt(X[:, 8]) +
        0.5 * X[:, 1] +
        0.3 * X[:, 4] * X[:, 7]
    )
    y = y + rng.normal(0, noise, size=n_samples)
    y = y.reshape(-1, 1)
    # Scale X to [0,1], keep y as-is or scale if desired
    scaler_X = MinMaxScaler()
    X_scaled = scaler_X.fit_transform(X)
    return X_scaled, y.ravel(), scaler_X

def get_variable_bounds():
    # All variables in [0,1] after scaling
    return [(0.0, 1.0)] * 9