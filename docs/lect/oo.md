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


# ez_class.py — Tutorial

---

# Part 1: Idioms

---

## 1. Walrus Operator `:=` mid-expression

Assigns a variable *and* uses it in the same expression.

```python
return -sum(p*log(p,2) for k in i if (p:=i[k]/n)>0)
```

`p` is assigned `i[k]/n`, tested `>0`, then used in `p*log(p,2)` —
all in one pass. Equivalent longhand:

```python
total = 0
for k in i:
    p = i[k] / n
    if p > 0:
        total += p * log(p, 2)
return -total
```

---

## 2. Docstring as Config Store

```python
the = o(**{k:cast(v) for k,v in re.findall(r"(\S+)=(\S+)", __doc__)})
```

The module docstring contains lines like `  -s seed=1`. The regex
finds every `key=value` pair, casts them to int/float/str, and builds
a config namespace. So `the.seed == 1`. To change a default, edit
the docstring — the code follows automatically.

---

## 3. Reservoir Sampling in `Num.add`

Keeps a fixed-size random sample of a stream without storing all of it.

```python
if len(i) < i.mx:
    insort(i, v)
elif r() < i.mx/i.seen:
    i.pop(int(r()*len(i)))
    insort(i, v)
```

Once the buffer is full, each new value has probability `mx/seen` of
replacing a random existing value. The result is a sorted uniform
random sample of at most `mx` items, regardless of stream length.

---

## 4. `next(items := iter(items))`

```python
i.cols = Cols(next(items := iter(items)))
[i.add(row) for row in items]
```

- `iter(items)` wraps the input as an iterator (harmless if already one)
- `:=` rebinds `items` to that iterator
- `next(...)` pops the *header row* for `Cols`
- The remaining rows are still in `items` for the list comp below

One expression consumes the header and advances the cursor.

---

## 5. Lambda as `__repr__`

```python
__repr__ = lambda i: str(i.names)
```

Equivalent to `def __repr__(self): return str(self.names)`. Python
just needs a callable bound to the dunder name. The parameter is
`i` not `self` — a consistent style choice throughout the file.

---

## 6. `col()` — Naming Convention as Type Dispatch

```python
def col(s:str): return (Num if s[0].isupper() else Sym)()
```

Column *names* encode their type: `"Weight"` → `Num`, `"color"` → `Sym`.
The `()` at the end calls whichever class was chosen, returning a
fresh instance. Convention doing the work of a type annotation.

---

## 7. Annotations as Runtime Coercers in `main()`

```python
def eg_s(n:int): the.seed=n; random.seed(n)

f(*[make(args.pop(0)) for make in f.__annotations__.values()])
```

`f.__annotations__` returns `{'n': int}`. The code uses `int` (the
type hint) *as a function* to cast the raw `sys.argv` string.
Type hints here do double duty: documentation *and* arg parsing.

---

# Part 2: Concepts Newbies Find Confusing

---

## Column Naming Conventions

Column names are not just labels — they control behavior:

| Suffix | Meaning                          | Goes into    |
|--------|----------------------------------|--------------|
| `+`    | y-goal, maximize                 | `cols.y`     |
| `-`    | y-goal, minimize                 | `cols.y`     |
| `!`    | class label (for Bayes etc.)     | `cols.klass` |
| `X`    | ignore this column               | neither      |
| upper  | numeric (`Num`)                  | `cols.x`     |
| lower  | symbolic (`Sym`)                 | `cols.x`     |

Everything without a special suffix goes into `cols.x` as a predictor.

---

## "Heaven" and `disty`

"Heaven" is the ideal point: all goals simultaneously at their best.
`disty` measures how far a row falls short of heaven:

```python
def disty(i, r:Row) -> float:
    return minkowski(c.norm(r[at]) - i.cols.w[at]
                     for at,c in i.cols.y.items())
```

`cols.w[at]` is `True` (1.0) for maximize (`+`) and `False` (0.0)
for minimize (`-`). After `norm`, a maximized column wants to be
near 1, so `norm(v) - 1` is near 0 when good. A minimized column
wants to be near 0, so `norm(v) - 0` is near 0 when good.
`sorty` floats the best rows to the top by sorting on `disty`.

---

## x cols vs y cols

