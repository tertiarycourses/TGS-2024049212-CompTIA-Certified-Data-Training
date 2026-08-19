# Lab 13 — dataset

A customer extract carrying real personal data patterns.

## Files

- **`customers.csv`** (2,776 bytes) — 40 records — cust_id, name, nric, email, postal, dept, salary.
- **`customers.xlsx`** (7,130 bytes) — The same data as an Excel workbook.

## Planted defects (this is what you are meant to find)

- NRIC is confidential PII; salary is sensitive PIFI; dept is internal
- postal codes repeat, so some quasi-identifier groups are small — the k-anonymity problem

---

Data is generated deterministically, so the numbers in the Learner Guide and the slides
always match what you see. Regenerate with:

```bash
python3 .claude/skills/courseware-build/build/make_lab_data.py
```
