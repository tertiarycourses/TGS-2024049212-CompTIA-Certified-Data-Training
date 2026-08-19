# Lab 4 — dataset

A deliberately dirty sales extract — profile it before trusting any number.

## Files

- **`sales_dirty.csv`** (2,656 bytes) — 63 rows, 5 columns.
- **`sales_dirty.xlsx`** (7,211 bytes) — The same data as an Excel workbook.

## Planted defects (this is what you are meant to find)

- 4 missing cities, 3 missing spends, 2 missing order_dates
- 3 exact duplicate rows
- 2 extreme outliers (99999.00 and 87500.00) — both flag at |z| > 3
- 1 value with leading/trailing spaces ('  Jurong  ') and 1 casing inconsistency ('singapore')

---

Data is generated deterministically, so the numbers in the Learner Guide and the slides
always match what you see. Regenerate with:

```bash
python3 .claude/skills/courseware-build/build/make_lab_data.py
```
