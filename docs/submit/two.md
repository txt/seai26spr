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

# Homework: Simulated Annealing

**Due:** One week from assignment  
**Deliverables:** `sa.py` (completed), `results.md` (writeup). 
- print out, 2 sided paper

---

## Overview

You will implement a simulated annealing optimizer, run experiments to understand its behavior, and write a brief analysis of your results.

**Files provided:**
- [sa](../lect/w3sa.md) — Background theory
- [ezr.py](ezr.py) — Data mining library (do not modify)
- [sa0.py](sa0.py) — Skeleton code with TODOs (rename to `sa.py`)
- [auto93.csv](auto93.csv) — Test dataset (automobile specifications)

---

## Part 1: Implementation (40 points)

Complete the three TODO sections in `sa0.py`:

### TODO 1: `mutate(c, v)` (15 points)

Mutate a single value `v` from column `c`. Handle both column types:

- **Symbolic columns** (`"has" in c`): Use `pick(c.has, c.n)` to sample from observed distribution
- **Numeric columns**: Apply Gaussian mutation centered at `v` with standard deviation `sd(c)`. Use modulo to wrap within bounds `[LO[c.at], HI[c.at]]`

### TODO 2: `score(row)` (10 points)

Estimate a row's quality using nearest-neighbor surrogate:

1. Find the nearest neighbor in `data.rows` using `nearest()`
2. Copy the neighbor's y-values to `row`
3. Return `disty(data, row)`

### TODO 3: Acceptance criterion (15 points)

Replace the `if False:` condition with the Metropolis-Hastings criterion:

- Always accept if `en < e` (new solution is better)
- Otherwise accept with probability `exp((e - en) / T)` where `T = 1 - heat/k`

### Testing Your Implementation

```bash
python sa.py 1 auto93.csv
```

Expected behavior:
- Output shows iteration number, score, and solution
- Score generally decreases over time
- Final score should be in range 0.05–0.15

Example output:
```
1     0.614 [4.33, 349.82, 130, 72.87, 1, 3632, 18, 20]
2     0.346 [4.33, 349.82, 130, 81.10, 1, 3015, 17, 40]
45    0.328 [5.54, 69.55, 130, 74.14, 2, 1963, 15.50, 30]
...
1731  0.075 [4.31, 99.14, 130, 77.63, 2, 1985, 21.50, 40]
```

---

## Part 2: Experiments (30 points)

### Experiment A: Baseline Performance (15 points)

Run SA with 10 different random seeds:

```bash
python sa.py 1 auto93.csv
python sa.py 2 auto93.csv
...
python sa.py 10 auto93.csv
```

Record the **final score** from each run. Report:
- Mean final score
- Standard deviation
- Best and worst scores

### Experiment B: Mutation Rate Study (15 points)

Modify `sa.py` to accept mutation rate as a command-line argument (or hardcode different values for separate runs).

Test with `m_rate` ∈ {0.1, 0.3, 0.5, 0.7, 0.9}

For each mutation rate, run 5 seeds and report mean final score.

---

## Part 3: Analysis (30 points)

Write `results.md` (roughly one page) addressing:

### 3.1 Results Table (10 points)

Present your experimental results clearly. Example format:

```
| Seed | Final Score |
|------|-------------|
| 1    | 0.075       |
| 2    | 0.082       |
| ...  | ...         |

Mean: X.XXX, Std: X.XXX
```

```
| m_rate | Mean Score (n=5) |
|--------|------------------|
| 0.1    | X.XXX            |
| ...    | ...              |
```

### 3.2 Why Accept Worse Solutions? (10 points)

In 1–2 paragraphs, explain:
- Why does SA sometimes accept solutions that are *worse* than the current one?
- Give a concrete example (you may sketch or describe a simple landscape) where always-greedy search would get stuck but SA could escape.

### 3.3 Mutation Rate Analysis (10 points)

Based on your Experiment B results:
- Which mutation rate performed best?
- Why might very low m_rate (0.1) perform poorly?
- Why might very high m_rate (0.9) perform poorly?

---

## Submission

Submit a zip file containing:
1. `sa.py` — Your completed implementation
2. `results.md` — Your writeup with tables and analysis

Do **not** submit `ezr.py` or `auto93.csv`.

---

## Grading Rubric

| Component | Points |
|-----------|--------|
| `mutate()` correct | 15 |
| `score()` correct | 10 |
| Acceptance criterion correct | 15 |
| Experiment A results | 15 |
| Experiment B results | 15 |
| Results presentation | 10 |
| "Why accept worse" explanation | 10 |
| Mutation rate analysis | 10 |
| **Total** | **100** |

---

## Hints

- Read `tutorial.md` sections 7 and 8 carefully before starting
- The `pick(d, n)` function samples key `k` with probability `d[k]/n`
- For numeric mutation: `LO + (gauss(v, sd(c)) - LO) % (HI - LO + 1E-32)`
- `1E-32` prevents division by zero when HI equals LO
- If your scores aren't decreasing, check your acceptance criterion—the temperature formula matters!

---

## Academic Integrity

You may discuss concepts with classmates but must write your own code and analysis. Do not share code or copy from online sources. Cite any external resources consulted.
