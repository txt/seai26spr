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

# Homework: Hyperparameter Optimization with pymoo
---

## **Course Reference**
| Date | Lecture Topic |
| :--- | :--- |
| **Mar 09** | [Optimization Algorithms](../../../docs/lect/optimization_tutorial.md) |

---
## **Deliverables** 

`hw4a.py`, `hw4b.py`, results, and writeup.

Submit pages stapled together. Page 1 has group number and student names and IDs.

Do **not** submit datasets.

---

## Required Packages

Install once in your terminal before starting:

```bash
pip install pymoo scikit-learn pandas numpy
```

No data files to download — all datasets are fetched inside the scripts.

---

## Background: pymoo in 60 Seconds

pymoo always **minimizes**. Every algorithm is just a different strategy for finding small `F` values. You define **what** to optimize (a `Problem`) and pymoo handles **how**. The same `minimize()` call works for GA, DE, NSGA-II — only the second argument changes.

```python
from pymoo.optimize import minimize
res = minimize(problem, algorithm, termination, seed=42)
# res.F  → objective value(s) of best solution found
# res.X  → the decision variables that achieved it
```

Three things pymoo needs from you:

1. **`xl`, `xu`** — lower and upper bounds on each variable
2. **`n_obj`** — how many objectives you have (1 for single-objective)
3. **`out["F"]`** — what you set in `_evaluate`; must be a number pymoo can **minimize**

One subtlety: `sklearn`'s `cross_val_score(..., scoring="neg_mean_squared_error")` returns **negative** numbers (e.g., `-3200.0`) so that "higher is better" works inside sklearn. pymoo always minimizes, so we flip the sign: `out["F"] = -scores.mean()` gives a **positive** MSE that pymoo drives down. Getting this sign right is the most common beginner mistake.

---

## Part 1: Your First HPO Problem

### Exercise 4a: GA on the Diabetes Dataset

**Theory.** A Genetic Algorithm (GA) maintains a **population** of candidate solutions. In hyperparameter optimization (HPO), each individual in the population is one set of hyperparameters (e.g., `max_depth=5, min_samples_leaf=3`). The GA evaluates every individual by actually training the model and measuring held-out error (cross-validation). Over generations, selection pressure keeps good configs alive; mutation and crossover explore new ones. The GA has no idea what the model is — it just sees a number to minimize. This separation is what makes the approach general: swap the model, keep the GA.

**About the baseline.** Before optimizing anything, the script measures how well a `DecisionTreeRegressor` performs using sklearn's *default* hyperparameters (no tuning at all). This default MSE is the **baseline** — it answers the question: *what does the model score without any help?* Every improvement the GA finds is then measured against this number. Reporting only the optimized result without the baseline would make it impossible to judge whether the effort was worthwhile. The printed line `Default Decision Tree MSE: XXXX.XX` is your starting point; the final `Improvement over default: XX.XX%` tells you how much the GA helped.

**The model: `DecisionTreeRegressor`.** Unlike `RandomForestRegressor` (an ensemble of many trees), a single decision tree is one recursive binary splitter. It is faster to evaluate — important when cross-validation calls `_evaluate` hundreds of times — but has higher variance. The three knobs we tune are:

- `max_depth` ∈ [1, 50] — how deep the tree can grow; deeper trees can overfit
- `min_samples_leaf` ∈ [1, 50] — minimum samples required at a leaf; larger values regularize
- `min_samples_split` ∈ [2, 50] — minimum samples to attempt a split at an internal node

**Task.** Complete the four `TODO` sections below. Run the script and fill up the expected output table. Then answer these questions in 3–4 sentences each:

1. The verbose output prints `f_avg` and `f_min` each generation. Does `f_min` always decrease, or can it stay flat? Why?
2. The search space has three integer knobs: `max_depth` ∈ [1,50], `min_samples_leaf` ∈ [1,50], `min_samples_split` ∈ [2,50]. **With arithmetic**, compute the total number of configurations. How does that compare to the 500 evaluations a 10-population, 50-generation GA performs? What does this tell you about how a GA works?
3. Look at your final "winning" hyperparameters. Are any of them exactly at the edge of the allowed range (e.g., `max_depth` = 1 or 50)? Generally, if a value hits the boundary, what does that suggest about your defined search space?

