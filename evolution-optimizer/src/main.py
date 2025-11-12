import sys
import inspect
import math
from interface import UserInterface
from optimizers.genetic_algorithm import GeneticAlgorithm
from optimizers.differential_evolution import DifferentialEvolution
from objectives import list_objectives, get_objective
from plotting import plot_history, plot_scherrer_fit
from problems.sample_problem import evaluate_solution, get_problem_bounds, plot_fit_comparison

def _prepare_kwargs(cls, params):
    """Return kwargs matching cls.__init__ parameter names."""
    sig = inspect.signature(cls.__init__)
    if any(p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values()):
        return params.copy()
    
    aliases = {'max_generations': 'generations'}
    allowed = [name for name, p in sig.parameters.items()
               if name != 'self' and p.kind in (inspect.Parameter.POSITIONAL_OR_KEYWORD, 
                                                inspect.Parameter.KEYWORD_ONLY)]
    out = {}
    for name in allowed:
        if name in params:
            out[name] = params[name]
        else:
            for alias, actual in aliases.items():
                if actual == name and alias in params:
                    out[name] = params[alias]
                    break
    return out

def main():
    ui = UserInterface()
    
    print("=== Scherrer Equation Fitting with Genetic Algorithm ===")
    print("\nThis example will fit synthetic XRD data using the Scherrer equation.")
    print("The GA will optimize parameters K, λ, and B to minimize prediction error.\n")
    
    # Use sample problem (Scherrer fitting)
    fitness_fn = evaluate_solution
    bounds = get_problem_bounds()
    minimize = True  # We're minimizing MSE
    
    ui.display_options()
    choice = sys.argv[1].strip() if len(sys.argv) > 1 else ui.get_user_input()
    
    try:
        if choice == '1':
            params = ui.get_algorithm_params('1')
            ga_params = {
                'population_size': params.get('population_size', 50),
                'mutation_rate': params.get('mutation_rate', 0.02),
                'crossover_rate': params.get('crossover_rate', 0.7),
                'max_generations': params.get('max_generations', 150)
            }
            ga_kwargs = _prepare_kwargs(GeneticAlgorithm, ga_params)
            ga = GeneticAlgorithm(**ga_kwargs)
            result = ga.run(fitness_fn, bounds, minimize=minimize)
            
        elif choice == '2':
            params = ui.get_algorithm_params('2')
            de_params = {
                'population_size': params.get('population_size', 50),
                'mutation_factor': params.get('mutation_factor', 0.8),
                'crossover_rate': params.get('crossover_rate', 0.9),
                'max_generations': params.get('max_generations', 150)
            }
            de_kwargs = _prepare_kwargs(DifferentialEvolution, de_params)
            de = DifferentialEvolution(**de_kwargs)
            result = de.run(fitness_fn, bounds, minimize=minimize)
            
        elif choice == '3':
            print("Exiting.")
            return
        else:
            print("Invalid choice.")
            return
        
        best = result['best_solution']
        best_mse = result['best_value']
        
        print("\n=== Optimization Results ===")
        print(f"Best parameters found:")
        print(f"  K (shape factor): {best[0]:.4f}")
        print(f"  λ (wavelength):   {best[1]:.4f} Å")
        print(f"  B (FWHM):         {best[2]:.6f} radians")
        print(f"\nMean Squared Error: {best_mse:.6f}")
        
        # Plot optimization progress
        progress_path = plot_history(result['history'], maximize=False)
        print(f"\nProgress plot saved: {progress_path}")
        
        # Plot Scherrer fit comparison
        fit_path = plot_fit_comparison(best)
        print(f"Fit comparison plot saved: {fit_path}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()