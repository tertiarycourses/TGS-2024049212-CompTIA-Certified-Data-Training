# Lab 4 — Explore a Dirty Dataset: Missing Values, Duplicates and Outliers

**Domain 02 — Data Acquisition and Preparation** (22% of the CompTIA Data+ (DA0-001) exam)  
**Maps to:** LU2 / LO2 (K1, A2)  
**Course:** WSQ - CompTIA Certified Data+ Training (TGS-2024049212)

---

## Exam objective

Perform data exploration: find missing values, duplication, redundancy or outliers (Domain 2); LO2 / K1 / A2.

## What you will do

You are handed a deliberately dirty sales extract and must profile it before trusting a single number. You quantify every defect class the exam names — nulls, duplicates, redundancy and outliers — and produce a data-quality report that says how bad the data is BEFORE you clean it.

## What you will produce

A data-quality profile report quantifying null counts per column, duplicate rows, and outliers detected by z-score.

## Tools

- Killercoda Ubuntu, Python 3, pandas
- **Environment:** https://killercoda.com/playgrounds/scenario/ubuntu

---

## Step-by-step

### Step 1

Download this lab's dataset. The same files ship in the course repo under this lab's data/ folder.

```bash
mkdir -p ~/dataplus/lab4 && cd ~/dataplus/lab4;
R=https://raw.githubusercontent.com/tertiarycourses;
B=$R/TGS-2024049212-CompTIA-Certified-Data-Training/main/labs;
D=lab-04-explore-a-dirty-dataset-missing-values-duplicates-an;
for f in sales_dirty.csv; do curl -fsSO $B/$D/data/$f || echo FAILED $f; done; ls -l
```

### Step 2

Load it and look at the shape and dtypes first — always know how many records you started with.

```bash
python3 -c "import pandas as pd;d=pd.read_csv('sales_dirty.csv');print(d.shape);print(d.dtypes)"
```

### Step 3

Count MISSING VALUES per column — the exam's first exploration task.

```bash
python3 -c "import pandas as pd;d=pd.read_csv('sales_dirty.csv');print(d.isnull().sum())"
```

### Step 4

Count DUPLICATE rows and show which ones they are.

```bash
python3 -c "import pandas as pd;d=pd.read_csv('sales_dirty.csv');print('dupes:',d.duplicated().sum());print(d[d.duplicated(keep=False)])"
```

### Step 5

Detect OUTLIERS with a z-score — any |z| above 3 is the standard flag.

```bash
python3 -c "import pandas as pd;d=pd.read_csv('sales_dirty.csv');s=pd.to_numeric(d['spend'],errors='coerce');z=(s-s.mean())/s.std();print(d.loc[z[abs(z)>3].index])"
```

### Step 6

Get the descriptive summary and note how badly the 99999 distorts the mean versus the median.

```bash
python3 -c "import pandas as pd;d=pd.read_csv('sales_dirty.csv');print(d['spend'].describe());print('median',d['spend'].median())"
```

### Step 7

Write the profile report to a file so the cleaning lab can be measured against it.

```bash
python3 -c "import pandas as pd;d=pd.read_csv('sales_dirty.csv');open('profile.txt','w').write(str(d.isnull().sum())+'\ndupes: '+str(d.duplicated().sum())+'\nmean: '+str(d.spend.mean())+'\nmedian: '+str(d.spend.median()))" && cat profile.txt
```

---

## Dataset

This lab ships with its own data — you do not have to type it in. See [`data/README.md`](data/README.md) for what each file contains and which defects are planted in it.

- [`data/sales_dirty.csv`](data/sales_dirty.csv) — 2,656 bytes
- [`data/sales_dirty.xlsx`](data/sales_dirty.xlsx) — 7,211 bytes

---

## Test it — expected result

Your profile reports 63 rows, 4 null cities, 3 null spends, 2 null order_dates and 3 duplicate rows. Two extreme outliers (99999.00 and 87500.00) are flagged at |z| > 3. The mean spend (~3348) is more than fifteen times the median (~219) — proof the outliers are distorting the mean.

## If it doesn't work

| Symptom | Fix |
|---|---|
| The CSV contains '404: Not Found' | curl wrote the error page into the file. Confirm the BASE URL, re-run with -fsSO so curl fails loudly, or copy the files from the repo folder you cloned. |
| ModuleNotFoundError: pandas | Run pip3 install pandas. On Killercoda add --break-system-packages if pip refuses. |
| The download produced an empty file | Check your internet connection and the BASE URL, or copy sales_dirty.csv from the repo folder you cloned. |
| z-score flags nothing | The spend column imported as text because of the blank cells. Wrap it in pd.to_numeric(..., errors='coerce') first, then recompute z. |

---

*© 2026 Tertiary Infotech Academy Pte Ltd. All rights reserved. · TGS-2024049212*
