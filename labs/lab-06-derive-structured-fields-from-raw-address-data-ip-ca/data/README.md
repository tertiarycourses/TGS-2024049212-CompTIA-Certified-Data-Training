# Lab 6 — dataset

10 network sites in CIDR notation, plus one malformed row.

## Files

- **`sites.csv`** (298 bytes) — 11 rows. Prefixes from /16 to /30 so the usable-host count varies widely.

## Planted defects (this is what you are meant to find)

- 'Legacy-Import' (10.0.5.0/22) has host bits set on purpose — it raises ValueError unless you pass strict=False

---

Data is generated deterministically, so the numbers in the Learner Guide and the slides
always match what you see. Regenerate with:

```bash
python3 .claude/skills/courseware-build/build/make_lab_data.py
```
