# Lab 6 — Derive Structured Fields from Raw Address Data (IP Calculator)

**Domain 02 — Data Acquisition and Preparation** (22% of the CompTIA Data+ (DA0-001) exam)  
**Maps to:** LU2 / LO2 (K1, A2)  
**Course:** WSQ - CompTIA Certified Data+ Training (TGS-2024049212)

---

## Exam objective

Apply data transformation: derived variables and formatting; use data acquisition methods (Domain 2); LO2 / A2.

## What you will do

A derived variable is a new field computed from existing data — one of the exam's named manipulation techniques. You take raw CIDR address data, use the IP Calculator to derive the network fields by hand first, then reproduce the same derivation in code and prove the two agree.

## What you will produce

A dataset enriched with four derived columns (network address, broadcast, usable hosts, subnet class) verified against the calculator.

## Tools

- IP Calculator (https://alfredang.github.io/ipcalculator/), Killercoda Ubuntu, Python 3, ipaddress module
- **Environment:** https://alfredang.github.io/ipcalculator/

---

## Step-by-step

### Step 1

Create the working folder and download this lab's dataset. The files also ship in the course repo under labs/lab-06-derive-structured-fields-from-raw-address-data-ip-ca/data/ — download them from GitHub or copy them from the folder you cloned.

```bash
mkdir -p ~/dataplus/lab6 && cd ~/dataplus/lab6 && BASE=https://raw.githubusercontent.com/tertiarycourses/TGS-2024049212-CompTIA-Certified-Data-Training/main/labs/lab-06-derive-structured-fields-from-raw-address-data-ip-ca/data && for f in sites.csv; do curl -fsSO $BASE/$f || echo FAILED $f; done && ls -l
```

### Step 2

Enter 192.168.10.0/24 and record the derived values: network, broadcast, usable host count and mask.

### Step 3

Repeat for 10.0.5.0/22 and 172.16.8.0/29 — note how the usable-host count changes with the prefix.

### Step 4

Derive the same four fields in code — this is the DERIVED VARIABLE technique from the exam objectives.

```bash
python3 -c "import pandas as pd,ipaddress as ip;d=pd.read_csv('sites.csv');n=d.cidr.map(ip.ip_network);d['network']=[str(x.network_address) for x in n];d['broadcast']=[str(x.broadcast_address) for x in n];d['usable_hosts']=[x.num_addresses-2 for x in n];d['mask']=[str(x.netmask) for x in n];print(d)"
```

### Step 5

Compare every derived value against what the IP Calculator gave you — they must match exactly.

### Step 6

Decide the storage trade-off the exam asks about: store the derived columns (fast reads, more space) or recompute on demand (less space, slower). Write your choice and the reason.

### Step 7

Save the enriched dataset.

```bash
python3 -c "import pandas as pd,ipaddress as ip;d=pd.read_csv('sites.csv');n=d.cidr.map(ip.ip_network);d['network']=[str(x.network_address) for x in n];d['usable_hosts']=[x.num_addresses-2 for x in n];d.to_csv('sites_enriched.csv',index=False)" && cat sites_enriched.csv
```

---

## Dataset

This lab ships with its own data — you do not have to type it in. See [`data/README.md`](data/README.md) for what each file contains and which defects are planted in it.

- [`data/sites.csv`](data/sites.csv) — 298 bytes

---

## Test it — expected result

The code and the IP Calculator agree: /24 gives 254 usable hosts, /22 gives 1022, and /29 gives 6. sites_enriched.csv carries the derived columns alongside the original CIDR.

## If it doesn't work

| Symptom | Fix |
|---|---|
| The CSV contains '404: Not Found' | curl wrote the error page into the file. Confirm the BASE URL, re-run with -fsSO so curl fails loudly, or copy the files from the repo folder you cloned. |
| ValueError: has host bits set | The address is not a valid network address for that prefix. Use ip_network(x, strict=False) or correct the CIDR. |
| usable_hosts is negative for /31 or /32 | Those prefixes have no usable host range by the -2 convention. Note this edge case in your report. |
| The numbers disagree with the calculator | Confirm you entered the same prefix length in both. A /22 is not a /24. |

---

*© 2026 Tertiary Infotech Academy Pte Ltd. All rights reserved. · TGS-2024049212*
