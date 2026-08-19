# Lab 1 — Build a Relational Schema and Prove Referential Integrity

**Domain 01 — Data Concepts and Environments** (20% of the CompTIA Data+ (DA0-001) exam)  
**Maps to:** LU1 / LO1 (K4, A1)  
**Course:** WSQ - CompTIA Certified Data+ Training (TGS-2024049212)

---

## Exam objective

Explain data concepts: database types, data structures and data types (Domain 1); LO1 / K4 / A1.

## What you will do

You design and build a small three-table sales schema in SQLite, declare the primary and foreign keys, and then deliberately attack it with an orphan record and a cascading delete so you can see referential integrity doing its job.

## What you will produce

A normalised 3NF SQLite database (customers, products, orders) with enforced foreign keys, plus evidence of a rejected orphan insert.

## Tools

- Killercoda Ubuntu, SQLite 3, SQL DDL/DML
- **Environment:** https://killercoda.com/playgrounds/scenario/ubuntu

---

## Step-by-step

### Step 1

Create the working folder and download this lab's dataset. The files also ship in the course repo under labs/lab-01-build-a-relational-schema-and-prove-referential-inte/data/ — download them from GitHub or copy them from the folder you cloned.

```bash
mkdir -p ~/dataplus/lab1 && cd ~/dataplus/lab1 && BASE=https://raw.githubusercontent.com/tertiarycourses/TGS-2024049212-CompTIA-Certified-Data-Training/main/labs/lab-01-build-a-relational-schema-and-prove-referential-inte/data && for f in customers.csv products.csv orders.csv; do curl -fsSO $BASE/$f || echo FAILED $f; done && ls -l
```

### Step 2

Turn foreign-key enforcement ON — SQLite leaves it off by default, which is the single most common cause of orphaned rows.

```bash
PRAGMA foreign_keys = ON;
```

### Step 3

Create the customers table with a primary key and typed columns (INTEGER, TEXT, DATE).

```bash
CREATE TABLE customers (customer_id INTEGER PRIMARY KEY, first_name TEXT NOT NULL, last_name TEXT NOT NULL, email TEXT UNIQUE, joined DATE);
```

### Step 4

Create the products table — note REAL for currency and the CHECK constraint enforcing domain integrity.

```bash
CREATE TABLE products (product_id INTEGER PRIMARY KEY, name TEXT NOT NULL, unit_price REAL CHECK (unit_price >= 0));
```

### Step 5

Create the orders fact table carrying TWO foreign keys with ON DELETE CASCADE.

```bash
CREATE TABLE orders (order_id INTEGER PRIMARY KEY, customer_id INTEGER REFERENCES customers(customer_id) ON DELETE CASCADE, product_id INTEGER REFERENCES products(product_id), qty INTEGER NOT NULL, order_date DATE);
```

### Step 6

Import the three CSV extracts into the tables you just created.

```bash
sqlite3 sales.db ".mode csv" ".import --skip 1 customers.csv customers" ".import --skip 1 products.csv products" ".import --skip 1 orders.csv orders" "SELECT COUNT(*) FROM customers; SELECT COUNT(*) FROM products; SELECT COUNT(*) FROM orders;"
```

### Step 7

Insert the product rows.

```bash
INSERT INTO products VALUES (10,'Wireless Mouse',24.90),(11,'USB-C Hub',59.00);
```

### Step 8

Insert valid orders that respect both foreign keys.

```bash
INSERT INTO orders VALUES (100,1,10,2,'2025-03-01'),(101,2,11,1,'2025-03-02');
```

### Step 9

ATTACK 1 — try to insert an order for a customer who does not exist. This MUST be rejected.

```bash
INSERT INTO orders VALUES (102,999,10,1,'2025-03-03');
```

### Step 10

ATTACK 2 — delete customer 1 and watch the cascade remove their orders, leaving nothing orphaned.

```bash
DELETE FROM customers WHERE customer_id = 1; SELECT * FROM orders;
```

### Step 11

Run a join across all three tables to confirm the schema answers a real business question.

```bash
SELECT c.first_name, p.name, o.qty, o.qty*p.unit_price AS line_total FROM orders o JOIN customers c ON c.customer_id=o.customer_id JOIN products p ON p.product_id=o.product_id;
```

---

## Dataset

This lab ships with its own data — you do not have to type it in. See [`data/README.md`](data/README.md) for what each file contains and which defects are planted in it.

- [`data/customers.csv`](data/customers.csv) — 2,282 bytes
- [`data/orders.csv`](data/orders.csv) — 2,904 bytes
- [`data/products.csv`](data/products.csv) — 282 bytes
- [`data/sales-schema.xlsx`](data/sales-schema.xlsx) — 11,436 bytes

---

## Test it — expected result

The three tables import 40 customers, 10 products and 120 orders. Attack 1 fails with 'FOREIGN KEY constraint failed'. Attack 2 deletes customer 1 AND cascades to their 2 orders, so the order count drops from 120 to 118. The final join returns 118 priced order lines.

## If it doesn't work

| Symptom | Fix |
|---|---|
| The CSV contains '404: Not Found' | curl wrote the error page into the file. Confirm the BASE URL, re-run with -fsSO so curl fails loudly, or copy the files from the repo folder you cloned. |
| The orphan insert SUCCEEDED | You forgot PRAGMA foreign_keys = ON. It resets on every new connection — re-run it after reopening sqlite3. |
| 'no such table' error | You are in a different database file. Run .databases inside sqlite3 to confirm you opened sales.db. |
| The cascade did not fire | ON DELETE CASCADE only works with foreign keys enforced. Re-check the PRAGMA, then re-create the orders table. |

---

*© 2026 Tertiary Infotech Academy Pte Ltd. All rights reserved. · TGS-2024049212*
