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

Create the lab folder and the three source extracts.

```bash
mkdir -p ~/dataplus/lab7 && cd ~/dataplus/lab7
```

### Step 2

Source A — the customer master (note: customer 4 appears here only).

```bash
printf 'customer_id,name,region\n1,Mei Tan,Central\n2,Ravi Kumar,West\n3,Siti Nur,North\n4,John Lee,East\n' > customers.csv
```

### Step 3

Source B — the order transactions (note: customer 4 has no orders; customer 5 has orders but no master record).

```bash
printf 'order_id,customer_id,amount\n100,1,240.50\n101,2,89.00\n102,1,120.00\n103,3,310.00\n104,5,55.00\n' > orders.csv
```

### Step 4

Source C — the regional targets used to enrich the result.

```bash
printf 'region,target\nCentral,500\nWest,300\nNorth,400\nEast,200\n' > targets.csv
```

### Step 5

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

### Step 6

INNER JOIN — returns only matched rows. Count them and note what you silently lost.

```bash
sqlite3 -header -column integrate.db "SELECT COUNT(*) AS inner_rows FROM orders o JOIN customers c ON c.customer_id=o.customer_id;"
```

### Step 7

LEFT JOIN from orders — keeps order 104 whose customer is missing, showing NULL in the master fields.

```bash
sqlite3 -header -column integrate.db "SELECT o.order_id, o.customer_id, c.name FROM orders o LEFT JOIN customers c ON c.customer_id=o.customer_id;"
```

### Step 8

LEFT JOIN from customers — keeps John Lee, who has no orders at all.

```bash
sqlite3 -header -column integrate.db "SELECT c.name, o.order_id FROM customers c LEFT JOIN orders o ON c.customer_id=o.customer_id;"
```

### Step 9

Build the integrated analysis table joining all three sources and aggregating per region.

```bash
sqlite3 -header -column integrate.db "SELECT c.region, COUNT(o.order_id) AS orders, ROUND(SUM(o.amount),2) AS revenue, t.target FROM customers c LEFT JOIN orders o ON c.customer_id=o.customer_id JOIN targets t ON t.region=c.region GROUP BY c.region, t.target;"
```

### Step 10

Add the derived performance measure and persist the result.

```bash
sqlite3 -header -column integrate.db "CREATE TABLE regional AS SELECT c.region, COUNT(o.order_id) AS orders, COALESCE(SUM(o.amount),0) AS revenue, t.target, ROUND(COALESCE(SUM(o.amount),0)*100.0/t.target,1) AS pct_of_target FROM customers c LEFT JOIN orders o ON c.customer_id=o.customer_id JOIN targets t ON t.region=c.region GROUP BY c.region,t.target; SELECT * FROM regional;"
```

### Step 11

Reconcile: explain in one line why the inner join returned 4 rows but there are 5 orders.

---

## Test it — expected result

The inner join returns 4 rows, not 5 — order 104 is dropped because customer 5 has no master record. The regional table shows East at 0% of target (John Lee ordered nothing) and Central above 70%.

## If it doesn't work

| Symptom | Fix |
|---|---|
| '.import' left the header as a data row | Older SQLite lacks --skip 1. Delete it after import: DELETE FROM customers WHERE customer_id='customer_id'; |
| SUM returns NULL for East | That is correct SQL — no rows to sum. COALESCE(...,0) is what turns it into a reportable zero. |
| Amounts sort wrongly | CSV import types everything as TEXT. Use CAST(amount AS REAL) or create the table with explicit types first. |

---

*© 2026 Tertiary Infotech Academy Pte Ltd. All rights reserved. · TGS-2024049212*
