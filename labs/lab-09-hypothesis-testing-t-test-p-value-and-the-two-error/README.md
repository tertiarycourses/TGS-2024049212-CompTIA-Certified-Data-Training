# Lab 9 — Hypothesis Testing: t-test, p-value and the Two Error Types

**Domain 03 — Data Analysis** (24% of the CompTIA Data+ (DA0-001) exam)  
**Maps to:** LU3 / LO3 (K2, A3)  
**Course:** WSQ - CompTIA Certified Data+ Training (TGS-2024049212)

---

## Exam objective

Select statistical methods: inferential techniques, hypothesis testing (Domain 3); LO3 / K2 / A3.

## What you will do

A marketing team claims the new checkout page lifts order value. You state the null and alternative hypotheses, run a two-sample t-test, read the p-value against the 0.05 threshold, and state your conclusion in business language — including which error type you would be risking if you are wrong.

## What you will produce

A completed hypothesis test: stated H0/H1, computed t-statistic and p-value, an accept/reject decision, and the business recommendation.

## Tools

- Killercoda Ubuntu, Python 3, pandas, scipy
- **Environment:** https://killercoda.com/playgrounds/scenario/ubuntu

---

## Step-by-step

### Step 1

Download this lab's dataset. The same files ship in the course repo under this lab's data/ folder.

```bash
mkdir -p ~/dataplus/lab9 && cd ~/dataplus/lab9;
R=https://raw.githubusercontent.com/tertiarycourses;
B=$R/TGS-2024049212-CompTIA-Certified-Data-Training/main/labs;
D=lab-09-hypothesis-testing-t-test-p-value-and-the-two-error;
for f in abtest.csv; do curl -fsSO $B/$D/data/$f || echo FAILED $f; done; ls -l
```

### Step 2

STATE THE HYPOTHESES before you look at any result — this is the discipline the exam tests.  H0: there is no difference in mean order value.  H1: the new page has a higher mean order value.

### Step 3

Look at the group means first — a difference here is necessary but NOT sufficient.

```bash
python3 -c "import pandas as pd;d=pd.read_csv('abtest.csv');print(d.groupby('group').order_value.agg(['count','mean','std']).round(2))"
```

### Step 4

Run the two-sample t-test and read the p-value.

```bash
python3 -c "import pandas as pd;from scipy import stats;d=pd.read_csv('abtest.csv');a=d[d.group=='A'].order_value;b=d[d.group=='B'].order_value;t,p=stats.ttest_ind(a,b);print('t =',round(t,4));print('p =',round(p,6))"
```

### Step 5

Apply the 0.05 decision rule explicitly.

```bash
python3 -c "import pandas as pd;from scipy import stats;d=pd.read_csv('abtest.csv');a=d[d.group=='A'].order_value;b=d[d.group=='B'].order_value;t,p=stats.ttest_ind(a,b);print('REJECT H0 - the difference is statistically significant' if p<0.05 else 'FAIL TO REJECT H0')"
```

### Step 6

Compute the 95% confidence interval for the difference so you can report a range, not just a verdict.

```bash
python3 -c "import pandas as pd,numpy as np;from scipy import stats;d=pd.read_csv('abtest.csv');a=d[d.group=='A'].order_value;b=d[d.group=='B'].order_value;diff=b.mean()-a.mean();se=np.sqrt(a.var()/len(a)+b.var()/len(b));print('diff',round(diff,2),'95% CI',(round(diff-1.96*se,2),round(diff+1.96*se,2)))"
```

### Step 7

Now the error-type question. Write down: if you reject H0 and you are WRONG, which error is that (Type I) and what does it cost the business? If you fail to reject and you are wrong (Type II), what does that cost?

### Step 8

Write the one-paragraph recommendation a manager could act on — no statistics jargon.

---

## Dataset

This lab ships with its own data — you do not have to type it in. See [`data/README.md`](data/README.md) for what each file contains and which defects are planted in it.

- [`data/abtest.csv`](data/abtest.csv) — 1,088 bytes
- [`data/abtest.xlsx`](data/abtest.xlsx) — 6,533 bytes

---

## Test it — expected result

With 60 observations per group the t-test returns t ≈ -11.3 and p ≈ 1.9e-20, far below 0.05, so you REJECT H0. Group B averages about 49.65 against 41.14 for group A — a lift of roughly 8.5, with a 95% confidence interval that excludes zero.

## If it doesn't work

| Symptom | Fix |
|---|---|
| The CSV contains '404: Not Found' | curl wrote the error page into the file. Confirm the BASE URL, re-run with -fsSO so curl fails loudly, or copy the files from the repo folder you cloned. |
| ModuleNotFoundError: scipy | Run pip3 install scipy, adding --break-system-packages if Killercoda's pip refuses. |
| p-value is nan | One group has fewer than two values or zero variance. Check your CSV loaded all 16 rows with d.shape. |
| The result feels too clean | It is a teaching dataset with clean separation. Ask the trainer for the noisy variant to see a borderline p-value. |

---

*© 2026 Tertiary Infotech Academy Pte Ltd. All rights reserved. · TGS-2024049212*
