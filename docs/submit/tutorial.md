# Theoretical Foundations for ezr.py and sa.py

This document explains the statistical, algorithmic, and software engineering concepts underlying `ezr.py` (a lightweight data mining toolkit) and `sa.py` (a simulated annealing optimizer). 

---

## 1. Incremental Statistics

### The Problem with Batch Statistics

Computing mean and standard deviation typically requires two passes over data:

```
μ = (1/n) Σ xᵢ           # first pass: compute mean
σ = √[(1/n) Σ (xᵢ - μ)²]  # second pass: compute variance
```

This is impractical for streaming data or when memory is constrained.

### Welford's Online Algorithm

Welford (1962) discovered a numerically stable single-pass algorithm. The key insight is maintaining running values that update incrementally:

```python
def add(i, v):
  # ...
  if "mu" in i:  # Num column
    d = v - i.mu
    i.mu += d / i.n
    i.m2 += d * (v - i.mu)  # Note: uses NEW i.mu
  # ...
```

The algorithm maintains:
- `i.mu`: running mean
- `i.m2`: sum of squared deviations from the current mean

**Why two different `d` values?** The line `i.m2 += d * (v - i.mu)` uses `d` (computed with the *old* mean) multiplied by the deviation from the *new* mean. This algebraic trick maintains the correct sum of squared deviations.

Standard deviation is then:

```python
def sd(i): return 0 if i.n < 2 else sqrt(i.m2 / (i.n - 1))
```

The `n-1` denominator is Bessel's correction for sample standard deviation (unbiased estimator).

---

## 2. Entropy and Information Theory

For symbolic (categorical) data, we measure "spread" using Shannon entropy:

```python
def ent(i):    
  return -sum(p*log(p,2) for n in i.has.values() if (p := n/i.n) > 0)
```

**Interpretation:** Entropy measures the average "surprise" or information content. Given a distribution over symbols:

- If one symbol dominates (p ≈ 1), entropy → 0 (no surprise)
- If all symbols equally likely, entropy is maximized (maximum uncertainty)

For k equally-likely symbols: H = log₂(k) bits.

**Example:** For `"aaaabbc"`:
- P(a) = 4/7, P(b) = 2/7, P(c) = 1/7
- H = -(4/7)log₂(4/7) - (2/7)log₂(2/7) - (1/7)log₂(1/7) ≈ 1.38 bits

---

## 3. Generating Gaussian Random Numbers

The code uses a clever approximation based on the Central Limit Theorem:

```python
def gauss(mu, sd1):
  return mu + 2 * sd1 * (sum(random.random() for _ in range(3)) - 1.5)
```

**How it works:**

1. `random.random()` returns Uniform(0,1) with mean=0.5, variance=1/12
2. Sum of 3 uniforms has mean=1.5, variance=3/12=0.25, sd=0.5
3. Subtracting 1.5 centers at zero
4. Multiplying by 2 scales sd from 0.5 to 1.0
5. Final scaling by `sd1` and shifting by `mu` gives N(mu, sd1²)

**Why only 3 samples?** The CLT converges quickly for uniform distributions. Three samples gives adequate approximation for most purposes, and it's fast.

---

## 4. Normalization Techniques

### Z-Score (Standard Score)

The z-score expresses how many standard deviations a value lies from the mean:

```python
def z(i, v): return (v - i.mu) / (sd(i) + 1/BIG)
```

The `1/BIG` prevents division by zero when sd=0.

**Properties:**
- z = 0 at the mean
- z = 1 means one standard deviation above mean
- Approximately 68% of data falls within z ∈ [-1, 1]
- Approximately 95% within z ∈ [-2, 2]

### Sigmoid Normalization

Raw z-scores are unbounded. The sigmoid function maps them to (0, 1):

```python
def norm(z): return 1 / (1 + exp(-1.7 * max(-3, min(3, z))))
```

This is a modified logistic function:

```
norm(z) = 1 / (1 + e^(-1.7z))
```

**Design choices:**