**Starter kit** (`hw4a.py`):

```python
#!/usr/bin/env python3 -B
"""hw4a.py: GA hyperparameter search on the Diabetes dataset."""
import numpy as np
from sklearn.datasets import load_diabetes
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import cross_val_score
from pymoo.core.problem import ElementwiseProblem
from pymoo.core.variable import Integer
from pymoo.core.callback import Callback
from pymoo.core.mixed import MixedVariableGA
from pymoo.optimize import minimize
from pymoo.termination import get_termination

# ── data ──────────────────────────────────────────────────────────────
X, y = load_diabetes(return_X_y=True)   # 442 patients, 10 features

# ── baseline: sklearn defaults ─────────────────────────────────────────
# Train with NO tuning to establish a comparison point.
# Every improvement the GA finds is measured against this number.
default_model = DecisionTreeRegressor(random_state=42)
default_scores = cross_val_score(default_model, X, y, cv=3,
                                 scoring="neg_mean_squared_error")
DEFAULT_MSE = -default_scores.mean()
print(f"Default Decision Tree MSE   : {DEFAULT_MSE:.2f}")

# ── problem ───────────────────────────────────────────────────────────
class RFHPOProblem(ElementwiseProblem):
    """
    Each individual = one set of DecisionTree hyperparameters.
    pymoo calls _evaluate() once per individual per generation.
    x is a dict; access knobs as x["max_depth"] etc.
    """
    def __init__(self):
        vars = {
            "max_depth":         Integer(bounds=(1,  50)),
            "min_samples_leaf":  Integer(bounds=(1,  50)),
            "min_samples_split": Integer(bounds=(2,  50)),
        }
        super().__init__(vars=vars, n_obj=1)

    def _evaluate(self, x, out, *args, **kwargs):
        model = DecisionTreeRegressor(
            max_depth=int(x["max_depth"]),
            min_samples_leaf=int(x["min_samples_leaf"]),
            min_samples_split=int(x["min_samples_split"]),
            random_state=42
        )
        # cross_val_score returns NEGATIVE MSE (e.g. -3200.0).
        # TODO 1: Run 3-fold cross-validation on `model` using X and y,
        #         with scoring="neg_mean_squared_error".
        #         Then set out["F"] to the POSITIVE mean MSE so pymoo
        #         can minimize it. Smaller out["F"] = better model.
        #         Hint: out["F"] = -scores.mean()
        scores = None   # ← replace: call cross_val_score here
        out["F"] = 0.0  # ← replace: negate scores.mean()

# ── callback: records best score per generation ────────────────────────
class HistoryCallback(Callback):
    """
    pymoo calls notify() at the end of every generation.
    algorithm.pop holds the current population of individuals.
    .get("F") returns an (n, 1) array of objective values.
    """
    def __init__(self):
        super().__init__()
        self.gen_best = []
        self.gen_avg  = []   # will store per-generation average MSE

    def notify(self, algorithm):
        f_values = algorithm.pop.get("F")   # shape: (pop_size, 1)
        # TODO 2a: append the MINIMUM F value in this generation to self.gen_best.
        #          Hint: float(f_values.min())
        pass

        # TODO 2b: append the MEAN (average) F value in this generation
        #          to self.gen_avg. This lets you see how the whole population
        #          improves, not just the single best individual.
        #          Hint: float(f_values.mean())
        pass

# ── run ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    callback = HistoryCallback()

    res = minimize(
        RFHPOProblem(),
        MixedVariableGA(pop_size=10),
        termination=get_termination("n_gen", 50),
        seed=42,
        callback=callback,
        verbose=True    # prints: n_gen | n_eval | f_avg | f_min each generation
    )

    # TODO 3: Compute the percentage improvement the GA achieved over the
    #         default baseline.
    #         improvement = ((DEFAULT_MSE - res.F[0]) / DEFAULT_MSE) * 100
    improvement = 0.0   # ← replace this line

    # TODO 4: Print the best MSE, the winning hyperparameter values, and
    #         the improvement computed above.
    #         res.F[0]                    → best objective value (MSE)
    #         res.X["max_depth"]          → best max_depth found
    #         res.X["min_samples_leaf"]   → best min_samples_leaf found
    #         res.X["min_samples_split"]  → best min_samples_split found
    #
    #         Format your output like:
    #           Default Decision Tree MSE   : XXXX.XX
    #           Best MSE found              : XXXX.XX
    #           max_depth                   = XX
    #           min_samples_leaf            = XX
    #           min_samples_split           = XX
    #           Improvement over default    : XX.XX%
```

