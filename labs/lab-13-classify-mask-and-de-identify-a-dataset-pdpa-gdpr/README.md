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

Create the lab folder and the sensitive source extract.

```bash
mkdir -p ~/dataplus/lab13 && cd ~/dataplus/lab13 && printf 'cust_id,name,nric,email,postal,dept,salary\n1,Mei Tan,S1234567A,mei.tan@example.sg,738099,Ops,4200\n2,Ravi Kumar,S2345678B,ravi.k@example.sg,600123,Sales,4500\n3,Siti Nur,S3456789C,siti@example.sg,310045,Tech,5200\n4,John Lee,S4567890D,john.lee@example.sg,529536,Ops,3900\n' > customers.csv
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

Test the re-identification risk. With only 4 rows, does the postal code alone identify someone? Discuss why small groups defeat de-identification (the k-anonymity problem).

```bash
python3 -c "import pandas as pd;d=pd.read_csv('customers.csv');print(d.groupby('postal').size())"
```

### Step 8

Save the release-ready pseudonymised extract and note who may access it under which role.

```bash
python3 -c "import pandas as pd,hashlib;d=pd.read_csv('customers.csv');d['subject_key']=d.nric.map(lambda v: hashlib.sha256(v.encode()).hexdigest()[:12]);d[['subject_key','postal','dept','salary']].to_csv('customers_release.csv',index=False)" && cat customers_release.csv
```

---

## Test it — expected result

Masking shows S****A. De-identification drops three columns. Pseudonymisation gives a stable 12-character key, and the departmental salary averages (Ops 4050, Sales 4500, Tech 5200) are identical to the originals.

## If it doesn't work

| Symptom | Fix |
|---|---|
| The email regex did not mask | Confirm regex=True is passed to str.replace and the backreferences use \1 and \2. |
| The hash changes between runs | SHA-256 is deterministic — if it changes, your input has stray whitespace. Strip it first. |
| Every postal group has size 1 | Exactly the point — with n=4 every quasi-identifier is unique, so de-identification alone is not enough. Record that finding. |

---

*© 2026 Tertiary Infotech Academy Pte Ltd. All rights reserved. · TGS-2024049212*
