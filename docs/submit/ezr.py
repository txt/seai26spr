#!/usr/bin/env python3 -B
"""
ezr.py: easy AI tools
(c)2026 Tim Menzies, MIT license.

Options:
   -p p=2   
   -s seed=1
"""
import re, sys, math, random, traceback
from math import sqrt, exp, log
BIG = 1E32
the = {}

# --- pretty print ---------------------------------------------------
def cast(s):
  try: return int(s)
  except ValueError:
    try: return float(s)
    except ValueError: return s.strip()

def csv(f):
  with open(f) as file:
    for line in file:
      line = re.sub(r'\s+', '', line.split("#")[0])
      if line: yield [cast(x) for x in line.split(",")]

def gauss(mu, sd1):
  return mu + 2 * sd1 * (sum(random.random() for _ in range(3)) - 1.5)

def pick(d, n):
  n *= random.random()
  for k, v in d.items():
    if (n := n - v) <= 0: break
  return k

def shuffle(lst): random.shuffle(lst); return lst

def o(t):
  match t:
    case dict(): return "{" + " ".join(f":{k} {o(t[k])}" for k in t) + "}"
    case float(): return f"{int(t)}" if int(t) == t else f"{t:.2f}"
    case list(): return "[" + ", ".join(o(x) for x in t) + "]"
    case tuple(): return "(" + ", ".join(o(x) for x in t) + ")"
    case _:  return str(t)

class Obj(dict):
  __getattr__,__setattr__,__repr__=dict.__getitem__,dict.__setitem__,o

# --- constructors ---------------------------------------------------
def Sym(n=0, s=" "): return Obj(at=n,txt=s,n=0,has={})
def Num(n=0, s=" "): return Obj(at=n,txt=s,n=0,mu=0,m2=0,goal=s[-1]!="-")
def Col(n=0, s=" "): return (Num if s[0].isupper() else Sym)(n, s)

def Cols(row):
  all = [Col(n, s) for n, s in enumerate(row)]
  return Obj(names=row, all=all,
             x=[c for c in all if not re.search(r"[+\-!X]$", c.txt)],
             y=[c for c in all if     re.search(r"[+\-!]$",  c.txt)])

def Data(src=None):
  data = Obj(n=0, rows=[], cols=None)
  if src: [add(data, r) for r in src]
  return data

def clone(data, rows=None): return Data([data.cols.names] + (rows or []))

def add(i, v):
  if "rows" in i:  # Data
    if not i.cols: i.cols = Cols(v)
    else: i.rows.append([add(c, v[c.at]) for c in i.cols.all])
  elif v != "?":
    i.n += 1
    if "mu" in i:  d = v - i.mu; i.mu += d / i.n; i.m2 += d * (v - i.mu)
    else: i.has[v] = 1 + i.has.get(v, 0)
  return v

def adds(items=[], obj=None):
  obj = obj or Num()
  for item in items: add(obj, item)
  return obj

# --- query ----------------------------------------------------------
def mids(data): return [mid(c) for c in data.cols.all]
def mid(col):   
  return col.mu if "mu" in col else max(col.has, key=col.has.get)

def spread(col): return sd(col)  if "mu" in col else ent(col)
def sd(num):     return 0 if num.n < 2 else sqrt(num.m2 / (num.n - 1))
def ent(sym):    
 return -sum(p*log(p,2) for n in sym.has.values() if (p:= n/sym.n) > 0)

def z(num, v):  return (v - num.mu) / (sd(num) + 1 / BIG)
def norm(z): return 1 / (1 + exp(-1.7 * max(-3, min(3, z))))

# --- distance -------------------------------------------------------
def minkowski(items):
  n, d = 0, 0
  for item in items: 
    n += 1
    d += item ** the.p
  return 0 if n == 0 else (d / n) ** (1 / the.p)

def disty(data, row):
  return minkowski(norm(z(c, row[c.at])) - c.goal for c in data.cols.y)

def distx(data, row1, row2):
  return minkowski(aha(c, row1[c.at], row2[c.at]) for c in data.cols.x)

def aha(col, u, v):
  if u == v == "?": return 1
  if "has" in col: return u != v
  u = "?" if u == "?" else norm(z(col, u))
  v = "?" if v == "?" else norm(z(col, v))
  u = u if u != "?" else (0 if v > 0.5 else 1)
  v = v if v != "?" else (0 if u > 0.5 else 1)
  return abs(u - v)

def furthest(data, row, rows):  return nearest(data, row, rows, max)

def nearest(data, row, rows, fn=min):  
  return fn(rows, key=lambda r: distx(data, row, r))

# --- cli ------------------------------------------------------------
def eg_h(_):    print(__doc__)
def eg__the(_): print(o(the))
def eg_s(n):    the.seed = n; random.seed(n)

def eg__sym(_):
  sym = adds("aaaabbc", Sym())
  e = ent(sym)
  print(o(e))
  assert abs(1.379 - e) < 0.05, "ent failed"

def eg__num(_):
  num = adds(gauss(10, 1) for _ in range(1000))
  print(Obj(mu=num.mu, sd=sd(num)))
  assert abs(10 - num.mu) < 0.05 and abs(1 - sd(num)) < 0.05, "num failed"

def eg__csv(f): [print(row) for row in list(csv(f))[::40]]

def eg__data(f):
  data = Data(csv(f))
  print(*data.cols.names)
  print(o(mids(data)))
  print(f"x: {[c.txt for c in data.cols.x]}")
  print(f"y: {[c.txt for c in data.cols.y]}")

def eg__clone(f):
  data1 = Data(csv(f))
  data2 = clone(data1, data1.rows[:10])
  print("original:", len(data1.rows), "clone:", len(data2.rows))
  print("cols match:", data1.cols.names == data2.cols.names)

def eg__spread(f):
  data = Data(csv(f))
  for c in data.cols.all:
    print(f"{c.txt:15} spread={o(spread(c)):8} mid={o(mid(c))}")

def eg__dist(f):
  data = Data(csv(f))
  row = data.rows[0]
  print("row0:", r)
  near = nearest(data, row, data.rows[1:])
  far = furthest(data, row, data.rows[1:])
  print("near:", near, "dist:", round(distx(data, row, near), 3))
  print("far: ", far, "dist:", round(distx(data, row, far), 3))

def eg__disty(f):
  data = Data(csv(f))
  print("disty",*data.cols.names,sep=",")
  for row in sorted(data.rows, key=lambda r: disty(data, r))[::25]:
    print(round(disty(data, row), 3), *row,sep=",")

# --- main -----------------------------------------------------------
the=Obj(**{k:cast(v) for k, v in re.findall(r"(\w+)=(\S+)", __doc__)})
random.seed(the.seed)

if __name__ == "__main__":
  for j, s in enumerate(sys.argv):
    if f := vars().get(f"eg{s.replace('-', '_')}"):
      try: f(sys.argv[j + 1] if j + 1 < len(sys.argv) else None)
      except Exception: traceback.print_exc()
    elif (k := s.lstrip("-")[:1]) in the:
      the[k] = cast(sys.argv[j + 1]) if j+1<len(sys.argv) else the[k]
