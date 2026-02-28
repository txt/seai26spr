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


# Naive Bayes: Why "Naive" is Actually Genius

---

## 1. Why Bother? (10 min)

Before we look at the algorithm, let us ask why anyone would
use it in 2024 when we have neural networks and gradient
boosting.

**Speed.** Training means reading each row once and updating
a counter or a sorted list. No matrix inversion, no gradient
descent, no epochs. Classification means one pass over the
columns.

**Memory.** You never store the rows. You store only summary
statistics — a frequency dictionary per symbolic column, a
sorted sample per numeric column. The model size is
proportional to the number of features, not the number of
training examples.

**Incrementality.** You can add a new row in O(1) time, and
— unusually — you can also *remove* a row in O(1) time. This
matters when data expires or when you want a sliding window
over a stream.

**Missing data.** If a value is `"?"`, you just skip that
column's contribution to the likelihood. No imputation, no
crash.

**Surprisingly competitive.** Domingos & Pazzani (1997)
compared NB against C4.5, PEBLS, and CN2 on 28 UCI
datasets. NB won more often than any of them, including
domains with strong attribute dependencies.

We will come back to *why* it works so well at the end.
First, let us build it from scratch.

---

## 2. The Core Idea: Ranking, Not Probabilities (10 min)

Bayes' theorem:

```
P(class | row) = P(class) × P(row | class) / P(row)
```

- **Prior** `P(class)`: how common is this class in training?
- **Likelihood** `P(row | class)`: how plausible is this row
  if we already know the class?
- **Posterior** `P(class | row)`: updated belief after seeing
  the row.

The key insight: we never need the actual posterior value. We
only need to know *which class wins*. The denominator
`P(row)` is the same for every class — it cancels. So we
just compare:

```
P(yes) × P(row | yes)   vs   P(no) × P(row | no)
```

The class with the bigger product wins. That is it. NB is
not a probability estimator — it is a *ranker*.

This distinction matters. As Domingos & Pazzani show, NB's
probability estimates are often badly wrong, but its
*rankings* are correct far more often than you would expect.

**Why "Naive"?** We assume all features are independent given
the class:

```
P(row | class) = P(f1 | class) × P(f2 | class) × ... 
```

This is almost never true. Weather features are correlated.
Words in a document are correlated. But NB still works — we
will prove why in Section 7.

---

## 3. The Zero Problem and Smoothing (5 min)

Suppose we are computing:

```
P(outlook=sunny | yes) × P(windy=true | yes) × ...
```

If `sunny` never appeared in any `yes` row in training, that
term is 0. Zero times anything is zero. The entire product
collapses, and we lose all information from every other
feature. One unseen value nukes the whole row.

**The fix: Laplace smoothing.** Add a small pseudocount to
every frequency before computing the ratio. We use two
smoothing parameters:

- `k` — smooths attribute frequencies (avoids zero when a
  value was never seen for a given class)
- `m` — smooths class priors (avoids zero for rare classes)

The formulas are:

```
P(value | class) = (count + k × prior) / (n_class + k)

P(class)         = (n_class + m) / (n_all + m × n_h)
```

where `n_h` is the number of distinct classes. With `k=1`
and `m=2` (the defaults in `ez_class.py`), no probability
is ever exactly zero, and the estimates are pulled only
gently toward the prior.

---

## 4. Avoiding Underflow: Log Space (5 min)

With many features, we multiply many small numbers together.
On a machine with 64-bit floats, the product quickly rounds
to zero even when the true value is not zero. This is called
**floating-point underflow**.

The fix: take the log of everything. The log of a product
is a sum of logs:

```
log(P(class) × P(f1|class) × P(f2|class) × ...)
= log P(class) + log P(f1|class) + log P(f2|class) + ...
```

Sums do not underflow. We compare log-posteriors, and the
class with the least-negative sum wins. We never convert
back to actual probabilities.

