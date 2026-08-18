# Lab 2 — Compare Structured, Semi-Structured and Unstructured Data

**Domain 01 — Data Concepts and Environments** (20% of the CompTIA Data+ (DA0-001) exam)  
**Maps to:** LU1 / LO1 (K4, A1)  
**Course:** WSQ - CompTIA Certified Data+ Training (TGS-2024049212)

---

## Exam objective

Explain data concepts: data structures, file extensions and data types; identify data sources (Domain 1); LO1 / K4.

## What you will do

You create the same customer record three ways — as a CSV row, as a JSON document and as free text — then measure how much work each format takes to query. This is the exam's structured vs semi-structured vs unstructured distinction, made concrete.

## What you will produce

Three files (customers.csv, customers.json, notes.txt) plus a Python script that queries each and reports the effort required.

## Tools

- Killercoda Ubuntu, Python 3, csv and json modules
- **Environment:** https://killercoda.com/playgrounds/scenario/ubuntu

---

## Step-by-step

### Step 1

Create the lab folder.

```bash
mkdir -p ~/dataplus/lab2 && cd ~/dataplus/lab2
```

### Step 2

Write the STRUCTURED version — a delimited CSV with a fixed header and one record per line.

```bash
printf 'customer_id,name,city,spend\n1,Mei Tan,Singapore,240.50\n2,Ravi Kumar,Jurong,89.00\n' > customers.csv
```

### Step 3

Write the SEMI-STRUCTURED version — JSON, which is self-describing and allows nested and ragged fields.

```bash
printf '[{"customer_id":1,"name":"Mei Tan","city":"Singapore","spend":240.50,"tags":["vip","repeat"]},{"customer_id":2,"name":"Ravi Kumar","city":"Jurong","spend":89.00}]' > customers.json
```

### Step 4

Write the UNSTRUCTURED version — the same facts buried in prose, with no schema at all.

```bash
printf 'Mei Tan from Singapore spent about $240.50 with us this quarter. Ravi Kumar (Jurong) spent 89 dollars.\n' > notes.txt
```

### Step 5

Query the CSV — three lines of code, because the structure is guaranteed.

```bash
python3 -c "import csv;print(sum(float(r['spend']) for r in csv.DictReader(open('customers.csv'))))"
```

### Step 6

Query the JSON — still easy, and it carries the extra 'tags' field the CSV could not hold.

```bash
python3 -c "import json;d=json.load(open('customers.json'));print(sum(r['spend'] for r in d));print(d[0].get('tags'))"
```

### Step 7

Try to query the unstructured text — you need a regular expression, and it is fragile.

```bash
python3 -c "import re;t=open('notes.txt').read();print(re.findall(r'[$]?([0-9]+(?:[.][0-9]{2})?)\s*(?:dollars)?',t))"
```

### Step 8

Compare the file sizes and record what each format cost you in query effort.

```bash
ls -l customers.csv customers.json notes.txt
```

---

## Test it — expected result

The CSV and JSON both total 329.5. The JSON also returns ['vip','repeat'] — a field the CSV cannot represent. The regex over notes.txt returns extra noise, proving unstructured data needs parsing before analysis.

## If it doesn't work

| Symptom | Fix |
|---|---|
| JSONDecodeError | The shell ate a quote. Re-run the printf line exactly, or use nano customers.json and paste the JSON in. |
| The regex returns '240.50' and '89' plus junk | That is the expected lesson — unstructured text has no guarantees. Tighten the pattern in RegexLab. |
| KeyError: 'spend' | Your CSV header row is missing or misspelled. Run head -1 customers.csv to check it. |

---

*© 2026 Tertiary Infotech Academy Pte Ltd. All rights reserved. · TGS-2024049212*
