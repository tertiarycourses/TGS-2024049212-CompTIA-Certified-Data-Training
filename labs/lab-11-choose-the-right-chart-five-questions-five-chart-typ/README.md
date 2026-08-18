# Lab 11 — Choose the Right Chart: Five Questions, Five Chart Types

**Domain 04 — Visualization and Reporting** (20% of the CompTIA Data+ (DA0-001) exam)  
**Maps to:** LU4 / LO4 (K3, A5)  
**Course:** WSQ - CompTIA Certified Data+ Training (TGS-2024049212)

---

## Exam objective

Create effective visuals: use charts, maps, tables and design elements (Domain 4); LO4 / K3 / A5.

## What you will do

Chart choice is not decoration — it is determined by the question being asked. You take ONE dataset and answer five different business questions from it, each demanding a different chart type, then build a deliberately wrong chart so you can articulate exactly why it misleads.

## What you will produce

Five correctly chosen charts (line, bar, pie, histogram, scatter) as PNG files, plus one annotated 'wrong chart' example.

## Tools

- Killercoda Ubuntu, Python 3, pandas, matplotlib
- **Environment:** https://killercoda.com/playgrounds/scenario/ubuntu

---

## Step-by-step

### Step 1

Create the lab folder and install matplotlib.

```bash
mkdir -p ~/dataplus/lab11 && cd ~/dataplus/lab11 && pip3 install matplotlib pandas --quiet
```

### Step 2

Create the quarterly sales dataset used for every chart in this lab.

```bash
printf 'month,region,revenue,orders,unit_price\nJan,Central,118,42,12.4\nFeb,Central,131,47,12.8\nMar,Central,152,55,13.1\nJan,West,88,31,11.9\nFeb,West,95,34,12.2\nMar,West,104,38,12.0\nJan,North,142,50,13.5\nFeb,North,138,49,13.3\nMar,North,161,58,13.9\n' > sales.csv
```

### Step 3

Q1 'How is revenue trending?' → LINE CHART, because the x-axis is time.

```bash
python3 -c "import pandas as pd,matplotlib;matplotlib.use('Agg');import matplotlib.pyplot as plt;d=pd.read_csv('sales.csv');p=d.pivot_table(index='month',columns='region',values='revenue').reindex(['Jan','Feb','Mar']);p.plot(marker='o');plt.title('Revenue Trend by Region');plt.ylabel('Revenue (SGD k)');plt.tight_layout();plt.savefig('01_line.png',dpi=120)"
```

### Step 4

Q2 'Which region sells most?' → BAR CHART, because you are comparing categories.

```bash
python3 -c "import pandas as pd,matplotlib;matplotlib.use('Agg');import matplotlib.pyplot as plt;d=pd.read_csv('sales.csv');d.groupby('region').revenue.sum().sort_values().plot(kind='barh',color='#1F6FEB');plt.title('Total Revenue by Region');plt.xlabel('Revenue (SGD k)');plt.tight_layout();plt.savefig('02_bar.png',dpi=120)"
```

### Step 5

Q3 'What share does each region hold?' → PIE CHART, because it is parts of one whole (and only 3 slices).

```bash
python3 -c "import pandas as pd,matplotlib;matplotlib.use('Agg');import matplotlib.pyplot as plt;d=pd.read_csv('sales.csv');d.groupby('region').revenue.sum().plot(kind='pie',autopct='%1.1f%%',colors=['#1F6FEB','#10B981','#7C3AED']);plt.title('Revenue Share by Region');plt.ylabel('');plt.tight_layout();plt.savefig('03_pie.png',dpi=120)"
```

### Step 6

Q4 'How are order sizes distributed?' → HISTOGRAM, because you want the shape of one variable.

```bash
python3 -c "import pandas as pd,matplotlib;matplotlib.use('Agg');import matplotlib.pyplot as plt;d=pd.read_csv('sales.csv');d.orders.plot(kind='hist',bins=5,color='#F59E0B',edgecolor='white');plt.title('Distribution of Order Counts');plt.xlabel('Orders per region-month');plt.tight_layout();plt.savefig('04_hist.png',dpi=120)"
```

### Step 7

Q5 'Do more orders mean higher revenue?' → SCATTER PLOT, because you are testing a relationship.

```bash
python3 -c "import pandas as pd,matplotlib;matplotlib.use('Agg');import matplotlib.pyplot as plt;d=pd.read_csv('sales.csv');plt.scatter(d.orders,d.revenue,c='#7C3AED',s=80);plt.title('Orders vs Revenue');plt.xlabel('Orders');plt.ylabel('Revenue (SGD k)');plt.tight_layout();plt.savefig('05_scatter.png',dpi=120)"
```

### Step 8

Now build the WRONG chart on purpose — a pie chart of a time series, which destroys the time ordering.

```bash
python3 -c "import pandas as pd,matplotlib;matplotlib.use('Agg');import matplotlib.pyplot as plt;d=pd.read_csv('sales.csv');d.groupby('month').revenue.sum().plot(kind='pie',autopct='%1.1f%%');plt.title('WRONG: revenue by month as a pie');plt.ylabel('');plt.tight_layout();plt.savefig('06_wrong.png',dpi=120)"
```

### Step 9

List the generated files and write one line per chart stating the question it answers.

```bash
ls -1 *.png
```

### Step 10

Write the critique of 06_wrong.png: what does a pie chart hide that a line chart shows?

---

## Test it — expected result

Six PNG files exist. Each of the five correct charts answers its stated question, and your critique of the wrong chart explains that a pie destroys the sequence and makes a trend impossible to read.

## If it doesn't work

| Symptom | Fix |
|---|---|
| No display / tkinter error | You must set matplotlib.use('Agg') BEFORE importing pyplot — headless terminals have no display. |
| The PNG is blank | You saved after calling plt.show() or a new figure. Call plt.savefig() before any clf/show, and use plt.close() between charts. |
| Months are out of order | Alphabetical sorting puts Feb first. The .reindex(['Jan','Feb','Mar']) call is what fixes it. |

---

*© 2026 Tertiary Infotech Academy Pte Ltd. All rights reserved. · TGS-2024049212*
