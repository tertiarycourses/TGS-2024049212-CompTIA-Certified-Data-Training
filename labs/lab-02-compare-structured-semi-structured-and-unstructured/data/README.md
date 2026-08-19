# Lab 2 — dataset

The SAME 12 customers held three different ways — the point of the lab.

## Files

- **`customers.csv`** (392 bytes) — STRUCTURED — fixed header, one record per line.
- **`customers.json`** (1,452 bytes) — SEMI-STRUCTURED — self-describing, with ragged 'tags' and nested 'contact' fields the CSV cannot hold.
- **`notes.txt`** (915 bytes) — UNSTRUCTURED — the same facts written as free prose by account managers.

---

Data is generated deterministically, so the numbers in the Learner Guide and the slides
always match what you see. Regenerate with:

```bash
python3 .claude/skills/courseware-build/build/make_lab_data.py
```
