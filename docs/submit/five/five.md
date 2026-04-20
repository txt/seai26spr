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

# Homework 5: Are Your Results Actually Different?

**Deadline:** One week from release date.

**Deliverables:** `hw5a.py`, `hw5b.py`, `hw5c.py`, and `writeup.md`.

Submit pages stapled together. Page 1 has group number and student names and IDs.

Do **not** submit datasets.

---

## Required Packages

```bash
pip install pymoo scikit-learn pandas numpy matplotlib
```

No data files to download — the MOOT dataset is fetched inside the scripts.

---

## Background

### The MOOT Dataset (used throughout)

All three exercises use the same pre-evaluated hyperparameter table from the MOOT benchmark:

```
URL = "https://raw.githubusercontent.com/timm/moot/master/optimize/hpo/Health-ClosedIssues0000.csv"
```

This CSV has rows of hyperparameter configurations for a `RandomForestRegressor` (columns: `N_estimators`, `criterion`, `Min_sample_leaves`, `Min_impurity_decrease`, `Max_depth`) and their measured outcomes (`MRE-` is Mean Relative Error to minimize, `ACC+` and `PRED40+` are accuracy metrics to maximize). Because training takes time, the table was computed once; optimizers *search* the table rather than re-running experiments.

### Three Searchers

You will compare three strategies for picking a row from this table:

- **Default:** Always return the row closest to sklearn's default hyperparameters (`n_estimators=100, criterion="squared_error", min_samples_leaf=1, min_impurity_decrease=0.0, max_depth=None`). This is the "no optimization" baseline — it answers the question *how well does the model do with factory settings?*
- **Random:** Pick a random row from the table each time. Represents unguided random search.
- **GA:** The Genetic Algorithm optimizer from HW4b — intelligently searches the table using selection, crossover, and mutation.

### Why Repeat Runs? Why Scott-Knott?

A single optimizer run is a single random walk. It might get lucky or unlucky. To make fair claims, we need to characterize *typical* performance across many runs with different random seeds.

