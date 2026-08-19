# Lab 10 — dataset

36 months of marketing spend, revenue and headcount.

## Files

- **`marketing.csv`** (666 bytes) — 36 rows — month, spend, revenue, staff.
- **`marketing.xlsx`** (5,879 bytes) — The same data as an Excel workbook.

## Planted defects (this is what you are meant to find)

- staff correlates with revenue at r ≈ 0.97 — a SPURIOUS relationship; growth over time drives both

---

Data is generated deterministically, so the numbers in the Learner Guide and the slides
always match what you see. Regenerate with:

```bash
python3 .claude/skills/courseware-build/build/make_lab_data.py
```
