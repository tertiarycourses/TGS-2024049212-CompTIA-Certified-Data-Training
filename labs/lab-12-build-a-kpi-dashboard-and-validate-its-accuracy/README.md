# Lab 12 — Build a KPI Dashboard and Validate Its Accuracy

**Domain 04 — Visualization and Reporting** (20% of the CompTIA Data+ (DA0-001) exam)  
**Maps to:** LU4 / LO4 (K3, A5)  
**Course:** WSQ - CompTIA Certified Data+ Training (TGS-2024049212)

---

## Exam objective

Deliver reports: dashboards and summaries; validate reporting accuracy (Domain 4); LO4 / K3 / A5.

## What you will do

You assemble a four-panel executive dashboard from the integrated dataset, then run the validation checks the exam requires — record-count reconciliation, recalculation and cross-validation — and deliberately plant one error so you can prove your validation process actually catches it.

## What you will produce

A four-panel KPI dashboard PNG plus a signed validation checklist that catches a planted reporting error.

## Tools

- Killercoda Ubuntu, Python 3, pandas, matplotlib
- **Environment:** https://killercoda.com/playgrounds/scenario/ubuntu

---

## Step-by-step

### Step 1

Create the lab folder and the source data for the dashboard.

```bash
mkdir -p ~/dataplus/lab12 && cd ~/dataplus/lab12 && printf 'month,region,revenue,orders,target\nJan,Central,118,42,120\nFeb,Central,131,47,120\nMar,Central,152,55,120\nJan,West,88,31,100\nFeb,West,95,34,100\nMar,West,104,38,100\nJan,North,142,50,130\nFeb,North,138,49,130\nMar,North,161,58,130\n' > kpi.csv
```

### Step 2

Compute the headline KPIs first — you must know the true numbers BEFORE you draw anything.

```bash
python3 -c "import pandas as pd;d=pd.read_csv('kpi.csv');print('total revenue',d.revenue.sum());print('total orders',d.orders.sum());print('avg order value',round(d.revenue.sum()*1000/d.orders.sum(),2));print('vs target',round(d.revenue.sum()*100/d.target.sum(),1),'%')"
```

### Step 3

Build the four-panel dashboard in one script.

```bash
cat > dashboard.py <<'EOF'
import pandas as pd, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
d = pd.read_csv('kpi.csv')
fig, ax = plt.subplots(2, 2, figsize=(12, 7))
fig.suptitle('Regional Sales Dashboard  ·  Q1', fontsize=15, fontweight='bold')
d.pivot_table(index='month', columns='region', values='revenue').reindex(['Jan','Feb','Mar']).plot(ax=ax[0][0], marker='o')
ax[0][0].set_title('Revenue Trend'); ax[0][0].set_ylabel('SGD k')
d.groupby('region').revenue.sum().plot(kind='bar', ax=ax[0][1], color='#1F6FEB')
ax[0][1].set_title('Revenue by Region')
act = d.groupby('region').revenue.sum(); tgt = d.groupby('region').target.sum()
(act/tgt*100).plot(kind='bar', ax=ax[1][0], color='#10B981')
ax[1][0].axhline(100, color='red', ls='--'); ax[1][0].set_title('% of Target')
ax[1][1].scatter(d.orders, d.revenue, c='#7C3AED', s=70)
ax[1][1].set_title('Orders vs Revenue'); ax[1][1].set_xlabel('Orders')
plt.tight_layout(rect=[0,0,1,0.95])
plt.savefig('dashboard.png', dpi=120)
print('dashboard.png written')
EOF
python3 dashboard.py
```

### Step 4

VALIDATION 1 — record count. Does the dashboard cover every source row?

```bash
python3 -c "import pandas as pd;d=pd.read_csv('kpi.csv');print('source rows',len(d));print('rows charted',d.groupby(['month','region']).ngroups)"
```

### Step 5

VALIDATION 2 — recalculate the headline total a second, independent way.

```bash
python3 -c "import pandas as pd;d=pd.read_csv('kpi.csv');a=d.revenue.sum();b=sum(d.groupby('region').revenue.sum());print('method A',a,'method B',b,'MATCH' if a==b else 'MISMATCH')"
```

### Step 6

VALIDATION 3 — cross-validate the % of target figure against a hand calculation.

```bash
python3 -c "import pandas as pd;d=pd.read_csv('kpi.csv');print('Central', round(d[d.region=='Central'].revenue.sum()/d[d.region=='Central'].target.sum()*100,1),'% expected 111.9')"
```

### Step 7

Now PLANT AN ERROR — corrupt one revenue value and rebuild the dashboard.

```bash
sed -i 's/Mar,North,161/Mar,North,1610/' kpi.csv && python3 dashboard.py
```

### Step 8

Re-run validation 2 and 3 and confirm your checks CATCH the planted error.

```bash
python3 -c "import pandas as pd;d=pd.read_csv('kpi.csv');print('total now',d.revenue.sum(),'(was 1129)');print('North % of target',round(d[d.region=='North'].revenue.sum()/d[d.region=='North'].target.sum()*100,1),'%')"
```

### Step 9

Restore the correct value and confirm the dashboard returns to its validated state.

```bash
sed -i 's/Mar,North,1610/Mar,North,161/' kpi.csv && python3 dashboard.py && python3 -c "import pandas as pd;print('total',pd.read_csv('kpi.csv').revenue.sum())"
```

### Step 10

Sign off the validation checklist: record count, recalculation, cross-validation, and visual review.

---

## Test it — expected result

dashboard.png shows four panels. Total revenue validates at 1129 by two independent methods. After the planted error the total jumps to 2578 and North shows 483% of target — an impossible figure your validation flags immediately.

## If it doesn't work

| Symptom | Fix |
|---|---|
| Panels overlap or the title is cut | Use plt.tight_layout(rect=[0,0,1,0.95]) so the suptitle gets its own space. |
| sed did not change anything | Check the exact text with grep 'Mar,North' kpi.csv — sed needs a byte-exact match. |
| The % of target axis looks wrong | Confirm you summed target per region (3 months × the monthly target), not just one month's value. |

---

*© 2026 Tertiary Infotech Academy Pte Ltd. All rights reserved. · TGS-2024049212*
