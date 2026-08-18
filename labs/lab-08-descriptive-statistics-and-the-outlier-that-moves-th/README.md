# Lab 8 — Descriptive Statistics and the Outlier That Moves the Mean

**Domain 03 — Data Analysis** (24% of the CompTIA Data+ (DA0-001) exam)  
**Maps to:** LU3 / LO3 (K2, A3)  
**Course:** WSQ - CompTIA Certified Data+ Training (TGS-2024049212)

---

## Exam objective

Select statistical methods: apply basic statistical techniques to data (Domain 3); LO3 / K2 / A3.

## What you will do

You compute every descriptive statistic the exam names — mean, median, mode, range, variance, standard deviation and z-score — on a real salary dataset, then remove one outlier and watch which statistics move and which do not. This is the exam's central-tendency-versus-robustness point, proven with numbers.

## What you will produce

A descriptive-statistics report showing mean, median, mode, range, variance, SD and z-scores, computed with and without the outlier.

## Tools

- Killercoda Ubuntu, Python 3, pandas, statistics
- **Environment:** https://killercoda.com/playgrounds/scenario/ubuntu

---

## Step-by-step

### Step 1

Create the lab folder and the salary dataset — one director salary is far above the rest.

```bash
mkdir -p ~/dataplus/lab8 && cd ~/dataplus/lab8 && printf 'employee,dept,salary\nA,Ops,3800\nB,Ops,4200\nC,Ops,4000\nD,Sales,4500\nE,Sales,3900\nF,Sales,4200\nG,Tech,5200\nH,Tech,4800\nI,Tech,5000\nJ,Exec,26000\n' > salaries.csv
```

### Step 2

Compute CENTRAL TENDENCY — mean, median and mode together.

```bash
python3 -c "import pandas as pd;d=pd.read_csv('salaries.csv');s=d.salary;print('mean',round(s.mean(),2));print('median',s.median());print('mode',s.mode().tolist())"
```

### Step 3

Compute DISPERSION — min, max, range, variance and standard deviation.

```bash
python3 -c "import pandas as pd;d=pd.read_csv('salaries.csv');s=d.salary;print('min',s.min(),'max',s.max(),'range',s.max()-s.min());print('variance',round(s.var(),2),'sd',round(s.std(),2))"
```

### Step 4

Compute the Z-SCORE for every row and flag anything beyond |z| > 2.

```bash
python3 -c "import pandas as pd;d=pd.read_csv('salaries.csv');s=d.salary;d['z']=((s-s.mean())/s.std()).round(2);print(d);print('FLAGGED:');print(d[abs(d.z)>2])"
```

### Step 5

Now remove the outlier and recompute the SAME statistics.

```bash
python3 -c "import pandas as pd;d=pd.read_csv('salaries.csv');c=d[d.salary<20000].salary;print('mean',round(c.mean(),2));print('median',c.median());print('sd',round(c.std(),2))"
```

### Step 6

Compare the two runs side by side and record which statistic moved most.

```bash
python3 -c "import pandas as pd;d=pd.read_csv('salaries.csv');a=d.salary;b=d[d.salary<20000].salary;print(f'mean   {a.mean():>9.2f} -> {b.mean():>8.2f}');print(f'median {a.median():>9.2f} -> {b.median():>8.2f}');print(f'sd     {a.std():>9.2f} -> {b.std():>8.2f}')"
```

### Step 7

Compute the departmental summary — this is the aggregation a manager actually asks for.

```bash
python3 -c "import pandas as pd;d=pd.read_csv('salaries.csv');print(d.groupby('dept').salary.agg(['count','mean','median','std']).round(2))"
```

### Step 8

Write your recommendation: which single number should be reported to the board, and why.

---

## Test it — expected result

With the outlier the mean is ~6560 but the median is only 4350. Removing it drops the mean to ~4400 while the median barely moves (4350 → 4200). The Exec row is flagged at z ≈ 2.8. Your report recommends the MEDIAN.

## If it doesn't work

| Symptom | Fix |
|---|---|
| mode returns several values | A dataset with no repeated value returns every value. pandas .mode() correctly returns a list — report it as 'no single mode'. |
| Variance looks enormous | Variance is in squared units. Report the standard deviation (its square root) instead, which is in dollars. |
| No row is flagged at |z|>2 | With n=10 a single extreme point inflates the SD and hides itself. Try the median-absolute-deviation method and discuss the difference. |

---

*© 2026 Tertiary Infotech Academy Pte Ltd. All rights reserved. · TGS-2024049212*
