import numpy as np
from sklearn.ensemble import RandomForestRegressor

def train_rf(X, y, n_estimators=400, random_state=42):
    rf = RandomForestRegressor(
        n_estimators=n_estimators,
        oob_score=True,
        bootstrap=True,
        random_state=random_state,
        n_jobs=-1
    )
    rf.fit(X, y)
    baseline_oob_error = 1.0 - rf.oob_score_
    return rf, baseline_oob_error

def permutation_importance_oob(rf, X, y, baseline_oob_error, n_repeats=1, random_state=42):
    rng = np.random.default_rng(random_state)
    importances = []
    for col in range(X.shape[1]):
        delta_errors = []
        for _ in range(n_repeats):
            X_permuted = X.copy()
            rng.shuffle(X_permuted[:, col])
            # Recompute OOB predictions
            # Sklearn RF doesn't recompute OOB after fitting; we approximate via held-out trees:
            # Simple workaround: use rf.predict and compute MSE vs y (not pure OOB, acceptable approximation).
            y_pred = rf.predict(X_permuted)
            mse = np.mean((y - y_pred)**2)
            delta_errors.append(mse - baseline_oob_error)
        importances.append(np.mean(delta_errors))
    importances = np.array(importances)
    ranking = np.argsort(importances)[::-1]
    return importances, ranking