`cols.x` are the *inputs* (predictors). `cols.y` are the *outputs*
(goals). Most methods that compute distance or likelihood use only
`cols.x` — because at prediction time you may not know the y values.
`disty` uses only `cols.y` — because it measures outcome quality.

---

## Why `log` in `like`

Naive Bayes multiplies many small probabilities:

```
P(class) * P(col1|class) * P(col2|class) * ...
```

Each factor may be 0.01 or smaller. With enough columns the product
underflows to zero (floating point can't represent it). Taking logs
converts multiplication to addition, which stays numerically stable:

```python
return log(prior) + sum(log(v) for v in ls if v>0)
```

The result is a log-likelihood. To compare classes you only need to
know which is *largest*, so the log transform is harmless.

---

## Laplace Smoothing (`the.m` and `the.k`)

What if a class has only 2 rows? Or a symbol value was never seen
in training? Raw frequency gives 0, and `log(0)` is undefined.

Smoothing adds a small pseudocount to avoid zeros:

```python
# Sym.like
return (i.get(v,0) + the.k*prior) / (n + the.k)

# Data.like
prior = (len(i.rows)+the.m) / (n_all+the.m*n_h)
```

`the.k=1` and `the.m=2` are classic defaults. They pull sparse
estimates gently toward the prior rather than leaving them at zero.

---

## Minkowski Distance and `p=2`

```python
def minkowski(items:Iterable) -> float:
    n=d=0
    for x in items: n,d = n+1, d+x**the.p
    return 0 if n==0 else (d/n)**(1/the.p)
```

With `the.p=2` this is Euclidean distance, averaged over columns
(the `d/n` normalizes for varying column counts). With `p=1` it
becomes Manhattan distance. Averaging not summing means distance
stays in `[0,1]` regardless of how many columns exist.

---

## `_mid` Cache with `or`

```python
def mid(i) -> Row:
    i._mid = i._mid or [c.mid() for c in i.cols.all.values()]
    return i._mid
```

`None or expr` evaluates `expr` only when `_mid` is `None`.
`add` and `sub` reset it to `None`, so the cache is invalidated
whenever the data changes. A cheap lazy-evaluation pattern.

---

## `pick`: Num vs Sym, and the Wrap-Around Trick

`pick` generates a mutated neighbor of a row — used in optimization
to explore nearby solutions.

**`Sym.pick`** samples uniformly from values already seen:

```python
def pick(i, _:Val=None) -> Val: return pick(i)   # weighted sample
```

Any seen symbol is a valid mutation. No notion of "nearby."

**`Num.pick`** perturbs the current value using random differences
drawn from existing samples:

```python
def pick(i, v:Qty=None) -> Val:
    result = (i.mid() if v is None or v=="?" else v) \
             + choice(i) - choice(i)
    lo, hi = i[0], i[-1]
    return lo + ((result - lo) % (hi - lo + 1E-32))
```

`choice(i) - choice(i)` is a symmetric random step whose size is
drawn from the actual data distribution — so large-range columns
take large steps and tight-range columns take small ones.

The **wrap-around** is the key safety device:
`(result - lo) % (hi - lo)` keeps the result inside `[lo, hi]`
by wrapping overshoots back from the other end. Without this,
repeated perturbations drift toward the boundaries and accumulate
there — the optimizer spends all its time "bumping into walls."
The tiny `1E-32` prevents division by zero when `lo == hi`.

---

# Part 3: Code Walkthrough

---

## Sorting and Searching

**`sorty`** — sort rows by distance to heaven (best possible y values)

```python
def sorty(i) -> "Data":
    i.rows.sort(key=lambda row: i.disty(row)); return i
```
Rows closest to ideal y values float to the top.

---

**`sortx`** — sort rows by distance to a reference row in x space

```python
def sortx(i, r:Row, rows:list[Row]) -> list[Row]:
    return sorted(rows, key=lambda r2: i.distx(r,r2))
```
Returns `rows` ordered nearest-to-furthest from `r`.

---

**`nearest` / `furthest`** — first and last of `sortx`

```python
def nearest(i,  r:Row, rows:list[Row]) -> Row: return i.sortx(r,rows)[0]
def furthest(i, r:Row, rows:list[Row]) -> Row: return i.sortx(r,rows)[-1]
```
Convenience wrappers. `nearest` is used heavily in active learning.

---

## Summarizing Columns: `mid`, `spread`, `norm`

**`mid`** — central tendency. Median for `Num`, mode for `Sym`.

```python
def mid(i) -> float: return i[len(i)//2] if i else 0   # Num
def mid(i) -> Val:   return max(i, key=i.get)           # Sym
```

---

**`spread`** — diversity. IQR-like range for `Num`, entropy for `Sym`.

```python
# Num: robust spread via 10th-90th percentile range
return (i[a]-i[b])/2.56

# Sym: entropy
return -sum(p*log(p,2) for k in i if (p:=i[k]/n)>0)
```
Both measure "how spread out" without being thrown off by outliers.

---

**`norm`** — rescale a `Num` value to `[0,1]`

```python
a,b = i[int(.05*len(i))], i[int(.95*len(i))]
return 0 if a==b else max(0, min(1, (v-a)/(b-a)))
```
Uses 5th–95th percentile as lo/hi to resist outlier distortion.

---

## Delegation: `Data` → `Num`/`Sym`

Each `Data` method loops over columns and calls the same-named
method on each col. `Num` and `Sym` share the protocol.

---

**`add` / `sub`**

```python
def add(i, row:Row) -> Row:
    for at,c in i.cols.all.items(): c.add(row[at])
    i.rows.append(row); return row
```
`Num.add` does reservoir sampling. `Sym.add` increments a count dict.
`sub` is the mirror — enables incremental delete.

---

**`mid` (Data level)**

```python
def mid(i) -> Row:
    i._mid = i._mid or [c.mid() for c in i.cols.all.values()]
    return i._mid
```
Lazily cached. Returns one representative value per column.
Cache invalidated by `add`/`sub` setting `i._mid = None`.

---

**`distx`** — x-space distance between two rows

```python
def distx(i, r1:Row, r2:Row) -> float:
    return minkowski(c.distx(r1[at],r2[at]) for at,c in i.cols.x.items())
```
Delegates per-column distance to `Num.distx` or `Sym.distx`,
then combines via Minkowski (default: Euclidean, `p=2`).

---

**`disty`** — distance from a row to heaven

```python
def disty(i, r:Row) -> float:
    return minkowski(c.norm(r[at]) - i.cols.w[at]
                     for at,c in i.cols.y.items())
```
`cols.w[at]` is `1` (maximize) or `0` (minimize). See concept note
on "Heaven" above.

---

**`like`** — naive Bayes log-likelihood of a row belonging to this Data

```python
def like(i, row:Row, n_all:int, n_h:int) -> float:
    prior = (len(i.rows)+the.m) / (n_all+the.m*n_h)
    ls = [c.like(v,prior) for at,c in i.cols.x.items()
          if (v:=row[at])!="?"]
    return log(prior) + sum(log(v) for v in ls if v>0)
```
Delegates to `Num.like` (Gaussian) or `Sym.like` (frequency).
Uses log to avoid underflow. `the.m` smooths sparse class counts.

---

**`pick`** — mutate a row by randomly perturbing some x columns

```python
def pick(i, row=None, n=1) -> Row:
    if not row: return [c.pick() for c in i.cols.all.values()]
    s, k = row[:], n if n > 0 else len(i.cols.x)
    for at, c in random.sample(list(i.cols.x.items()),
                                min(k, len(i.cols.x))):
      s[at] = c.pick(s[at])
    return s
```
`Num.pick` perturbs with wrap-around to stay in range.
`Sym.pick` samples from seen values. See concept note above.

---

## Factory: `col()` and `Cols`

**`col()`** — name convention dispatches to `Num` or `Sym`

```python
def col(s:str): return (Num if s[0].isupper() else Sym)()
```
Uppercase first letter → `Num`. Lowercase → `Sym`.

**`Cols`** — organizes all columns into roles

```python
i.x  = {at:c for at,c in i.all.items() if at not in i.w ...}
i.y  = {at:i.all[at] for at in i.w}
i.klass = next((at for at,s in enumerate(names) if s[-1]=="!"), None)
```
`x` = independent cols, `y` = goal cols (marked `+`, `-`),
`klass` = classification target (marked `!`).

## Classification Tutorial

```
▶ ./bayes_class.py --data ~/gits/moot/classify/diabetes.csv
          label,   n, pd, pf, prec, acc
tested_positive, 262, 74, 32,   55,  70
tested_negative, 496, 67, 25,   83,  70
       _OVERALL, 758, 70, 29,   70,  70
```

```
▶ ./bayes_class.py --data ~/gits/moot/classify/soybean.csv
                      label,   n,  pd, pf, prec, acc
           herbicide-injury,   8,  75,  0,   85,  99
      diaporthe-stem-canker,  10, 100,  0,   76,  99
              cyst-nematode,  14,  85,  0,  100,  99
diaporthe-pod-&-stem-blight,  15,  80,  0,  100,  99
               2-4-d-injury,  16,  50,  0,  100,  98
               charcoal-rot,  20,  95,  0,   79,  99
       rhizoctonia-root-rot,  20,  95,  0,   86,  99
             powdery-mildew,  20,  85,  0,   85,  99
               downy-mildew,  20,  95,  0,   90,  99
           bacterial-blight,  20,  65,  0,   68,  98
          bacterial-pustule,  20,  80,  0,   80,  98
          purple-seed-stain,  20,  80,  0,   94,  99
     phyllosticta-leaf-spot,  20,  45,  0,   81,  98
             brown-stem-rot,  44,  93,  0,   91,  98
                anthracnose,  44,  93,  0,   89,  98
           phytophthora-rot,  88,  96,  1,   93,  98
        alternarialeaf-spot,  91,  87,  3,   77,  94
         frog-eye-leaf-spot,  91,  70,  0,   95,  95
                 brown-spot,  92,  92,  5,   73,  94
                   _OVERALL, 673,  84,  0,   84,  98
```

## Part 1: Naive Bayes — Prior, Evidence, Posterior

Bayes' theorem says:

```
P(class | data) ∝ P(class) × P(data | class)
```

- **Prior** `P(class)`: how common is this class before seeing data?
- **Likelihood** `P(data | class)`: how probable is this row given
  we already know the class?
- **Posterior** `P(class | data)`: updated belief after seeing row.

We never need the exact posterior. We only need to know *which
class wins*, i.e., which has the highest posterior. So we compare:

```
P(A) × P(row | A)   vs   P(B) × P(row | B)
```

The denominator `P(data)` is the same for all classes — it cancels.

In `ez_class.py`, `Data.like` computes the log-posterior:

```python
def like(i, row:Row, n_all:int, n_h:int) -> float:
    prior = (len(i.rows)+the.m) / (n_all+the.m*n_h)
    ls = [c.like(v,prior) for at,c in i.cols.x.items()
          if (v:=row[at])!="?"]
    return log(prior) + sum(log(v) for v in ls if v>0)
```

`log(prior)` is the log-prior. `sum(log(v) ...)` accumulates
log-likelihoods from each column. Logs turn multiplication into
addition, avoiding floating-point underflow when many small
probabilities are multiplied together.

The class with the *largest* log value wins. We never convert back
to probabilities. If `P(A|row) > P(B|row)` then
`log P(A|row) > log P(B|row)` — the ranking is preserved.

In `bayes_class.py`:

```python
def best(k):
    return ks[k].like(r, len(every.rows), len(ks))
...
confuse(cf, str(k), str(max(ks, key=best)))
```

`max(ks, key=best)` picks the winning class purely by rank.

---

### Laplace Smoothing (`the.m` and `the.k`)

What if a class has only 2 rows? Or a symbol was never seen in
training? Raw frequency gives 0, and `log(0)` is undefined.

Smoothing adds a small pseudocount:

```python
## Sym.like: frequency with k-smoothing
return (i.get(v,0) + the.k*prior) / (n + the.k)

## Data.like: class prior with m-smoothing
prior = (len(i.rows)+the.m) / (n_all+the.m*n_h)
```

`the.k=1` and `the.m=2` are classic defaults. They pull sparse
estimates gently toward the prior rather than crashing to zero.

---

## Part 2: The Confusion Matrix (2-class case)

Given true class (want) and predicted class (got), we tally four
cells. Using the notation from "Problems with Precision":

```
              Predicted
              yes      no
Actual  yes   D=TP     B=FN
        no    C=FP     A=TN
```

Four standard measures:

```
pd   = recall    = D / (B+D)      # of actual yes, how many caught?
pf   = false alarm = C / (A+C)    # of actual no, how many flagged?
prec = precision = D / (D+C)      # of flagged, how many real?
acc  = accuracy  = (A+D)/(A+B+C+D)
```

#### Worked example

100 rows: 20 actually defective (pos), 80 not (neg).
Classifier finds: 15 TP, 5 FN, 10 FP, 70 TN.

```
A=70  B=5  C=10  D=15

pd   = 15/(5+15)    = 15/20  = 75%
pf   = 10/(10+70)   = 10/80  = 13%
prec = 15/(15+10)   = 15/25  = 60%
acc  = (70+15)/100  = 85/100 = 85%
```

---

## Part 3: The 3-Class Case

With 3 classes (A, B, C), we generate *three separate* binary
confusion matrices using a one-vs-rest strategy.

For class X: label each row as `X` or `not-X`, compute
A, B, C, D as before, derive pd/pf/prec/acc independently.

#### Example: 90 rows across 3 classes

Predictions yield:

```
Class A: TP=28, FN=2,  FP=8,  TN=52
Class B: TP=21, FN=9,  FP=4,  TN=56
Class C: TP=18, FN=6,  FP=3,  TN=63
```

For class A:
```
pd   = 28/(2+28)  = 93%
pf   =  8/(8+52)  = 13%
prec = 28/(28+8)  = 78%
acc  = (28+52)/90 = 89%
```

For class B:
```
pd   = 21/(9+21)  = 70%
pf   =  4/(4+56)  =  7%
prec = 21/(21+4)  = 84%
acc  = (21+56)/90 = 86%
```

For class C:
```
pd   = 18/(6+18)  = 75%
pf   =  3/(3+63)  =  5%
prec = 18/(18+3)  = 86%
acc  = (18+63)/90 = 90%
```

The `_OVERALL` summary row sums all TP, FP, FN, TN across classes
before recomputing the rates — as `stats.py` does with
`summary=True`.

---

## Part 4: How `stats.py` Tracks A, B, C, D Incrementally

```python
def confuse(cf:Confuse, want:str, got:str) -> str:
  for x in (want, got):
    if x not in cf.klasses:
      cf.klasses[x] = o(label=x, tn=cf.total, fn=0, fp=0, tp=0)
  for c in cf.klasses.values():
    if c.label == want: c.tp += got == want;    c.fn += got != want
    else:               c.fp += got == c.label; c.tn += got != c.label
  cf.total += 1
  return got
```

Key points:

- A new class is initialized with `tn=cf.total`: all rows seen
  so far that didn't mention this class count as true negatives —
  the one-vs-rest setup applied retroactively in one line.
- Each call loops over **all known classes**, updating every one.
  This is how one-vs-rest is done incrementally with no storage.
- `c.fp += got == c.label` catches cases where the classifier
  wrongly predicted *this* class for a row that wasn't it.
- Everything is online: no rows stored, just running counts.

Then `confused()` derives the rates:

```python
c.pd, c.prec, c.pf, c.acc = (
  p(c.tp, c.tp+c.fn), p(c.tp, c.fp+c.tp),
  p(c.fp, c.fp+c.tn), p(c.tp+c.tn, c.tp+c.fp+c.fn+c.tn))
```

And `bayes_class.py` feeds it incrementally:

```python
if len(every.rows) >= warmup:
    confuse(cf, str(k), str(max(ks, key=best)))
ks[k].add(every.add(r))
```

The `warmup` period lets the Bayes models accumulate enough data
before predictions are scored.

---

## Part 5: The Problem with Precision

From Menzies et al. "Problems with Precision" (TSE 2007), the
key equation derived from the Zhangs' formula is:

```
prec = 1 / (1 + (neg/pos) × pf/recall)
```

Rearranged:

```
pf = (pos/neg) × ((1 - prec)/prec) × recall
```

**Precision is not a free parameter.** Given a fixed dataset —
fixed neg/pos ratio — fixing recall and pf *determines* precision.
You cannot independently tune all four measures. They are all
connected through the structure of the data being explored.

#### Consequences for SE data

SE datasets often have very large neg/pos ratios. The DMP paper
studied datasets with neg/pos of 1.04, 7.33, 9, 10.11, 13.29,
15.67, and 249. At high neg/pos, achieving high precision requires
pf to be vanishingly small — almost never achievable in practice.

This also explains why **precision is unstable** across datasets.
At very small pf values, tiny changes in pf cause huge swings in
prec (sudden jumps from 0 to 1). All other measures — pd, pf,
acc — vary far more smoothly. Precision is a derived consequence
of the data's neg/pos ratio, not something a learner controls.

Practical advice from the paper: prefer pd and pf as your
evaluation measures. They are stable. Precision is not.

#### When low precision is still useful

- When missing a target is very costly (safety, security): aim
  for pd=100%, accept low precision.
- When false alarm inspection is cheap (Google-style search):
  users scan a few false alarms without minding.
- When selectivity is small: only a small fraction of data is
  returned, so even imprecise detectors surface real issues.

---

## Part 6: The §5.9 Evaluation Criteria (Shrikanth & Menzies 2023)

The "Early Bird" paper (arXiv 2105.11082) uses eight measures to
assess defect predictors. These go beyond pd/pf/prec/acc because
no single measure tells the whole story — and because the measures
can contradict each other by design.

### Recall (pd) — maximize

```
Recall = TP / (TP + FN)
```

Of all actual defects, how many did we find? The primary goal.
A classifier can trivially achieve Recall=100% by flagging
everything — but then PF=100% too.

### False Positive Rate (PF) — minimize

```
PF = FP / (FP + TN)
```

Of all clean commits, how many did we wrongly flag? High PF
erodes developer trust. A classifier can get PF=0 by flagging
nothing — but then Recall=0 too.

### AUC — maximize

Area under the ROC curve (PF on x-axis, Recall on y-axis).
Threshold-free summary: 1.0 is perfect, 0.5 is random.

### D2H (Distance to Heaven) — minimize

"Heaven" is Recall=1, PF=0. D2H measures how far we are:

```
D2H = sqrt((1-Recall)^2 + (0-PF)^2) / sqrt(2)
```

Aggregates both goals into one number, normalized to [0,1].

### G-Measure (GM) — maximize

Harmonic mean of Recall and (1-PF):

```
GM = 2 × Recall × (1-PF) / (Recall + (1-PF))
```

GM and D2H combine the same two quantities differently. The paper
notes that good GM does not guarantee good D2H, or vice versa.

### Brier Score — minimize

Mean squared error between actual outcome y ∈ {0,1} and the
predicted probability p:

```
Brier = (1/n) × Σ (y_i - p_i)²
```

Penalizes confident wrong predictions most heavily. Note Brier
and Recall are antithetical: minimizing loss can lower recall.

### IFA (Initial False Alarms) — minimize

Commits are sorted by predicted defect probability. IFA counts
the false alarms encountered before the *first* real defect is
found. Based on Parnin & Orso's finding that developers lose
trust in analytics after many early false alarms.

### MCC (Matthews Correlation Coefficient) — maximize

Uses all four cells of the confusion matrix:

```
MCC = (TP×TN - FP×FN) / sqrt((TP+FP)(TP+FN)(TN+FP)(TN+FN))
```

Returns [-1, +1]. Unlike accuracy, MCC is fair on heavily
imbalanced data. The paper includes it as a substitute for
precision/f-measure, which are unreliable on SE datasets.

#### Summary

| Measure | Direction | What it captures             |
|---------|-----------|------------------------------|
| Recall  | maximize  | coverage of actual defects   |
| PF      | minimize  | false alarm burden            |
| AUC     | maximize  | threshold-free ROC summary   |
| D2H     | minimize  | distance from ideal (0,1)    |
| GM      | maximize  | recall + specificity balance |
| Brier   | minimize  | probability calibration      |
| IFA     | minimize  | early false alarm trust      |
| MCC     | maximize  | balanced confusion summary   |

The paper deliberately **excludes precision**:
"Prior work has shown that precision has significant issues for
unbalanced data. We do not include that in our evaluation."
MCC draws from all four corners of the confusion matrix without
precision's instability problems — that is why it is included.
