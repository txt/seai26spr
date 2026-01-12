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
<h1 align="center">:cyclone: CSC491/591: Software Engineering and AI <br>NC State, Spring '26</h1>
<img src="https://raw.githubusercontent.com/txt/seai26spr/main/docs/lect/banner.png"> 


#  Homework 1: From Random to Hill-Climbing


<img align=right width="275" height="183" alt="image" src="https://github.com/user-attachments/assets/8b1959b4-1fe9-4812-adad-a63097f03869" />

> Now here this:
do not stress on this homework.
This is just a calibration
exercise, to warm us up after a cold December
Everyone who hands
in anything at all (working or not) will get full marks on this homework. 

## What to hand-in

One piece of paper per group with: 

- your group names and student numbers at the top.
- screen shot showing a command line running my_hc.py and rand.py (defined below).
- On the back of the paper, show your code (or in the front if it fits).
  - Feel free to use 7 point font size to make it fit

By the way, my hill climber is about 50 lines of code.

## 1. Installing Python 3.14

### macOS
```bash
brew install python@3.14
# Or download from python.org
```

### Ubuntu WSL
```bash
sudo apt update
sudo apt install python3.14 python3.14-venv
```

Verify installation:
```bash
python3.14 --version  # Should show 3.14.x
```

Create and activate a virtual environment:
```bash
python3.14 -m venv .venv
source .venv/bin/activate
python3 --version
```

## 2. Installing xai.py and MOOT

Find the code on line at https://github.com/timm/xai/blob/main/xai.py

- And the raw code is at https://raw.githubusercontent.com/timm/xai/refs/heads/main/xai.py

Download xai.py to a new directory.

### Setup
```bash
# Make xai.py executable
chmod +x xai.py

# Create directory and clone MOOT data repository
mkdir -p $HOME/gits
git clone http://github.com/timm/moot $HOME/gits/moot

# Test installation
./xai.py -h
```

> **WSL note**  
> If `./xai.py` does not run in WSL, edit the first line of `xai.py` and replace:
> ```bash
> #!/usr/bin/env python3 -B
> ```
> with:
> ```bash
> #!/usr/bin/env -S python3 -B
> ```

### Verify Everything Works
```bash
# Test basic functionality
./xai.py --num

# Test with real data
./xai.py --csv ~/gits/moot/optimize/misc/auto93.csv

# Run full optimizer test
./xai.py --tree ~/gits/moot/optimize/misc/auto93.csv
```

Expected output from `--tree` should show a decision tree
with scores, row counts, and goal values.

## 3. Understanding xai.py Internals

For this homework you'll be using xai.py's internal functions.
So you need  to know a little how its organized. Note that xai.py is about 400 lines and for this homework
you'll only need to understand the first 100-ish lines (everything before the heading _Cutting_).

### Core Data Structures

**Num**: Tracks numeric columns using incremental statistics
- `mu`: mean
- `m2`: sum of squared deviations (for standard deviation)
- `n`: count

**Sym**: Tracks symbolic columns with frequency counts
- `has`: dictionary of value frequencies

**Data**: Container for rows and columns
- `rows`: list of data rows
- `cols.x`: independent variables
- `cols.y`: dependent variables (goals to optimize)

Data is some csv file whose first row names the column names and the optimization goals. 
For example, in this file, the goal is to  minimize Error and maximize salary.  
"Name" is marked with and trailing "X" which means "ignore this column".
Column names beginning with upper case (e.g. "Age") become **NUM**s and
everyone else becomes a **SYM**.


```
nameX,    Age,  Salary+,  Error-
alice,   25,   50000,    0.1
bob,     35,   60000,    0.05
charlie, 45,   80000,    0.2
...
```
To read a  _data_ from the hard drive:

```
from xai import Data,csv
data = Data(csv(filename))
print(data)
```

### Key Distance Functions

**disty(data, row)**: Distance to "heaven"
- Normalizes each goal (0 to 1 scale)
- For minimization goals, flips target to 0
- For maximization goals, uses target of 1
- Returns Euclidean distance across all goals
- Lower is better (closer to ideal)

e.g. to sort all the rows on their distance to heaven:


```
data.rows.sort(key=lambda row: disty(data,row))
```

**distx(data, row1, row2)**: Distance between two rows
- Measures similarity in feature space (x columns)
- Handles missing values via _aha()
- Returns normalized Euclidean distance (0 to 1)

e.g. to sort all the rows on their distance to row[0]:


```
r1 = data.rows[0]
data.rows.sort(key=lambda r2: distx(data,r1,r2))
```

