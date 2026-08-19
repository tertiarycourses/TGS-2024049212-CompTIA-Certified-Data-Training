# Lab 1 — dataset

The three source extracts for the sales schema.

## Files

- **`customers.csv`** (2,282 bytes) — 40 customers — customer_id, first_name, last_name, email, region, joined.
- **`products.csv`** (282 bytes) — 10 products — product_id, name, unit_price (REAL currency).
- **`orders.csv`** (2,904 bytes) — 120 orders — the fact table, with foreign keys to customers and products.
- **`sales-schema.xlsx`** (11,436 bytes) — The same three tables as an Excel workbook, one sheet each.

---

Data is generated deterministically, so the numbers in the Learner Guide and the slides
always match what you see. Regenerate with:

```bash
python3 .claude/skills/courseware-build/build/make_lab_data.py
```
