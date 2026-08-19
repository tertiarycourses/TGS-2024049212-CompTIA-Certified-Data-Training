# Lab 8 — dataset

Salary data for descriptive statistics.

## Files

- **`salaries.csv`** (1,256 bytes) — 61 employees across 5 departments.
- **`salaries.xlsx`** (6,156 bytes) — The same data as an Excel workbook.

## Planted defects (this is what you are meant to find)

- E999 (Executive, 26000) is a single planted outlier at z ≈ 7.5

---

Data is generated deterministically, so the numbers in the Learner Guide and the slides
always match what you see. Regenerate with:

```bash
python3 .claude/skills/courseware-build/build/make_lab_data.py
```
