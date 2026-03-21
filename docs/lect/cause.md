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
<h1 align="center">:cyclone: CSC491/591 (013): Software Engineering and AI
<br>NC State, Spring '26</h1>
<img src="https://raw.githubusercontent.com/txt/seai26spr/main/docs/lect/banner.png">

# From Black Boxes to Small Trees
A lecture on explainable optimization


## Part 1: Why Locality Matters 

### The distributed dogma

For decades, the orthodoxy was that neural networks, deep elarenrs, Large language models
are inexplicable black boxes, beyond the ken or mortal man (sic).

Why? Because inside that kind of 
knowledge is *distributed* — smeared across millions
of weights, impossible to localize. Dropout trains
networks to survive losing random neurons. Adversarial
examples show tiny input perturbations flip outputs.
The implication: no single neuron "knows" anything.

### The surprise

Three results broke this story:

**Elhage et al. (2022)** showed that polysemantic
neurons — neurons responding to unrelated concepts —
arise from *compression*, not true distribution.
Networks pack more features than they have neurons
via "superposition." The distributed look is an
encoding trick, not a fundamental property.

**Dai et al. (2022)** found that specific factual
knowledge in BERT ("The capital of Ireland is ___")
localizes to tiny subsets of FFN neurons. Suppressing
those neurons drops correct recall by ~29%. Suppressing
random neurons of the same count: ~1.5%. You can
surgically edit, update, or erase individual facts
without retraining.

