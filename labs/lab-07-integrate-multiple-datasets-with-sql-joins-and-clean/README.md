# Lab 7 — Integrate Multiple Datasets with SQL Joins and Cleanse the Result

**Domain 02 — Data Acquisition and Preparation** (22% of the CompTIA Data+ (DA0-001) exam)  
**Maps to:** LU2 / LO2 (K1, A2)  
**Course:** WSQ - CompTIA Certified Data+ Training (TGS-2024049212)

---

## Exam objective

Use data acquisition methods: data integration and queries to gather and combine data (Domain 2); LO2 / A1 / A2.

## What you will do

This is the integration lab that LO1 and LO2 both rest on. You load three separate source extracts into SQLite, combine them with the four join types, watch how inner versus left join silently changes your record count, and then cleanse the merged result.

## What you will produce

A single integrated, deduplicated analysis table built from three sources, with the record count reconciled at every join.

## Tools

- Killercoda Ubuntu, SQLite 3, SQL joins, Python 3/pandas
- **Environment:** https://killercoda.com/playgrounds/scenario/ubuntu

---

## Step-by-step

### Step 1

Create the working folder and download this lab's dataset. The files also ship in the course repo under labs/lab-07-integrate-multiple-datasets-with-sql-joins-and-clean/data/ — download them from GitHub or copy them from the folder you cloned.

```bash
mkdir -p ~/dataplus/lab7 && cd ~/dataplus/lab7 && BASE=https://raw.githubusercontent.com/tertiarycourses/TGS-2024049212-CompTIA-Certified-Data-Training/main/labs/lab-07-integrate-multiple-datasets-with-sql-joins-and-clean/data && for f in customers.csv orders.csv targets.csv; do curl -fsSO $BASE/$f || echo FAILED $f; done && ls -l
```

### Step 2

Load all three into SQLite in one go.

```bash
sqlite3 integrate.db <<'EOF'
.mode csv
.import customers.csv customers
.import orders.csv orders
.import targets.csv targets
.headers on
SELECT COUNT(*) AS customers FROM customers; SELECT COUNT(*) AS orders FROM orders;
EOF
```

### Step 3

INNER JOIN — returns only matched rows. Count them and note what you silently lost.

```bash
sqlite3 -header -column integrate.db "SELECT COUNT(*) AS inner_rows FROM orders o JOIN customers c ON c.customer_id=o.customer_id;"
```

### Step 4

LEFT JOIN from orders — keeps order 104 whose customer is missing, showing NULL in the master fields.

```bash
sqlite3 -header -column integrate.db "SELECT o.order_id, o.customer_id, c.name FROM orders o LEFT JOIN customers c ON c.customer_id=o.customer_id;"
```

### Step 5

LEFT JOIN from customers — keeps John Lee, who has no orders at all.

```bash
sqlite3 -header -column integrate.db "SELECT c.name, o.order_id FROM customers c LEFT JOIN orders o ON c.customer_id=o.customer_id;"
```

### Step 6

Build the integrated analysis table joining all three sources and aggregating per region.

```bash
sqlite3 -header -column integrate.db "SELECT c.region, COUNT(o.order_id) AS orders, ROUND(SUM(o.amount),2) AS revenue, t.target FROM customers c LEFT JOIN orders o ON c.customer_id=o.customer_id JOIN targets t ON t.region=c.region GROUP BY c.region, t.target;"
```

### Step 7

Add the derived performance measure and persist the result.

```bash
sqlite3 -header -column integrate.db "CREATE TABLE regional AS SELECT c.region, COUNT(o.order_id) AS orders, COALESCE(SUM(o.amount),0) AS revenue, t.target, ROUND(COALESCE(SUM(o.amount),0)*100.0/t.target,1) AS pct_of_target FROM customers c LEFT JOIN orders o ON c.customer_id=o.customer_id JOIN targets t ON t.region=c.region GROUP BY c.region,t.target; SELECT * FROM regional;"
```

### Step 8

Reconcile: explain in one line why the inner join returned 4 rows but there are 5 orders.

---

## Dataset

This lab ships with its own data — you do not have to type it in. See [`data/README.md`](data/README.md) for what each file contains and which defects are planted in it.

- [`data/customers.csv`](data/customers.csv) — 683 bytes
- [`data/integration-sources.xlsx`](data/integration-sources.xlsx) — 8,642 bytes
- [`data/orders.csv`](data/orders.csv) — 1,203 bytes
- [`data/targets.csv`](data/targets.csv) — 63 bytes

---

## Test it — expected result

The sources hold 31 customers and 81 orders. The INNER JOIN returns only 80 rows — order 999 is dropped because customer 77 has no master record. Four customers have no orders at all and survive only via the LEFT JOIN. The regional table reports every region's revenue against its target.

## If it doesn't work

| Symptom | Fix |
|---|---|
| The CSV contains '404: Not Found' | curl wrote the error page into the file. Confirm the BASE URL, re-run with -fsSO so curl fails loudly, or copy the files from the repo folder you cloned. |
| '.import' left the header as a data row | Older SQLite lacks --skip 1. Delete it after import: DELETE FROM customers WHERE customer_id='customer_id'; |
| SUM returns NULL for East | That is correct SQL — no rows to sum. COALESCE(...,0) is what turns it into a reportable zero. |
| Amounts sort wrongly | CSV import types everything as TEXT. Use CAST(amount AS REAL) or create the table with explicit types first. |

---

*© 2026 Tertiary Infotech Academy Pte Ltd. All rights reserved. · TGS-2024049212*
