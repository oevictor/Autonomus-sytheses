import numpy as np
import math
import matplotlib.pyplot as plt
from sklearn.manifold import MDS
from sklearn.preprocessing import StandardScaler

class MaxMinDiversification:
    """
    Max-Min distance strategy for generating diverse parameter sets.
    Useful for chemical recipes where you want to explore diverse parameter combinations.
    """
    
    def __init__(self, bounds, num_samples=10, initial_samples=None):
        """
        Args:
            bounds: list of (min, max) tuples for each parameter
            num_samples: number of diverse samples to generate
            initial_samples: optional list of initial parameter sets (recipes)
        """
        self.bounds = bounds
        self.num_samples = num_samples
        self.dims = len(bounds)
        self.samples = []
        
        if initial_samples is not None:
            self.samples = [np.array(s) for s in initial_samples]
    
    def _distance(self, point1, point2):
        """Euclidean distance between two points (normalized by bounds)."""
        normalized_diff = []
        for i, (p1, p2) in enumerate(zip(point1, point2)):
            lo, hi = self.bounds[i]
            range_val = hi - lo
            if range_val > 0:
                normalized_diff.append(((p1 - p2) / range_val) ** 2)
            else:
                normalized_diff.append(0)
        return math.sqrt(sum(normalized_diff))
    
    def _min_distance_to_samples(self, candidate):
        """Find minimum distance from candidate to existing samples."""
        if len(self.samples) == 0:
            return float('inf')
        return min(self._distance(candidate, s) for s in self.samples)
    
    def generate_diverse_samples(self, candidates_per_iteration=100):
        """
        Generate diverse parameter sets using Max-Min strategy.
        
        Args:
            candidates_per_iteration: number of random candidates to evaluate per iteration
            
        Returns:
            list of diverse parameter sets (numpy arrays)
        """
        # If no initial samples, start with a random one
        if len(self.samples) == 0:
            initial = np.array([np.random.uniform(lo, hi) for lo, hi in self.bounds])
            self.samples.append(initial)
        
        # Iteratively add samples that maximize minimum distance
        while len(self.samples) < self.num_samples:
            # Generate random candidates
            candidates = []
            for _ in range(candidates_per_iteration):
                candidate = np.array([np.random.uniform(lo, hi) for lo, hi in self.bounds])
                min_dist = self._min_distance_to_samples(candidate)
                candidates.append((min_dist, candidate))
            
            # Select candidate with maximum minimum distance
            best_candidate = max(candidates, key=lambda x: x[0])
            self.samples.append(best_candidate[1])
        
        return self.samples
    
    def get_diversity_score(self):
        """Calculate diversity score (average pairwise distance)."""
        if len(self.samples) < 2:
            return 0.0
        
        total_dist = 0
        count = 0
        for i in range(len(self.samples)):
            for j in range(i + 1, len(self.samples)):
                total_dist += self._distance(self.samples[i], self.samples[j])
                count += 1
        
        return total_dist / count if count > 0 else 0.0
    
    def visualize_mds(self, output_path="output/maxmin_mds_projection.png", 
                      compare_random=True, param_names=None):
        """
        Visualize diversification using Multidimensional Scaling (MDS) 2D projection.
        
        Args:
            output_path: where to save the plot
            compare_random: if True, also show random sampling for comparison
            param_names: list of parameter names for the title
        """
        import os
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        if len(self.samples) < 2:
            print("Need at least 2 samples for MDS visualization")
            return None
        
        # Prepare data
        maxmin_samples = np.array(self.samples)
        
        # Generate random samples for comparison
        if compare_random:
            random_samples = np.array([
                [np.random.uniform(lo, hi) for lo, hi in self.bounds]
                for _ in range(len(self.samples))
            ])
            all_samples = np.vstack([maxmin_samples, random_samples])
            labels = ['MaxMin'] * len(maxmin_samples) + ['Random'] * len(random_samples)
        else:
            all_samples = maxmin_samples
            labels = ['MaxMin'] * len(maxmin_samples)
        
        # Normalize data
        scaler = StandardScaler()
        all_samples_normalized = scaler.fit_transform(all_samples)
        
        # Apply MDS
        mds = MDS(n_components=2, random_state=42, dissimilarity='euclidean')
        samples_2d = mds.fit_transform(all_samples_normalized)
        
        # Create figure with subplots
        fig = plt.figure(figsize=(14, 6))
        
        # Plot 1: MDS projection
        ax1 = plt.subplot(1, 2, 1)
        if compare_random:
            maxmin_2d = samples_2d[:len(maxmin_samples)]
            random_2d = samples_2d[len(maxmin_samples):]
            
            ax1.scatter(maxmin_2d[:, 0], maxmin_2d[:, 1], 
                       c='blue', s=100, alpha=0.7, label='MaxMin', edgecolors='black', linewidth=1.5)
            ax1.scatter(random_2d[:, 0], random_2d[:, 1], 
                       c='red', s=100, alpha=0.5, label='Random', marker='s', edgecolors='black', linewidth=1)
            
            # Add connecting lines for MaxMin to show sequence
            for i in range(len(maxmin_2d) - 1):
                ax1.plot([maxmin_2d[i, 0], maxmin_2d[i+1, 0]], 
                        [maxmin_2d[i, 1], maxmin_2d[i+1, 1]], 
                        'b--', alpha=0.3, linewidth=0.8)
        else:
            ax1.scatter(samples_2d[:, 0], samples_2d[:, 1], 
                       c='blue', s=100, alpha=0.7, edgecolors='black', linewidth=1.5)
        
        ax1.set_xlabel('MDS Dimension 1', fontsize=11)
        ax1.set_ylabel('MDS Dimension 2', fontsize=11)
        title = 'MaxMin Diversification - MDS Projection'
        if param_names:
            title += f'\nParameters: {", ".join(param_names)}'
        ax1.set_title(title, fontsize=12, fontweight='bold')
        if compare_random:
            ax1.legend(fontsize=10)
        ax1.grid(alpha=0.3)
        
        # Plot 2: Distance matrix heatmap
        ax2 = plt.subplot(1, 2, 2)
        distance_matrix = np.zeros((len(maxmin_samples), len(maxmin_samples)))
        for i in range(len(maxmin_samples)):
            for j in range(len(maxmin_samples)):
                distance_matrix[i, j] = self._distance(maxmin_samples[i], maxmin_samples[j])
        
        im = ax2.imshow(distance_matrix, cmap='YlOrRd', aspect='auto')
        ax2.set_xlabel('Sample Index', fontsize=11)
        ax2.set_ylabel('Sample Index', fontsize=11)
        ax2.set_title('Pairwise Distance Matrix\n(MaxMin Samples)', fontsize=12, fontweight='bold')
        plt.colorbar(im, ax=ax2, label='Normalized Distance')
        
        # Add diversity score
        diversity_score = self.get_diversity_score()
        fig.text(0.5, 0.02, f'Diversity Score: {diversity_score:.4f}', 
                ha='center', fontsize=11, fontweight='bold')
        
        plt.tight_layout(rect=[0, 0.03, 1, 1])
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"MDS visualization saved to: {output_path}")
        return output_path