### Understanding Normalization
The distance functions normalize numeric ranges 0..1 for min..max.

`norm(num, n)` converts raw values to 0-1 range:
- Maps μ±3σ to approximately 0-1
- Uses sigmoid for smooth scaling
- Handles outliers gracefully

### Why These Matter

For optimization, we need:
1. **disty**: Find rows closest to ideal goals
2. **distx**: Measure similarity between examples
3. Together: Project data onto "good" vs "bad" axis

## 4. Understanding rand.py

This baseline establishes random sampling performance.

```python
def Y(r): return round(xai.disty(data,r),2)
```
Y() is the objective function - lower is better.

```python
def report(what,rows):
    a=sorted(rows[:],key=Y)
    print(f":n {len(a):4} :lo {Y(a[0]):5.2f} "
          f":mid {Y(a[len(a)//2]):5.2f}", what)
```
Shows: count, best score (lo), median score (mid)

**Baseline**: All 398 rows, best=0.07, median=0.54
**Sample**: Random 30 rows, best=0.15, median=0.53

Random sampling finds worse solutions than looking at
all data. Can we do better with the same budget?

## 5. Building Baseline Optimizations

### Setup Your Workspace

Create a new file `my_hc.py`:

```python
#!/usr/bin/env python3 -B
# ./rand.py $RANDOM ~/gits/moot/optimize/misc/auto93.csv

import random, sys, xai
xai.the.data=sys.argv[2]
random.seed(int(sys.argv[1]))

data = xai.Data(xai.csv(xai.the.data))

def Y(r): return round(xai.disty(data,r),2)

def report(what,rows):
    a=sorted(rows[:],key=Y)
    print(f":n {len(a):4} :lo {Y(a[0]):5.2f} :mid {Y(a[len(a)//2]):5.2f}", what)

report("baseline",data.rows)
report("sample", xai.shuffle(data.rows)[:30])
```

### Exercise 1: Reporting Progress
Make it executable: `chmod +x my_hc.py`

Run it

      python3 -B rand.py 1 ~/gits/moot/optimize/misc/auto93.csv

You should see

```
:n  398 :lo  0.07 :mid  0.54 baseline
:n   30 :lo  0.15 :mid  0.53 sample
```
First line says that in all the data, 
_disty_ runs from 0.07 (lowest) to 0.54 (median).

Second line says that after looking at 30 random rows, we found a row with _disty_ of 0.15. WHish is not lowest
but it is 

    1 - (0.17 - 0.07) / (0.54 - 0.07) = 0.79

i.e. nearly 80% of the way from median to best. Not bad for 30 examples. hey?

### Exercise 2: Reporting Progress

**Goal**: Create a function that shows the best disty score
in a list of rows.

**Task**: Write `report(rows)` that:
- Sorts rows by Y()
- Prints the best (lowest) Y value, rounded to 2 decimals

**Expected Output**: something less that 0.1


### Exercise 3: Finding Extremes

**Goal**: Find "good" and "bad" examples to guide search.

**Background**: In a list sorted by disty,  the 10th percentile
represents "good" examples, the 90th percentile represents
"bad" ones. These extremes define a search direction.

**Task**: Write `extremes(rows)` that:
- Sorts rows by Y() 
- Calculates n = len(rows)//10
- Returns the row at position n (good) and 9*n (bad)

**Test**:
```python
rows = shuffle(data.rows[:])[:30]
ok, no = extremes(rows)
print(f"Good: {Y(ok):.2f}, Bad: {Y(no):.2f}")
```

**Expected Output**: Two different scores, "Good" < "Bad"

- Why is "Good" less than "Bad"?
- Because we are measure distance to heaven and the smaller the disty, the closer we are to heaven.

---

### Exercise 4: Projection Geometry

**Goal**: Project points onto the ok-no axis.

**Background**: Given two points (ok, no), we can project
any third point onto the line between them using the
law of cosines. Points projecting closer to "ok" are
better candidates.

**Math Review**:
```
Given triangle with sides a, b, c:
c² = a² + b² - 2ab·cos(θ)

Rearranging for projection distance:
proj = (a² + c² - b²) / (2c)
```

Where:
- a = distance from point to ok
- b = distance from point to no  
- c = distance from ok to no

**Task**: Write `project(r, ok, no)` that:
- Calculates c = x(data, ok, no)
- Calculates a = x(data, r, ok)
- Calculates b = x(data, r, no)
- Returns (a² + c² - b²) / (2c + 1e-32)

Note: 1e-32 prevents division by zero.

