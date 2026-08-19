# Lab 15 — dataset

Two daily order feeds — one clean, one broken.

## Files

- **`feed_good.csv`** (1,415 bytes) — 40 rows that pass all five quality dimensions.
- **`feed_bad.csv`** (1,416 bytes) — 40 rows that fail ALL FIVE dimensions.
- **`daily-feeds.xlsx`** (8,280 bytes) — Both feeds as an Excel workbook, one sheet each.

## Planted defects (this is what you are meant to find)

- completeness: 2 null customer_id
- uniqueness: 2 duplicate order_id
- validity: 2 negative amounts
- consistency: 2 invalid status values ('TELEPORTED', 'shipped')
- accuracy: 1 unparseable date ('15/03/2025' instead of ISO)

---

Data is generated deterministically, so the numbers in the Learner Guide and the slides
always match what you see. Regenerate with:

```bash
python3 .claude/skills/courseware-build/build/make_lab_data.py
```