1. **Clamping to [-3, 3]:** Values beyond ±3 standard deviations are extreme outliers (~0.3% of normal data). Clamping prevents numerical overflow and reduces outlier influence.

2. **The 1.7 coefficient:** Standard logistic uses coefficient 1.0, giving norm(±3) ≈ {0.05, 0.95}. The 1.7 stretches the sigmoid so that ±3σ maps closer to {0, 1}, using more of the output range.

```
z     | norm(z) with 1.7
------+-----------------
-3    | 0.006
-1    | 0.154
 0    | 0.500
+1    | 0.846
+3    | 0.994
```

---

## 5. Distance Metrics

### Minkowski Distance

The generalized Minkowski distance between points x and y:

```
d(x,y) = (Σ |xᵢ - yᵢ|^p)^(1/p)
```

The code computes the *averaged* Minkowski distance:

```python
def minkowski(src):
  n, d = 0, 0
  for v in src: n, d = n + 1, d + v ** the.p
  return 0 if n == 0 else (d / n) ** (1 / the.p)
```

**Special cases:**
- p = 1: Manhattan distance (city-block)
- p = 2: Euclidean distance (default)
- p → ∞: Chebyshev distance (maximum coordinate difference)

**Why average?** Dividing by n makes the distance independent of dimensionality, allowing fair comparison across datasets with different numbers of features.

### Heterogeneous Distance (aha function)

