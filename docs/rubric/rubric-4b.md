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
      src="https://img.shields.io/badge/©%20timm%202026-%234b4b4b?style=flat-square&logoColor=white" /></a>
</p>

<h1 align="center">:cyclone: CSC491/591 (013): Software Engineering and AI <br>NC State, Spring '26</h1>

# HW4 Grading Sheet — Hyperparameter Optimization with pymoo
**CSC 491/591 · NC State · Spring 2026**

**Student:** ___________________________  &nbsp; **Type:** [ ] Undergrad &nbsp; [ ] Grad  
**Grader:** ___________________________ &nbsp; **Total:** _____ / 10

---

## Part 1 — GA on the Diabetes Dataset `hw4a.py` &nbsp;&nbsp; _____ / 5

### Code Correctness &nbsp;&nbsp; _____ / 3

| pts | criteria |
|---|---|
| 3 | All 4 TODOs complete and correct: cross-validation runs with `neg_mean_squared_error`, sign is flipped properly for `out["F"]`, both `gen_best` and `gen_avg` recorded in callback, improvement percentage computed and summary printed in correct format |
| 2 | 3 of 4 TODOs correct; output mostly matches expected shape |
| 1 | 1–2 TODOs correct; script runs but output incomplete or malformed |
| 0 | Missing or broken |

### Written Questions &nbsp;&nbsp; _____ / 2

| pts | criteria |
|---|---|
| 1 | **Q1:** Correctly explains that `f_min` can plateau (elitism preserves best; new mutations may not improve it) |
| 0.5 | **Q2:** Correct arithmetic (50×50×49 = 122,500 configs); notes GA explores ~0.4% of space and uses fitness signal rather than exhaustive search |
| 0.5 | **Q3:** Identifies whether any winning params hit boundaries; correctly interprets boundary-hitting as evidence the search space may be too narrow and should be expanded |

---

## Part 2 — Searching a Pre-Evaluated Table `hw4b.py` &nbsp;&nbsp; _____ / 5

### Code Correctness &nbsp;&nbsp; _____ / 3

| pts | criteria |
|---|---|
| 3 | All 3 TODOs complete: `out["F"]` correctly set from `Y_pymoo[idx, mre_col]`, callback appends `gen_best` correctly, summary block printed with all five required lines (baseline, best GA MRE, best table MRE, improvement %, eval count) |
| 2 | 2 of 3 TODOs correct; script runs and produces partial output |
| 1 | 1 TODO correct or script runs with significant errors in output |
| 0 | Missing or broken |

### Written Questions &nbsp;&nbsp; _____ / 2

| pts | criteria |
|---|---|
| 0.5 | **Q1:** Reports actual `res.F[0]` vs `df["MRE-"].min()` and comments on the gap; recognizes GA may not reach the global optimum due to limited evaluations |
| 0.5 | **Q2:** Computes fraction of table visited (500 / table size); discusses whether this is efficient relative to the improvement achieved |
| 1 | **Q3:** Explains that nearest-neighbor lookup is needed because the GA proposes real-valued candidates not guaranteed to exist in the table; without it, `_evaluate` would fail or return meaningless results |

---

**Notes:**
