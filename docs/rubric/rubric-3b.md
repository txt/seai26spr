
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


# HW3 Grading Sheet — Stats, Search & Assumptions
**CSC 491/591 · NC State · Spring 2026**

**Student:** ___________________________  &nbsp; **Type:** [ ] Undergrad &nbsp; [ ] Grad  
**Grader:** ___________________________ &nbsp; **Total:** _____ / 13

---

## Part 1a — When Accuracy Lies `hw1a.py` &nbsp;&nbsp; _____ / 2

| pts | criteria |
|---|---|
| 2 | Code runs, table correct for all 5 ratios × 4 metrics, explanation clearly ties numbers to TN inflation |
| 1 | Code runs but output/explanation incomplete or vague |
| 0 | Missing or broken |

---

## Part 1b — Weibull Stress Test `hw1b.py` &nbsp;&nbsp; _____ / 2

| pts | criteria |
|---|---|
| 2 | Correct pooled sd, `top()` called with `eps=0.35*sd`, avg/min/max reported, note on eps ↔ winner size |
| 1 | Partial — output present but check or note missing |
| 0 | Missing or broken |

---

## Part 2 — MOOT Tournament `hw2.py` &nbsp;&nbsp; _____ / 3

| pts | criteria |
|---|---|
| 3 | Runs across 120+ files, energies collected, `top()` per file, win table printed, discussion cites numbers |
| 2 | Runs but discussion vague or minor code issue |
| 1 | Partial — loop incomplete or wins not counted |
| 0 | Missing or broken |

---

## Part 3 — Welford vs Reservoir `hw3.py` &nbsp;&nbsp; _____ / 3

| pts | criteria |
|---|---|
| 3 | All `WelfordNum` methods correct, both tables produced, discussion compares results directly |
| 2 | Implementation mostly correct but one method wrong or only one table |
| 1 | Skeleton only / no meaningful output |
| 0 | Missing or broken |

---

## Part 4 — Hyperparameter Sensitivity `hw4.py` &nbsp;&nbsp; _____ / 1.5
*Grad only*

| pts | criteria |
|---|---|
| 1.5 | All 10 (algo, param) tuples run, win table correct, discussion connects ties to SE tuning effort |
| 0.75 | Partial implementation or shallow discussion |
| 0 | Missing |

---

## Part 5 — Sample Size Sensitivity `hw5.py` &nbsp;&nbsp; _____ / 1.5
*Grad only*

| pts | criteria |
|---|---|
| 1.5 | All 16 (algo, n) tuples run, tiebreak logic correct, discussion addresses labeling cost in SE |
| 0.75 | Missing tiebreak or shallow discussion |
| 0 | Missing |

---

**Notes:** Total score should be out of 13
