# Lab 13 — Classify, Mask and De-Identify a Dataset (PDPA/GDPR)

**Domain 05 — Data Governance, Quality and Controls** (14% of the CompTIA Data+ (DA0-001) exam)  
**Maps to:** LU5 / LO5 (A4)  
**Course:** WSQ - CompTIA Certified Data+ Training (TGS-2024049212)

---

## Exam objective

Compare privacy and protection strategies: access control, encryption and masking (Domain 5); LO5 / A4.

## What you will do

You receive a customer extract containing NRIC numbers, emails and salaries. You classify every column by sensitivity, then apply the three protection techniques the exam distinguishes — masking, de-identification and pseudonymisation via a surrogate index field — and prove the analytical value survives the treatment.

## What you will produce

A classification matrix for every column plus three protected versions of the dataset (masked, de-identified, pseudonymised) with the analysis still working.

## Tools

- Killercoda Ubuntu, Python 3, pandas, hashlib
- **Environment:** https://killercoda.com/playgrounds/scenario/ubuntu

---

## Step-by-step

### Step 1

Create the working folder and download this lab's dataset. The files also ship in the course repo under labs/lab-13-classify-mask-and-de-identify-a-dataset-pdpa-gdpr/data/ — download them from GitHub or copy them from the folder you cloned.

```bash
mkdir -p ~/dataplus/lab13 && cd ~/dataplus/lab13 && BASE=https://raw.githubusercontent.com/tertiarycourses/TGS-2024049212-CompTIA-Certified-Data-Training/main/labs/lab-13-classify-mask-and-de-identify-a-dataset-pdpa-gdpr/data && for f in customers.csv; do curl -fsSO $BASE/$f || echo FAILED $f; done && ls -l
```

### Step 2

CLASSIFY first. For each column write down its classification (public / internal / sensitive / confidential) and its data type tag (PII, PIFI, none). NRIC is confidential PII; salary is sensitive PIFI; dept is internal.

### Step 3

Apply MASKING — the value stays partly visible so it can still be recognised by an authorised human.

```bash
python3 -c "import pandas as pd;d=pd.read_csv('customers.csv');d['nric']=d.nric.str[0]+'****'+d.nric.str[-1];d['email']=d.email.str.replace(r'(.).*(@.*)',r'\1****\2',regex=True);print(d[['cust_id','name','nric','email']])"
```

### Step 4

Apply DE-IDENTIFICATION — the identifying columns are removed outright.

```bash
python3 -c "import pandas as pd;d=pd.read_csv('customers.csv');deid=d.drop(columns=['name','nric','email']);print(deid)"
```

### Step 5

Apply PSEUDONYMISATION — replace the identifier with a non-reversible surrogate INDEX FIELD.

```bash
python3 -c "import pandas as pd,hashlib;d=pd.read_csv('customers.csv');d['subject_key']=d.nric.map(lambda v: hashlib.sha256(v.encode()).hexdigest()[:12]);print(d[['cust_id','subject_key','dept','salary']])"
```

### Step 6

Prove the ANALYSIS STILL WORKS on the protected data — this is the whole point of the technique.

```bash
python3 -c "import pandas as pd,hashlib;d=pd.read_csv('customers.csv');d['subject_key']=d.nric.map(lambda v: hashlib.sha256(v.encode()).hexdigest()[:12]);print(d.groupby('dept').salary.mean().round(2))"
```

### Step 7

Test the re-identification risk: group by postal code and find the SMALLEST group. Any group of 1 is uniquely identifying. Discuss why small groups defeat de-identification (the k-anonymity problem).

```bash
python3 -c "import pandas as pd;d=pd.read_csv('customers.csv');print(d.groupby('postal').size())"
```

### Step 8

Save the release-ready pseudonymised extract and note who may access it under which role.

```bash
python3 -c "import pandas as pd,hashlib;d=pd.read_csv('customers.csv');d['subject_key']=d.nric.map(lambda v: hashlib.sha256(v.encode()).hexdigest()[:12]);d[['subject_key','postal','dept','salary']].to_csv('customers_release.csv',index=False)" && cat customers_release.csv
```

---

## Dataset

This lab ships with its own data — you do not have to type it in. See [`data/README.md`](data/README.md) for what each file contains and which defects are planted in it.

- [`data/customers.csv`](data/customers.csv) — 2,776 bytes
- [`data/customers.xlsx`](data/customers.xlsx) — 7,130 bytes

---

## Test it — expected result

Across 40 records masking shows the NRIC as S****G form. De-identification drops name, nric and email. Pseudonymisation gives a stable 12-character key, and the departmental salary averages (Operations 4006.25, Sales 4518.75, Technology 5431.25, Finance 4612.50, Marketing 4268.75) are identical to those computed on the raw data.

## If it doesn't work

| Symptom | Fix |
|---|---|
| The CSV contains '404: Not Found' | curl wrote the error page into the file. Confirm the BASE URL, re-run with -fsSO so curl fails loudly, or copy the files from the repo folder you cloned. |
| The email regex did not mask | Confirm regex=True is passed to str.replace and the backreferences use \1 and \2. |
| The hash changes between runs | SHA-256 is deterministic — if it changes, your input has stray whitespace. Strip it first. |
| Some postal groups are small | That is the k-anonymity problem: a group of 1 identifies a person even with the name removed. Note which postal codes fail a k=5 threshold. |

---

*© 2026 Tertiary Infotech Academy Pte Ltd. All rights reserved. · TGS-2024049212*
