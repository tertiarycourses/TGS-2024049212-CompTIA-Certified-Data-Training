# Lab 5 — Build Parsing Patterns in RegexLab and Apply Them

**Domain 02 — Data Acquisition and Preparation** (22% of the CompTIA Data+ (DA0-001) exam)  
**Maps to:** LU2 / LO2 (K1, A2)  
**Course:** WSQ - CompTIA Certified Data+ Training (TGS-2024049212)

---

## Exam objective

Apply data transformation: cleansing, parsing and formatting data (Domain 2); LO2 / K1.

## What you will do

Real source fields arrive as one messy string — 'Mei Tan <mei.tan@example.sg> +65 9123 4567'. You use RegexLab to build and validate the extraction patterns interactively, then apply the proven patterns in pandas to split one dirty column into three clean, typed fields.

## What you will produce

Three validated regex patterns (name, email, phone) and a cleaned CSV with the single contact column parsed into three columns.

## Tools

- RegexLab (https://alfredang.github.io/regexgenerator/), Killercoda Ubuntu, Python 3, pandas
- **Environment:** https://alfredang.github.io/regexgenerator/

---

## Step-by-step

### Step 1

Create the working folder and download this lab's dataset. The files also ship in the course repo under labs/lab-05-build-parsing-patterns-in-regexlab-and-apply-them/data/ — download them from GitHub or copy them from the folder you cloned.

```bash
mkdir -p ~/dataplus/lab5 && cd ~/dataplus/lab5 && BASE=https://raw.githubusercontent.com/tertiarycourses/TGS-2024049212-CompTIA-Certified-Data-Training/main/labs/lab-05-build-parsing-patterns-in-regexlab-and-apply-them/data && for f in contacts.csv; do curl -fsSO $BASE/$f || echo FAILED $f; done && ls -l
```

### Step 2

Paste these three messy contact records into the Test String box:  Mei Tan <mei.tan@example.sg> +65 9123 4567

### Step 3

Build the EMAIL pattern and watch the match count update live. Confirm it matches all three records.

```bash
[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}
```

### Step 4

Build the SINGAPORE PHONE pattern — 8 digits starting 6, 8 or 9, with optional +65 and spaces.

```bash
(?:\+65[ ]?)?[689][0-9]{3}[ ]?[0-9]{4}
```

### Step 5

Build the NAME pattern — everything before the first angle bracket, trimmed.

```bash
^([A-Za-z ]+?)\s*<
```

### Step 6

Use the Substitution panel to confirm your pattern replaces cleanly before you trust it in code.

### Step 7

Apply the SAME patterns you validated in RegexLab, using pandas str.extract.

```bash
python3 -c "import pandas as pd;d=pd.read_csv('contacts.csv');d['name']=d.contact.str.extract(r'^([A-Za-z ]+?)\s*<');d['email']=d.contact.str.extract(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})');d['phone']=d.contact.str.extract(r'((?:\+65 ?)?[689][0-9]{3} ?[0-9]{4})');print(d[['id','name','email','phone']])"
```

### Step 8

Normalise the phone format — strip +65 and spaces so every value has the same shape.

```bash
python3 -c "import pandas as pd,re;d=pd.read_csv('contacts.csv');d['phone']=d.contact.str.extract(r'((?:\+65 ?)?[689][0-9]{3} ?[0-9]{4})')[0].str.replace(r'[^0-9]','',regex=True).str[-8:];print(d[['id','phone']])"
```

### Step 9

Save the cleaned, parsed output.

```bash
python3 -c "import pandas as pd;d=pd.read_csv('contacts.csv');d['name']=d.contact.str.extract(r'^([A-Za-z ]+?)\s*<');d['email']=d.contact.str.extract(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})');d['phone']=d.contact.str.extract(r'((?:\+65 ?)?[689][0-9]{3} ?[0-9]{4})')[0].str.replace(r'[^0-9]','',regex=True).str[-8:];d[['id','name','email','phone']].to_csv('contacts_clean.csv',index=False)" && cat contacts_clean.csv
```

---

## Dataset

This lab ships with its own data — you do not have to type it in. See [`data/README.md`](data/README.md) for what each file contains and which defects are planted in it.

- [`data/contacts.csv`](data/contacts.csv) — 1,555 bytes

---

## Test it — expected result

contacts_clean.csv holds 30 rows, each with a name, an email and a normalised 8-digit phone. All 30 rows match all three patterns — no NaN in any column, no angle brackets, no +65 prefixes and no leftover spaces.

## If it doesn't work

| Symptom | Fix |
|---|---|
| The CSV contains '404: Not Found' | curl wrote the error page into the file. Confirm the BASE URL, re-run with -fsSO so curl fails loudly, or copy the files from the repo folder you cloned. |
| RegexLab shows 0 matches | Check the flags — you usually want 'g' (global) so every record is matched, not just the first. |
| extract returns NaN | pandas needs a capturing group. Confirm your pattern has parentheses around the part you want. |
| The phone keeps its +65 | The .str.replace step is what strips it. Confirm regex=True is set, then take the last 8 characters. |

---

*© 2026 Tertiary Infotech Academy Pte Ltd. All rights reserved. · TGS-2024049212*
