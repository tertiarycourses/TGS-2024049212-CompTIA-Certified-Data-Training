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
            ("Open the Killercoda Ubuntu playground in your browser and confirm SQLite is available.", "sqlite3 --version"),
            ("Create the lab folder and open a new database file.", "mkdir -p ~/dataplus/lab1 && cd ~/dataplus/lab1 && sqlite3 sales.db"),
            ("Turn foreign-key enforcement ON — SQLite leaves it off by default, which is the single most common cause of orphaned rows.",
             "PRAGMA foreign_keys = ON;"),
            ("Create the customers table with a primary key and typed columns (INTEGER, TEXT, DATE).",
             "CREATE TABLE customers (customer_id INTEGER PRIMARY KEY, first_name TEXT NOT NULL, last_name TEXT NOT NULL, email TEXT UNIQUE, joined DATE);"),
            ("Create the products table — note REAL for currency and the CHECK constraint enforcing domain integrity.",
             "CREATE TABLE products (product_id INTEGER PRIMARY KEY, name TEXT NOT NULL, unit_price REAL CHECK (unit_price >= 0));"),
            ("Create the orders fact table carrying TWO foreign keys with ON DELETE CASCADE.",
             "CREATE TABLE orders (order_id INTEGER PRIMARY KEY, customer_id INTEGER REFERENCES customers(customer_id) ON DELETE CASCADE, product_id INTEGER REFERENCES products(product_id), qty INTEGER NOT NULL, order_date DATE);"),
            ("Insert reference data into the two dimension tables.",
             "INSERT INTO customers VALUES (1,'Mei','Tan','mei.tan@example.sg','2025-01-14'),(2,'Ravi','Kumar','ravi.k@example.sg','2025-02-03');"),
            ("Insert the product rows.",
             "INSERT INTO products VALUES (10,'Wireless Mouse',24.90),(11,'USB-C Hub',59.00);"),
            ("Insert valid orders that respect both foreign keys.",
             "INSERT INTO orders VALUES (100,1,10,2,'2025-03-01'),(101,2,11,1,'2025-03-02');"),
            ("ATTACK 1 — try to insert an order for a customer who does not exist. This MUST be rejected.",
             "INSERT INTO orders VALUES (102,999,10,1,'2025-03-03');"),
            ("ATTACK 2 — delete customer 1 and watch the cascade remove their orders, leaving nothing orphaned.",
             "DELETE FROM customers WHERE customer_id = 1; SELECT * FROM orders;"),
            ("Run a join across all three tables to confirm the schema answers a real business question.",
             "SELECT c.first_name, p.name, o.qty, o.qty*p.unit_price AS line_total FROM orders o JOIN customers c ON c.customer_id=o.customer_id JOIN products p ON p.product_id=o.product_id;"),
        ],
        test=("Attack 1 fails with 'FOREIGN KEY constraint failed' and attack 2 removes order 100 automatically. "
              "The final join returns one row (Ravi · USB-C Hub · 1 · 59.0)."),
        troubleshoot=[
            ("The orphan insert SUCCEEDED", "You forgot PRAGMA foreign_keys = ON. It resets on every new connection — re-run it after reopening sqlite3."),
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
            ("Create the lab folder.", "mkdir -p ~/dataplus/lab2 && cd ~/dataplus/lab2"),
            ("Write the STRUCTURED version — a delimited CSV with a fixed header and one record per line.",
             "printf 'customer_id,name,city,spend\\n1,Mei Tan,Singapore,240.50\\n2,Ravi Kumar,Jurong,89.00\\n' > customers.csv"),
            ("Write the SEMI-STRUCTURED version — JSON, which is self-describing and allows nested and ragged fields.",
             "printf '[{\"customer_id\":1,\"name\":\"Mei Tan\",\"city\":\"Singapore\",\"spend\":240.50,\"tags\":[\"vip\",\"repeat\"]},{\"customer_id\":2,\"name\":\"Ravi Kumar\",\"city\":\"Jurong\",\"spend\":89.00}]' > customers.json"),
            ("Write the UNSTRUCTURED version — the same facts buried in prose, with no schema at all.",
             "printf 'Mei Tan from Singapore spent about $240.50 with us this quarter. Ravi Kumar (Jurong) spent 89 dollars.\\n' > notes.txt"),
            ("Query the CSV — three lines of code, because the structure is guaranteed.",
             "python3 -c \"import csv;print(sum(float(r['spend']) for r in csv.DictReader(open('customers.csv'))))\""),
            ("Query the JSON — still easy, and it carries the extra 'tags' field the CSV could not hold.",
             "python3 -c \"import json;d=json.load(open('customers.json'));print(sum(r['spend'] for r in d));print(d[0].get('tags'))\""),
            ("Try to query the unstructured text — you need a regular expression, and it is fragile.",
             "python3 -c \"import re;t=open('notes.txt').read();print(re.findall(r'[$]?([0-9]+(?:[.][0-9]{2})?)\\s*(?:dollars)?',t))\""),
            ("Compare the file sizes and record what each format cost you in query effort.",
             "ls -l customers.csv customers.json notes.txt"),
        ],
        test=("The CSV and JSON both total 329.5. The JSON also returns ['vip','repeat'] — a field the CSV cannot "
              "represent. The regex over notes.txt returns extra noise, proving unstructured data needs parsing before analysis."),
        troubleshoot=[
            ("JSONDecodeError", "The shell ate a quote. Re-run the printf line exactly, or use nano customers.json and paste the JSON in."),
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
