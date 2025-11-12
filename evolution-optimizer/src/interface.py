class UserInterface:
    """Simple command-line interface in English for selecting algorithms and entering parameters."""

    def display_options(self):
        print("Select an optimizer:")
        print("  1) Genetic Algorithm")
        print("  2) Differential Evolution")
        print("  3) Exit")

    def get_user_input(self):
        choice = input("Enter choice (1/2/3) [1]: ").strip()
        return choice or '1'

    def _parse_int(self, prompt, default):
        val = input(f"{prompt} [{default}]: ").strip()
        if val == "":
            return int(default)
        try:
            return int(val)
        except ValueError:
            print("Invalid integer, using default.")
            return int(default)

    def _parse_float(self, prompt, default):
        val = input(f"{prompt} [{default}]: ").strip()
        if val == "":
            return float(default)
        try:
            return float(val)
        except ValueError:
            print("Invalid number, using default.")
            return float(default)

    def get_algorithm_params(self, choice):
        """Return a dict with parameters depending on the chosen algorithm."""
        params = {}
        if choice == '1':
            print("Genetic Algorithm parameters:")
            params['population_size'] = self._parse_int("Population size", 30)
            params['mutation_rate'] = self._parse_float("Mutation rate (0-1)", 0.01)
            params['crossover_rate'] = self._parse_float("Crossover rate (0-1)", 0.7)
            params['max_generations'] = self._parse_int("Max generations", 100)
        elif choice == '2':
            print("Differential Evolution parameters:")
            params['population_size'] = self._parse_int("Population size", 30)
            params['mutation_factor'] = self._parse_float("Mutation factor (F, e.g. 0.8)", 0.8)
            params['crossover_rate'] = self._parse_float("Crossover rate (CR, 0-1)", 0.9)
            params['max_generations'] = self._parse_int("Max generations", 100)
        return params

    def display_results(self, result):
        print("\nResult:")
        print(result)

    # --- new objective selection UI ---
    def display_objective_options(self, objectives):
        print("\nSelect an objective / equation to optimize:")
        for k, info in objectives.items():
            print(f"  {k}) {info['name']} - {info['description']} (dims: {info['dims']}")
        print("  x) Cancel")

    def get_objective_choice(self):
        choice = input("Enter objective choice [1]: ").strip()
        return choice or '1'

    def confirm_bounds_override(self):
        val = input("Do you want to override bounds for variables? (y/N): ").strip().lower()
        return val == 'y'

    def get_bounds_from_user(self, default_bounds):
        new_bounds = []
        for i, (lo, hi) in enumerate(default_bounds):
            s = input(f"Variable {i} bounds (min,max) [{lo},{hi}]: ").strip()
            if s == "":
                new_bounds.append((lo, hi))
                continue
            try:
                parts = [float(p.strip()) for p in s.split(',')]
                if len(parts) != 2 or parts[0] >= parts[1]:
                    print("Invalid range, using default.")
                    new_bounds.append((lo, hi))
                else:
                    new_bounds.append((parts[0], parts[1]))
            except Exception:
                print("Parse error, using default.")
                new_bounds.append((lo, hi))
        return new_bounds

    def get_scherrer_inputs(self):
        print("\nEnter Scherrer equation input data:")
        K = self._parse_float("Shape factor K (0.5-1.0)", 0.9)
        lam = self._parse_float("Wavelength lambda (Å)", 1.54)
        B = self._parse_float("Peak FWHM B (radians)", 0.02)
        theta_deg = self._parse_float("Bragg angle theta (degrees)", 30.0)
        import math
        theta = math.radians(theta_deg)
        return K, lam, B, theta

    def ask_extend_bounds(self):
        val = input("Auto-create bounds around entered values? (Y/n) [Y]: ").strip().lower()
        return val != 'n'