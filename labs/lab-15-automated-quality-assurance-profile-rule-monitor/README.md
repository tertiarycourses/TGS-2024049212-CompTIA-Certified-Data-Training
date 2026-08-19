# Lab 15 — Automated Quality Assurance: Profile, Rule, Monitor

**Domain 05 — Data Governance, Quality and Controls** (14% of the CompTIA Data+ (DA0-001) exam)  
**Maps to:** LU5 / LO5 (A4)  
**Course:** WSQ - CompTIA Certified Data+ Training (TGS-2024049212)

---

## Exam objective

Implement quality assurance: profiling, monitoring and testing for data quality; explain data management practices (Domain 5); LO5 / A4.

## What you will do

The capstone governance lab. You write an automated data-quality suite that tests a daily feed against explicit rules across the exam's quality dimensions — completeness, accuracy, consistency, uniqueness and validity — then run it against a clean file and a broken one so it proves it can actually fail.

## What you will produce

A reusable dq_check.py suite that scores five quality dimensions, exits non-zero on failure, and produces a dated quality report.

## Tools

- Killercoda Ubuntu, Python 3, pandas
- **Environment:** https://killercoda.com/playgrounds/scenario/ubuntu

---

## Step-by-step

### Step 1

Download this lab's dataset. The same files ship in the course repo under this lab's data/ folder.

```bash
mkdir -p ~/dataplus/lab15 && cd ~/dataplus/lab15;
R=https://raw.githubusercontent.com/tertiarycourses;
B=$R/TGS-2024049212-CompTIA-Certified-Data-Training/main/labs;
D=lab-15-automated-quality-assurance-profile-rule-monitor;
for f in feed_good.csv feed_bad.csv; do curl -fsSO $B/$D/data/$f || echo FAILED $f; done; ls -l
```

### Step 2

Write the quality suite — one function per quality dimension.

```bash
cat > dq_check.py <<'EOF'
import sys, pandas as pd
VALID_STATUS = {'SHIPPED','PENDING','CANCELLED'}

def run(path):
    d = pd.read_csv(path)
    results = []
    # COMPLETENESS - no required field may be null
    nulls = d[['order_id','customer_id','order_date','amount']].isnull().sum().sum()
    results.append(('completeness', nulls == 0, f'{nulls} null(s) in required fields'))
    # UNIQUENESS - the primary key must be unique
    dupes = d.order_id.duplicated().sum()
    results.append(('uniqueness', dupes == 0, f'{dupes} duplicate order_id'))
    # VALIDITY - amount must be positive
    neg = (d.amount < 0).sum()
    results.append(('validity', neg == 0, f'{neg} negative amount(s)'))
    # CONSISTENCY - status must be from the agreed domain
    bad = (~d.status.isin(VALID_STATUS)).sum()
    results.append(('consistency', bad == 0, f'{bad} invalid status value(s)'))
    # ACCURACY (proxy) - dates must parse
    parsed = pd.to_datetime(d.order_date, errors='coerce').isnull().sum()
    results.append(('accuracy', parsed == 0, f'{parsed} unparseable date(s)'))

    passed = sum(1 for _, ok, _ in results if ok)
    print(f'\nDATA QUALITY REPORT - {path}')
    print('-' * 52)
    for dim, ok, msg in results:
        print(f'  {"PASS" if ok else "FAIL"}  {dim:<14} {msg}')
    print('-' * 52)
    print(f'  SCORE: {passed}/5 dimensions passed\n')
    return 0 if passed == 5 else 1

if __name__ == '__main__':
    sys.exit(run(sys.argv[1]))
EOF
echo written
```

### Step 3

Run the suite against the GOOD feed — it must pass all five and exit 0.

```bash
python3 dq_check.py feed_good.csv; echo "exit code: $?"
```

### Step 4

Run it against the BROKEN feed — it must fail four dimensions and exit 1.

```bash
python3 dq_check.py feed_bad.csv; echo "exit code: $?"
```

### Step 5

This exit code is what makes it MONITORING rather than a report — a scheduler can now block a bad load.

```bash
python3 dq_check.py feed_bad.csv > /dev/null 2>&1 && echo 'LOAD APPROVED' || echo 'LOAD BLOCKED - do not ingest'
```

### Step 6

Save a dated quality report so you build a quality history, not just a snapshot.

```bash
python3 dq_check.py feed_good.csv > dq_report_$(date +%Y%m%d).txt; ls -1 dq_report_*.txt
```

### Step 7

Add the lineage note: record the source, the owner, the rule version and the run date. This is the documentation half of the exam's data-management objective.

```bash
printf 'source: orders feed (daily)\nowner: Sales Ops\nsteward: Data Quality team\nrules version: 1.0\nrun: %s\n' "$(date +%F)" > lineage.txt && cat lineage.txt
```

---

## Dataset

This lab ships with its own data — you do not have to type it in. See [`data/README.md`](data/README.md) for what each file contains and which defects are planted in it.

- [`data/daily-feeds.xlsx`](data/daily-feeds.xlsx) — 8,280 bytes
- [`data/feed_bad.csv`](data/feed_bad.csv) — 1,416 bytes
- [`data/feed_good.csv`](data/feed_good.csv) — 1,415 bytes

---

## Test it — expected result

feed_good.csv (40 rows) scores 5/5 and exits 0. feed_bad.csv (40 rows) fails ALL FIVE dimensions — 2 nulls, 2 duplicate order_ids, 2 negative amounts, 2 invalid status values and 1 unparseable date — so it scores 0/5, exits 1, and the 'LOAD BLOCKED' branch fires.

## If it doesn't work

| Symptom | Fix |
|---|---|
| The CSV contains '404: Not Found' | curl wrote the error page into the file. Confirm the BASE URL, re-run with -fsSO so curl fails loudly, or copy the files from the repo folder you cloned. |
| The heredoc breaks on the f-strings | Ensure you used <<'EOF' with the quotes — that stops the shell expanding anything inside. |
| Exit code is always 0 | You ran it inside another command. Test with python3 dq_check.py feed_bad.csv; echo $? on its own line. |
| accuracy fails on the good feed | Your dates are not ISO format. pandas parses YYYY-MM-DD reliably — normalise the feed first. |

---

*© 2026 Tertiary Infotech Academy Pte Ltd. All rights reserved. · TGS-2024049212*
