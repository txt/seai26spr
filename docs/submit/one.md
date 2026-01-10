.

# Homework 1

Two basic search methods are random search and hillclimbing.

In random search:

- grab, say, 100 examples at random
- Sort them by their 

## Background: Sort Rows with Many Goals

How to sort rows with multiple goals.

```
Clndrs,Volume,HpX,Model,origin,Lbs-,Acc+,Mpg+
8,304,193,70,1,4732,18.5,10
8,360,215,70,1,4615,14,10
8,307,200,70,1,4376,15,10
8,318,210,70,1,4382,13.5,10
8,429,208,72,1,4633,11,10
8,400,150,73,1,4997,14,10
8,350,180,73,1,3664,11,10
8,383,180,71,1,4955,11.5,10
8,350,160,72,1,4456,13.5,10
```

This data has the goals marked with "-" and "+". Here, three goals

    Lbs-, Acc+, Mpg+

that we want to minimize, maximize and maximize. For these roows,
"heaven" is

    0,1,1

For each row of data, we normalize the goals 0..1 for min..max.

```
Clndrs,Volume,HpX,Model,origin,Lbs- (Norm),Acc+ (Norm),Mpg+ (Norm)*
8,304,193,70,1,0.80,1.00,0.0
8,360,215,70,1,0.71,0.40,0.0
8,307,200,70,1,0.53,0.53,0.0
8,318,210,70,1,0.54,0.33,0.0
8,429,208,72,1,0.73,0.00,0.0
8,400,150,73,1,1.00,0.40,0.0
8,350,180,73,1,0.00,0.00,0.0
8,383,180,71,1,0.97,0.07,0.0
8,350,160,72,1,0.59,0.33,0.0
```
Then run an aggregation function to compute distance to heaven
_d2h_. E,g for the last row we have average weight (.59), low
acceleration (0.33) and very low miles per hour (0).  So, the _d2h_
is:

    sqrt(squred(.59-0) + squared(.22 - 1) + squared(0 - 1)) / sqrt(3)
    = sqrt(0.3481 + 0.4489 + 1)
    = 0.77

Note that _smaller_ distance are _better_ since that means we are
getting closer to heaven. This particular car is not very good
(since its _d2h_ is over half).
