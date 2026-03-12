<p align="center">
  <a href="https://github.com/txt/seai26spr/blob/main/README.md"><img 
     src="https://img.shields.io/badge/Home-%23ff5733?style=flat-square&logo=home&logoColor=white" /></a>
  <a href="https://github.com/txt/seai26spr/blob/main/docs/lect/syllabus.md#top"><img 
      src="https://img.shields.io/badge/Syllabus-%230055ff?style=flat-square&logo=openai&logoColor=white" /></a>
  <a href="https://docs.google.com/spreadsheets/d/19HJRraZex9ckdIaDHaTi0cGsvUcIhdTH6kIGoC_FODY/edit?gid=0#gid=0"><img 
      src="https://img.shields.io/badge/Teams-%23ffd700?style=flat-square&logo=users&logoColor=white" /></a>
  <a href="https://moodle-courses2527.wolfware.ncsu.edu/course/view.php?id=8118&bp=s"><img 
      src="https://img.shields.io/badge/Moodle-%23dc143c?style=flat-square&logo=moodle&logoColor=white" /></a>
  <a href="https://discord.gg/vCCXMfzQ"><img 
      src="https://img.shields.io/badge/Chat-%23008080?style=flat-square&logo=discord&logoColor=white" /></a>
  <a href="https://github.com/txt/seai26spr/blob/main/LICENSE.md"><img 
      src="https://img.shields.io/badge/©%20timm%202026-%234b4b4b?style=flat-square&logoColor=white" /></a></p>
<h1 align="center">:cyclone: CSC491/591 (013): Software Engineering and AI <br>NC State, Spring '26</h1>
<img src="https://raw.githubusercontent.com/txt/seai26spr/main/docs/lect/banner.png">



# Week 5: Optimization — Review Notes


## Part 1: Glossary

### Core Optimization Concepts

- **objective** — a scorecard function you want to minimize or maximize; `F(x)` over decision variables `x`
- **decision variable** — what you control (compiler flags, team sizes, config knobs, etc.)
- **search space X** — the set of all feasible solutions; may be continuous, discrete, or mixed
- **constraint** — inequality (`g_i(x) ≤ 0`) or equality (`h_j(x) = 0`) that limits valid solutions
- **fitness landscape** — mental model where terrain elevation = f(x); algorithms navigate this terrain
- **local optimum** — solution better than all neighbors but not globally best; the enemy of greedy search
- **global optimum** — the best solution in the entire search space
- **evaluation budget** — total number of times you can call f(x); the primary currency of SE optimization
- **SBSE** — Search-Based Software Engineering; applying metaheuristic search to SE tasks

---

### Era 1 — Trajectory Methods

- **hill climbing** — always move to a better neighbor; gets permanently stuck at the first local optimum
- **simulated annealing (SA)** — accepts worse moves with probability `exp(-Δ/T)`; high T = explore, low T = exploit
- **temperature T** — SA's control parameter; starts high (random walk) and decreases (greedy)
- **cooling schedule** — plan for lowering T; typically geometric: `T ← T * cooling_rate` (0.95–0.999)
- **escape probability** — `exp(-(curr-best)/T)`; allows SA to escape local optima early in the run
- **trajectory method** — single-point method; only remembers current position, not the whole population

---

### Era 2 — Discrete Populations (Genetic Algorithms)

- **population** — a set of N candidate solutions explored in parallel
- **selection** — choosing fitter individuals to reproduce; tournament selection most common
- **crossover** — combining two parents to produce offspring; e.g., single-point, SBX
- **mutation** — small random perturbation of an individual; maintains diversity
- **elitism** — always copying the best individual(s) forward unchanged; prevents regression
- **tournament selection** — sample k individuals at random, return the best; larger k = stronger pressure
- **Hamming cliff** — nearby real numbers having very different binary representations; plagues binary GAs
- **Genetic Programming (GP)** — GA where individuals are syntax trees (programs), not parameter vectors
- **GenProg** — landmark automated program repair tool using GP; fitness = weighted test pass rate