**Expected output shape** (Fill up with your output):
```
n_gen  | n_eval  | f_avg    | f_min
-----  | ------  | ------   | ------
1      | 10      | XXXX.XX  | XXXX.XX
2      | 20      | XXXX.XX  | XXXX.XX
...
50     | 500     | XXXX.XX  | XXXX.XX

Default Decision Tree MSE   : XXXX.XX
Best MSE found              : XXXX.XX
max_depth                   = XX
min_samples_leaf            = XX
min_samples_split           = XX
Improvement over default    : XX.XX%
```

**Deliverable.** Filled-in `hw4a.py`, its printed output, and answers to the three questions above.

---

### Exercise 4b: Searching a Pre-Evaluated Table

**Theory.** Running `cross_val_score` for every candidate works on a small dataset, but imagine the model takes hours to train. Researchers handle this by **pre-evaluating** a large grid of configurations and storing results in a table. The optimizer then **searches the table** rather than re-running experiments — the same idea behind the MOOT benchmark used throughout this course.

There is one catch: the GA proposes continuous candidates, but the table only contains rows that were actually evaluated. We snap each proposal to the **nearest row** using Euclidean distance in normalized feature space. This lookup is fully provided below — read it carefully to understand how it works, but you don't need to rewrite it.

**Task.** Complete the three `TODO` blocks below. Run the script and print the output. Then answer in 3–4 sentences each:

