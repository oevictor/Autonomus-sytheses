import math
from diversification import MaxMinDiversification

"funtions that are defined as objectives for optimization"

def scherrer_from_vector(x):
    """Scherrer equation objective.
    x = [K, lambda_, B, theta]
    Returns crystal size D = (K * lambda) / (B * cos(theta))
    
    The Scherrer equation, in X-ray diffraction and crystallography, is a formula that relates the size 
    of sub-micrometre crystallites in a solid to the broadening of a peak in a diffraction pattern.
    It is often referred to, incorrectly, as a formula for particle size measurement or analysis. 
    It is named after Paul Scherrer.[1][2] It is used in the determination of size of crystals in the form of powder.
    https://en.wikipedia.org/wiki/Scherrer_equation
    
    K--> is a dimensionless shape factor, with a value close to unity. 
    The shape factor has a typical value of about 0.9, but varies with the actual shape of the crystallite;
    ʎ is the X-ray wavelength;
    β is the line broadening at half the maximum intensity (FWHM), after subtracting the instrumental line broadening, in radians. 
    θ is the Bragg angle.

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
    
    # maybe making this more flexible by allowing arbitrary bounds and dims in the future
    
    '1': {
        'name': 'Scherrer equation (crystallite size)',
        'func': scherrer_from_vector,
        'bounds': [
            (0.5, 1.0),       # K (shape factor)
            (0.5, 2.0),       # lambda_ (Å)
            (0.001, 0.1),     # B (radians) avoid zero
            (0.0, math.pi/2)  # theta (radians)
        ],
        'dims': 4,
        'minimize': False,
        'description': 'D = (K * lambda) / (B * cos(theta))',
        'use_maxmin': True,
        'param_names': ['K', 'λ (Å)', 'B (rad)', 'θ (rad)']
    },
    '2': {
        'name': 'Sphere function (3D)',
        'func': sphere,
        'bounds': [(-5.0, 5.0)] * 3,
        'dims': 3,
        'minimize': True,
        'description': 'Simple quadratic minimization',
        'use_maxmin': False
    },
    '3': {
        'name': 'Rastrigin (3D)',
        'func': rastrigin,
        'bounds': [(-5.12, 5.12)] * 3,
        'dims': 3,
        'minimize': True,
        'description': 'Multimodal benchmark function',
        'use_maxmin': False
    },
    '4': {
        'name': 'Rosenbrock (3D)',
        'func': rosenbrock,
        'bounds': [(-2.0, 2.0)] * 3,
        'dims': 3,
        'minimize': True,
        'description': 'Valley-shaped benchmark function',
        'use_maxmin': False
    }
}

def list_objectives():
    return {k: {'name': v['name'], 'description': v['description'], 'dims': v['dims']} for k, v in OBJECTIVES.items()}

def get_objective(key):
    return OBJECTIVES.get(key)

def generate_diverse_initial_population(objective_key, num_samples=20):
    
    """Generate diverse initial population using MaxMin for given objective."""
    
    obj = get_objective(objective_key)
    if obj is None or not obj.get('use_maxmin', False):
        return None
    
    diversifier = MaxMinDiversification(obj['bounds'], num_samples=num_samples)
    diverse_samples = diversifier.generate_diverse_samples(candidates_per_iteration=100)
    
    # Create MDS visualization
    param_names = obj.get('param_names', [f'Param {i}' for i in range(obj['dims'])])
    diversifier.visualize_mds(
        output_path=f"output/{obj['name'].replace(' ', '_')}_maxmin_mds.png",
        compare_random=True,
        param_names=param_names
    )
    
    return diverse_samples