class ChemicalRecipeMaxMin:
    """
    Specialized Max-Min for chemical recipes with categorical and continuous parameters.
    """
    
    def __init__(self, continuous_bounds, categorical_choices=None, num_samples=10):
        """
        Args:
            continuous_bounds: list of (min, max) for continuous params (e.g., temperature, concentration)
            categorical_choices: dict of {param_name: [choice1, choice2, ...]} for discrete choices
            num_samples: number of diverse recipes to generate
        """
        self.continuous_bounds = continuous_bounds
        self.categorical_choices = categorical_choices or {}
        self.num_samples = num_samples
        self.recipes = []
    
    def _distance(self, recipe1, recipe2):
        """Distance between two recipes (continuous + categorical)."""
        # Continuous parameters distance
        cont_dist = 0
        for i, (val1, val2) in enumerate(zip(recipe1['continuous'], recipe2['continuous'])):
            lo, hi = self.continuous_bounds[i]
            range_val = hi - lo
            if range_val > 0:
                cont_dist += ((val1 - val2) / range_val) ** 2
        cont_dist = math.sqrt(cont_dist)
        
        # Categorical parameters distance (0 if same, 1 if different)
        cat_dist = 0
        for key in recipe1['categorical']:
            if recipe1['categorical'][key] != recipe2['categorical'][key]:
                cat_dist += 1
        
        # Combined distance (weighted)
        total_dist = cont_dist + 0.5 * cat_dist
        return total_dist
    
    def _min_distance_to_recipes(self, candidate):
        """Find minimum distance from candidate to existing recipes."""
        if len(self.recipes) == 0:
            return float('inf')
        return min(self._distance(candidate, r) for r in self.recipes)
    
    def generate_diverse_recipes(self, candidates_per_iteration=50):
        """
        Generate diverse chemical recipes.
        
        Returns:
            list of dicts with 'continuous' and 'categorical' keys
        """
        # Start with a random recipe
        if len(self.recipes) == 0:
            initial = {
                'continuous': np.array([np.random.uniform(lo, hi) 
                                       for lo, hi in self.continuous_bounds]),
                'categorical': {key: np.random.choice(choices) 
                               for key, choices in self.categorical_choices.items()}
            }
            self.recipes.append(initial)
        
        # Iteratively add diverse recipes
        while len(self.recipes) < self.num_samples:
            candidates = []
            for _ in range(candidates_per_iteration):
                candidate = {
                    'continuous': np.array([np.random.uniform(lo, hi) 
                                           for lo, hi in self.continuous_bounds]),
                    'categorical': {key: np.random.choice(choices) 
                                   for key, choices in self.categorical_choices.items()}
                }
                min_dist = self._min_distance_to_recipes(candidate)
                candidates.append((min_dist, candidate))
            
            best_candidate = max(candidates, key=lambda x: x[0])
            self.recipes.append(best_candidate[1])
        
        return self.recipes
    
    def export_recipes_to_dict_list(self):
        """Export recipes as list of combined parameter dicts."""
        result = []
        for recipe in self.recipes:
            combined = {}
            # Add continuous parameters with names
            for i, val in enumerate(recipe['continuous']):
                combined[f'param_{i}'] = val
            # Add categorical parameters
            combined.update(recipe['categorical'])
            result.append(combined)
        return result
    
    def visualize_mds(self, output_path="output/chemical_recipe_mds.png"):
        """Visualize chemical recipes using MDS (continuous params only)."""
        import os
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        if len(self.recipes) < 2:
            print("Need at least 2 recipes for MDS visualization")
            return None
        
        # Extract continuous parameters
        continuous_data = np.array([r['continuous'] for r in self.recipes])
        
        # Normalize
        scaler = StandardScaler()
        continuous_normalized = scaler.fit_transform(continuous_data)
        
        # Apply MDS
        mds = MDS(n_components=2, random_state=42)
        recipes_2d = mds.fit_transform(continuous_normalized)
        
        # Plot
        plt.figure(figsize=(10, 8))
        scatter = plt.scatter(recipes_2d[:, 0], recipes_2d[:, 1], 
                            c=range(len(recipes_2d)), cmap='viridis', 
                            s=150, alpha=0.7, edgecolors='black', linewidth=1.5)
        
        # Add labels
        for i, (x, y) in enumerate(recipes_2d):
            plt.annotate(f'R{i+1}', (x, y), fontsize=9, ha='center', va='center', 
                        fontweight='bold', color='white')
        
        plt.colorbar(scatter, label='Recipe Order')
        plt.xlabel('MDS Dimension 1', fontsize=12)
        plt.ylabel('MDS Dimension 2', fontsize=12)
        plt.title('Chemical Recipe Diversification - MDS Projection', 
                 fontsize=14, fontweight='bold')
        plt.grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"Chemical recipe MDS visualization saved to: {output_path}")
        return output_path


