#!/usr/bin/env python3 -B
"""
sa.py: simulated annealing optimizer
Homework skeleton - complete the TODOs
"""
import sys, math, random
from ezr import csv, distx, disty, gauss, sd, pick, Data, nearest, o

def sa(data, k=4000, m_rate=0.5, loud=False):
  # Extract bounds for numeric columns
  LO, HI = {}, {}
  for c in data.cols.x:
    if "mu" in c:
      LO[c.at], *_, HI[c.at] = sorted(r[c.at] for r in data.rows if r[c.at] != "?")

  def mutate(c, v):
    """TODO 1: Return mutated value.
    - For symbolic cols ("has" in c): use pick(c.has, c.n)
    - For numeric cols: Gaussian mutation within [LO, HI] bounds
      Use: LO[c.at] + (gauss(v, sd(c)) - LO[c.at]) % (HI[c.at] - LO[c.at] + 1E-32)
    """
    pass  # <- Replace this

  def score(row):
    """TODO 2: Estimate row's quality using nearest neighbor surrogate.
    - Find nearest neighbor in data.rows using nearest(data, row, data.rows)
    - Copy neighbor's y-values to row: for y in data.cols.y: row[y.at] = near[y.at]
    - Return disty(data, row)
    """
    pass  # <- Replace this

  # Initialize: random starting point
  s = random.choice(data.rows)[:]
  e, best = score(s), s[:]

  for heat in range(k):
    # Generate neighbor by mutating some features
    sn = s[:]
    for c in random.choices(data.cols.x, k=max(1, int(m_rate * len(data.cols.x)))):
      sn[c.at] = mutate(c, sn[c.at])

    en = score(sn)
    
    # TODO 3: Replace "False" with Metropolis-Hastings acceptance criterion
    # Accept if: (1) en < e (better), OR (2) random.random() < exp((e - en) / T)
    # where T = 1 - heat/k (temperature that cools from 1 to 0)
    if False:  # <- Replace this condition
      s, e = sn, en
      if en < disty(data, best):
        best = s[:]
        if loud: print(f"{heat:<5} {e:.3f}", o(best))

  return best

if __name__ == "__main__":
  seed, file = sys.argv[1:]
  random.seed(int(seed))
  sa(Data(csv(file)), loud=True)