```python
# from ez_class.py
def like(i, row:Row, n_all:int, n_h:int) -> float:
    prior = (len(i.rows)+the.m) / (n_all+the.m*n_h)
    ls = [c.like(v,prior) for at,c in i.cols.x.items()
          if (v:=row[at])!="?"]
    return log(prior) + sum(log(v) for v in ls if v>0)
```

`"?" → skip`. `v > 0 → skip` catches any residual zeros.
The result is a single float, the log-posterior. The class
with the highest (least negative) value is predicted.

---

## 5. The Delegation Protocol (15 min)

`ez_class.py` has three classes that work together:
`Sym`, `Num`, and `Data`. The design pattern is
**delegation**: `Data.like` does not compute likelihoods
itself. It asks each column object for its own likelihood.

```
Data.like(row)
  → for each column c and value v:
      c.like(v, prior)      ← Sym or Num handles this
  → sum the logs
  → return log-posterior
```

### Sym (symbolic columns)

`Sym` is just a `dict` mapping values to counts.

```python
class Sym(dict):
    def add(i, v:Val) -> Val:
        if v != "?": i[v] = i.get(v,0) + 1
        return v

    def sub(i, v:Val) -> Val:
        if v != "?": i[v] = i.get(v,0) - 1
        return v

    def like(i, v:Val, prior:float=0) -> float:
        n = sum(i.values())
        return max(1/BIG, (i.get(v,0) + the.k*prior) / (n + the.k))
```

`add` and `sub` each touch one dictionary entry — O(1).
`like` applies the Laplace formula. `max(1/BIG, ...)` is
a belt-and-suspenders guard against zero.

### Num (numeric columns)

`Num` is a sorted list (via `insort`) that keeps a random
reservoir of at most `the.Keep` values.

```python
class Num(list):
    def add(i, v:Val) -> Val:
        if v != "?":
            i.seen += 1
            if len(i) < i.mx: insort(i, v)
            elif r() < i.mx/i.seen:
                i.pop(int(r()*len(i))); insort(i, v)
        return v

    def sub(i, v:Val) -> Val:
        if v != "?":
            i.seen -= 1
            if (p:=bisect_left(i,v)) < len(i) and i[p]==v:
                i.pop(p)
        return v
```

The reservoir sampling in `add` keeps the list bounded while
maintaining a representative sample. `sub` is an exact
deletion using binary search — O(log n).

For likelihoods, `Num` assumes a Gaussian distribution
parameterised by **median** and **spread**:

```python
    def mid(i) -> float: return i[len(i)//2] if i else 0

    def spread(i) -> float:
        if len(i) < 2: return 0
        n = max(1, len(i)//10)
        a, b = min(9*n, len(i)-1), min(n, len(i)-1)
        return (i[a]-i[b])/2.56

    def like(i, v:Qty, prior:float=0) -> float:
        s = i.spread() + 1/BIG
        return (1/sqrt(2*pi*s*s)) * exp(-((v-i.mid())**2)/(2*s*s))
```

Median is more robust than mean to outliers. The spread
`(90th percentile − 10th percentile) / 2.56` estimates the
standard deviation without being thrown off by extreme
values (2.56 = distance between the 10th and 90th
percentiles of a standard normal).

### Data (the container)

`Data` holds a list of rows and a `Cols` object that maps
column indices to `Sym` or `Num` instances. Column type
is decided by the **name**: uppercase first letter → `Num`,
lowercase → `Sym`.

```python
class Data:
    def add(i, row:Row) -> Row:
        i._mid = None
        for at,c in i.cols.all.items(): c.add(row[at])
        i.rows.append(row)
        return row

    def sub(i, row:Row) -> Row:
        i._mid = None
        for at,c in i.cols.all.items(): c.sub(row[at])
        i.rows.remove(row)
        return row

    def like(i, row:Row, n_all:int, n_h:int) -> float:
        prior = (len(i.rows)+the.m) / (n_all+the.m*n_h)
        ls = [c.like(v,prior) for at,c in i.cols.x.items()
              if (v:=row[at])!="?"]
        return log(prior) + sum(log(v) for v in ls if v>0)
```

