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

Create the lab folder and install pandas if it is not already present.

```bash
mkdir -p ~/dataplus/lab4 && cd ~/dataplus/lab4 && pip3 install pandas --quiet
```

### Step 2

Create the dirty dataset — note the blank cells, the repeated row, and the 99999 spend.

```bash
cat > sales_dirty.csv <<'EOF'
order_id,customer,city,spend,order_date
1,Mei Tan,Singapore,240.50,2025-03-01
2,Ravi Kumar,Jurong,89.00,2025-03-02
3,Siti Nur,,145.25,2025-03-02
4,Mei Tan,Singapore,240.50,2025-03-01
5,John Lee,Tampines,,2025-03-04
6,Wei Ming,Bedok,99999.00,2025-03-05
7,Siti Nur,Woodlands,310.00,
EOF
```

### Step 3

Load it and look at the shape and dtypes first — always know how many records you started with.

```bash
python3 -c "import pandas as pd;d=pd.read_csv('sales_dirty.csv');print(d.shape);print(d.dtypes)"
```

### Step 4

Count MISSING VALUES per column — the exam's first exploration task.

```bash
python3 -c "import pandas as pd;d=pd.read_csv('sales_dirty.csv');print(d.isnull().sum())"
```

### Step 5

Count DUPLICATE rows and show which ones they are.

```bash
python3 -c "import pandas as pd;d=pd.read_csv('sales_dirty.csv');print('dupes:',d.duplicated().sum());print(d[d.duplicated(keep=False)])"
```

### Step 6

Detect OUTLIERS with a z-score — any |z| above 3 is the standard flag.

```bash
python3 -c "import pandas as pd;d=pd.read_csv('sales_dirty.csv');s=d['spend'].dropna();z=(s-s.mean())/s.std();print(d.loc[z[abs(z)>1.5].index])"
```

### Step 7

Get the descriptive summary and note how badly the 99999 distorts the mean versus the median.

```bash
python3 -c "import pandas as pd;d=pd.read_csv('sales_dirty.csv');print(d['spend'].describe());print('median',d['spend'].median())"
```

### Step 8

Write the profile report to a file so the cleaning lab can be measured against it.

```bash
python3 -c "import pandas as pd;d=pd.read_csv('sales_dirty.csv');open('profile.txt','w').write(str(d.isnull().sum())+'\ndupes: '+str(d.duplicated().sum())+'\nmean: '+str(d.spend.mean())+'\nmedian: '+str(d.spend.median()))" && cat profile.txt
```

---

## Test it — expected result

Your profile reports 7 rows, 1 null city, 1 null spend, 1 null order_date, 1 duplicate row, and one extreme outlier (99999.00). The mean spend (~16720) is wildly above the median (~240.50) — proof the outlier is distorting it.

## If it doesn't work

| Symptom | Fix |
|---|---|
| ModuleNotFoundError: pandas | Run pip3 install pandas. On Killercoda add --break-system-packages if pip refuses. |
| The heredoc pasted as one line | Paste the cat > ... <<'EOF' block line by line, or use nano sales_dirty.csv instead. |
| z-score flags nothing | With only 6 values the standard deviation is huge. That is why the lab uses a 1.5 threshold — explain this effect in your report. |

---

*© 2026 Tertiary Infotech Academy Pte Ltd. All rights reserved. · TGS-2024049212*
