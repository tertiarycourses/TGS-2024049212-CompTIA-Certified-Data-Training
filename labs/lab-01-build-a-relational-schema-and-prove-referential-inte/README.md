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

Open the Killercoda Ubuntu playground in your browser and confirm SQLite is available.

```bash
sqlite3 --version
```

### Step 2

Create the lab folder and open a new database file.

```bash
mkdir -p ~/dataplus/lab1 && cd ~/dataplus/lab1 && sqlite3 sales.db
```

### Step 3

Turn foreign-key enforcement ON — SQLite leaves it off by default, which is the single most common cause of orphaned rows.

```bash
PRAGMA foreign_keys = ON;
```

### Step 4

Create the customers table with a primary key and typed columns (INTEGER, TEXT, DATE).

```bash
CREATE TABLE customers (customer_id INTEGER PRIMARY KEY, first_name TEXT NOT NULL, last_name TEXT NOT NULL, email TEXT UNIQUE, joined DATE);
```

### Step 5

Create the products table — note REAL for currency and the CHECK constraint enforcing domain integrity.

```bash
CREATE TABLE products (product_id INTEGER PRIMARY KEY, name TEXT NOT NULL, unit_price REAL CHECK (unit_price >= 0));
```

### Step 6

Create the orders fact table carrying TWO foreign keys with ON DELETE CASCADE.

```bash
CREATE TABLE orders (order_id INTEGER PRIMARY KEY, customer_id INTEGER REFERENCES customers(customer_id) ON DELETE CASCADE, product_id INTEGER REFERENCES products(product_id), qty INTEGER NOT NULL, order_date DATE);
```

### Step 7

Insert reference data into the two dimension tables.

```bash
INSERT INTO customers VALUES (1,'Mei','Tan','mei.tan@example.sg','2025-01-14'),(2,'Ravi','Kumar','ravi.k@example.sg','2025-02-03');
```

### Step 8

Insert the product rows.

```bash
INSERT INTO products VALUES (10,'Wireless Mouse',24.90),(11,'USB-C Hub',59.00);
```

### Step 9

Insert valid orders that respect both foreign keys.

```bash
INSERT INTO orders VALUES (100,1,10,2,'2025-03-01'),(101,2,11,1,'2025-03-02');
```

### Step 10

ATTACK 1 — try to insert an order for a customer who does not exist. This MUST be rejected.

```bash
INSERT INTO orders VALUES (102,999,10,1,'2025-03-03');
```

### Step 11

ATTACK 2 — delete customer 1 and watch the cascade remove their orders, leaving nothing orphaned.

```bash
DELETE FROM customers WHERE customer_id = 1; SELECT * FROM orders;
```

### Step 12

Run a join across all three tables to confirm the schema answers a real business question.

```bash
SELECT c.first_name, p.name, o.qty, o.qty*p.unit_price AS line_total FROM orders o JOIN customers c ON c.customer_id=o.customer_id JOIN products p ON p.product_id=o.product_id;
```

---

## Test it — expected result

Attack 1 fails with 'FOREIGN KEY constraint failed' and attack 2 removes order 100 automatically. The final join returns one row (Ravi · USB-C Hub · 1 · 59.0).

## If it doesn't work

| Symptom | Fix |
|---|---|
| The orphan insert SUCCEEDED | You forgot PRAGMA foreign_keys = ON. It resets on every new connection — re-run it after reopening sqlite3. |
| 'no such table' error | You are in a different database file. Run .databases inside sqlite3 to confirm you opened sales.db. |
| The cascade did not fire | ON DELETE CASCADE only works with foreign keys enforced. Re-check the PRAGMA, then re-create the orders table. |

---

*© 2026 Tertiary Infotech Academy Pte Ltd. All rights reserved. · TGS-2024049212*