1. Compare `res.F[0]` (GA's best MRE) to `df["MRE-"].min()` (the best row in the full table). How close did the GA get?
2. The GA runs `50 × 10 = 500` evaluations on a table with many more rows. What fraction of the table did it actually visit? Is this efficient?
3. Why is nearest-neighbor lookup necessary here? What would break if we skipped it?

**Starter kit** (`hw4b.py`):

```python
#!/usr/bin/env python3 -B
"""hw4b.py: GA HPO on a MOOT pre-evaluated config table."""
import numpy as np
import pandas as pd
from pymoo.core.problem import ElementwiseProblem
from pymoo.core.variable import Integer, Real, Choice
from pymoo.core.callback import Callback
from pymoo.core.mixed import MixedVariableGA
from pymoo.optimize import minimize
from pymoo.termination import get_termination

# ── load data directly from GitHub — no local file needed ─────────────
URL = ("https://raw.githubusercontent.com/timm/moot/master"
       "/optimize/hpo/Health-ClosedIssues0000.csv")
df = pd.read_csv(URL)
print(f"Table: {df.shape[0]} rows × {df.shape[1]} columns")
print(df.head(3))

# ── parse MOOT column conventions ─────────────────────────────────────
#   column ends with '-'  →  minimize this metric
#   column ends with '+'  →  maximize (we flip the sign for pymoo)
obj_cols  = [c for c in df.columns if c.endswith('+') or c.endswith('-')]
feat_cols = [c for c in df.columns if c not in obj_cols]

# encode the one categorical column as 0/1 so arithmetic works on it
df_enc = df.copy()
df_enc["criterion"] = (df["criterion"] == "absolute_error").astype(float)

# normalise every feature column to [0, 1] using the table's own min/max
feat_vals = df_enc[feat_cols].values.astype(float)
feat_min  = feat_vals.min(axis=0)
feat_max  = feat_vals.max(axis=0)
feat_norm = (feat_vals - feat_min) / (feat_max - feat_min + 1e-9)

# flip sign of '+' objectives so pymoo can minimise everything uniformly
Y_data  = df[obj_cols].values.astype(float)
signs   = np.array([-1.0 if c.endswith('+') else 1.0 for c in obj_cols])
Y_pymoo = Y_data * signs   # MRE- stays positive; ACC+/PRED40+ become negative

# ── baseline: median MRE across all pre-evaluated rows ────────────────
# The median of the table tells us what a random (unoptimized) config
# typically achieves. Improvement is measured against this baseline.
BASELINE_MRE = df["MRE-"].median()
print(f"Median MRE (baseline): {BASELINE_MRE:.4f}")

# ── nearest-neighbour lookup (provided — read it, don't rewrite it) ───
def lookup(x: dict) -> int:
    """
    Snap a GA candidate config to the closest row in the table.

    Steps:
      1. Build a query vector matching the column order in feat_norm.
      2. Encode 'criterion' as 1.0 (absolute_error) or 0.0.
      3. Normalise the query using the table's feat_min / feat_max.
      4. Compute Euclidean distance from the query to all rows at once
         (numpy broadcasts the subtraction across feat_norm's rows).
      5. Return the index of the closest row.
    """
    crit = 1.0 if x["criterion"] == "absolute_error" else 0.0
    query = np.array([x["N_estimators"], crit,
                      x["Min_sample_leaves"],
                      x["Min_impurity_decrease"],
                      x["Max_depth"]], dtype=float)
    q_norm = (query - feat_min) / (feat_max - feat_min + 1e-9)
    dists  = np.linalg.norm(feat_norm - q_norm, axis=1)
    return int(np.argmin(dists))

# ── problem ────────────────────────────────────────────────────────────
class MOOTHPOProblem(ElementwiseProblem):
    """Single objective: minimise MRE by searching the pre-evaluated table."""
    def __init__(self):
        vars = {
            "N_estimators":          Integer(bounds=(40, 200)),
            "Min_sample_leaves":     Integer(bounds=(1,  18)),
            "Min_impurity_decrease": Real(bounds=(0.5, 6.75)),
            "Max_depth":             Integer(bounds=(4,  20)),
            "criterion": Choice(options=["squared_error", "absolute_error"]),
        }
        super().__init__(vars=vars, n_obj=1)

    def _evaluate(self, x, out, *args, **kwargs):
        idx     = lookup(x)              # snap to nearest table row
        mre_col = obj_cols.index("MRE-")
        # TODO 1: Set out["F"] to the MRE value for the matched row.
        #         Use Y_pymoo[idx, mre_col].
        #         out["F"] must be a positive number; smaller = better.
        out["F"] = 0.0   # ← replace this line

# ── callback ───────────────────────────────────────────────────────────
class HistoryCallback(Callback):
    def __init__(self):
        super().__init__()
        self.gen_best = []

    def notify(self, algorithm):
        # TODO 2: Append the minimum F value in this generation to
        #         self.gen_best, exactly as you did in hw4a.
        #         Hint: float(algorithm.pop.get("F").min())
        pass

callback = HistoryCallback()

# ── run ────────────────────────────────────────────────────────────────
res = minimize(
    MOOTHPOProblem(),
    MixedVariableGA(pop_size=10),
    termination=get_termination("n_gen", 50),
    seed=42,
    callback=callback,
    verbose=True
)

# TODO 3: Compute the following values and print the summary block below.
#         total_evals = n_gen × pop_size  (fill in the numbers)
#         best_mre    = res.F[0]
#         improvement = percentage improvement of best_mre over BASELINE_MRE
#                       formula: ((BASELINE_MRE - best_mre) / BASELINE_MRE) * 100
#
#         Then print:
#           Median MRE (baseline)     : X.XXXX
#           Best MRE found (GA)       : X.XXXX
#           Best MRE in table         : X.XXXX   ← use df["MRE-"].min()
#           Improvement over baseline : XX.XX%
#           GA evaluated ~NNN configs out of NNN in the table
total_evals = 0      # ← replace
best_mre    = 0.0    # ← replace
improvement = 0.0    # ← replace
```

**Deliverable.** Filled-in `hw4b.py`, its printed output, and answers to the three questions above.

---

## Submission Checklist

- [ ] `hw4a.py` — 4 TODOs (full code) + print summary + writeup
- [ ] `hw4b.py` — 3 TODOs (full code) + print summar + writeup

Submit one submission with all codes, outputs and written answers (keep written answers brief).