# Lab 14 — Assess Data-Leakage Risk and Set Access Controls

**Domain 05 — Data Governance, Quality and Controls** (14% of the CompTIA Data+ (DA0-001) exam)  
**Maps to:** LU5 / LO5 (A4)  
**Course:** WSQ - CompTIA Certified Data+ Training (TGS-2024049212)

---

## Exam objective

Summarize compliance requirements; compare privacy and protection strategies (Domain 5); LO5 / A4.

## What you will do

Governance is a set of decisions, not a document. You use the Cybersecurity Threat Simulator's data-leakage risk estimator to score a realistic set of handling practices, then translate the score into a concrete role-based access matrix and a retention schedule for the Lab 13 dataset.

## What you will produce

A completed risk assessment with a before/after score, a role-based access control matrix, and a retention & destruction schedule.

## Tools

- Cybersecurity Threat Simulator (https://alfredang.github.io/cybersecuritysimulator/), the Lab 13 dataset
- **Environment:** https://alfredang.github.io/cybersecuritysimulator/

---

## Step-by-step

### Step 1

Open the Cybersecurity Threat Simulator and go to the Data Leakage Risk Estimator.

### Step 2

Set the toggles to describe a BAD baseline: no encryption, shared logins, no access review, data kept forever. Record the risk score and its level (Critical / High / Medium).

### Step 3

Now switch on the controls one at a time — encryption at rest, role-based access, periodic review, defined retention. Record how much each single control moves the score.

### Step 4

Note which single control reduced the risk most. That is where governance effort pays off first.

### Step 5

Open the Password Strength Analyzer and test a weak versus a strong credential — this is the access control layer protecting everything you built in Lab 13.

### Step 6

Build the ACCESS MATRIX for the Lab 13 dataset. For each of the four roles (Data Owner, Data Steward, Data Custodian, Analyst) decide access to: raw NRIC, masked extract, pseudonymised release, salary.

### Step 7

Write the RETENTION SCHEDULE: how long is each artefact kept, what triggers destruction, and which method is used (removal vs destruction vs sanitisation)?

### Step 8

Map each decision to its compliance driver — Singapore PDPA for the personal data, and the organisation's own audit requirement for the retention log.

---

## Test it — expected result

Your risk score drops from Critical to Medium or lower once encryption, RBAC, review and retention are enabled. Your access matrix gives the Analyst the pseudonymised release ONLY, never the raw NRIC.

## If it doesn't work

| Symptom | Fix |
|---|---|
| The score does not change | Some toggles only affect certain threat categories. Change one at a time and re-read the score after each. |
| Unsure which role gets what | Apply least privilege: the Analyst needs the analytical columns, never the identifiers. Only the Data Owner authorises raw access. |
| Retention period unclear | Where no statutory period applies, set it from business need and document the rationale — an undocumented period is itself an audit finding. |

---

*© 2026 Tertiary Infotech Academy Pte Ltd. All rights reserved. · TGS-2024049212*
