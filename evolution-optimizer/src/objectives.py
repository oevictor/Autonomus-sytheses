import math

def scherrer_from_vector(x):
    """Scherrer equation objective.
    x = [K, lambda_, B, theta]
    Returns crystal size D = (K * lambda) / (B * cos(theta))
    """
    K, lambda_, B, theta = x
    # Protect against invalid cos(theta) or zero B
    cos_t = math.cos(theta)
    if B <= 0 or abs(cos_t) < 1e-12:
        return float('inf')
    return (K * lambda_) / (B * cos_t)

def sphere(x):
    """Simple sphere function (minimize)."""
    return sum(v * v for v in x)

def rastrigin(x):
    """Rastrigin function (minimize)."""
    A = 10
    return A * len(x) + sum((v * v - A * math.cos(2 * math.pi * v)) for v in x)

def rosenbrock(x):
    """Rosenbrock function (minimize)."""
    return sum(100.0 * (x[i+1] - x[i]**2)**2 + (x[i] - 1)**2 for i in range(len(x)-1))

# Registry of available objectives
OBJECTIVES = {
    '1': {
        'name': 'Scherrer equation (crystallite size)',
        'func': scherrer_from_vector,
        # bounds: (min, max) for each variable in the vector [K, lambda_, B, theta]
        # reasonable defaults (user can change later)
        'bounds': [
            (0.5, 1.0),       # K (shape factor)
            (0.5, 2.0),       # lambda_ (Å)
            (0.001, 0.1),     # B (radians) avoid zero
            (0.0, math.pi/2)  # theta (radians)
        ],
        'dims': 4,
        'minimize': False,  # typically one might want to estimate D (we return D); optimization goal depends on use-case
        'description': 'D = (K * lambda) / (B * cos(theta))'
    },
    '2': {
        'name': 'Sphere function (3D)',
        'func': sphere,
        'bounds': [(-5.0, 5.0)] * 3,
        'dims': 3,
        'minimize': True,
        'description': 'Simple quadratic minimization'
    },
    '3': {
        'name': 'Rastrigin (3D)',
        'func': rastrigin,
        'bounds': [(-5.12, 5.12)] * 3,
        'dims': 3,
        'minimize': True,
        'description': 'Multimodal benchmark function'
    },
    '4': {
        'name': 'Rosenbrock (3D)',
        'func': rosenbrock,
        'bounds': [(-2.0, 2.0)] * 3,
        'dims': 3,
        'minimize': True,
        'description': 'Valley-shaped benchmark function'
    }
}

def list_objectives():
    return {k: {'name': v['name'], 'description': v['description'], 'dims': v['dims']} for k, v in OBJECTIVES.items()}

def get_objective(key):
    return OBJECTIVES.get(key)