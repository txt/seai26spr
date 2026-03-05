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



# Homework: Stats, Search, and Assumptions
## Required Files

- [`ez.py`](ez.py) — data, cols, csv, main
- [`sa.py`](sa.py) — sa, oneplus1
- [`locals.py`](locals.py) — ls, lsRminus, saRplus
- [`stats.py`](stats.py) — Confuse, confuse, confused, same, top

As well as MOOT data installed somehwere on your system. Download from 
[http://github.com/timm/moot](http://github.com/timm/moot)


## Part 1: Statistical Assessment

### Exercise 1a: When Accuracy Lies

**Theory.** In binary classification, _accuracy_ = (TP+TN)/N.
When the target class is rare (e.g. 1% positive), a model
that always says "negative" scores 99% accuracy yet catches
zero positives. Precision degrades similarly: as the minority
shrinks, metrics mixing in TN inflate and mislead. Better
alternatives for rare events include pd (recall), pf (false
alarm), or their combinations (F1, G-mean).

**Task.** Using `stats.py`'s `Confuse`/`confuse`/`confused`,
build confusion matrices for a classifier with a _fixed_ 70%
true-positive rate across five imbalance ratios: 50/50,
90/10, 95/5, 99/1, 99.9/0.1. Print acc, pd, pf, prec for
each. Explain (3–4 sentences) why accuracy misleads here.

**Starter kit** (`hw1a.py`):

```python
#!/usr/bin/env python3 -B
"""hw1a.py: accuracy under class imbalance"""
import random
from stats import Confuse, confuse, confused

random.seed(1)

RATIOS = [              # (num_pos, num_neg)
  (50,  50),
  (10,  90),
  (5,   95),
  (1,   99),
  (1,   999)]

TP_RATE = 0.70          # classifier catches 70% of +
FP_RATE = 0.05          # classifier false-alarms 5%

print(f"{'ratio':>10} {'acc':>5} {'pd':>5}"
      f" {'pf':>5} {'prec':>5}")
print("-" * 40)

for n_pos, n_neg in RATIOS:
  cf = Confuse()
  for _ in range(n_pos):
    # TODO: predict "pos" with prob TP_RATE, else "neg"
    got = "???"
    confuse(cf, "pos", got)
  for _ in range(n_neg):
    # TODO: predict "pos" with prob FP_RATE, else "neg"
    got = "???"
    confuse(cf, "neg", got)
  summary = confused(cf, summary=True)
  # TODO: print ratio, summary.acc, summary.pd,
  #       summary.pf, summary.prec
```

**Deliverable.** Filled-in `hw1a.py`, its output table,
and 3–4 sentences on _why_ accuracy grows uninformative.

---------------------------------------------------------------------

### Exercise 1b: What "Top" Means (Weibull Stress Test)

**Theory.** Given _m_ treatments each with _n_ observations,
`top()` returns those treatments statistically
indistinguishable from the best (using Cliff's Delta for
effect size and KS for distribution shape). The `eps`
parameter sets a minimum practical difference—below it,
even a significant split is ignored. A pragmatic choice is
`eps = 0.35 * sd` of a baseline (untreated) distribution:
differences smaller than about a third of the natural
spread are not practically interesting.

**Task.** Generate 20 Weibull treatments (n=20 each).
Compute the pooled sd, set `eps = 0.35 * sd`, then call
`top()`. Repeat 50 times. Report average/min/max number
of winners, and verify winners always have similar means.

**Starter kit** (`hw1b.py`):

```python
#!/usr/bin/env python3 -B
"""hw1b.py: top() with pragmatic eps"""
import random, math, statistics
from stats import top

random.seed(1)

def weibull(n=20):
  shape = random.uniform(0.5, 3)
  scale = random.uniform(1, 4)
  return [min(10,
    scale*(-math.log(random.random()))**(1/shape)*2.5)
    for _ in range(n)]

sizes = []
for trial in range(50):
  rxs = {i: weibull() for i in range(20)}

  # baseline = pool all observations
  pooled = []  # TODO: flatten all rxs values
  sd     = 0   # TODO: statistics.stdev(pooled)

  winners = top(rxs, eps=0.35 * sd)
  sizes.append(len(winners))

  # TODO: check that all winner means are
  #       within eps of each other

print(f"avg winners: {sum(sizes)/len(sizes):.1f}/20")
print(f"min winners: {min(sizes)}")
print(f"max winners: {max(sizes)}")
# TODO: does larger eps -> more or fewer winners? why?
```

**Deliverable.** Filled-in `hw1b.py` plus a short note on
the relationship between `eps` and winner-set size.

---------------------------------------------------------------------

## Part 2: Comparing Local Search Algorithms

### Exercise 2: Tournament on MOOT Data Sets

**Theory.** Simulated annealing (SA) sometimes accepts
worse solutions (cooling schedule) to escape local optima.
Local search (LS) only moves downhill but uses restarts
to explore. `saRplus` adds 100 restarts to SA; `lsRminus`
removes all restarts from LS. A fair comparison: run all
four on identical shuffled subsets, repeat 20 times per
file, then use `top()` to find which are statistically
best. Do this across 120+ MOOT data sets.

**Task.** For every CSV in `moot/optimize/*/*.csv`, run
sa, ls, lsRminus, saRplus on 20 shuffled 50-row samples.
Collect final energies. Call `top()` per file. Count wins.

**Starter kit** (`hw2.py`):

```python
#!/usr/bin/env python3 -B
"""hw2.py: tournament across MOOT data sets"""
import random, glob, statistics, traceback
from ez import csv, Data, shuffle, main, filename
from sa import sa
from locals import ls, lsRminus, saRplus
from stats import top

ALGOS   = [sa, ls, lsRminus, saRplus]
REPEATS = 20
SAMPLE  = 50

def eg__tour(d:filename):
  "run tournament on moot/optimize/*/*.csv"
  files = glob.glob(d + "/*/*.csv")
  print(f"found {len(files)} csv files")
  wins = {a.__name__: 0 for a in ALGOS}

  for f in sorted(files):
    try:
      d0 = Data(csv(f))
      if len(d0.rows) < SAMPLE: continue
    except Exception:
      continue

    # --- baseline: untreated energies for eps ---
    baseline = []
    for _ in range(REPEATS):
      rows = shuffle(d0.rows[:])[:SAMPLE]
      d1   = Data([d0.cols.names] + rows)
      for r in d1.rows:
        baseline.append(d1.disty(r))
    sd = statistics.stdev(baseline) \
         if len(baseline) > 1 else 1

    seen = {a.__name__: [] for a in ALGOS}
    for _ in range(REPEATS):
      rows = shuffle(d0.rows[:])[:SAMPLE]
      d1   = Data([d0.cols.names] + rows)
      for algo in ALGOS:
        # TODO: run algo(d1), iterate to final e
        #   for h, e, row in algo(d1): pass
        #   seen[algo.__name__].append(int(100*e))
        pass

    # TODO: winners = top(seen, eps=0.35 * sd)
    # TODO: for w in winners: wins[w] += 1

  print(f"\n{'algo':>12} {'wins':>6}")
  print("-" * 25)
  for name in sorted(wins):
    print(f"{name:>12} {wins[name]:>6}")

if __name__ == "__main__": main(globals())
```

**Run as:** `python hw2.py --tour moot/optimize`

**Deliverable.** Filled-in `hw2.py`, the output table,
and 3–4 sentences: do restarts help? Does SA beat LS?

---------------------------------------------------------------------

## Part 3: Parametric vs Non-Parametric Assumptions

### Exercise 3: Welford's Num — Does It Matter?

**Theory.** `Num` in `ez.py` is non-parametric: it keeps a
reservoir sample, uses median and IQR spread, assumes
nothing about shape. An alternative: Welford's online
algorithm tracks running mean and variance in O(1) space
but assumes roughly Gaussian data. With no stored lo/hi
we approximate the range as `mu ± 3*sd`. If data is
skewed or heavy-tailed, this Gaussian approximation could
change which algorithm "wins" in Part 2.

**Task.**
1. Write `WelfordNum` (subclass of `Num`) using Welford's
   running stats instead of the reservoir.
2. Monkey-patch `ez.col` so numeric columns use it.
3. Re-run Part 2's tournament.
4. Compare: does the parametric assumption change winners?

**Starter kit** (`hw3.py`):

```python
#!/usr/bin/env python3 -B
"""hw3.py: Welford Num vs reservoir Num"""
import random, math, glob, statistics
from ez import csv, Data, shuffle, Num, col
from sa import sa
from locals import ls, lsRminus, saRplus
from stats import top
import ez

class WelfordNum(Num):
  """Welford online mean/variance. No reservoir.
  Approximate lo/hi as mu +/- 3*sd."""

  def __init__(self, mx=None):
    list.__init__(self)       # empty list (unused)
    self.n    = 0
    self.mu   = 0.0
    self.m2   = 0.0
    self.seen = 0
    self.mx   = mx or 256

  def add(self, v):
    if v == "?": return v
    self.seen += 1
    self.n   += 1
    # TODO: Welford incremental update
    #   delta   = v - self.mu
    #   self.mu += delta / self.n
    #   delta2  = v - self.mu
    #   self.m2 += delta * delta2
    return v

  def sub(self, v):
    if v == "?": return v
    self.seen -= 1
    if self.n <= 1:
      self.n, self.mu, self.m2 = 0, 0.0, 0.0
      return v
    # TODO: reverse Welford
    #   delta   = v - self.mu
    #   self.n -= 1
    #   self.mu -= delta / self.n
    #   delta2  = v - self.mu
    #   self.m2 -= delta * delta2
    return v

  def mid(self):
    return 0  # TODO: return self.mu

  def spread(self):
    return 0  # TODO: sqrt(m2/(n-1)) if n>1 else 0

  def _lo(self): return self.mu - 3*self.spread()
  def _hi(self): return self.mu + 3*self.spread()

  def norm(self, v):
    if v == "?": return v
    lo, hi = self._lo(), self._hi()
    # TODO: normalize v into 0..1 using lo, hi
    #   return 0 if lo==hi else max(0,min(1,...))
    return v

  def pick(self, v=None):
    # TODO: gaussian perturbation around v or mu
    #   base = self.mu if v is None or v=="?" else v
    #   result = random.gauss(base, self.spread())
    #   clamp to [_lo(), _hi()]
    return self.mu

  def distx(self, u, v):
    if u == v == "?": return 1
    u, v = self.norm(u), self.norm(v)
    u = u if u != "?" else (0 if v > 0.5 else 1)
    v = v if v != "?" else (0 if u > 0.5 else 1)
    return abs(u - v)

  def like(self, v, prior=0):
    s = self.spread() + 1e-32
    return ((1/math.sqrt(2*math.pi*s*s))
            * math.exp(-((v-self.mu)**2)/(2*s*s)))

# --- monkey-patch ---
_original_col = ez.col
def welford_col(s):
  if s[0].isupper(): return WelfordNum()
  return _original_col(s)

def run_tour(files, use_welford=False):
  ez.col = welford_col if use_welford else _original_col
  ALGOS   = [sa, ls, lsRminus, saRplus]
  REPEATS = 20; SAMPLE = 50
  wins = {a.__name__: 0 for a in ALGOS}

  for f in sorted(files):
    try:
      d0 = Data(csv(f))
      if len(d0.rows) < SAMPLE: continue
    except Exception:
      continue

    baseline = []
    for _ in range(REPEATS):
      rows = shuffle(d0.rows[:])[:SAMPLE]
      d1   = Data([d0.cols.names] + rows)
      for r in d1.rows:
        baseline.append(d1.disty(r))
    sd = statistics.stdev(baseline) \
         if len(baseline) > 1 else 1

    seen = {a.__name__: [] for a in ALGOS}
    for _ in range(REPEATS):
      rows = shuffle(d0.rows[:])[:SAMPLE]
      d1 = Data([d0.cols.names] + rows)
      for algo in ALGOS:
        # TODO: run algo, collect final energy
        #   for h, e, row in algo(d1): pass
        #   seen[algo.__name__].append(int(100*e))
        pass

    # TODO: winners = top(seen, eps=0.35 * sd)
    # TODO: for w in winners: wins[w] += 1

  for name in sorted(wins):
    print(f"  {name:>12} {wins[name]:>6}")

def eg__compare(d:filename):
  "parametric vs non-parametric tournament"
  files = glob.glob(d + "/*/*.csv")
  print(f"found {len(files)} csv files")
  print("\n=== RESERVOIR (non-parametric) ===")
  run_tour(files, use_welford=False)
  print("\n=== WELFORD (Gaussian) ===")
  run_tour(files, use_welford=True)

if __name__ == "__main__":
  from ez import main
  main(globals())
```

**Run as:** `python hw3.py --compare moot/optimize`

**Deliverable.** Filled-in `hw3.py`, both tables, and
3–4 sentences: does the parametric assumption matter?

---------------------------------------------------------------------

## Part 4 (Grad Students Only): Hyperparameter Sensitivity

### Exercise 4: Do the Knobs Matter?

**Theory.** SA has a cooling parameter `m` (fraction of
x-columns to mutate); LS has a restart count. Practitioners
often spend days tuning such knobs. But if `top()` says
many settings are statistically tied, the tuning was
wasted effort. This connects to the "dodge" result: for
many SE tasks, hyperparameters matter less than algorithm
structure.

**Task.** Vary SA's `m` in {0.1, 0.3, 0.5, 0.7, 0.9}
and LS's restart count in {0, 25, 50, 100, 200}. Run
the MOOT tournament with treatment names as tuples:
`("sa", 0.3)`, `("ls", 50)`, etc. Use `top()` to find
winners per file. Count how often each (algo, param)
tuple wins. Are many settings tied?

Note: Python tuples are hashable, so they work as dict
keys — `top()` doesn't care about key type.

**Starter kit** (`hw4.py`):

```python
#!/usr/bin/env python3 -B
"""hw4.py: hyperparameter sensitivity (grad only)"""
import random, glob, statistics
from ez import csv, Data, shuffle, main, filename
from sa import sa, oneplus1
from locals import ls
from stats import top

SA_MS    = [0.1, 0.3, 0.5, 0.7, 0.9]
LS_RS    = [0, 25, 50, 100, 200]
REPEATS  = 20
SAMPLE   = 50

def eg__hparam(d:filename):
  "hyperparameter sensitivity across MOOT"
  files = glob.glob(d + "/*/*.csv")
  print(f"found {len(files)} csv files")

  # treatment names are tuples
  treatments = ([("sa",m)  for m in SA_MS] +
                [("ls",rs) for rs in LS_RS])
  wins = {t: 0 for t in treatments}

  for f in sorted(files):
    try:
      d0 = Data(csv(f))
      if len(d0.rows) < SAMPLE: continue
    except Exception:
      continue

    # --- baseline eps ---
    baseline = []
    for _ in range(REPEATS):
      rows = shuffle(d0.rows[:])[:SAMPLE]
      d1   = Data([d0.cols.names] + rows)
      for r in d1.rows:
        baseline.append(d1.disty(r))
    sd = statistics.stdev(baseline) \
         if len(baseline) > 1 else 1

    seen = {t: [] for t in treatments}
    for _ in range(REPEATS):
      rows = shuffle(d0.rows[:])[:SAMPLE]
      d1   = Data([d0.cols.names] + rows)
      for name, param in treatments:
        # TODO: if name=="sa":
        #   run sa(d1, m=param), get final e
        # TODO: if name=="ls":
        #   run ls(d1, restarts=param), get final e
        # seen[(name,param)].append(int(100*e))
        pass

    # TODO: winners = top(seen, eps=0.35 * sd)
    # TODO: for w in winners: wins[w] += 1

  print(f"\n{'treatment':>15} {'wins':>6}")
  print("-" * 25)
  for t in sorted(wins, key=lambda t: -wins[t]):
    print(f"{str(t):>15} {wins[t]:>6}")

if __name__ == "__main__": main(globals())
```

**Run as:** `python hw4.py --hparam moot/optimize`

**Deliverable.** Filled-in `hw4.py`, the output table,
and 3–4 sentences: do hyperparameters matter? Are many
settings tied? What does this say about tuning effort?

---------------------------------------------------------------------

## Part 5 (Grad Students Only): Sample Size Sensitivity

### Exercise 5: How Much Data Do You Need?

**Theory.** Part 2 hardcodes `SAMPLE=50`. But how much
data does an optimizer actually need? If 30 rows gives
the same winners as 200, collecting more is wasted effort.
Treatment names are now tuples: `("sa", 50)` = (algorithm,
sample size). When `top()` returns ties, we prefer the
treatment using _fewer_ samples — cheaper data collection
is always better, all else equal.

**Task.** Combine algo × sample-size where sizes are
{30, 50, 100, 200}. Run the tournament. Among tied
winners, award the win to the smallest sample size.

**Starter kit** (`hw5.py`):

```python
#!/usr/bin/env python3 -B
"""hw5.py: sample size sensitivity (grad only)"""
import random, glob, statistics
from ez import csv, Data, shuffle, main, filename
from sa import sa
from locals import ls, lsRminus, saRplus
from stats import top

ALGOS   = [sa, ls, lsRminus, saRplus]
SAMPLES = [30, 50, 100, 200]
REPEATS = 20

def eg__sample(d:filename):
  "sample size sensitivity across MOOT"
  files = glob.glob(d + "/*/*.csv")
  print(f"found {len(files)} csv files")

  # treatments: (algo_name, sample_size)
  treatments = [(a.__name__, n)
                for a in ALGOS for n in SAMPLES]
  wins = {t: 0 for t in treatments}
  algo_by_name = {a.__name__: a for a in ALGOS}

  for f in sorted(files):
    try:
      d0 = Data(csv(f))
      if len(d0.rows) < max(SAMPLES): continue
    except Exception:
      continue

    # --- baseline eps from largest sample ---
    baseline = []
    for _ in range(REPEATS):
      rows = shuffle(d0.rows[:])[:max(SAMPLES)]
      d1   = Data([d0.cols.names] + rows)
      for r in d1.rows:
        baseline.append(d1.disty(r))
    sd = statistics.stdev(baseline) \
         if len(baseline) > 1 else 1

    seen = {t: [] for t in treatments}
    for _ in range(REPEATS):
      for name, n in treatments:
        rows = shuffle(d0.rows[:])[:n]
        d1   = Data([d0.cols.names] + rows)
        algo = algo_by_name[name]
        # TODO: run algo(d1) to get final energy
        #   for h, e, row in algo(d1): pass
        #   seen[(name, n)].append(int(100*e))
        pass

    # TODO: winners = top(seen, eps=0.35 * sd)
    #
    # tiebreak: prefer smallest sample
    # TODO:
    #   best_n  = min(n for (_,n) in winners)
    #   winners = {w for w in winners if w[1]==best_n}
    #
    # TODO: for w in winners: wins[w] += 1

  print(f"\n{'treatment':>20} {'wins':>6}")
  print("-" * 30)
  for t in sorted(wins, key=lambda t: -wins[t]):
    print(f"{str(t):>20} {wins[t]:>6}")

if __name__ == "__main__": main(globals())
```

**Run as:** `python hw5.py --sample moot/optimize`

**Deliverable.** Filled-in `hw5.py`, the output table,
and 3–4 sentences: at what sample size do winners
stabilize? Does less data ever win? What does that
imply for expensive-to-label SE tasks?

---------------------------------------------------------------------

## Submission Checklist

**All students:**
- [ ] `hw1a.py` — imbalance table + explanation
- [ ] `hw1b.py` — Weibull/top experiment + eps note
- [ ] `hw2.py`  — MOOT tournament table + discussion
- [ ] `hw3.py`  — Welford comparison + discussion

**Grad students also:**
- [ ] `hw4.py`  — hyperparameter sensitivity + discussion
- [ ] `hw5.py`  — sample size sensitivity + discussion

**Everyone:** One PDF or markdown with all outputs and
written answers (undergrad: < 2 pages; grad: < 3 pages).
