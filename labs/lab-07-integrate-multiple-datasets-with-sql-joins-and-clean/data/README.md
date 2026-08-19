# Lab 7 — dataset

Three separate source extracts that must be integrated.

## Files

- **`customers.csv`** (683 bytes) — 31 customers.
- **`orders.csv`** (1,203 bytes) — 81 orders.
- **`targets.csv`** (63 bytes) — One revenue target per region.
- **`integration-sources.xlsx`** (8,642 bytes) — All three sources as an Excel workbook.

## Planted defects (this is what you are meant to find)

- order 999 is an ORPHAN — customer_id 77 has no master record, so an INNER JOIN silently drops it
- 4 customers have NO orders — they survive only via a LEFT JOIN
- targets straddle actual revenue: 2 regions miss, 2 beat

---

Data is generated deterministically, so the numbers in the Learner Guide and the slides
always match what you see. Regenerate with:

```bash
python3 .claude/skills/courseware-build/build/make_lab_data.py
```