`i.cols.x` contains only the input columns (not the class
label, not columns suffixed `X`). So the class column never
contributes to its own likelihood calculation.

**Try it yourself:**

```python
from ez_class import Data, csv
d = Data(csv("weather.csv"))
print(d.mid())            # the "average" row
for row in d.rows:
    print(row, d.like(row, len(d.rows), 2))
```

Rows that are typical of the dataset get higher (less
negative) log-likelihoods.

---

## 6. Incremental Speed: add and sub (10 min)

One of NB's underappreciated strengths is that you can add
*and remove* rows without retraining from scratch. This
matters for:

- **Streaming data**: the model grows with new observations.
- **Sliding windows**: old data expires and is removed.
- **Cross-validation**: hold out a fold by subtracting it,
  evaluate, then add it back.

Watch how `mid()` stays consistent as rows are deleted and
re-added:

```python
# from eg__addsub in ez_class.py
d1 = Data([d.cols.names] + d.rows[:the.Keep])
rows = d1.rows[:]
m1 = d1.mid()

for row in rows[::-1]:      # delete all rows
    d1.sub(row)

for row in rows:            # add them back
    d1.add(row)

m2 = d1.mid()
assert m1 == m2             # identical: order doesn't matter
```

**Try it yourself:**

```bash
./ez_class.py --addsub path/to/diabetes.csv
```

Watch the midpoints at 1/3 and 2/3 capacity match whether
you build the dataset by deleting or by adding. This is the
O(1) update guarantee in action.

---

## 7. Full Example: Classifying Weather Data (20 min)

### The data

```
outlook   temp  humidity  windy  play
sunny      85      85     false   no
sunny      80      90     true    no
overcast   83      86     false   yes
rainy      70      96     false   yes
rainy      68      80     false   yes
rainy      65      70     true    no
overcast   64      65     true    yes
sunny      72      95     false   no
sunny      69      70     false   yes
overcast   75      90     true    no
```

5 yes rows, 5 no rows, n=10.

### Step 1: Priors (m=2, n_h=2)

```
P(yes) = (5+2)/(10+2×2) = 7/14 = 0.500
P(no)  = (5+2)/(10+2×2) = 7/14 = 0.500
```

Equal counts → equal priors. The features will do the work.

### Step 2: Frequency tables

```
outlook:  sunny  overcast  rainy     windy:  false  true
  yes       1       2        2          yes    4      1
  no        3       1        1          no     2      3

temp (sorted):
  yes: [64,68,69,70,83]  median=69  spread=5.86
  no:  [65,72,75,80,85]  median=75  spread=5.08

humidity (sorted):
  yes: [65,70,80,86,96]  median=80  spread=10.16
  no:  [70,85,90,90,95]  median=90  spread=3.91
```

### Step 3: Classify `sunny, temp=72, humidity=90, windy=true`

**Log-posterior for yes** (prior=0.500):

```
outlook=sunny:  (1 + 1×0.5) / (5+1) = 1.5/6  = 0.250
windy=true:     (1 + 1×0.5) / (5+1) = 1.5/6  = 0.250
temp=72:        Gauss(72; μ=69, σ=5.86)        = 0.060
humidity=90:    Gauss(90; μ=80, σ=10.16)       = 0.024

log(0.500) + log(0.250) + log(0.250) + log(0.060) + log(0.024)
= -0.693  + -1.386    + -1.386    + -2.818    + -3.722
= -10.005
```

**Log-posterior for no** (prior=0.500):