---

### Era 3 — Continuous Vectors

- **Evolution Strategies (ES)** — include step-size σ *inside* the individual so evolution tunes it automatically
- **CMA-ES** — Covariance Matrix Adaptation ES; adapts full covariance of search distribution; gold standard for smooth single-objective problems up to ~200 variables
- **Differential Evolution (DE)** — mutation via vector differences: `v = a + F*(b-c)`; self-scaling step sizes
- **scale factor F** — DE parameter (~0.5–0.8) controlling mutation magnitude
- **crossover rate CR** — DE parameter (~0.7–0.9) controlling how many genes come from the mutant
- **DE/rand/1/bin** — standard DE variant: random base vector, 1 difference vector, binomial crossover
- **self-scaling** — DE's `b-c` shrinks as population converges → automatic exploitation/exploration balance

---

### Era 4 — Multi-Objective (Pareto Revolution)

- **Pareto dominance** — solution `a` dominates `b` if `a` is no worse on all objectives and better on at least one
- **Pareto front** — the set of non-dominated solutions; the best achievable trade-offs
- **non-dominated solution** — no other solution dominates it; Pareto-optimal
- **scalarization** — combining objectives as `w1*f1 + w2*f2`; simple but requires weight choice and misses non-convex regions
- **NSGA-I** — first MOEA with non-dominated sorting; slow O(MN³), requires manual σ_share, no elitism
- **NSGA-II** — fast sort O(MN²) + crowding distance + (N+N) elitist pool; workhorse of SBSE
- **crowding distance** — average side-length of cuboid of nearest neighbors in objective space; rewards diversity with no parameters
- **(N+N) selection** — NSGA-II combines parents and offspring into 2N pool, keeps best N; no good solution ever lost
- **NSGA-III** — replaces crowding distance with structured reference points on the objective hyperplane; handles M ≥ 4
- **reference points** — uniformly distributed directions on the unit simplex (Das-Dennis method); guide NSGA-III diversity
- **MOEA/D** — decomposes multi-objective problem into N scalar sub-problems via weight vectors; uses Tchebycheff aggregation
- **Tchebycheff scalarization** — `max_i { λ_i * |f_i(x) - z*_i| }`; used in MOEA/D; handles non-convex fronts
- **SPEA2** — Strength Pareto EA 2; uses k-NN archive truncation for diversity; good spread, more memory
- **SMS-EMOA** — steady-state MOEA with hypervolume contribution deletion; theoretically strong HV properties
- **many-objective** — M ≥ 4 objectives; crowding distance breaks down; need NSGA-III or MOEA/D

---

### Era 5 — Multi-Fidelity (Training Wall)

- **fidelity** — how much compute budget (epochs, samples) you give one evaluation
- **multi-fidelity** — using cheap partial evaluations to triage bad configurations early
- **Successive Halving (SHA)** — run N configs for budget b; keep top half; double budget; repeat
- **Hyperband** — runs multiple SHA brackets with different starting budgets to hedge against early-stopping errors
- **ASHA** — Asynchronous SHA; promotes workers immediately when eligible; never idles GPUs
- **DEHB** — Differential Evolution + Hyperband; replaces Hyperband's random sampling with DE mutations that learn from past brackets

---

### Era 6 — Surrogate Models

- **surrogate** — a cheap mathematical model trained on previous evaluations to approximate f(x)
- **Gaussian Process (GP)** — surrogate in BO; provides mean prediction and uncertainty estimate
- **epistemic uncertainty** — "map ignorance"; uncertainty from lack of data in a region; drives exploration
- **acquisition function** — decides where to sample next by balancing mean (exploit) and uncertainty (explore)
- **Expected Improvement (EI)** — acquisition function: E[max(0, f_best - f(x))]
- **UCB** — Upper Confidence Bound acquisition: μ(x) - κ·σ(x); simple and tunable
- **EGO** — Efficient Global Optimization; BO with GP surrogate and EI; Jones et al. 1998
- **SMAC** — Surrogate Model Algorithm Configuration; uses Random Forest surrogate; handles mixed (categorical + continuous) spaces