# Example usage functions
def example_scherrer_maxmin():
    """Example: Generate diverse Scherrer equation parameters."""
    print("=== Scherrer Equation - MaxMin Diversification ===\n")
    
    # Scherrer bounds: [K, lambda, B, theta]
    bounds = [
        (0.5, 1.0),       # K (shape factor)
        (1.0, 2.0),       # lambda (wavelength, Å)
        (0.005, 0.05),    # B (FWHM, radians)
        (0.1, 1.4)        # theta (Bragg angle, radians)
    ]
    
    param_names = ['K', 'λ (Å)', 'B (rad)', 'θ (rad)']
    
    diversifier = MaxMinDiversification(bounds, num_samples=15)
    diverse_samples = diversifier.generate_diverse_samples(candidates_per_iteration=100)
    
    print(f"Generated {len(diverse_samples)} diverse parameter sets:")
    print("K\t\tλ(Å)\t\tB(rad)\t\tθ(rad)")
    print("-" * 60)
    for i, sample in enumerate(diverse_samples):
        print(f"{sample[0]:.4f}\t\t{sample[1]:.4f}\t\t{sample[2]:.6f}\t\t{sample[3]:.4f}")
    
    diversity_score = diversifier.get_diversity_score()
    print(f"\nDiversity Score: {diversity_score:.4f}")
    
    # Visualize with MDS
    diversifier.visualize_mds(
        output_path="output/scherrer_maxmin_mds.png",
        compare_random=True,
        param_names=param_names
    )
    
    return diverse_samples


def example_chemical_recipe_maxmin():
    """Example: Generate diverse chemical synthesis recipes."""
    print("\n=== Chemical Recipe - MaxMin Diversification ===\n")
    
    # Continuous parameters: [temperature(°C), time(h), concentration(M)]
    continuous_bounds = [
        (100, 400),   # temperature
        (0.5, 24),    # reaction time
        (0.01, 2.0)   # concentration
    ]
    
    # Categorical parameters
    categorical_choices = {
        'solvent': ['water', 'ethanol', 'acetone', 'DMF'],
        'catalyst': ['Pt', 'Pd', 'Au', 'none'],
        'atmosphere': ['air', 'N2', 'Ar']
    }
    
    recipe_gen = ChemicalRecipeMaxMin(
        continuous_bounds=continuous_bounds,
        categorical_choices=categorical_choices,
        num_samples=12
    )
    
    diverse_recipes = recipe_gen.generate_diverse_recipes(candidates_per_iteration=50)
    
    print(f"Generated {len(diverse_recipes)} diverse chemical recipes:")
    print("\nTemp(°C)\tTime(h)\t\tConc(M)\t\tSolvent\t\tCatalyst\tAtmosphere")
    print("-" * 90)
    for i, recipe in enumerate(diverse_recipes):
        cont = recipe['continuous']
        cat = recipe['categorical']
        print(f"{cont[0]:.1f}\t\t{cont[1]:.2f}\t\t{cont[2]:.3f}\t\t{cat['solvent']}\t\t{cat['catalyst']}\t\t{cat['atmosphere']}")
    
    # Visualize with MDS
    recipe_gen.visualize_mds(output_path="output/chemical_recipe_mds.png")
    
    return diverse_recipes


if __name__ == "__main__":
    # Run examples
    example_scherrer_maxmin()
    example_chemical_recipe_maxmin()