```
outlook=sunny:  (3 + 1×0.5) / (5+1) = 3.5/6  = 0.583
windy=true:     (3 + 1×0.5) / (5+1) = 3.5/6  = 0.583
temp=72:        Gauss(72; μ=75, σ=5.08)        = 0.066
humidity=90:    Gauss(90; μ=90, σ=3.91)        = 0.102

log(0.500) + log(0.583) + log(0.583) + log(0.066) + log(0.102)
= -0.693  + -0.539    + -0.539    + -2.717    + -2.281
= -6.769
```

**Decision: no** (−6.769 > −10.005)

The decisive features were `outlook` and `windy`: sunny
appears 3× in no rows and only 1× in yes rows, and true
wind follows the same pattern. Together they outweigh
everything else.

---

## 8. The Full Classifier: bayes_class.py (10 min)

```python
def nbayes(src:Iterable, warmup:int=10) -> Confuse:
    rows = iter(src)
    d    = Data([next(rows)])
    every, ks, cf = Data([d.cols.names]), {}, Confuse()

    def best(k):
        return ks[k].like(r, len(every.rows), len(ks))

    for r in rows:
        k = r[d.cols.klass]
        if k not in ks: ks[k] = Data([d.cols.names])
        if len(every.rows) >= warmup:
            confuse(cf, str(k), str(max(ks, key=best)))
        ks[k].add(every.add(r))
    return cf
```

Walk through each line:

- `d = Data([next(rows)])` — reads the header row to learn
  column names and types.
- `every` — a `Data` that holds all rows regardless of class,
  used for `n_all` (the total row count in the prior formula).
- `ks` — a dict mapping each class label to its own `Data`
  holding only that class's rows.
- `warmup` — we wait for 10 rows before predicting. With
  fewer rows, the frequency tables are too sparse to trust.
- `max(ks, key=best)` — calls `like` on each class-specific
  `Data`, returns the class with the highest log-posterior.
- `confuse(cf, str(k), str(...))` — records want vs got in
  the confusion matrix.
- `ks[k].add(every.add(r))` — the row goes into `every` and
  into its class-specific `Data`. The model learns *after*
  predicting, so we never cheat by training on test data.

This is a true online learner. Every row is classified using
only what came before it, then immediately incorporated into
the model.

**Try it yourself:**

```bash
./bayes_class.py --data path/to/soybean.csv
```

You should see a table of `pd`, `pf`, `prec`, `acc` per
class. Soybean is one of the datasets where NB achieves
100% accuracy (Domingos & Pazzani Table 1).

---

## 9. Why It Works: The Optimality Result (10 min)

Here is the surprising theory behind NB's practical success.
Domingos & Pazzani (1997) ask: when is NB *optimal* even
when its independence assumption is false?

**Zero-one loss** means we only care whether the predicted
class is correct or not. We don't care how wrong the
probability estimate is, as long as the right class wins.

**Theorem 1** (Domingos & Pazzani): NB is optimal under
zero-one loss for a given example if and only if

```
(p ≥ ½  and  r ≥ s)   or   (p ≤ ½  and  r ≤ s)
```

where `p = P(+ | example)` is the true class probability,
`r = P(+) ∏ P(Aj | +)` is NB's discriminant for class `+`,
and `s` is the same for class `−`.

**Corollary 1**: This condition holds over exactly *half the
volume* of all possible (p, r, s) combinations. The
independence assumption, by contrast, is needed only on a
second-order infinitesimal fraction of that space. So NB's
true region of optimality is vastly larger than the
independence assumption suggests.

Put plainly: NB only needs to get the *sign* right, not the
*magnitude*. Even if its probability estimates are badly
wrong, it will pick the correct class as long as the ranking
is preserved.

**Conjunctions and disjunctions** (Theorems 7 & 8): NB is
provably globally optimal for learning conjunctive and
disjunctive concepts — even though these concepts
decisively violate the independence assumption.

**Small sample advantage**: Because NB has low variance
(it stores O(features) parameters, not O(rows)), it often
outperforms C4.5 on datasets with fewer than ~1000 rows
even when C4.5's learning bias is more appropriate. At
small sample sizes, variance dominates bias, and NB wins.

