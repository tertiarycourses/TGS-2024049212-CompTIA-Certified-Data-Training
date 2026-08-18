# Lab 3 — Profile Machine/Log Data as a Data Source (PCAP Analyzer)

**Domain 01 — Data Concepts and Environments** (20% of the CompTIA Data+ (DA0-001) exam)  
**Maps to:** LU1 / LO1 (K4, A1)  
**Course:** WSQ - CompTIA Certified Data+ Training (TGS-2024049212)

---

## Exam objective

Identify data sources: logs, machine data and repositories; recognise infrastructure concepts (Domain 1); LO1 / A1.

## What you will do

Machine-generated data is one of the exam's named data sources, and it never arrives analysis-ready. You load a packet capture into the browser-based PCAP Analyzer, read the statistics it derives, and translate what you see into the data-analyst vocabulary of records, fields, dimensions and measures.

## What you will produce

A completed data-source profile of a machine-data feed: record count, field inventory, dimensions vs measures, and three analytical questions it can answer.

## Tools

- PCAP Analyzer (https://alfredang.github.io/pcapanalyzer/), any .pcap/.pcapng sample
- **Environment:** https://alfredang.github.io/pcapanalyzer/

---

## Step-by-step

### Step 1

Open the PCAP Analyzer in your browser. Everything is parsed locally — nothing is uploaded.

### Step 2

Generate a small capture on Killercoda if you do not have one, then download it to your machine.

```bash
sudo tcpdump -i any -c 200 -w ~/sample.pcap 2>/dev/null || echo 'use the sample capture supplied by your trainer'
```

### Step 3

Drag the .pcap file onto the drop zone and wait for the four summary statistics to appear.

### Step 4

Record the four derived MEASURES: packet count, total bytes, capture duration and average packet size.

### Step 5

Open the Protocol Distribution panel — this is a categorical frequency table, exactly like a GROUP BY.

### Step 6

Open Top Talkers and Top Conversations — these are aggregations over a source/destination DIMENSION.

### Step 7

Click any single packet to inspect its fields, and list which are dimensions (IP, protocol) and which are measures (length).

### Step 8

Write down three business questions this feed could answer, and one it cannot — noting what extra data you would need.

---

## Test it — expected result

You can state the record count and average packet size, classify at least five fields as dimension or measure, and explain why Protocol Distribution is a frequency table rather than a raw record list.

## If it doesn't work

| Symptom | Fix |
|---|---|
| The file will not load | The analyser accepts .pcap and .pcapng only. Confirm the extension, and that the file is not zero bytes (ls -l). |
| tcpdump: permission denied | Prefix with sudo on Killercoda. If it is still blocked, use the sample capture your trainer provides. |
| The statistics look empty | A capture with zero packets produces zero rows. Re-capture with a larger -c value while browsing in another tab. |

---

*© 2026 Tertiary Infotech Academy Pte Ltd. All rights reserved. · TGS-2024049212*
