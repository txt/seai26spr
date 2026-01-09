<p align="center">
  <a href="https://github.com/txt/seai26spr/blob/main/README.md"><img src="https://img.shields.io/badge/Home-%23ff5733?style=flat-square&logo=home&logoColor=white" /></a>
  <a href="/docs/lect/syllabus.md#top"><img src="https://img.shields.io/badge/Syllabus-%230055ff?style=flat-square&logo=openai&logoColor=white" /></a>
  <a href="https://docs.google.com/spreadsheets/d/19HJRraZex9ckdIaDHaTi0cGsvUcIhdTH6kIGoC_FODY/edit?gid=0#gid=0"><img src="https://img.shields.io/badge/Teams-%23ffd700?style=flat-square&logo=users&logoColor=white" /></a>
  <a href="https://moodle-courses2527.wolfware.ncsu.edu/course/view.php?id=8118&bp=s"><img src="https://img.shields.io/badge/Moodle-%23dc143c?style=flat-square&logo=moodle&logoColor=white" /></a>
  <a href="https://discord.gg/vCCXMfzQ"><img src="https://img.shields.io/badge/Chat-%23008080?style=flat-square&logo=discord&logoColor=white" /></a>
  <a href="/LICENSE.md"><img src="https://img.shields.io/badge/©%20timm%202026-%234b4b4b?style=flat-square&logoColor=white" /></a></p>
<h1 align="center">:cyclone: CSC491/591: Software Engineering and AI <br>NC State, Fall '25</h1>
<img src="/docs/lect/banner.png"> 


Here is the combined list of canonical algorithms in the optimization and Search-Based Software Engineering (SBSE) space, sorted chronologically by their introduction and rise to prominence:

* [**Random Search (1950s):**](src/hillc.md) The essential baseline "sanity check" to prove complex methods are actually adding value.
* [**Hill Climbing (1950s):**](src/hillc.md)  The fundamental local search strategy that iteratively moves to better neighbors.
* **Simulated Annealing / SA (1983):** A probabilistic technique using "temperature" to accept worse solutions early on to escape local optima.
* [**Tabu Search (1986):**](src/tabu.md) A metaheuristic using memory structures (forbidden lists) to force exploration and avoid cycling.
* **Genetic Programming / GP (1992):** Evolves actual parse trees or source code (e.g., automated bug fixing) rather than parameter vectors.
* **Genetic Algorithms / GA (1975):** The grandfather of evolutionary computation, using selection, crossover, and mutation on bitstrings.
* **Ant Colony Optimization / ACO (1992):** Uses pheromone trails to solve path-based problems like test sequence generation.
* **Particle Swarm Optimization / PSO (1995):** Simulates flocking behavior (birds/fish) to move candidates through continuous search spaces.
* **MaxWalkSat (1996):** A stochastic local search algorithm combining greedy moves with random walks, essential for SAT solving.
* **Differential Evolution / DE (1997):** A vector-based evolutionary algorithm that optimizes continuous problems using vector differences.
* **NSGA-II (2002):** The "gold standard" for multi-objective optimization using non-dominated sorting and crowding distance.
* **SPEA2 (2001):** An early modern multi-objective algorithm using "strength" values and nearest-neighbor density estimation.
* **IBEA (2004):** Optimizes quality indicators (like Hypervolume) directly rather than relying solely on dominance ranking.
* **MOEA/D (2007):** Decomposes a multi-objective problem into many scalar sub-problems and optimizes them simultaneously.
* **TPE (2011):** Tree-structured Parzen Estimator, a Bayesian approach for hyperparameter tuning that models $p(x|y)$.
* **SMBO (2011):** Sequential Model-Based Optimization, a broad class (including SMAC) that builds surrogates to choose the next sample.
* **GPM (2010s):** Gaussian Process Models, used within SMBO to provide probabilistic predictions (mean and variance) for expensive functions.
* **FLASH (2017):** A sequential model-based optimizer that uses decision trees (CART) to quickly find solutions with very few evaluations.
* **SWAY (2018):** A recursive spectral clustering method that samples data to approximate the Pareto frontier (very relevant to your `tree.py`).