---

### Era 7 — Extreme Scarcity

- **label scarcity** — regime where you can afford < 100 evaluations total; standard MOEAs fail here
- **LITE / EZR** — binary contrastive classifier approach; label "good" vs "bad" with very few examples; active research
- **contrastive surrogate** — learns to distinguish good from bad rather than fitting a regression surface

---

### Evaluation Metrics

- **Hypervolume (HV)** — volume of objective space dominated by the approximation set and bounded by a reference point; higher is better; no true front needed; Pareto-compliant
- **IGD** — Inverted Generational Distance; each point on the true front finds its nearest approximation solution; measures convergence + coverage; lower is better
- **GD** — Generational Distance; each approximation solution finds its nearest point on the true front; gameable (one lucky point → GD = 0)
- **D2H** — Distance to Heaven; normalizes objectives to [0,1] globally, computes mean Euclidean distance to ideal (0,0,…,0); lower is better; works for single-obj and multi-obj alike
- **Spread Δ** — measures uniformity of gaps between solutions; orthogonal to convergence; lower is better
- **reference point** — a point dominated by all solutions; required by HV; must be set outside the known front
- **proxy front** — union of all algorithm results filtered to non-dominated solutions; used as a true-front approximation when the true PF is unknown

---

### pymoo API Quick Reference

| Concept | pymoo Pattern |
|---|---|
| Batch problem | Subclass `Problem`, override `_evaluate(self, X, out)` |
| Single-row problem | Subclass `ElementwiseProblem`, override `_evaluate(self, x, out)` |
| Objectives | `out["F"]` — always minimize; negate to maximize |
| Constraints | `out["G"]` — feasible when `G ≤ 0` |
| Run | `minimize(problem, algorithm, termination, seed=)` |
| Termination | `get_termination("n_gen", 100)` |
| Results | `res.F` (objectives), `res.X` (decision vars) |
| Crossover | `SBX(prob=0.9, eta=15)` |
| Mutation | `PM(eta=20)` |
| Reference dirs | `get_reference_directions("das-dennis", M, n_partitions=p)` |
| Hypervolume | `HV(ref_point=r).do(F)` |
| IGD | `IGD(ref_pf).do(F)` |

---

## Part 2: The POM3a Algorithm Comparison — Explained

Nine optimization algorithms were run on **POM3a**, a software process simulation model with three conflicting objectives: minimize idle rate, minimize cost, and maximize completion rate. All algorithms ran for 100 generations.

![POM3a Multi-Metric Algorithm Comparison](result_opt.png)

### Reading the Three Metrics

**Hypervolume (HV) — higher is better.**
HV measures the volume of objective space that the returned solution set "covers" (dominates), bounded by a reference point. A value of 0.0 means the algorithm returned only a single point (not a spread of trade-offs), so it dominates zero volume in multi-objective space.

**Distance to Heaven (D2H) — lower is better.**
Objectives are normalized globally to [0, 1], and "heaven" is the ideal point (0, 0, 0) — best on all three at once. D2H is the mean distance of the returned solutions from heaven. Lower = solutions are closer to the ideal.