**Voria et al. (2026)** extended this to social bias.
Gender, age, and race stereotypes similarly concentrate
in sparse neuron subsets. Zeroing them selectively
reduces bias while leaving unrelated fluency intact
(p < 0.0001, Cliff's delta = 1.0). Scaling the model
doesn't spread bias — it *concentrates* it into fewer,
more specialized neurons.

Knowledge is sparse. Knowledge is local. Surgery works.

---

## Part 2: Why Interpretable, Not Explainable 

### Rudin's argument (2019)

If knowledge is localizable, why not build models that
*are* the sparse structure from the start?

**The myth.** DARPA published a figure showing a smooth
accuracy-interpretability tradeoff. Rudin points out
it was generated from no data. The axes have no units.

**The evidence.** On structured data with meaningful
features, simple models routinely match complex ones.
Rudin's NYC power grid study: algorithms differed by
≤1% on static data, but the ability to *interpret and
reprocess* led to significant gains. The best models
were sparse.

**The logic.** If an explanation were perfectly faithful
to the black box, it *would be* the black box — and
you wouldn't need the black box. So every explanation
is, by definition, unfaithful somewhere. 90% faithful
means wrong 10% of the time — and you can't know when.

**The poster child.** COMPAS: 130+ input factors,
proprietary, used for U.S. bail decisions. Typos in the
130-factor survey sometimes determine who goes free.

CORELS produces a 3-rule model matching COMPAS accuracy:

```text
IF age 18-20 AND male       → predict arrest
ELSE IF age 21-23 AND 2-3 priors → predict arrest
ELSE IF more than 3 priors  → predict arrest
ELSE → predict no arrest
```

Three rules. Computable on a napkin. No typos.

### Gigerenzer's heuristics (2008)

Why does simplicity *work*? Not just because data are
easy — because simplicity is an *active advantage* in
uncertain environments.

**1/N beats the Nobel.** Markowitz won the Nobel for
optimal portfolio theory. For his *own* retirement he
used 1/N: split money equally. DeMiguel et al. tested
12 optimal strategies against 1/N. None beat it. The
optimizers overfit past data. 1/N estimates zero
parameters, so it *cannot* overfit.

**Fast-and-frugal trees save lives.** Green and Mehr
built a 3-question tree for coronary care that beat
logistic regression and the physicians themselves.
The hospital still uses it decades later.

The principle: **the noisier the environment, the more
information you should ignore.**

And: humans reason in *symbols*, not weight vectors.
A rule that says "if ST elevated → ICU" maps onto
how a doctor actually thinks. The representation
determines whether the human can integrate the model
with their own knowledge — which Rudin identifies as
a key failure mode of black boxes.

---

## Part 3: The Simplest Useful Model 

### How the tree works

One file. ~700 lines. Here's the pipeline:

**Step 1: Header is schema.** No config files.
Column names encode everything:

```python
# [A-Z]* → Numeric    [a-z]* → Symbolic
# *+     → Maximize    *-     → Minimize
# *X     → Ignore      ?      → Missing value

class Cols:
  def __init__(i, names):
    i.names = names
    i.all = {at: col(s)
             for at,s in enumerate(names)}
    i.w = {at: s[-1]!="-"
           for at,s in enumerate(names)
           if s[-1] in "-+!"}
    i.x = {at:c for at,c in i.all.items()
            if at not in i.w
            and names[at][-1] != "X"}
    i.y = {at: i.all[at] for at in i.w}
```

`EFFORT-` means "numeric, minimize." `Mpg+` means
"numeric, maximize." Lowercase `origin` means
"symbolic, independent." The system figures out X vs Y
from the punctuation.

**Step 2: Distance to heaven.** Every row gets one
score: how far from the ideal point where all goals
are simultaneously at their best?

```python
def disty(i, r):
  return minkowski(
    abs(c.norm(r[at]) - i.cols.w[at])
    for at,c in i.cols.y.items())
```

`i.cols.w[at]` is 1 for maximize, 0 for minimize.
`c.norm` squashes to 0..1. Result: 0 = perfect,
1 = worst possible. One number per row.

**Step 3: Split on median.** The nonstandard choice.
Most trees split numerics at minimum expected variance,
evaluating every possible cut. We split on the
**median** — one cut per feature:

```python
def splits(at, c, rs, d):
  vs = [r[at] for r in rs if r[at] != "?"]
  if not vs: return
  cuts = (set(vs) if isinstance(c, Sym)
          else [sorted(vs)[len(vs)//2]])
  for cut in cuts:
    ...
```

Symbolics: try every value. Numerics: one cut, the
middle. Tested across 127 SE datasets — median splits
were as good or better, and far cheaper.

**Step 4: Recurse, sort best-to-worst.**

```python
def build(d, rs):
  t = Tree(d, rs)
  if len(rs) >= 2 * the.learn.leaf:
    bestW, best = BIG, None
    for at, c in t.d.cols.x.items():
      for cut, L, R, w in splits(at, c, rs, d):
        if (min(len(L), len(R)) >= the.learn.leaf
            and w < bestW):
          bestW, best = w, (at,..., cut, L, R)
    if best:
      t.at, t.txt, t.cut, L, R = best
      t.L, t.R = build(d, L), build(d, R)
  return t
```

Recurse until leaves have ≤ `leaf` rows. Nodes print
sorted by `disty` score — best regions first.

### Reading the output

Real run on XOMO (NASA software cost model, 4 goals:
minimize effort, months, defects, risks):

```text
                         ,0.50 ,( 50), {EFF=655  MON=24  DEF=5917  RSK=0.95}
KLOC <= 227              ,0.40 ,( 26), {EFF=409  MON=21  DEF=4044  RSK=0.99}
|  KLOC <= 93            ,0.32 ,( 14), {EFF=239  MON=18  DEF=1886  RSK=0.84}
|  |  RELY > 2.51        ,0.22 ,(  6), {EFF=199  MON=17  DEF=1258  RSK=0.31}
|  |  RELY <= 2.51       ,0.39 ,(  8), {EFF=270  MON=19  DEF=2356  RSK=1.24}
|  KLOC > 93             ,0.49 ,( 12), {EFF=607  MON=24  DEF=6563  RSK=1.16}
|  |  KLOC <= 212        ,0.42 ,(  7), {EFF=418  MON=22  DEF=3494  RSK=0.92}
|  |  |  ACAP <= 4.38    ,0.35 ,(  4), {EFF=368  MON=21  DEF=2621  RSK=0.54}
|  |  |  ACAP > 4.38     ,0.52 ,(  3), {EFF=485  MON=23  DEF=4660  RSK=1.43}
|  |  KLOC > 212         ,0.59 ,(  5), {EFF=872  MON=26  DEF=10860 RSK=1.50}
KLOC > 227               ,0.62 ,( 24), {EFF=922  MON=28  DEF=7945  RSK=0.90}
|  RESL > 3.82           ,0.54 ,( 11), {EFF=648  MON=25  DEF=5457  RSK=1.00}
|  RESL <= 3.82          ,0.68 ,( 13), {EFF=1155 MON=30  DEF=10050 RSK=0.82}
|  |  SITE > 3.63        ,0.57 ,(  6), {EFF=710  MON=27  DEF=6055  RSK=1.07}
|  |  SITE <= 3.63       ,0.78 ,(  7), {EFF=1536 MON=34  DEF=13474 RSK=0.61}
|  |  |  CPLx <= 1.99    ,0.74 ,(  4), {EFF=1399 MON=32  DEF=11907 RSK=0.54}
|  |  |  CPLx > 1.99     ,0.83 ,(  3), {EFF=1718 MON=36  DEF=15564 RSK=0.72}
```

How to read it:

- **First column**: the branch condition. Indentation
  shows depth. `|` marks parent branches.
- **Second column** (e.g. `0.50`): median distance to
  heaven for that node. Lower = better. Sorted
  best-first top-to-bottom.
- **Third column** (e.g. `(50)`): how many rows.
- **Fourth column**: median goal values for those rows.

**Best leaf**: `KLOC ≤ 93 AND RELY > 2.51` — 6 rows,
score 0.22. Small programs with high reliability
requirements. Effort=199, Months=17, Defects=1258.

**Worst leaf**: `KLOC > 227 AND RESL ≤ 3.82 AND
SITE ≤ 3.63 AND CPLx > 1.99` — 3 rows, score 0.83.
Large, complex, poorly-resolved, distributed projects.
Effort=1718, Months=36, Defects=15564.

8.6× the effort. 2.1× the schedule. 12× the defects.
The tree *is* the explanation.

---

## Part 4: The Causal Ladder — on One Slide 

### Pearl's three rungs

Pearl (2000) defined a hierarchy of causal questions:

**Rung 1 — See.** "What patterns exist?" Query P(Y|X)
from observed data. Pure association.

**Rung 2 — Act.** "What does the model predict for
*this* row?" Apply a model to new data. The model is
the intervention.

**Rung 3 — Imagine.** "What *would have happened*
if one thing were different?" The key: the observed
state (you're in a bad leaf) contradicts the
hypothetical (what if you were in a good one?). You
need a model to connect the two worlds.

Here's the insight: **if the tree is small enough to
fit on one slide, you can do all three rungs visually
— with a finger and a printout.**

### Rung 1 — See: read the tree top to bottom

Look at the XOMO tree above. Reading it gives you:

- **Trends**: KLOC dominates the first split. Size
  matters most.
- **Summarization**: each leaf's goal values tell you
  what that region achieves.
- **Ranking**: nodes are sorted. Best leaf (0.22) is
  at the top. Worst (0.83) is at the bottom.

No code needed. Just read.

### Rung 2 — Act: drop a new row down the tree

A new project comes in: KLOC=300, RESL=3, SITE=2,
CPLx=2.5. Trace it with your finger:

```text
KLOC > 227?      YES → go right
  RESL > 3.82?   NO  → go right
    SITE > 3.63? NO  → go right
      CPLx > 1.99? YES → leaf: 0.83
```

Predicted: score 0.83. Effort ~1718. Months ~36.
That's a bad outcome. You flagged it — that's the
**alert**. The path tells you why — that's the
**comparison** to the baseline.

Still no code. Still just a finger on a printout.

### Rung 3 — Imagine: walk up, check siblings

You're stuck in the worst leaf. Now the counterfactual
question: **what single change moves you to a better
place?** Walk up the tree from your leaf. At each
branch point, the *sibling* tells you what one change
buys you:

```text
You are here: KLOC>227 RESL≤3.82 SITE≤3.63 CPLx>1.99
              Score: 0.83  Effort: 1718

Walk up and check each sibling:

Step 1: What if CPLx ≤ 1.99?
  → sibling score: 0.74, effort: 1399
  → saves 319 effort. Modest gain.

Step 2: What if SITE > 3.63?
  → sibling score: 0.57, effort: 710
  → saves 1008 effort. Big gain.
  → BEST SINGLE CHANGE.

Step 3: What if RESL > 3.82?
  → sibling score: 0.54, effort: 648
  → saves 1070 effort. Similar gain.

Step 4: What if KLOC ≤ 227?
  → sibling score: 0.40, effort: 409
  → saves 1309 effort. Biggest gain
    but requires descoping the project.
```

**This is a menu of interventions, cheapest first.**
Each row is a single-variable counterfactual. The
practical advice jumps out:

- Reducing complexity barely helps (0.83 → 0.74).
- Improving site collocation is the **best bang for
  one change**: effort drops from 1718 to 710.
- Improving risk resolution gives similar gains but
  may be harder to action.
- Shrinking KLOC is the nuclear option.

A manager does this with a printout and a finger.
No code. No what-if tool. No simulation engine.
The tree *is* the causal model connecting the real
world to the hypothetical.

The `whatif` function just automates the finger:

```python
def whatif(t, r, at, val):
  r2 = r[:]; r2[at] = val
  return leaf(t, r2)
```

Two lines. But most of the time you don't need them.


### Why walk up — not jump across?

A naive optimizer would say: "You're in the worst leaf
(0.83). The best leaf is 0.22. Just go there." But
going there means changing KLOC, RELY, and possibly
everything else. That's not advice — that's "be a
different project."

Counterfactuals are not optimization. Three constraints
separate them:

**Freeze the individual.** Pearl calls this U — the
unobserved background. In the tree, U is everything in
the row you don't change. When you ask "what if
SITE > 3.63?", the project's size, complexity,
personnel, and history stay frozen. You're asking about
*this* project, not some hypothetical ideal one.

**Minimal change.** Walking up one branch tests one
variable at a time. That's not a limitation — it's the
point. A manager can action one change. Two changes are
harder. Three are a reorg. The tree's branching
structure naturally decomposes the counterfactual into
single-variable interventions ranked by impact.

**Stay in observed territory.** Every sibling leaf
contains real rows — projects that actually existed.
You're not extrapolating to a fantasy configuration.
You're saying "projects like yours, but with better
site collocation, looked like *this*." The tree can't
send you somewhere the data hasn't been.

The `whatif` function encodes all three constraints
in two lines:

    r2 = r[:]          # freeze U (copy the row)
    r2[c.at] = mid(c)  # minimal change (one feature)
    return leaf(t, r2)  # stay in observed territory
                         # (the tree routes to a real leaf)

This is what distinguishes Rung 3 from Rung 2.
Intervention asks "what does the model predict for
new data?" Counterfactual asks "what would *this
specific individual* experience if *one thing* were
different — holding everything else fixed?"

### The 3×3 grid collapses

Buse and Zimmermann's analytics framework looks like
9 different tools:

```text
           Past       Present     Future
Find     Trends      Alerts     Forecast
Explain  Summarize   Compare    Root cause
Compare  Model       Benchmark  Simulate
```

But we just did all 9 with one tree on one slide:

- **Past column** (See): read the tree top-to-bottom.
  Trends, summarization, and ranking in one glance.
- **Present column** (Act): trace a new row with your
  finger. Alert, comparison, benchmark in one path.
- **Future column** (Imagine): walk up from a bad leaf,
  check siblings. Forecast, root cause, simulation
  in one walk.

For automation, the three `eg_` functions do exactly
what the finger does:

```text
| See (train)   | Act (test)  | Imagine (perturb) |
|---------------|-------------|---------------------|
| eg_see        | eg_act      | eg_imagine          |
| read tree     | trace path  | walk up, check sibs |
| Rung 1        | Rung 2      | Rung 3              |
```

9 cells. 3 functions. 1 tree. 0 separate tools.

---

## Part 5: Should We Accept This? 

### The question

We've seen that:

- Knowledge in large models is sparser than expected.
  50 neurons encode what 340 million parameters carry.
- Simple models match complex ones on structured data.
  3 rules match 130 factors for recidivism prediction.
- Ignoring information *improves* prediction in noisy
  environments. 1/N beats the Nobel laureate's own
  optimal strategy.
- A small tree on one slide gives you association,
  intervention, and counterfactual reasoning — all
  three rungs of Pearl's ladder — with no code, no
  post-hoc explainer, and no black box.

So the question is not a technical one. It's a
choice.

### Should we accept that AI is inexplicable?

Some people say yes. They say:

- Models are too complex to understand.
- The accuracy-interpretability tradeoff is real.
- Post-hoc explanations are good enough.

We've spent a hour or so showing that all three claims
are empirically false for structured data — which is
most of what SE, healthcare, criminal justice, and
finance actually use.

The real reason black boxes persist is not technical.
It's economic. COMPAS costs money. CORELS is free.
A 130-factor proprietary model has a business model.
A 3-rule public model does not. Rudin's proposed
mandate: no black box should be deployed when an
equally accurate interpretable model exists.

### The alternative

Build models that *are* the explanation. Small enough
to fit on one slide. Frugal enough to resist
overfitting. Symbolic enough that a human can check
them, debate them, and override them with domain
knowledge.

Then use the same model for prediction, intervention,
and counterfactual reasoning — because when the tree
is small, those three acts collapse into one:
**reading**.

That's not a compromise. It's the goal.

---

### References

- Dai et al. "Knowledge Neurons in Pretrained
  Transformers." ACL 2022.
- Elhage et al. "Toy Models of Superposition."
  Anthropic, 2022.
- Gigerenzer. "Why Heuristics Work." Perspectives
  on Psychological Science, 2008.
- Green & Mehr. "What Alters Physicians' Decisions
  to Admit to the Coronary Care Unit?" Journal of
  Family Practice, 1997.
- Pearl. Causality. Cambridge University Press, 2000.
- Rudin. "Stop Explaining Black Box Models for High
  Stakes Decisions." Nature Machine Intelligence, 2019.
- Voria et al. "Tracing Stereotypes in Pre-trained
  Transformers." MSR 2026.