---

## 10. When NB Struggles, and Fixes (10 min)

NB's independence assumption creates two systematic biases
that Rennie et al. (ICML 2003) identified for text
classification. Both have simple fixes.

### Problem 1: Skewed training data

If class A has 1000 training examples and class B has 10,
NB will produce weight estimates for class B that are
systematically too low (because the log function is concave
and the expectation of log is less than log of expectation
for small samples). The classifier then unfairly prefers
class A.

**Fix: Complement Naive Bayes (CNB)**. Estimate weights for
class C using all examples *not* in class C:

```
θ̂_{ci_complement} = (N_{ci_complement} + α) / (N_{c_complement} + α×vocab)
```

Each class now uses a roughly equal amount of training data
for its estimates. CNB's weights are more stable across
varying dataset sizes (see Rennie et al. Figure 1).

### Problem 2: Word dependencies inflate magnitudes

When two words always appear together ("San" and
"Francisco"), NB double-counts their evidence. The
magnitude of the weight vector for the dependent class
grows artificially large, biasing predictions toward it.

**Fix: Weight normalization**. Divide each weight by the
sum of absolute weights for that class:

```
ŵ_{ci} = log θ̂_{ci} / Σ_k |log θ̂_{ck}|
```

This keeps classes with more dependencies from dominating.

### The result

Plain MNB on Industry Sector: **58%** accuracy.  
Transformed Weight-normalized CNB (TWCNB): **92%**.  
Support Vector Machine: **93%**.

TWCNB approaches SVM accuracy while being far faster and
easier to implement. For the full transform pipeline (log
term frequency, IDF weighting, length normalization,
complement estimation, weight normalization) see Table 4 of
Rennie et al.

The key lesson: NB's failures are not fundamental — they
are correctable with simple, motivated heuristics.

---

## 11. Summary

| Property         | Why it helps                                    |
|------------------|-------------------------------------------------|
| O(1) add/sub     | streaming, expiry, cross-validation             |
| O(features) mem  | no rows stored, model stays small               |
| Handles "?"      | just skip that column's likelihood term         |
| Log space        | avoids floating-point underflow                 |
| Smoothing        | avoids zero probabilities for unseen values     |
| Ranking only     | doesn't need good probability estimates to win  |
| Optimal for AND/OR| works despite independence assumption failure  |
| Low variance     | beats complex models on small datasets          |

NB is not a toy. It is the right first model to try — fast
to implement, interpretable, incremental, and surprisingly
hard to beat at small to medium dataset sizes.

---

## 12. Lab Exercises

### A: Explore the likelihood scores

```bash
./ez_class.py --like path/to/weather.csv
```

Which rows get the highest log-likelihood? Which the lowest?
What does that tell you about the "typical" row?

### B: Sensitivity to smoothing

Edit `the.k` and `the.m` in `ez_class.py` (line 12-14).

- Set `k=0`. What happens to `Sym.like` when it encounters
  a value it has never seen for a given class?
- Set `m=0`. What happens to the prior for a very rare class?
- Restore defaults and re-run. Do the confusion matrix
  numbers change? By how much?

### C: Change the warmup

In `bayes_class.py`, change `warmup=10` to `warmup=1`.

- Does accuracy improve or degrade on soybean?
- Now try `warmup=50`. What happens on a small dataset?
- Why does warmup exist at all?

### D: add/sub consistency check

```bash
./ez_class.py --addsub path/to/diabetes.csv
```

The assert at the end checks that midpoints after deletion
equal midpoints after insertion. Read the code. Why does the
order of deletion not matter? What would break if `sub`
decremented `seen` but did not remove the value from the
list?

### E: Try complement NB (advanced)

Using `ez_class.py` primitives, implement Complement NB:
for each class, build a `Data` from all rows *not* in that
class, and use its `like` score negated for classification.
Compare accuracy on `diabetes.csv` against the standard NB.