Real datasets mix numeric and symbolic attributes. The `aha` function (named after David Aha's instance-based learning work) handles both:

```python
def aha(i, u, v):
  if u == v == "?": return 1           # both unknown: maximum distance
  if "has" in i: return u != v         # symbolic: 0 if same, 1 if different
  u = "?" if u == "?" else norm(z(i, u))
  v = "?" if v == "?" else norm(z(i, v))
  u = u if u != "?" else (0 if v > 0.5 else 1)  # unknown: assume worst case
  v = v if v != "?" else (0 if u > 0.5 else 1)
  return abs(u - v)                    # numeric: absolute difference
```

**Key design decisions:**

1. **Symbolic attributes:** Binary distance (0 or 1). This is the "overlap metric."

2. **Numeric attributes:** Normalized then differenced. Since both values are in [0,1], the distance is also in [0,1].

3. **Missing values:** Assume the worst case. If one value is known and > 0.5 (high), assume the unknown is 0 (low), maximizing distance. This is conservative—we don't pretend to know what we don't.

### Distance in X-space vs Y-space

The code separates:

- **distx:** Distance using independent variables (features/predictors)
- **disty:** Distance using dependent variables (goals/targets)

```python
def disty(i, row):
  return minkowski(norm(z(c, row[c.at])) - c.goal for c in i.cols.y)

def distx(i, row1, row2):
  return minkowski(aha(c, row1[c.at], row2[c.at]) for c in i.cols.x)
```

---

## 6. Multi-Objective Optimization

### Goal Encoding

Column names encode optimization direction:
- Suffix `+` or no suffix: maximize (goal = True = 1)
- Suffix `-`: minimize (goal = False = 0)

```python
def Num(n=0, s=" "): return Obj(at=n, txt=s, n=0, mu=0, m2=0, goal=s[-1]!="-")
```

### Scalarization via Distance-to-Heaven

Multi-objective optimization typically produces a Pareto frontier. For simplicity, we scalarize: combine multiple objectives into one number.

```python
def disty(i, row):
  return minkowski(norm(z(c, row[c.at])) - c.goal for c in i.cols.y)
```

**Interpretation:** Each objective is normalized to [0,1]. The "heaven point" is where all goals are achieved:
- For maximization goals: heaven = 1
- For minimization goals: heaven = 0

The `disty` function computes distance from this heaven point. **Lower is better.**

**Example:** For columns `[Weight-, Mpg+]`:
- A car with low weight (normalized to 0.2) and high mpg (normalized to 0.8)
- Goals: [0, 1] (minimize weight, maximize mpg)
- Distances from goals: |0.2 - 0| = 0.2, |0.8 - 1| = 0.2
- disty = √((0.2² + 0.2²)/2) ≈ 0.2

---

## 7. Simulated Annealing

Simulated annealing (Kirkpatrick et al., 1983) is a probabilistic optimization algorithm inspired by metallurgical annealing—slowly cooling metal to reduce defects.

### Core Idea

SA explores a solution space by:
1. Starting from a random solution
2. Repeatedly generating "neighbor" solutions via small mutations
3. Always accepting better solutions
4. Sometimes accepting worse solutions (to escape local optima)
5. Gradually reducing the probability of accepting worse solutions

### The Metropolis-Hastings Criterion

The key insight is the acceptance probability for worse solutions:

```
P(accept) = exp((current_energy - new_energy) / temperature)
```

Where:
- **Energy** = solution quality (lower is better, like `disty`)
- **Temperature** = starts high, decreases over time

**Behavior:**

| Condition | Result |
|-----------|--------|
| New solution is better | Always accept (probability > 1) |
| New solution is worse, high temperature | Often accept (explore) |
| New solution is worse, low temperature | Rarely accept (exploit) |

**Intuition:** Early on (high temperature), we explore freely, accepting worse solutions to escape local optima. Later (low temperature), we become greedy, only accepting improvements.

### Temperature Schedule

A simple linear cooling schedule:

```
T = 1 - (iteration / max_iterations)
```

- Starts at T = 1 (hot, exploratory)
- Ends at T → 0 (cold, greedy)

### Mutation Operators

To generate neighbor solutions, we mutate the current solution:

**Symbolic attributes:** Sample from the observed distribution. If a column has seen {red: 10, blue: 5, green: 2}, sample proportionally.

**Numeric attributes:** Add Gaussian noise centered at current value. The standard deviation of the column is a natural scale for "small" mutations. Use modulo arithmetic to keep values within observed bounds [LO, HI].

### Mutation Rate

Rather than mutating all features, mutate a random subset (e.g., 50%). This balances:
- Too few mutations → slow exploration
- Too many mutations → essentially random restart

---

## 8. Surrogate Modeling

### The Expensive Evaluation Problem

In many optimization scenarios, evaluating a solution's true quality is expensive (physical experiments, simulations, human evaluation). A **surrogate model** provides a cheap approximation.

### Nearest Neighbor as Surrogate

The simplest surrogate: find the most similar known solution and assume similar quality.

1. Given a candidate solution (with unknown Y-values)
2. Find its nearest neighbor in X-space (feature space)
3. Copy that neighbor's Y-values to the candidate
4. Compute quality from the borrowed Y-values

**Assumption:** Similar inputs produce similar outputs (smoothness/continuity). This is the foundation of instance-based learning.

**Trade-off:** The surrogate is only as good as the training data. Predictions in unexplored regions are unreliable—but SA's acceptance criterion will eventually reject poor solutions.

---

## 9. Python Implementation Patterns

### Duck Typing for Polymorphism

Instead of class hierarchies, we use structural typing:

```python
if "mu" in i:   # it's a Num
if "has" in i:  # it's a Sym  
if "rows" in i: # it's a Data
```

**Advantages:**
- No inheritance complexity
- Objects are just dictionaries with conventions
- Easy serialization (dicts are JSON-compatible)

### The Obj Class

```python
class Obj(dict):
  __getattr__, __setattr__, __repr__ = dict.__getitem__, dict.__setitem__, o
```

This one-liner creates a dict subclass where:
- `obj.x` is equivalent to `obj["x"]` (attribute access)
- `obj.x = v` is equivalent to `obj["x"] = v` (attribute assignment)
- `repr(obj)` uses our custom `o()` pretty-printer

### Factory Functions vs Classes

```python
def Num(n=0, s=" "): return Obj(at=n, txt=s, n=0, mu=0, m2=0, goal=s[-1]!="-")
```

Factory functions (capitalized by convention) return configured Obj instances. This is simpler than full classes when:
- No method inheritance needed
- Behavior is in standalone functions
- Objects are primarily data containers

### The `i` Convention

Throughout the code, `i` refers to "this instance"—the object being operated on:

```python
def add(i, v):    # add v to instance i
def mid(i):       # get midpoint of instance i
def sd(i):        # get standard deviation of instance i
```

This is a deliberate choice to avoid `self` outside of class definitions, keeping the functional style while maintaining clarity about which object is being modified.

---

## 10. Useful Functions in ezr.py

For your implementation, these functions are available:

| Function | Purpose |
|----------|---------|
| `nearest(data, row, rows)` | Find closest row to `row` in `rows` using X-distance |
| `distx(data, row1, row2)` | Distance between two rows in feature space |
| `disty(data, row)` | Distance from row to "heaven" (lower = better) |
| `gauss(mu, sd)` | Generate Gaussian random number |
| `sd(col)` | Standard deviation of a Num column |
| `pick(d, n)` | Weighted random selection from dict `d` with total count `n` |

---

---

# Advanced Topics (Graduate Students)

The following sections cover theoretical foundations and extensions beyond the basic implementation.

---

## A1. Convergence Theory for Simulated Annealing

### SA as a Markov Chain

Each state in SA is a solution; transitions are proposed mutations accepted or rejected by the Metropolis criterion. This defines a **Markov chain** where the probability of moving from state `i` to state `j` depends only on `i`, not on history.

The transition probability from solution `i` to solution `j` is:

```
P(i → j) = g(i,j) · α(i,j)
```

Where:
- `g(i,j)` = probability of *proposing* j from i (mutation distribution)
- `α(i,j)` = probability of *accepting* the proposal

For the Metropolis criterion:

```
α(i,j) = min(1, exp((E(i) - E(j)) / T))
```

### Detailed Balance

SA satisfies **detailed balance** (reversibility):

```
π(i) · P(i → j) = π(j) · P(j → i)
```

Where `π` is the stationary distribution. At temperature T, this distribution is the **Boltzmann distribution**:

```
π(i) ∝ exp(-E(i) / T)
```

As T → 0, this distribution concentrates on global minima.

### Cooling Schedule and Convergence

**Theorem (Geman & Geman, 1984):** SA converges to a global optimum with probability 1 if the cooling schedule satisfies:

```
T(k) ≥ C / log(k + 1)
```

Where C is related to the maximum "energy barrier" in the landscape.

**Practical implication:** Logarithmic cooling is *very* slow. The linear schedule `T = 1 - k/K` used in our implementation does not guarantee convergence but works well in practice. This is the exploration-exploitation tradeoff: theoretical guarantees require impractical runtimes.

### Alternative Cooling Schedules

| Schedule | Formula | Properties |
|----------|---------|------------|
| Linear | T = 1 - k/K | Simple, fast, no guarantees |
| Geometric | T = T₀ · αᵏ (α ≈ 0.95) | Slower cooling, common in practice |
| Logarithmic | T = C / log(k+1) | Theoretically optimal, impractically slow |
| Adaptive | Adjust based on acceptance rate | Self-tuning, more complex |

**Geometric cooling** is popular: if α = 0.95 and T₀ = 1, after 100 iterations T ≈ 0.006.

---

## A2. Connection to MCMC Methods

### Metropolis-Hastings in Context

The acceptance criterion in SA is a special case of the **Metropolis-Hastings algorithm**, a cornerstone of Bayesian inference and computational statistics.

General Metropolis-Hastings:

```
α(i,j) = min(1, [π(j) · q(j→i)] / [π(i) · q(i→j)])
```

Where:
- π is the target distribution we want to sample from
- q is the proposal distribution

When q is symmetric (q(i→j) = q(j→i)), this simplifies to:

```
α(i,j) = min(1, π(j) / π(i))
```

For SA with Boltzmann distribution:

```
π(j)/π(i) = exp(-E(j)/T) / exp(-E(i)/T) = exp((E(i) - E(j)) / T)
```

This recovers our acceptance criterion.

### SA vs. MCMC Sampling

| Aspect | MCMC Sampling | Simulated Annealing |
|--------|---------------|---------------------|
| Goal | Sample from distribution | Find optimum |
| Temperature | Fixed | Decreasing |
| Output | Samples (many) | Single best solution |
| Guarantees | Converges to π | Converges to optimum (with log cooling) |

**Insight:** SA is "MCMC with a cooling schedule." At fixed T, we'd sample from Boltzmann; by cooling, we concentrate samples at the mode (optimum).

---

## A3. Beyond Nearest Neighbor: Gaussian Process Surrogates

### Limitations of 1-NN Surrogate

The nearest-neighbor surrogate in our implementation is simple but limited:

1. **No uncertainty quantification:** We get a point estimate, not a confidence interval
2. **Discontinuous:** Small moves in X can jump to different neighbors
3. **No extrapolation:** Far from data, predictions are meaningless

### Gaussian Process Regression

A **Gaussian Process (GP)** defines a distribution over functions. Given training points, the posterior is also a GP, providing:

- **Mean prediction:** μ(x) — the surrogate's estimate
- **Variance:** σ²(x) — uncertainty (high far from training data)

The GP is defined by a kernel function k(x, x') measuring similarity. Common choice:

```
k(x, x') = exp(-||x - x'||² / 2ℓ²)  # RBF/squared exponential
```

### Bayesian Optimization

**Bayesian Optimization (BO)** combines GP surrogates with intelligent sampling. Instead of random mutations, BO selects the next point by optimizing an **acquisition function**:

**Expected Improvement (EI):**
```
EI(x) = E[max(0, f_best - f(x))]
```

This balances:
- **Exploitation:** Sample where μ(x) is good
- **Exploration:** Sample where σ(x) is high (uncertain regions)

**Comparison:**

| Method | Surrogate | Next Point Selection | Evaluations |
|--------|-----------|---------------------|-------------|
| SA + 1-NN | Nearest neighbor | Random mutation + Metropolis | Many (thousands) |
| Bayesian Opt | Gaussian Process | Maximize acquisition function | Few (tens to hundreds) |

BO is preferred when true evaluations are *very* expensive (hours/days per evaluation). SA is preferred for cheap evaluations or high-dimensional spaces (GPs scale as O(n³)).

---

## A4. Multi-Objective Theory

### Pareto Dominance

Solution **a dominates b** (written a ≻ b) if:
- a is at least as good as b in all objectives
- a is strictly better than b in at least one objective

The **Pareto frontier** is the set of non-dominated solutions—no solution dominates any frontier member.

### Why Scalarization?

Our `disty` function scalarizes multiple objectives into one number. This is convenient but has limitations:

**Weighted sum:** `f(x) = Σ wᵢ · fᵢ(x)`
- Can only find solutions on **convex** portions of Pareto frontier
- Different weights find different solutions

**Distance to ideal (our approach):** `f(x) = ||normalize(x) - goal||`
- Can find non-convex regions
- Assumes objectives are commensurable after normalization

**Chebyshev scalarization:** `f(x) = max_i |wᵢ · (fᵢ(x) - goalᵢ)|`
- Guaranteed to find any Pareto-optimal point with appropriate weights
- More robust than weighted sum

### Multi-Objective SA

Rather than scalarizing, **multi-objective SA** maintains an archive of non-dominated solutions:

1. Generate neighbor by mutation
2. If neighbor is non-dominated by archive, add it
3. Remove any archive members dominated by neighbor
4. Accept moves toward less-crowded regions of frontier

Algorithms: AMOSA (Archived Multi-Objective SA), PESA, NSGA-II (genetic algorithm variant).

---

## A5. The Curse of Dimensionality

### Why High Dimensions Break Instance-Based Methods

Our distance-based surrogate relies on "similar inputs → similar outputs." In high dimensions, this intuition fails.

**Concentration of distances:** In d dimensions, for uniformly distributed points:

```
E[dist_max] / E[dist_min] → 1  as d → ∞
```

All points become approximately equidistant. "Nearest" neighbor becomes meaningless.

**Volume of hypersphere:** The volume of a d-dimensional unit ball:

```
V_d = π^(d/2) / Γ(d/2 + 1)
```

This goes to 0 as d → ∞. Most volume concentrates in a thin shell near the surface. To capture a fixed fraction of data, neighborhoods must grow exponentially with dimension.

### Implications for SA

1. **Distance metrics become unreliable** in high-d spaces
2. **More training data needed** — exponential in dimension
3. **Feature selection matters** — reduce dimension before optimization

**Mitigations:**
- Use only relevant features (our `cols.x` vs `cols.y` separation helps)
- Normalize features (our z-score + sigmoid)
- Consider dimensionality reduction (PCA) for very high-d problems
- Use learned distance metrics

---

## A6. Mutation Distribution Design

### Theoretical Considerations

The mutation distribution g(i,j) affects SA's efficiency. Desirable properties:

1. **Ergodicity:** Any state reachable from any other (eventually)
2. **Local bias:** Small changes more likely than large ones
3. **Adaptive scale:** Mutation size should match landscape features

### Gaussian Mutation Analysis

Our implementation: `new = old + N(0, σ)` where σ = column standard deviation.

**Why column SD?** It's a natural scale:
- Features with high variance get larger mutations
- Features with low variance get smaller mutations
- No manual tuning required

**Self-adaptive mutation (advanced):** Evolve σ alongside the solution:

```
σ' = σ · exp(τ · N(0,1))
x' = x + N(0, σ')
```

This is used in Evolution Strategies (ES). Large σ survives if exploration helps; small σ survives near optima.

### Mutation Rate Analysis

With mutation rate m, expected number of changed features = m · d.

| m | Changed features (d=10) | Behavior |
|---|------------------------|----------|
| 0.1 | 1 | Very local, slow exploration |
| 0.5 | 5 | Balanced |
| 0.9 | 9 | Nearly random restart |

**Theory suggests:** Start with higher m (exploration), decrease over time (exploitation). This parallels temperature cooling. Our fixed m = 0.5 is a compromise.

---

## A7. Landscape Analysis

### Fitness Landscape Concepts

A **fitness landscape** visualizes solution quality over the search space:
- **Peaks/valleys:** Local optima
- **Ridges:** Connected regions of good solutions
- **Plateaus:** Flat regions where gradient is zero

### Landscape Characteristics Affecting SA

**Ruggedness:** Many local optima close together
- SA struggles; needs high T for long time
- Consider: memetic algorithms (SA + local search)

**Deceptiveness:** Gradient points away from global optimum
- SA's random acceptance helps
- Consider: different distance metrics

**Neutrality:** Many solutions with equal fitness
- Random walk on plateaus
- Consider: drift strategies, larger mutations

### Big Valley Hypothesis

Many combinatorial problems exhibit "big valley" structure:
- Local optima are clustered
- Better local optima are closer to global optimum
- Distance to best correlates with quality

If true, local search + restarts works well. SA exploits this by eventually settling into the "big valley" containing the global optimum.

---

## References

- Welford, B.P. (1962). "Note on a method for calculating corrected sums of squares and products." *Technometrics*.
- Shannon, C.E. (1948). "A Mathematical Theory of Communication." *Bell System Technical Journal*.
- Kirkpatrick, S., Gelatt, C.D., Vecchi, M.P. (1983). "Optimization by Simulated Annealing." *Science*.
- Aha, D.W., Kibler, D., Albert, M.K. (1991). "Instance-Based Learning Algorithms." *Machine Learning*.
- Geman, S., Geman, D. (1984). "Stochastic Relaxation, Gibbs Distributions, and the Bayesian Restoration of Images." *IEEE TPAMI*.
- Rasmussen, C.E., Williams, C.K.I. (2006). *Gaussian Processes for Machine Learning*. MIT Press.
- Deb, K. (2001). *Multi-Objective Optimization using Evolutionary Algorithms*. Wiley.
- Beyer, H.-G., Schwefel, H.-P. (2002). "Evolution Strategies: A Comprehensive Introduction." *Natural Computing*.