**IGD — lower is better.**
IGD uses a proxy Pareto front (the union of all algorithms' non-dominated solutions). Each reference front point finds its nearest solution in the algorithm's output. Lower IGD = the algorithm's output covers the front well and converges closely.

---

### Algorithm-by-Algorithm Interpretation

| Algorithm | HV ↑ | D2H ↓ | IGD ↓ | Notes |
|---|---|---|---|---|
| **NSGA-II** | 1.263 | 0.292 | 0.005 | Best all-rounder; (N+N) elitism + crowding distance ideal for 3-obj |
| **SMS-EMOA** | 1.254 | 0.238 | 0.009 | HV-contribution deletion pushes solutions toward heaven; 2nd best D2H |
| **NSGA-III** | 1.253 | 0.271 | 0.012 | Reference-point niching competitive; real advantage kicks in at M≥4 |
| **SPEA2** | 1.236 | 0.384 | 0.004 | Best IGD (most uniform front coverage) but weakest convergence of true MOEAs |
| **Random** | 1.229 | 0.327 | 0.042 | Surprisingly strong — POM3's landscape is not rugged enough to punish random |
| **MOEA/D** | 1.110 | **0.161** | 0.277 | Best D2H (closest to heaven) but clustered front; decomposition biases convergence over spread |
| **CMA-ES / DE / GA** | 0.000 | 0.066 | 0.281 | Single-objective: one best point, zero volume covered, front not approximated |

**Why CMA-ES/DE/GA score HV = 0:** these are single-objective algorithms that collapse all three POM3 objectives into one scalar. They return one point, which dominates zero volume. Their D2H (0.066) is actually decent — the single point is close to heaven — but they give you no trade-off surface to reason about.

**Why MOEA/D wins D2H but loses IGD:** decomposition via weight vectors converges solutions aggressively toward the ideal but clusters them near the "best" weight directions, leaving gaps in the front. NSGA-II's crowding distance spreads solutions more uniformly, so it wins on coverage (IGD) even though MOEA/D's solutions are individually closer to heaven.

**Why Random is competitive:** POM3a's objective space is not highly rugged. Uniform random sampling naturally covers its extent. This is a key SBSE lesson — random search is always a required baseline.

---

### Key Takeaways from the Comparison

1. **Single-objective algorithms are not wrong — just different.** CMA-ES/DE/GA get very close to one ideal point (D2H ≈ 0.066) but give you no trade-off surface. Use them only when the weight between objectives is already decided.

2. **No single algorithm wins on all three metrics.** NSGA-II wins HV, MOEA/D wins D2H, SPEA2 wins IGD. Always report multiple metrics.

3. **IGD requires a proxy front.** Since the true POM3 Pareto front is unknown, the chart uses the union of all algorithms' non-dominated solutions. This makes IGD relative, not absolute.

4. **MOEA/D's decomposition biases convergence over spread** on this problem. If your application needs diversity (e.g., for a decision-maker to explore options), NSGA-II or SPEA2 is safer.

5. **Random is a meaningful baseline.** In any SBSE experiment, always compare against random search. If your sophisticated algorithm barely beats random, the fitness landscape may be easy or your evaluation budget is too large.

---

## Part 3: Review Questions

---

**Q1 — Why Classical Methods Fail in SE**

- List four assumptions classical gradient-based optimizers make. For each, explain *specifically* why it breaks in a software engineering context (e.g., config tuning, test selection, automated repair).
- What is the *only* requirement for an evolutionary optimizer to work? Why does this make EAs so broadly applicable?

**Q2 — SA vs Hill Climbing**

- Explain why hill climbing fails on rugged landscapes. What single change does SA make to fix this, and what determines how aggressive the fix is?
- Trace SA on a 1D problem: current best = 5, candidate = 7 (worse), T = 10, Δ = 2. What is the escape probability? At T = 0.1, what is it? What behavior does this model?

**Q3 — GA Operators**

- A GA uses tournament selection with k=5 on a population of 20. What is the selection pressure compared to k=2? When would you prefer strong vs weak selection pressure?
- Explain the Hamming cliff problem with binary GAs. A solution encodes a real number in 4 bits. The values 7 (0111) and 8 (1000) are adjacent but their Hamming distance is 4. Why is this a problem for crossover and mutation?

**Q4 — DE Self-Scaling**

- Write out the DE/rand/1/bin mutation and crossover steps. Explain in plain English why `F*(b-c)` is self-scaling without needing a manual σ.
- When would you choose DE over CMA-ES? When would CMA-ES win? (Consider dimensionality, noise, and problem structure.)

**Q5 — Pareto Dominance and NSGA-II**

- Given solutions A=(1,4), B=(2,3), C=(3,2), D=(4,1), E=(3,4), F=(2,5) with both objectives minimized: identify the Pareto front and which solutions are dominated.
- Trace NSGA-II's (N+N) selection for a population of 3 parents and 3 offspring. You have fronts F1={a,b}, F2={c,d,e,f}. N=4. Which solutions survive and why?

**Q6 — Crowding Distance and NSGA-III**

- Crowding distance breaks down when M > 3. Give an intuitive explanation of why. What does NSGA-III substitute?
- For M=3 with 6 divisions, NSGA-III generates 28 reference points. For M=5 with 6 divisions, it generates 210. Why does this scale the way it does? (Hint: stars-and-bars combinatorics.)

**Q7 — MOEA/D vs NSGA-II**

- MOEA/D decomposes a 3-objective problem into N scalar sub-problems. What is the Tchebycheff aggregation function? How do sub-problems share information with neighbors?
- On POM3a, MOEA/D achieves D2H=0.16 (best) but IGD=0.28 (worst among true MOEAs). Explain why decomposition tends to produce this pattern.

**Q8 — Multi-Fidelity**

- What is the core insight of Successive Halving? Why can it unfairly kill good configurations?
- Hyperband runs multiple SHA brackets. ASHA adds asynchronous promotion. What specific hardware scenario motivated ASHA? What happens to workers in synchronous SHA when configs train at different speeds?

**Q9 — Surrogates and Acquisition Functions**

- A Gaussian Process surrogate returns μ(x)=0.3, σ(x)=0.1 at point x₁ and μ(x)=0.5, σ(x)=0.4 at x₂. The current best is 0.2. Which point would EI acquisition prefer and why?
- Why does SMAC use a Random Forest surrogate instead of a Gaussian Process? What class of SE configuration problems does this make it better for?

**Q10 — Evaluation Metrics**

- HV = 0 for GA, DE, and CMA-ES on POM3a even though their D2H is 0.066 (better than random's 0.33). Explain this apparent contradiction — is lower D2H always better?
- You run NSGA-II and MOEA/D on a new SE problem and find NSGA-II wins HV but MOEA/D wins IGD. Sketch the shape of each algorithm's output in 2D objective space that would produce this result. Which metric should you report to a project manager and why?

---

## Recommended Reading

### Foundational

- Holland, J.H. (1975). *Adaptation in Natural and Artificial Systems*. University of Michigan Press.
- Goldberg, D.E. (1989). *Genetic Algorithms in Search, Optimization, and Machine Learning*. Addison-Wesley.
- Kirkpatrick, S., Gelatt, C.D. & Vecchi, M.P. (1983). Optimization by Simulated Annealing. *Science* 220(4598), 671–680.
- Storn, R. & Price, K. (1997). Differential Evolution — A Simple and Efficient Heuristic for Global Optimization over Continuous Spaces. *Journal of Global Optimization* 11(4), 341–359.
- Hansen, N. & Ostermeier, A. (2001). Completely Derandomized Self-Adaptation in Evolution Strategies. *Evolutionary Computation* 9(2), 159–195.

### NSGA Family and Multi-Objective

- Srinivas, N. & Deb, K. (1994). Multiobjective Optimization Using Nondominated Sorting in Genetic Algorithms. *Evolutionary Computation* 2(3), 221–248. *(NSGA-I)*
- Deb, K., Pratap, A., Agarwal, S. & Meyarivan, T. (2002). A Fast and Elitist Multiobjective Genetic Algorithm: NSGA-II. *IEEE Transactions on Evolutionary Computation* 6(2), 182–197.
- Deb, K. & Jain, H. (2014). An Evolutionary Many-Objective Optimization Algorithm Using Reference-Point-Based Nondominated Sorting Approach, Part I: Solving Problems with Box Constraints. *IEEE Transactions on Evolutionary Computation* 18(4), 577–601. *(NSGA-III)*
- Zhang, Q. & Li, H. (2007). MOEA/D: A Multiobjective Evolutionary Algorithm Based on Decomposition. *IEEE Transactions on Evolutionary Computation* 11(6), 712–731.
- Zitzler, E., Laumanns, M. & Thiele, L. (2002). SPEA2: Improving the Strength Pareto Evolutionary Algorithm for Multiobjective Optimization. In *Evolutionary Methods for Design, Optimization and Control* (EUROGEN 2001), CIMNE, Barcelona, pp. 95–100.
- Beume, N., Naujoks, B. & Emmerich, M. (2007). SMS-EMOA: Multiobjective Selection Based on Dominated Hypervolume. *European Journal of Operational Research* 181(3), 1653–1669.

### Multi-Fidelity and Surrogates

- Li, L., Jamieson, K., DeSalvo, G., Rostamizadeh, A. & Talwalkar, A. (2017). Hyperband: A Novel Bandit-Based Approach to Hyperparameter Optimization. *Journal of Machine Learning Research* 18(185), 1–52.
- Li, L., Jamieson, K., Rostamizadeh, A., Gonina, E., Hardt, M., Recht, B. & Talwalkar, A. (2018). Massively Parallel Hyperparameter Tuning. *arXiv:1810.05934*. *(ASHA)*
- Awad, N.H., Mallik, N. & Hutter, F. (2021). DEHB: Evolutionary Hyperband for Scalable, Robust, and Efficient Hyperparameter Optimization. *Proceedings of IJCAI 2021*, 2147–2153.
- Jones, D.R., Schonlau, M. & Welch, W.J. (1998). Efficient Global Optimization of Expensive Black-Box Functions. *Journal of Global Optimization* 13, 455–492. *(EGO/BO)*
- Hutter, F., Hoos, H.H. & Leyton-Brown, K. (2011). Sequential Model-Based Optimization for General Algorithm Configuration. *Proceedings of LION 2011*, 507–523. *(SMAC)*

### Search-Based Software Engineering (SBSE)

- **Harman, M., McMinn, P., de Souza, J.T. & Yoo, S. (2012). Search-Based Software Engineering: Techniques, Taxonomy, Tutorial. In Bernardo, M., Di Penta, M. & Inverardi, P. (Eds.), *Empirical Software Engineering and Verification: International Summer Schools, LASER 2008–2010*, Lecture Notes in Computer Science vol. 7007. Springer, Berlin, Heidelberg, pp. 1–59.** *(The main SBSE survey recommended for this course)*
- Harman, M. & Jones, B.F. (2001). Search-Based Software Engineering. *Information and Software Technology* 43(14), 833–839. *(Original SBSE paper)*
- Le Goues, C., Nguyen, T., Forrest, S. & Weimer, W. (2012). GenProg: A Generic Method for Automatic Software Repair. *IEEE Transactions on Software Engineering* 38(1), 54–72.
- Fraser, G. & Arcuri, A. (2011). EvoSuite: Automatic Test Suite Generation for Object-Oriented Software. *Proceedings of ESEC/FSE 2011*, 416–419.
- Yoo, S. & Harman, M. (2012). Regression Testing Minimization, Selection and Prioritization: A Survey. *Software Testing, Verification and Reliability* 22(2), 67–120.
- Nair, V., Menzies, T., Siegmund, N. & Apel, S. (2018). Faster Discovery of Faster System Configurations with FLASH. *Proceedings of ESEC/FSE 2018*.
- Menzies, T. et al. (2025). MOOT: Many-Objective Optimization Toolkit. *arXiv:2511.16882*.

### Lecture Notes

- **Grosse, R. Lecture 7: Optimization.** University of Toronto. Available via course notes for CSC321/CSC2541. *(Covers gradient-based and gradient-free optimization; useful complement for the continuous-domain perspective)*