**Test**:
```python
rows = shuffle(data.rows[:])[:30]
ok, no = extremes(rows)
for r in rows[:5]:
    p = project(r, ok, no)
    print(f"Y={Y(r):.2f}, proj={p:.3f}")
```

**Expected**: Smaller Y values should correlate with
smaller projection values.

---

### Exercise 5: Pruning the Population

**Goal**: Keep only the promising half of candidates.

**Task**: Write `prune(rows, ok, no)` that:
- Sorts rows by their projection onto ok-no axis
- Returns first half of sorted list

**Test**:
```python
rows = shuffle(data.rows[:])[:40]
ok, no = extremes(rows)
before = [Y(r) for r in rows]
after = [Y(r) for r in prune(rows, ok, no)]

print(f"Before prune - median: {sorted(before)[20]:.2f}")
print(f"After prune  - median: {sorted(after)[10]:.2f}")
```

**Expected**: After-median of rows' _disty_ should be lower (better)
than before-median.


### Exercise 6: Convergence Detection

**Goal**: Stop when improvements become negligible.

**Background**: Cohen's d effect size suggests 0.35 of 
standard deviations as a "small" effect. 
Given a sorted list of numbers, the standard deviation is 

    sd = ((90th percentile) - (10th eprcentile)) / 2.56

We'll use this
threshold to detect convergence.

**Task**: Add these helper functions:
```python
def top(a): a.sort(); return a[0]
def mid(a): a.sort(); n=len(a)//10; return a[5*n]  
def sd(a):  a.sort(); n=len(a)//10; return (a[9*n]-a[n])/2.56

cohen = 0.35
```

Then compute the convergence threshold:
```python
fn = sd  # or mid or top
eps = fn([Y(r) for r in data.rows]) * cohen
print(f"Convergence threshold: {eps:.2f}")
```

**Test**: Run and verify you get a small positive number.

**Expected Output**: Around `0.07` to `0.09`

---

### Exercise 7: Single Hill-Climbing Run

**Goal**: Put it all together for one optimization run.

**Task**: Write a loop that:
1. Starts with shuffled data.rows
2. Maintains `labelled` list (initially empty)
3. Each iteration:
   - Add `step=5` random rows to labelled; i.e. at each round of the loop, look at five more rows.
   - Find ok, no = extremes(labelled)
   - Prune rows to better half
   - Report progress on labelled
4. Stop when you've labelled `budget=100` rows

**Pseudocode**:
```python
budget = 100
step = 5
labelled, rows = [], shuffle(data.rows[:])

report(rows)
while len(labelled) < budget:
    labelled += shuffle(rows)[:step]
    ok, no = extremes(labelled)
    rows = prune(rows, ok, no)
    report(labelled)
print(", ", len(labelled), end=", ")
report(labelled)
print("")
```

**Test**: Run once and observe the sequence of scores
should generally improve (decrease).

---

### Exercise 8: Adding Convergence Check

**Goal**: Stop early if converged.

**Task**: Modify the loop from Exercise 6:
- Track `b4 = 1e32` (before value)
- After each report, calculate `now = fn([Y(r) for r in labelled])`
- If `abs(b4 - now) > eps`: update `b4 = now`
- Else: `break` (converged)

**Test**: Run and note it may stop before 100 evaluations.

---

### Exercise 9: Multiple Runs with Statistics

**Goal**: Run 20 times to get robust statistics.

**Task**: Wrap Exercise 7 in a for loop:
```python
print(round(eps, 2))
for _ in range(20):
    # Your Exercise 7 code here
```

**Test**: Run and pipe through sort/column:
```bash
python3 -B my_hc.py 1 ~/gits/moot/optimize/misc/auto93.csv \
  | sort -t, -k 3 -n | column -s, -t | cat -n
```

**Expected**: Should match the pattern from `make hc`,
with varying numbers of evaluations but most runs
finding scores around 0.09-0.15.

---

### Final Notes

**What You've Built**: A semi-supervised optimizer that:
- Uses small labeled samples to guide search
- Projects unlabeled data onto good-bad axis
- Prunes away unpromising regions iteratively
- Converges when improvements plateau

**Performance**: With 15-40 evaluations (vs 100 random),
you typically find solutions competitive with searching
all 398 rows.

**Key Insight**: Geometry (projection) + Iterative
refinement (pruning) >> Random search

Compare your results:
- Random (30 eval): median=0.53, best=0.15
- Your HC (20-40 eval): median≈0.15, best≈0.09
- All data: best=0.07

You're finding near-optimal solutions with 5-10% of
the evaluation budget!

