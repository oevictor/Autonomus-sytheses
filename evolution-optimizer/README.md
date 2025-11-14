# Evolution Optimizer — Synthesis Playground

Welcome to the Evolution Optimizer — your mischievous lab assistant for exploring synthesis parameter space with evolutionary algorithms.  
This little toolkit helps you poke, prod and optimize synthesis recipes (or toy problems like the Scherrer equation) using Genetic Algorithms, Differential Evolution and a few smart hacks.

Think of it as: part scientist, part mad algorithm, part plotting machine.


One time the PHD candite João Alves did somthing woere with me.. be alived. So as revenge I will replace be machine. this article is bsa in the work of
Capturing chemical intuition in synthesis of metalorganic frameworks  Seyed Mohamad Moosavi 1, Arunraj Chidambaram 1, Leopold Talirz1,2, Maciej Haranczyk 3,  Kyriakos C. Stylianou 1 & Berend Smit 1
https://doi.org/10.1038/s41467-019-08483-9


## What it does (short version)
- Tries to find good synthesis parameters using GA and DE.
- Lets you test a Scherrer equation fitting example with synthetic XRD data.
- Can use Random Forests as surrogate fitness for faster search and feature ranking.
- Generates pretty plots so you can actually see what the algorithms did.

## Why this exists
Because brute force is boring and humans need better suggestions than random guesses. This project helps you explore parameter spaces, find interesting candidates and visualize results — fast.

## Quick start (Windows)
1. Open a terminal in the project root (VS Code integrated terminal recommended).
2. Create a virtual environment and install deps:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Run the demo CLI:
   ```powershell
   python src\main.py
   ```
4. Follow prompts to choose optimizer, objective (Scherrer, benchmarks) and parameters. Plots and outputs are saved in the `output/` folder.

## Features
- Genetic Algorithm and Differential Evolution implementations (easy to tweak).
- Scherrer equation demo with synthetic noisy XRD-like data and fit plots.
- Hybrid RF + GA workflow for surrogate-assisted optimization and feature importance.
- Max-Min diversification to generate diverse initial candidates and MDS projection for visualization.
- Simple CLI that’s easy to extend or swap for a GUI later.

## Files you’ll care about
- `src/main.py` — demo CLI (Scherrer example).
- `src/problems/sample_problem.py` — synthetic data + fitness function + plotting.
- `src/optimizers/` — GA and DE implementations.
- `src/models/` — Random Forest training and permutation importance.
- `src/diversification.py` — MaxMin diversifier + MDS visualization.
- `output/` — generated plots and results.

## Tips & tricks
- Replace the synthetic data with your experimental CSV: adapt `generate_synthetic_dataset()` to load real data.
- Use the RF+GA hybrid when evaluations are expensive: the RF predicts outcomes and the GA searches the predictions.
- Increase GA population/generations for tougher problems; lower them for quick experiments.

## Contributing
Pull requests, issues and weird ideas are welcome. Keep changes modular and add tests where useful.

## License
MIT — see LICENSE file.

Have fun optimizing. May your parameter space be forever interesting.



