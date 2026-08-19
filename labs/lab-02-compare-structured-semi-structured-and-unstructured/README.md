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

Download this lab's dataset. The same files ship in the course repo under this lab's data/ folder.

```bash
mkdir -p ~/dataplus/lab2 && cd ~/dataplus/lab2;
R=https://raw.githubusercontent.com/tertiarycourses;
B=$R/TGS-2024049212-CompTIA-Certified-Data-Training/main/labs;
D=lab-02-compare-structured-semi-structured-and-unstructured;
for f in customers.csv customers.json notes.txt; do curl -fsSO $B/$D/data/$f || echo FAILED $f; done; ls -l
```

### Step 2

Query the CSV — three lines of code, because the structure is guaranteed.

```bash
python3 -c "import csv;print(sum(float(r['spend']) for r in csv.DictReader(open('customers.csv'))))"
```

### Step 3

Query the JSON — still easy, and it carries the extra 'tags' field the CSV could not hold.

```bash
python3 -c "import json;d=json.load(open('customers.json'));print(sum(r['spend'] for r in d));print(d[0].get('tags'))"
```

### Step 4

Try to query the unstructured text — you need a regular expression, and it is fragile.

```bash
python3 -c "import re;t=open('notes.txt').read();print(re.findall(r'[$]?([0-9]+(?:[.][0-9]{2})?)\s*(?:dollars)?',t))"
```

### Step 5

Compare the file sizes and record what each format cost you in query effort.

```bash
ls -l customers.csv customers.json notes.txt
```

---

## Dataset

This lab ships with its own data — you do not have to type it in. See [`data/README.md`](data/README.md) for what each file contains and which defects are planted in it.

- [`data/customers.csv`](data/customers.csv) — 392 bytes
- [`data/customers.json`](data/customers.json) — 1,452 bytes
- [`data/notes.txt`](data/notes.txt) — 915 bytes

---

## Test it — expected result

The CSV and the JSON both total 2293.17 across 12 customers. The JSON also returns ['vip','repeat'] for the first record — a field the flat CSV cannot represent at all. The regex over notes.txt returns extra noise, proving unstructured text needs parsing before it can be analysed.

## If it doesn't work

| Symptom | Fix |
|---|---|
| The CSV contains '404: Not Found' | curl wrote the error page into the file. Confirm the BASE URL, re-run with -fsSO so curl fails loudly, or copy the files from the repo folder you cloned. |
| JSONDecodeError | customers.json did not download cleanly. Check it with head -c 80 customers.json — if it starts with '404' the URL is wrong. |
| The regex returns '240.50' and '89' plus junk | That is the expected lesson — unstructured text has no guarantees. Tighten the pattern in RegexLab. |
| KeyError: 'spend' | Your CSV header row is missing or misspelled. Run head -1 customers.csv to check it. |

---

*© 2026 Tertiary Infotech Academy Pte Ltd. All rights reserved. · TGS-2024049212*
