"""
Domain 1 — Data Concepts and Environments (20% of the CompTIA Data+ DA0-001 exam).
Maps to LU1 / LO1 (K4, A1).

Labs run on the Killercoda Ubuntu playground (browser terminal, no install) and on
the browser-based PCAP Analyzer for the machine/log data source.
"""

KILLERCODA = "https://killercoda.com/playgrounds/scenario/ubuntu"

DOMAIN1 = [
    dict(
        num=1,
        topic=1,
        title="Lab 1 — Build a Relational Schema and Prove Referential Integrity",
        objective="Explain data concepts: database types, data structures and data types (Domain 1); LO1 / K4 / A1.",
        desc=("You design and build a small three-table sales schema in SQLite, declare the primary and "
              "foreign keys, and then deliberately attack it with an orphan record and a cascading delete "
              "so you can see referential integrity doing its job."),
        build="A normalised 3NF SQLite database (customers, products, orders) with enforced foreign keys, plus evidence of a rejected orphan insert.",
        services="Killercoda Ubuntu, SQLite 3, SQL DDL/DML",
        env=KILLERCODA,
        steps=[
            ("Download this lab's dataset. The same files ship in the course repo under this lab's data/ folder.",
             "mkdir -p ~/dataplus/lab1 && cd ~/dataplus/lab1;\nR=https://raw.githubusercontent.com/tertiarycourses;\nB=$R/TGS-2024049212-CompTIA-Certified-Data-Training/main/labs;\nD=lab-01-build-a-relational-schema-and-prove-referential-inte;\nfor f in customers.csv products.csv orders.csv; do curl -fsSO $B/$D/data/$f || echo FAILED $f; done; ls -l"),
                        ("Turn foreign-key enforcement ON — SQLite leaves it off by default, which is the single most common cause of orphaned rows.",
             "PRAGMA foreign_keys = ON;"),
            ("Create the customers table — the columns must match customers.csv exactly, or .import silently drops data.",
             "CREATE TABLE customers (customer_id INTEGER PRIMARY KEY, first_name TEXT NOT NULL, last_name TEXT NOT NULL, email TEXT UNIQUE, region TEXT, joined DATE);"),
            ("Create the products table — note REAL for currency and the CHECK constraint enforcing domain integrity.",
             "CREATE TABLE products (product_id INTEGER PRIMARY KEY, name TEXT NOT NULL, unit_price REAL CHECK (unit_price >= 0));"),
            ("Create the orders fact table carrying TWO foreign keys with ON DELETE CASCADE.",
             "CREATE TABLE orders (order_id INTEGER PRIMARY KEY, customer_id INTEGER REFERENCES customers(customer_id) ON DELETE CASCADE, product_id INTEGER REFERENCES products(product_id), qty INTEGER NOT NULL, order_date DATE);"),
            ("Import the three CSV extracts into the tables you just created.",
             "sqlite3 sales.db \".mode csv\" \".import --skip 1 customers.csv customers\" \".import --skip 1 products.csv products\" \".import --skip 1 orders.csv orders\" \"SELECT COUNT(*) FROM customers; SELECT COUNT(*) FROM products; SELECT COUNT(*) FROM orders;\""),
            ("ATTACK 1 — insert an order for a customer who does not exist, using a FREE order_id so the "
             "error you see is the foreign key firing and not a duplicate primary key. This MUST be rejected.",
             "INSERT INTO orders VALUES (9999,999,10,1,'2025-03-03');"),
            ("ATTACK 2 — delete customer 1 and watch the cascade remove their orders, leaving nothing orphaned.",
             "DELETE FROM customers WHERE customer_id = 1; SELECT * FROM orders;"),
            ("Run a join across all three tables to confirm the schema answers a real business question.",
             "SELECT c.first_name, p.name, o.qty, o.qty*p.unit_price AS line_total FROM orders o JOIN customers c ON c.customer_id=o.customer_id JOIN products p ON p.product_id=o.product_id;"),
        ],
        test=("The three tables import 40 customers, 10 products and 120 orders. Attack 1 fails with "
              "'FOREIGN KEY constraint failed'. Attack 2 deletes customer 1 AND cascades to their 2 orders, "
              "so the order count drops from 120 to 118. The final join returns 118 priced order lines."),
        troubleshoot=[
            ("The CSV contains '404: Not Found'", "curl wrote the error page into the file. Confirm the BASE URL, re-run with -fsSO so curl fails loudly, or copy the files from the repo folder you cloned."),
            ("The orphan insert SUCCEEDED", "You forgot PRAGMA foreign_keys = ON. It resets on every new connection — re-run it after reopening sqlite3."),
            ("It says UNIQUE constraint failed, not FOREIGN KEY", "That order_id already exists in orders.csv. Pick an unused id (9999) so the foreign key is what fails."),
            ("'expected 5 columns but found 6 - extras ignored'", "Your CREATE TABLE does not match the CSV header. Run head -1 customers.csv and make the column list identical, then DROP and re-import."),
            ("'no such table' error", "You are in a different database file. Run .databases inside sqlite3 to confirm you opened sales.db."),
            ("The cascade did not fire", "ON DELETE CASCADE only works with foreign keys enforced. Re-check the PRAGMA, then re-create the orders table."),
        ],
    ),
    dict(
        num=2,
        topic=1,
        title="Lab 2 — Compare Structured, Semi-Structured and Unstructured Data",
        objective="Explain data concepts: data structures, file extensions and data types; identify data sources (Domain 1); LO1 / K4.",
        desc=("You create the same customer record three ways — as a CSV row, as a JSON document and as free "
              "text — then measure how much work each format takes to query. This is the exam's structured vs "
              "semi-structured vs unstructured distinction, made concrete."),
        build="Three files (customers.csv, customers.json, notes.txt) plus a Python script that queries each and reports the effort required.",
        services="Killercoda Ubuntu, Python 3, csv and json modules",
        env=KILLERCODA,
        steps=[
            ("Download this lab's dataset. The same files ship in the course repo under this lab's data/ folder.",
             "mkdir -p ~/dataplus/lab2 && cd ~/dataplus/lab2;\nR=https://raw.githubusercontent.com/tertiarycourses;\nB=$R/TGS-2024049212-CompTIA-Certified-Data-Training/main/labs;\nD=lab-02-compare-structured-semi-structured-and-unstructured;\nfor f in customers.csv customers.json notes.txt; do curl -fsSO $B/$D/data/$f || echo FAILED $f; done; ls -l"),
                                                ("Query the CSV — three lines of code, because the structure is guaranteed.",
             "python3 -c \"import csv;print(sum(float(r['spend']) for r in csv.DictReader(open('customers.csv'))))\""),
            ("Query the JSON — still easy, and it carries the extra 'tags' field the CSV could not hold.",
             "python3 -c \"import json;d=json.load(open('customers.json'));print(sum(r['spend'] for r in d));print(d[0].get('tags'))\""),
            ("Try to query the unstructured text — you need a regular expression, and it is fragile.",
             "python3 -c \"import re;t=open('notes.txt').read();print(re.findall(r'[$]?([0-9]+(?:[.][0-9]{2})?)\\s*(?:dollars)?',t))\""),
            ("Compare the file sizes and record what each format cost you in query effort.",
             "ls -l customers.csv customers.json notes.txt"),
        ],
        test=("The CSV and the JSON both total 2293.17 across 12 customers. The JSON also returns ['vip','repeat'] "
              "for the first record — a field the flat CSV cannot represent at all. The regex over notes.txt returns "
              "extra noise, proving unstructured text needs parsing before it can be analysed."),
        troubleshoot=[
            ("The CSV contains '404: Not Found'", "curl wrote the error page into the file. Confirm the BASE URL, re-run with -fsSO so curl fails loudly, or copy the files from the repo folder you cloned."),
            ("JSONDecodeError", "customers.json did not download cleanly. Check it with head -c 80 customers.json — if it starts with '404' the URL is wrong."),
            ("The regex returns '240.50' and '89' plus junk", "That is the expected lesson — unstructured text has no guarantees. Tighten the pattern in RegexLab."),
            ("KeyError: 'spend'", "Your CSV header row is missing or misspelled. Run head -1 customers.csv to check it."),
        ],
    ),
    dict(
        num=3,
        topic=1,
        title="Lab 3 — Profile Machine/Log Data as a Data Source (PCAP Analyzer)",
        objective="Identify data sources: logs, machine data and repositories; recognise infrastructure concepts (Domain 1); LO1 / A1.",
        desc=("Machine-generated data is one of the exam's named data sources, and it never arrives analysis-ready. "
              "You load a packet capture into the browser-based PCAP Analyzer, read the statistics it derives, and "
              "translate what you see into the data-analyst vocabulary of records, fields, dimensions and measures."),
        build="A completed data-source profile of a machine-data feed: record count, field inventory, dimensions vs measures, and three analytical questions it can answer.",
        services="PCAP Analyzer (https://alfredang.github.io/pcapanalyzer/), any .pcap/.pcapng sample",
        env="https://alfredang.github.io/pcapanalyzer/",
        steps=[
            ("Open the PCAP Analyzer in your browser. Everything is parsed locally — nothing is uploaded.", ""),
            ("Generate a small capture on Killercoda if you do not have one, then download it to your machine.",
             "sudo tcpdump -i any -c 200 -w ~/sample.pcap 2>/dev/null || echo 'use the sample capture supplied by your trainer'"),
            ("Drag the .pcap file onto the drop zone and wait for the four summary statistics to appear.", ""),
            ("Record the four derived MEASURES: packet count, total bytes, capture duration and average packet size.", ""),
            ("Open the Protocol Distribution panel — this is a categorical frequency table, exactly like a GROUP BY.", ""),
            ("Open Top Talkers and Top Conversations — these are aggregations over a source/destination DIMENSION.", ""),
            ("Click any single packet to inspect its fields, and list which are dimensions (IP, protocol) and which are measures (length).", ""),
            ("Write down three business questions this feed could answer, and one it cannot — noting what extra data you would need.", ""),
        ],
        test=("You can state the record count and average packet size, classify at least five fields as dimension or "
              "measure, and explain why Protocol Distribution is a frequency table rather than a raw record list."),
        troubleshoot=[
            ("The file will not load", "The analyser accepts .pcap and .pcapng only. Confirm the extension, and that the file is not zero bytes (ls -l)."),
            ("tcpdump: permission denied", "Prefix with sudo on Killercoda. If it is still blocked, use the sample capture your trainer provides."),
            ("The statistics look empty", "A capture with zero packets produces zero rows. Re-capture with a larger -c value while browsing in another tab."),
        ],
    ),
]
