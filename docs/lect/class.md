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



# Naive Bayes — Worked Example (Weather Data)

---
```
▶ ./bayes_class.py --data ~/gits/moot/classify/diabetes.csv
          label,   n, pd, pf, prec, acc
tested_positive, 262, 74, 32,   55,  70
tested_negative, 496, 67, 25,   83,  70
       _OVERALL, 758, 70, 29,   70,  70
```

```
🧩ezr/ezr tools26 ▶ ./bayes_class.py --data ~/gits/moot/classify/soybean.csv
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

## Bayes

- Low Memory footprint
- Incremental
- Fast
- Can handle incompelte data
- Surprisngly effective

## Step 1: The Training Data

10 rows, 4 features, 2 classes (play = yes/no).

| outlook  | temp | humidity | windy | play |
|----------|------|----------|-------|------|
| sunny    |  85  |    85    | false | no   |
| sunny    |  80  |    90    | true  | no   |
| overcast |  83  |    86    | false | yes  |
| rainy    |  70  |    96    | false | yes  |
| rainy    |  68  |    80    | false | yes  |
| rainy    |  65  |    70    | true  | no   |
| overcast |  64  |    65    | true  | yes  |
| sunny    |  72  |    95    | false | no   |
| sunny    |  69  |    70    | false | yes  |
| overcast |  75  |    90    | true  | no   |

- **yes rows**: overcast/86, rainy/96, rainy/80, overcast/65,
  sunny/70   → **5 rows**
- **no rows**: sunny/85, sunny/90, rainy/70, sunny/95,
  overcast/90 → **5 rows**

---

## Step 2: Priors (with Laplace m-smoothing, m=2, n_h=2)

```
P(yes) = (count_yes + m) / (n_all + m × n_h)
       = (5 + 2)    / (10  + 2 × 2)
       = 7/14 = 0.500

P(no)  = (5 + 2) / 14 = 0.500
```

With equal class counts the priors are equal — they won't
differentiate the classes here, but they are still included
in the log-posterior sum.

---

## Step 3: Feature Tables

**Symbolic counts** (n=5 per class):

```
outlook:  sunny  overcast  rainy      windy:  false  true
  yes       1       2        2           yes    4      1
  no        3       1        1           no     2      3
```

Likelihood: `P(v|class) = (count + k×prior) / (n + k)`  with k=1

**Numeric summaries** (sorted values → median, spread=(s[90%]-s[10%])/2.56):

```
            yes: [64,68,69,70,83]    no: [65,72,75,80,85]
temp:       median=69  spread=5.86       median=75  spread=5.08

            yes: [65,70,80,86,96]    no: [70,85,90,90,95]
humidity:   median=80  spread=10.16      median=90  spread=3.91
```

Likelihood: `P(v|class) = Gauss(v; median, spread)`

---

## Step 5: Classify a New Row

**New row**: `sunny, temp=72, humidity=90, windy=true, play=?`

We compute the **log-posterior** for each class:

```
log P(class | row) = log P(class)
                   + log P(outlook | class)
                   + log P(windy   | class)
                   + log P(temp    | class)
                   + log P(humidity| class)
```

### Class = yes  (prior = 0.500)

**outlook = sunny** (count_yes=1, n_yes=5, prior=0.500):
```
P(sunny|yes) = (1 + 1×0.500) / (5 + 1) = 1.5/6 = 0.2500
```

**windy = true** (count_yes=1, n_yes=5, prior=0.500):
```
P(true|yes) = (1 + 1×0.500) / (5 + 1) = 1.5/6 = 0.2500
```

**temp = 72** (μ=69, σ=5.86):
```
P(72|yes) = Gauss(72; 69, 5.86)
          = (1/√(2π×5.86²)) × exp(-(72-69)²/(2×5.86²))
          = (1/14.67) × exp(-9/68.75)
          = 0.06815 × exp(-0.1309)
          = 0.06815 × 0.8774
          = 0.0598
```

**humidity = 90** (μ=80, σ=10.16):
```
P(90|yes) = Gauss(90; 80, 10.16)
          = (1/25.42) × exp(-(90-80)²/(2×10.16²))
          = (1/25.42) × exp(-100/206.45)
          = 0.03934 × exp(-0.4844)
          = 0.03934 × 0.6161
          = 0.0242
```

**log-posterior (yes)**:
```
  log(0.5000)  = -0.693
  log(0.2500)  = -1.386
  log(0.2500)  = -1.386
  log(0.0598)  = -2.818
  log(0.0242)  = -3.722
  ─────────────────────
  total        = -10.005
```

---

### Class = no  (prior = 0.500)

**outlook = sunny** (count_no=3, n_no=5, prior=0.500):
```
P(sunny|no) = (3 + 1×0.500) / (5 + 1) = 3.5/6 = 0.5833
```

**windy = true** (count_no=3, n_no=5, prior=0.500):
```
P(true|no) = (3 + 1×0.500) / (5 + 1) = 3.5/6 = 0.5833
```

**temp = 72** (μ=75, σ=5.08):
```
P(72|no) = Gauss(72; 75, 5.08)
         = (1/12.71) × exp(-(72-75)²/(2×5.08²))
         = (1/12.71) × exp(-9/51.61)
         = 0.07867 × exp(-0.1744)
         = 0.07867 × 0.8400
         = 0.0661
```

**humidity = 90** (μ=90, σ=3.91):
```
P(90|no) = Gauss(90; 90, 3.91)
         = (1/9.78) × exp(-(90-90)²/(2×3.91²))
         = (1/9.78) × exp(0)
         = 0.1022 × 1.000
         = 0.1022
```

**log-posterior (no)**:
```
  log(0.5000)  = -0.693
  log(0.5833)  = -0.539
  log(0.5833)  = -0.539
  log(0.0661)  = -2.717
  log(0.1022)  = -2.281
  ─────────────────────
  total        = -6.769
```

---

## Step 6: Decision

```
log P(yes | row) = -10.005
log P(no  | row) =  -6.769   ← higher (less negative)
```

**Prediction: no** — don't play.

The two decisive features were:

- **outlook**: sunny appears 3× in no rows vs 1× in yes rows.
  `P(sunny|no)=0.583` vs `P(sunny|yes)=0.250`
- **windy**: true appears 3× in no rows vs 1× in yes rows.
  Same ratio. These two features push the score strongly
  toward "no" and the numeric features don't overcome them.

---

## Step 7: Connection to `bayes_class.py`

The code does the same computation, just online and in a loop:

```python
# ks[k] is a Data object holding all rows seen so far for class k
def best(k):
    return ks[k].like(r, len(every.rows), len(ks))

confuse(cf, str(k), str(max(ks, key=best)))
```

`Data.like` returns the log-posterior above.  
`max(ks, key=best)` picks the class with the least-negative score.  
No probabilities are ever converted back — only the ranking matters.
