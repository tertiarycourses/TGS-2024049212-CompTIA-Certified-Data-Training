# Lab 10 — Correlation, Regression and the Causation Trap

**Domain 03 — Data Analysis** (24% of the CompTIA Data+ (DA0-001) exam)  
**Maps to:** LU3 / LO3 (K2, A3)  
**Course:** WSQ - CompTIA Certified Data+ Training (TGS-2024049212)

---

## Exam objective

Select statistical methods: correlation and regression; troubleshoot analysis issues (Domain 3); LO3 / LO5 / A3 / A4.

## What you will do

You measure the relationship between marketing spend and revenue with Pearson's r and R-squared, fit a regression line, use it to predict — and then meet a third dataset where two variables correlate almost perfectly with no causal link at all. Recognising that trap is an exam objective and a professional duty.

## What you will produce

A correlation matrix, a fitted regression equation with R-squared, a prediction, and a written spurious-correlation analysis.

## Tools

- Killercoda Ubuntu, Python 3, pandas, scipy
- **Environment:** https://killercoda.com/playgrounds/scenario/ubuntu

---

## Step-by-step

### Step 1

Create the working folder and download this lab's dataset. The files also ship in the course repo under labs/lab-10-correlation-regression-and-the-causation-trap/data/ — download them from GitHub or copy them from the folder you cloned.

```bash
mkdir -p ~/dataplus/lab10 && cd ~/dataplus/lab10 && BASE=https://raw.githubusercontent.com/tertiarycourses/TGS-2024049212-CompTIA-Certified-Data-Training/main/labs/lab-10-correlation-regression-and-the-causation-trap/data && for f in marketing.csv; do curl -fsSO $BASE/$f || echo FAILED $f; done && ls -l
```

### Step 2

Compute the full CORRELATION MATRIX — every pair at once.

```bash
python3 -c "import pandas as pd;d=pd.read_csv('marketing.csv');print(d[['spend','revenue','staff']].corr().round(4))"
```

### Step 3

Get Pearson's r and its p-value for spend versus revenue specifically.

```bash
python3 -c "import pandas as pd;from scipy import stats;d=pd.read_csv('marketing.csv');r,p=stats.pearsonr(d.spend,d.revenue);print('r =',round(r,4));print('r-squared =',round(r**2,4));print('p =',round(p,8))"
```

### Step 4

Fit the REGRESSION LINE and read off the slope and intercept.

```bash
python3 -c "import pandas as pd;from scipy import stats;d=pd.read_csv('marketing.csv');lr=stats.linregress(d.spend,d.revenue);print(f'revenue = {lr.slope:.3f} * spend + {lr.intercept:.3f}');print('R-squared =',round(lr.rvalue**2,4))"
```

### Step 5

Use the model to PREDICT revenue at a spend level you have never observed.

```bash
python3 -c "import pandas as pd;from scipy import stats;d=pd.read_csv('marketing.csv');lr=stats.linregress(d.spend,d.revenue);print('predicted revenue at spend=40:',round(lr.slope*40+lr.intercept,2))"
```

### Step 6

State the limit of that prediction: spend=40 is outside the observed range (10–33). Write down why extrapolating beyond your data is the analysis error the exam warns about.

### Step 7

THE TRAP — now look at staff versus revenue. The correlation is nearly as strong.

```bash
python3 -c "import pandas as pd;from scipy import stats;d=pd.read_csv('marketing.csv');r,p=stats.pearsonr(d.staff,d.revenue);print('staff vs revenue r =',round(r,4))"
```

### Step 8

Explain in writing: does hiring staff CAUSE revenue? Identify the confounding variable that drives both, and state the one sentence every analyst must be able to defend — correlation is not causation.

---

## Dataset

This lab ships with its own data — you do not have to type it in. See [`data/README.md`](data/README.md) for what each file contains and which defects are planted in it.

- [`data/marketing.csv`](data/marketing.csv) — 666 bytes
- [`data/marketing.xlsx`](data/marketing.xlsx) — 5,879 bytes

---

## Test it — expected result

Across 36 months spend and revenue correlate at r ≈ 0.991 with R-squared ≈ 0.982, giving revenue ≈ 6.55 × spend + 54.1. Staff headcount ALSO correlates with revenue at r ≈ 0.970 — but growth over time drives both, so that second relationship is not causal.

## If it doesn't work

| Symptom | Fix |
|---|---|
| The CSV contains '404: Not Found' | curl wrote the error page into the file. Confirm the BASE URL, re-run with -fsSO so curl fails loudly, or copy the files from the repo folder you cloned. |
| r is exactly 1.0 | Perfect correlation means the data is synthetic and noise-free. Note that real business data never looks like this. |
| linregress has no attribute rvalue | You are on a very old scipy. Use r,p = stats.pearsonr(...) and square r yourself. |
| The prediction looks unreasonable | That is the extrapolation lesson — a linear model fitted on 10–33 has no evidence about 40. Say so in the report. |

---

*© 2026 Tertiary Infotech Academy Pte Ltd. All rights reserved. · TGS-2024049212*
