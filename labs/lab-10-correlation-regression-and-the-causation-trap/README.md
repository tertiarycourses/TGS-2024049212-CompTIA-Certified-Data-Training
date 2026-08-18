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

Create the lab folder and the monthly marketing dataset.

```bash
mkdir -p ~/dataplus/lab10 && cd ~/dataplus/lab10 && printf 'month,spend,revenue,staff\n1,10,118,12\n2,12,131,12\n3,15,152,13\n4,18,171,14\n5,20,188,14\n6,22,197,15\n7,25,221,16\n8,28,238,16\n9,30,255,17\n10,33,271,18\n' > marketing.csv
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

## Test it — expected result

Spend and revenue correlate at r ≈ 0.999 with R-squared ≈ 0.998, giving revenue ≈ 6.6 × spend + 52. Staff also correlates ≈ 0.99 with revenue — but growth over time drives both, so the link is not causal.

## If it doesn't work

| Symptom | Fix |
|---|---|
| r is exactly 1.0 | Perfect correlation means the data is synthetic and noise-free. Note that real business data never looks like this. |
| linregress has no attribute rvalue | You are on a very old scipy. Use r,p = stats.pearsonr(...) and square r yourself. |
| The prediction looks unreasonable | That is the extrapolation lesson — a linear model fitted on 10–33 has no evidence about 40. Say so in the report. |

---

*© 2026 Tertiary Infotech Academy Pte Ltd. All rights reserved. · TGS-2024049212*