Once we have distributions of scores from multiple runs, we need a principled way to ask: *are these distributions actually different, or just noise?* The **Scott-Knott** test answers this by recursively splitting a ranked list of treatments into groups that are statistically distinguishable from each other (using a KS test and Cliff's delta effect size). Treatments in the same group are considered equivalent.

The `stats.py` module (provided in the same folder as this homework, **do not modify**) implements this for you via the `top(rxs)` function:

```python
from stats import top, same
# rxs is a dict mapping treatment name → list of scores (lower is better)
# top() returns the set of names in the *best* (lowest) group
winners = top({"GA": ga_scores, "Random": rand_scores, "Default": default_scores})
```

`top()` always selects for *lower* values. Since MRE is something we minimize, this fits perfectly. `same(x, y)` returns `True` if two lists are statistically indistinguishable.

---

## Exercise 5a: Seed Sensitivity on the MOOT Dataset

**Theory.** In HW4 you saw seed sensitivity on a live cross-validation problem. Here you apply the same idea to the MOOT table lookup. Because the table lookup is deterministic — the same hyperparameters always return the same row — all variability comes from *which configurations the GA proposes* across its random initialization and mutation. Running 10 seeds quantifies that variability and establishes a credible distribution of GA performance.

**Task.** Complete the four `TODO` sections below. For each of 10 seeds (0–9), run `MixedVariableGA(pop_size=10)` for 50 generations on `MOOTHPOProblem` and record the **final best MRE** found. Fill in the results table in `writeup.md` and answer the questions.

**Starter kit** (`hw5a.py`):

```python
#!/usr/bin/env python3 -B
"""hw5a.py: Seed sensitivity of the GA on the MOOT HPO table."""
import numpy as np
import pandas as pd
import statistics
from pymoo.core.problem import ElementwiseProblem
from pymoo.core.variable import Integer, Real, Choice
from pymoo.core.callback import Callback
from pymoo.core.mixed import MixedVariableGA
from pymoo.optimize import minimize
from pymoo.termination import get_termination

# ── load MOOT table ────────────────────────────────────────────────────
URL = ("https://raw.githubusercontent.com/timm/moot/master"
       "/optimize/hpo/Health-ClosedIssues0000.csv")
df = pd.read_csv(URL)

obj_cols  = [c for c in df.columns if c.endswith('+') or c.endswith('-')]
feat_cols = [c for c in df.columns if c not in obj_cols]

df_enc = df.copy()
df_enc["criterion"] = (df["criterion"] == "absolute_error").astype(float)

feat_vals = df_enc[feat_cols].values.astype(float)
feat_min  = feat_vals.min(axis=0)
feat_max  = feat_vals.max(axis=0)
feat_norm = (feat_vals - feat_min) / (feat_max - feat_min + 1e-9)

Y_data  = df[obj_cols].values.astype(float)
signs   = np.array([-1.0 if c.endswith('+') else 1.0 for c in obj_cols])
Y_pymoo = Y_data * signs

def lookup(x: dict) -> int:
    crit  = 1.0 if x["criterion"] == "absolute_error" else 0.0
    query = np.array([x["N_estimators"], crit,
                      x["Min_sample_leaves"],
                      x["Min_impurity_decrease"],
                      x["Max_depth"]], dtype=float)
    q_norm = (query - feat_min) / (feat_max - feat_min + 1e-9)
    dists  = np.linalg.norm(feat_norm - q_norm, axis=1)
    return int(np.argmin(dists))

class MOOTHPOProblem(ElementwiseProblem):
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
        idx     = lookup(x)
        mre_col = obj_cols.index("MRE-")
        # TODO 1: Set out["F"] to the MRE for the matched row.
        #         Use Y_pymoo[idx, mre_col].
        out["F"] = 0.0  # ← replace this line

class HistoryCallback(Callback):
    def __init__(self):
        super().__init__()
        self.gen_best = []

    def notify(self, algorithm):
        # TODO 2: Append the minimum F value this generation to self.gen_best.
        #         Hint: float(algorithm.pop.get("F").min())
        pass

# ── run 10 seeds ───────────────────────────────────────────────────────
N_SEEDS    = 10
all_finals = []

for seed in range(N_SEEDS):
    cb = HistoryCallback()
    minimize(
        MOOTHPOProblem(),
        MixedVariableGA(pop_size=10),
        termination=get_termination("n_gen", 50),
        seed=seed,
        callback=cb,
        verbose=False
    )
    # TODO 3: Append the FINAL best MRE from this run to all_finals.
    #         cb.gen_best is a list with one entry per generation;
    #         the last entry is the best score the GA reached.
    pass

# TODO 4: Print the results table and summary statistics.
#
#   Seed | Final MRE
#   -----+----------
#      0 | X.XXXX
#      ...
#   Mean : X.XXXX
#   Stdev: X.XXXX
#   Best seed : N  (MRE = X.XXXX)
#   Worst seed: N  (MRE = X.XXXX)
#
#   Use statistics.mean() and statistics.stdev().
#   Use all_finals.index(min(all_finals)) for the best seed index.
```

**Fill in this table in `writeup.md`** (replace `???` with your values):

```
Seed | Final MRE
-----+----------
   0 | ???
   1 | ???
   2 | ???
   3 | ???
   4 | ???
   5 | ???
   6 | ???
   7 | ???
   8 | ???
   9 | ???

Mean : ???
Stdev: ???
Best seed : ???  (MRE = ???)
Worst seed: ???  (MRE = ???)
```

**Answer these questions in `writeup.md`** (3–4 sentences each):

1. How large is the gap between your best and worst seed? If someone ran just one seed and reported it as "the result," what problem does this create for scientific reproducibility?
2. Compare the standard deviation of your GA runs to the range `[df["MRE-"].min(), df["MRE-"].max()]`. How much of the table's total MRE range does one standard deviation span?
3. Based on this table alone, is seed 0 meaningfully better than seed 5? What additional analysis would let you answer this properly?

---

## Exercise 5b: Scott-Knott Ranking of GA, Random, and Default

**Theory.** Now that you know a single run is noisy, run all three searchers 10 times each and apply the **Scott-Knott** test to determine which — if any — are statistically distinguishable. Scott-Knott works by sorting treatments by mean, then recursively splitting them into groups wherever the split produces the largest between-group variance *and* the two halves are statistically different (KS test + Cliff's delta). Treatments in the same final group are considered equivalent — you cannot claim one beats the other.

The three searchers are:

- **Default:** Use the `lookup()` function with a fixed dict representing sklearn defaults: `{"N_estimators": 100, "criterion": "squared_error", "Min_sample_leaves": 1, "Min_impurity_decrease": 0.0, "Max_depth": 20}`. Returns the same row every time — no randomness, so 10 "runs" all give the same MRE. This is intentional: it models a practitioner who never tunes.
- **Random:** Pick a uniformly random row index from the table (`np.random.randint(0, len(df))`). Each seed gives a different random row and thus a different MRE.
- **GA:** From Exercise 5a — the best MRE found after 50 generations with `pop_size=10`.

**Task.** Complete the five `TODO` sections below. Run the script, paste the Scott-Knott output table into `writeup.md`, and answer the questions.

**Starter kit** (`hw5b.py`):

```python
#!/usr/bin/env python3 -B
"""hw5b.py: Scott-Knott comparison of GA, Random, and Default on MOOT table."""
import numpy as np
import pandas as pd
from pymoo.core.problem import ElementwiseProblem
from pymoo.core.variable import Integer, Real, Choice
from pymoo.core.callback import Callback
from pymoo.core.mixed import MixedVariableGA
from pymoo.optimize import minimize
from pymoo.termination import get_termination
from stats import top, same   # provided — do NOT modify stats.py

# ── load MOOT table ────────────────────────────────────────────────────
URL = ("https://raw.githubusercontent.com/timm/moot/master"
       "/optimize/hpo/Health-ClosedIssues0000.csv")
df = pd.read_csv(URL)

obj_cols  = [c for c in df.columns if c.endswith('+') or c.endswith('-')]
feat_cols = [c for c in df.columns if c not in obj_cols]
mre_col   = obj_cols.index("MRE-")

df_enc = df.copy()
df_enc["criterion"] = (df["criterion"] == "absolute_error").astype(float)

feat_vals = df_enc[feat_cols].values.astype(float)
feat_min  = feat_vals.min(axis=0)
feat_max  = feat_vals.max(axis=0)
feat_norm = (feat_vals - feat_min) / (feat_max - feat_min + 1e-9)

Y_data  = df[obj_cols].values.astype(float)
signs   = np.array([-1.0 if c.endswith('+') else 1.0 for c in obj_cols])
Y_pymoo = Y_data * signs
MRE_ALL = df["MRE-"].values   # raw MRE for every row (used for random)

def lookup(x: dict) -> int:
    crit  = 1.0 if x["criterion"] == "absolute_error" else 0.0
    query = np.array([x["N_estimators"], crit,
                      x["Min_sample_leaves"],
                      x["Min_impurity_decrease"],
                      x["Max_depth"]], dtype=float)
    q_norm = (query - feat_min) / (feat_max - feat_min + 1e-9)
    dists  = np.linalg.norm(feat_norm - q_norm, axis=1)
    return int(np.argmin(dists))

# ── MOOT problem (same as hw5a) ────────────────────────────────────────
class MOOTHPOProblem(ElementwiseProblem):
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
        idx = lookup(x)
        out["F"] = Y_pymoo[idx, mre_col]

class HistoryCallback(Callback):
    def __init__(self):
        super().__init__()
        self.gen_best = []
    def notify(self, algorithm):
        self.gen_best.append(float(algorithm.pop.get("F").min()))

# ── collect 10 runs per treatment ─────────────────────────────────────
N_SEEDS  = 10
ga_scores      = []
random_scores  = []
default_scores = []

# sklearn-default hyperparameters snapped to table bounds
DEFAULT_CONFIG = {
    "N_estimators":          100,
    "criterion":             "squared_error",
    "Min_sample_leaves":     1,
    "Min_impurity_decrease": 0.5,   # clamped to table lower bound
    "Max_depth":             20,    # clamped to table upper bound
}

for seed in range(N_SEEDS):
    np.random.seed(seed)

    # TODO 1: Run the GA (pop_size=10, 50 generations) with this seed.
    #         Append the final best MRE (last entry in cb.gen_best) to ga_scores.
    pass

    # TODO 2: Append a random row's MRE to random_scores.
    #         Pick a random row index: np.random.randint(0, len(df))
    #         Then use MRE_ALL[idx].
    pass

    # TODO 3: Append the default config's MRE to default_scores.
    #         Use lookup(DEFAULT_CONFIG) to get the nearest row index,
    #         then MRE_ALL[that index].
    #         (All 10 default scores will be identical — that's correct.)
    pass

# ── Scott-Knott via stats.top() ────────────────────────────────────────
rxs = {
    "GA":      ga_scores,
    "Random":  random_scores,
    "Default": default_scores,
}

# TODO 4: Call top(rxs) to get the set of best-performing treatment names.
#         Assign the result to `winners`.
winners = set()  # ← replace this line

# TODO 5: Print a ranked summary table.
#
#   Rank all three treatments by their mean MRE (ascending).
#   Mark treatments in `winners` with a star (*).
#   Format:
#
#   Rank | Treatment | Mean MRE | Stdev  | Best   | In top group?
#   -----|-----------|----------|--------|--------|-------------
#      1 | GA        | X.XXXX   | X.XXXX | X.XXXX | *
#      2 | Random    | X.XXXX   | X.XXXX | X.XXXX |
#      3 | Default   | X.XXXX   | X.XXXX | X.XXXX |
#
#   Also print whether any pair is statistically indistinguishable:
#     same(ga_scores, random_scores)  → True/False
#     same(ga_scores, default_scores) → True/False
#     same(random_scores, default_scores) → True/False
import statistics as st
```

**Paste the printed table into `writeup.md`** and **answer these questions** (3–4 sentences each):

1. Which treatment(s) are in the top Scott-Knott group? Does the GA statistically beat random search? Does it beat the default?
2. All 10 default runs return the same MRE — they have zero variance. Does having no variance help or hurt in a Scott-Knott test? What does it mean for a searcher to have zero variance?
3. `same()` uses both Cliff's delta and a KS test. Why are *two* statistical criteria needed rather than just one? What does each test catch that the other might miss?
4. If the GA is in the same Scott-Knott group as Random, what does that imply about whether hyperparameter optimization is worth the computational cost for this dataset?

---

## Exercise 5c: Plotting Your hw5b Results

**Theory.** Numbers in a table are precise but hard to read at a glance. Two standard plots make the same information immediately intuitive: a **box plot** shows spread and overlap between treatments, while an **ECDF** shows where each searcher lands relative to the full landscape of possible scores in the table.

**No new experiments.** Copy your `ga_scores`, `random_scores`, and `default_scores` lists directly from hw5b — just paste them into the placeholders at the top of the script.

**Task.** Complete the two `TODO` sections below to produce a single two-panel figure saved as `hw5c_plot.png`.

**Starter kit** (`hw5c.py`):

```python
#!/usr/bin/env python3 -B
"""hw5c.py: Two-panel summary plot using your hw5b scores (no new runs)."""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from stats import top   # provided — do NOT modify stats.py

# ── paste your hw5b scores here ────────────────────────────────────────
# Replace the placeholder lists with your actual hw5b output.
ga_scores      = [...]   # 10 values
random_scores  = [...]   # 10 values
default_scores = [...]   # 10 values (all identical is fine)

# ── load table for reference lines only (no new optimizer runs) ────────
URL     = ("https://raw.githubusercontent.com/timm/moot/master"
           "/optimize/hpo/Health-ClosedIssues0000.csv")
df      = pd.read_csv(URL)
MRE_ALL = df["MRE-"].values

winners = top({"GA": ga_scores, "Random": random_scores, "Default": default_scores})

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
fig.suptitle("HW5 Summary: GA vs Random vs Default on MOOT Table", fontsize=13)

# ── TODO 1: Box plot (left panel) ─────────────────────────────────────
# Draw side-by-side box plots for ga_scores, random_scores, default_scores.
# Append " *" to the label of any treatment whose name is in `winners`.
# Add a horizontal dashed red line for MRE_ALL.min()       (table best).
# Add a horizontal dashed grey line for np.median(MRE_ALL) (table median).
# y-axis label: "Final MRE".  Title: "Score Distributions".
#
# Hint:
#   labels = ["GA *" if "GA" in winners else "GA", ...]
#   ax1.boxplot([ga_scores, random_scores, default_scores], labels=labels, ...)
#   ax1.axhline(MRE_ALL.min(), color="red",  linestyle="--", ...)
#   ax1.axhline(np.median(MRE_ALL), color="grey", linestyle="--", ...)
pass   # ← replace with your code

# ── TODO 2: ECDF (right panel) ────────────────────────────────────────
# Plot ECDFs for: MRE_ALL (grey, thin), ga_scores (steelblue), random_scores (orange).
# Mark default_scores[0] as a vertical dashed red line.
# x-label: "MRE".  y-label: "Cumulative Fraction".  Title: "ECDF".
# Add a legend.
#
# Hint for one ECDF:
#   sv  = np.sort(values)
#   cdf = np.arange(1, len(sv)+1) / len(sv)
#   ax2.plot(sv, cdf, ...)
pass   # ← replace with your code

plt.tight_layout()
plt.savefig("hw5c_plot.png", dpi=120)
plt.close()
print("Saved hw5c_plot.png")
```

**Answer these questions in `writeup.md`** (2–3 sentences each):

1. In the box plot, which treatment has the largest interquartile range? What does a wide box tell you about that searcher's reliability across seeds?
2. In the ECDF, does the GA curve sit clearly to the left of the Random curve, or do they overlap? What would overlap mean for the claim that GA outperforms random search?
3. The Default scores form a flat point (zero variance) in both plots. Why is zero variance not necessarily a good thing for a searcher?

---

## Submission Checklist

- [ ] `hw5a.py` — seed sensitivity on MOOT, printed table, + 3 discussion questions answered in `writeup.md`
- [ ] `hw5b.py` — Scott-Knott comparison of GA / Random / Default, printed table, + 4 discussion questions answered in `writeup.md`
- [ ] `hw5c.py` — `hw5c_plot.png` (two-panel figure), + 3 discussion questions answered in `writeup.md`
- [ ] `writeup.md` — all tables, all answers

One submission with all code, outputs, plots, and written answers (keep written answers brief).
