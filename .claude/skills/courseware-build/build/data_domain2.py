"""
Domain 2 — Data Acquisition and Preparation (22% of the CompTIA Data+ DA0-001 exam).
Maps to LU2 / LO2 (K1, A2).

Labs use the Killercoda Ubuntu playground plus the browser-based RegexLab (parsing)
and IP Calculator (deriving structured fields from raw address data).
"""

KILLERCODA = "https://killercoda.com/playgrounds/scenario/ubuntu"

DOMAIN2 = [
    dict(
        num=4,
        topic=2,
        title="Lab 4 — Explore a Dirty Dataset: Missing Values, Duplicates and Outliers",
        objective="Perform data exploration: find missing values, duplication, redundancy or outliers (Domain 2); LO2 / K1 / A2.",
        desc=("You are handed a deliberately dirty sales extract and must profile it before trusting a single number. "
              "You quantify every defect class the exam names — nulls, duplicates, redundancy and outliers — and "
              "produce a data-quality report that says how bad the data is BEFORE you clean it."),
        build="A data-quality profile report quantifying null counts per column, duplicate rows, and outliers detected by z-score.",
        services="Killercoda Ubuntu, Python 3, pandas",
        env=KILLERCODA,
        steps=[
            ("Create the lab folder and install pandas if it is not already present.",
             "mkdir -p ~/dataplus/lab4 && cd ~/dataplus/lab4 && pip3 install pandas --quiet"),
            ("Create the dirty dataset — note the blank cells, the repeated row, and the 99999 spend.",
             "cat > sales_dirty.csv <<'EOF'\norder_id,customer,city,spend,order_date\n1,Mei Tan,Singapore,240.50,2025-03-01\n2,Ravi Kumar,Jurong,89.00,2025-03-02\n3,Siti Nur,,145.25,2025-03-02\n4,Mei Tan,Singapore,240.50,2025-03-01\n5,John Lee,Tampines,,2025-03-04\n6,Wei Ming,Bedok,99999.00,2025-03-05\n7,Siti Nur,Woodlands,310.00,\nEOF"),
            ("Load it and look at the shape and dtypes first — always know how many records you started with.",
             "python3 -c \"import pandas as pd;d=pd.read_csv('sales_dirty.csv');print(d.shape);print(d.dtypes)\""),
            ("Count MISSING VALUES per column — the exam's first exploration task.",
             "python3 -c \"import pandas as pd;d=pd.read_csv('sales_dirty.csv');print(d.isnull().sum())\""),
            ("Count DUPLICATE rows and show which ones they are.",
             "python3 -c \"import pandas as pd;d=pd.read_csv('sales_dirty.csv');print('dupes:',d.duplicated().sum());print(d[d.duplicated(keep=False)])\""),
            ("Detect OUTLIERS with a z-score — any |z| above 3 is the standard flag.",
             "python3 -c \"import pandas as pd;d=pd.read_csv('sales_dirty.csv');s=d['spend'].dropna();z=(s-s.mean())/s.std();print(d.loc[z[abs(z)>1.5].index])\""),
            ("Get the descriptive summary and note how badly the 99999 distorts the mean versus the median.",
             "python3 -c \"import pandas as pd;d=pd.read_csv('sales_dirty.csv');print(d['spend'].describe());print('median',d['spend'].median())\""),
            ("Write the profile report to a file so the cleaning lab can be measured against it.",
             "python3 -c \"import pandas as pd;d=pd.read_csv('sales_dirty.csv');open('profile.txt','w').write(str(d.isnull().sum())+'\\ndupes: '+str(d.duplicated().sum())+'\\nmean: '+str(d.spend.mean())+'\\nmedian: '+str(d.spend.median()))\" && cat profile.txt"),
        ],
        test=("Your profile reports 7 rows, 1 null city, 1 null spend, 1 null order_date, 1 duplicate row, and one "
              "extreme outlier (99999.00). The mean spend (~16720) is wildly above the median (~240.50) — proof the outlier is distorting it."),
        troubleshoot=[
            ("ModuleNotFoundError: pandas", "Run pip3 install pandas. On Killercoda add --break-system-packages if pip refuses."),
            ("The heredoc pasted as one line", "Paste the cat > ... <<'EOF' block line by line, or use nano sales_dirty.csv instead."),
            ("z-score flags nothing", "With only 6 values the standard deviation is huge. That is why the lab uses a 1.5 threshold — explain this effect in your report."),
        ],
    ),
    dict(
        num=5,
        topic=2,
        title="Lab 5 — Build Parsing Patterns in RegexLab and Apply Them",
        objective="Apply data transformation: cleansing, parsing and formatting data (Domain 2); LO2 / K1.",
        desc=("Real source fields arrive as one messy string — 'Mei Tan <mei.tan@example.sg> +65 9123 4567'. "
              "You use RegexLab to build and validate the extraction patterns interactively, then apply the "
              "proven patterns in pandas to split one dirty column into three clean, typed fields."),
        build="Three validated regex patterns (name, email, phone) and a cleaned CSV with the single contact column parsed into three columns.",
        services="RegexLab (https://alfredang.github.io/regexgenerator/), Killercoda Ubuntu, Python 3, pandas",
        env="https://alfredang.github.io/regexgenerator/",
        steps=[
            ("Open RegexLab in your browser and clear the sample test string.", ""),
            ("Paste these three messy contact records into the Test String box:  Mei Tan <mei.tan@example.sg> +65 9123 4567", ""),
            ("Build the EMAIL pattern and watch the match count update live. Confirm it matches all three records.",
             "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}"),
            ("Build the SINGAPORE PHONE pattern — 8 digits starting 6, 8 or 9, with optional +65 and spaces.",
             "(?:\\+65[ ]?)?[689][0-9]{3}[ ]?[0-9]{4}"),
            ("Build the NAME pattern — everything before the first angle bracket, trimmed.",
             "^([A-Za-z ]+?)\\s*<"),
            ("Use the Substitution panel to confirm your pattern replaces cleanly before you trust it in code.", ""),
            ("Switch to Killercoda and create the messy source file.",
             "mkdir -p ~/dataplus/lab5 && cd ~/dataplus/lab5 && cat > contacts.csv <<'EOF'\nid,contact\n1,Mei Tan <mei.tan@example.sg> +65 9123 4567\n2,Ravi Kumar <ravi.k@example.sg> 81234567\n3,Siti Nur <siti@example.sg> +65 6100 0613\nEOF"),
            ("Apply the SAME patterns you validated in RegexLab, using pandas str.extract.",
             "python3 -c \"import pandas as pd;d=pd.read_csv('contacts.csv');d['name']=d.contact.str.extract(r'^([A-Za-z ]+?)\\s*<');d['email']=d.contact.str.extract(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,})');d['phone']=d.contact.str.extract(r'((?:\\+65 ?)?[689][0-9]{3} ?[0-9]{4})');print(d[['id','name','email','phone']])\""),
            ("Normalise the phone format — strip +65 and spaces so every value has the same shape.",
             "python3 -c \"import pandas as pd,re;d=pd.read_csv('contacts.csv');d['phone']=d.contact.str.extract(r'((?:\\+65 ?)?[689][0-9]{3} ?[0-9]{4})')[0].str.replace(r'[^0-9]','',regex=True).str[-8:];print(d[['id','phone']])\""),
            ("Save the cleaned, parsed output.",
             "python3 -c \"import pandas as pd;d=pd.read_csv('contacts.csv');d['name']=d.contact.str.extract(r'^([A-Za-z ]+?)\\s*<');d['email']=d.contact.str.extract(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,})');d['phone']=d.contact.str.extract(r'((?:\\+65 ?)?[689][0-9]{3} ?[0-9]{4})')[0].str.replace(r'[^0-9]','',regex=True).str[-8:];d[['id','name','email','phone']].to_csv('contacts_clean.csv',index=False)\" && cat contacts_clean.csv"),
        ],
        test=("contacts_clean.csv holds three rows with name, email and an 8-digit phone each — 91234567, 81234567 "
              "and 61000613. No angle brackets, no +65 prefixes, no leftover spaces."),
        troubleshoot=[
            ("RegexLab shows 0 matches", "Check the flags — you usually want 'g' (global) so every record is matched, not just the first."),
            ("extract returns NaN", "pandas needs a capturing group. Confirm your pattern has parentheses around the part you want."),
            ("The phone keeps its +65", "The .str.replace step is what strips it. Confirm regex=True is set, then take the last 8 characters."),
        ],
    ),
    dict(
        num=6,
        topic=2,
        title="Lab 6 — Derive Structured Fields from Raw Address Data (IP Calculator)",
        objective="Apply data transformation: derived variables and formatting; use data acquisition methods (Domain 2); LO2 / A2.",
        desc=("A derived variable is a new field computed from existing data — one of the exam's named manipulation "
              "techniques. You take raw CIDR address data, use the IP Calculator to derive the network fields by hand "
              "first, then reproduce the same derivation in code and prove the two agree."),
        build="A dataset enriched with four derived columns (network address, broadcast, usable hosts, subnet class) verified against the calculator.",
        services="IP Calculator (https://alfredang.github.io/ipcalculator/), Killercoda Ubuntu, Python 3, ipaddress module",
        env="https://alfredang.github.io/ipcalculator/",
        steps=[
            ("Open the IP Calculator in your browser.", ""),
            ("Enter 192.168.10.0/24 and record the derived values: network, broadcast, usable host count and mask.", ""),
            ("Repeat for 10.0.5.0/22 and 172.16.8.0/29 — note how the usable-host count changes with the prefix.", ""),
            ("Switch to Killercoda and create the source dataset of raw CIDR strings.",
             "mkdir -p ~/dataplus/lab6 && cd ~/dataplus/lab6 && printf 'site,cidr\\nHQ,192.168.10.0/24\\nBranch,10.0.5.0/22\\nDMZ,172.16.8.0/29\\n' > sites.csv"),
            ("Derive the same four fields in code — this is the DERIVED VARIABLE technique from the exam objectives.",
             "python3 -c \"import pandas as pd,ipaddress as ip;d=pd.read_csv('sites.csv');n=d.cidr.map(ip.ip_network);d['network']=[str(x.network_address) for x in n];d['broadcast']=[str(x.broadcast_address) for x in n];d['usable_hosts']=[x.num_addresses-2 for x in n];d['mask']=[str(x.netmask) for x in n];print(d)\""),
            ("Compare every derived value against what the IP Calculator gave you — they must match exactly.", ""),
            ("Decide the storage trade-off the exam asks about: store the derived columns (fast reads, more space) "
             "or recompute on demand (less space, slower). Write your choice and the reason.", ""),
            ("Save the enriched dataset.",
             "python3 -c \"import pandas as pd,ipaddress as ip;d=pd.read_csv('sites.csv');n=d.cidr.map(ip.ip_network);d['network']=[str(x.network_address) for x in n];d['usable_hosts']=[x.num_addresses-2 for x in n];d.to_csv('sites_enriched.csv',index=False)\" && cat sites_enriched.csv"),
        ],
        test=("The code and the IP Calculator agree: /24 gives 254 usable hosts, /22 gives 1022, and /29 gives 6. "
              "sites_enriched.csv carries the derived columns alongside the original CIDR."),
        troubleshoot=[
            ("ValueError: has host bits set", "The address is not a valid network address for that prefix. Use ip_network(x, strict=False) or correct the CIDR."),
            ("usable_hosts is negative for /31 or /32", "Those prefixes have no usable host range by the -2 convention. Note this edge case in your report."),
            ("The numbers disagree with the calculator", "Confirm you entered the same prefix length in both. A /22 is not a /24."),
        ],
    ),
    dict(
        num=7,
        topic=2,
        title="Lab 7 — Integrate Multiple Datasets with SQL Joins and Cleanse the Result",
        objective="Use data acquisition methods: data integration and queries to gather and combine data (Domain 2); LO2 / A1 / A2.",
        desc=("This is the integration lab that LO1 and LO2 both rest on. You load three separate source extracts into "
              "SQLite, combine them with the four join types, watch how inner versus left join silently changes your "
              "record count, and then cleanse the merged result."),
        build="A single integrated, deduplicated analysis table built from three sources, with the record count reconciled at every join.",
        services="Killercoda Ubuntu, SQLite 3, SQL joins, Python 3/pandas",
        env=KILLERCODA,
        steps=[
            ("Create the lab folder and the three source extracts.",
             "mkdir -p ~/dataplus/lab7 && cd ~/dataplus/lab7"),
            ("Source A — the customer master (note: customer 4 appears here only).",
             "printf 'customer_id,name,region\\n1,Mei Tan,Central\\n2,Ravi Kumar,West\\n3,Siti Nur,North\\n4,John Lee,East\\n' > customers.csv"),
            ("Source B — the order transactions (note: customer 4 has no orders; customer 5 has orders but no master record).",
             "printf 'order_id,customer_id,amount\\n100,1,240.50\\n101,2,89.00\\n102,1,120.00\\n103,3,310.00\\n104,5,55.00\\n' > orders.csv"),
            ("Source C — the regional targets used to enrich the result.",
             "printf 'region,target\\nCentral,500\\nWest,300\\nNorth,400\\nEast,200\\n' > targets.csv"),
            ("Load all three into SQLite in one go.",
             "sqlite3 integrate.db <<'EOF'\n.mode csv\n.import customers.csv customers\n.import orders.csv orders\n.import targets.csv targets\n.headers on\nSELECT COUNT(*) AS customers FROM customers; SELECT COUNT(*) AS orders FROM orders;\nEOF"),
            ("INNER JOIN — returns only matched rows. Count them and note what you silently lost.",
             "sqlite3 -header -column integrate.db \"SELECT COUNT(*) AS inner_rows FROM orders o JOIN customers c ON c.customer_id=o.customer_id;\""),
            ("LEFT JOIN from orders — keeps order 104 whose customer is missing, showing NULL in the master fields.",
             "sqlite3 -header -column integrate.db \"SELECT o.order_id, o.customer_id, c.name FROM orders o LEFT JOIN customers c ON c.customer_id=o.customer_id;\""),
            ("LEFT JOIN from customers — keeps John Lee, who has no orders at all.",
             "sqlite3 -header -column integrate.db \"SELECT c.name, o.order_id FROM customers c LEFT JOIN orders o ON c.customer_id=o.customer_id;\""),
            ("Build the integrated analysis table joining all three sources and aggregating per region.",
             "sqlite3 -header -column integrate.db \"SELECT c.region, COUNT(o.order_id) AS orders, ROUND(SUM(o.amount),2) AS revenue, t.target FROM customers c LEFT JOIN orders o ON c.customer_id=o.customer_id JOIN targets t ON t.region=c.region GROUP BY c.region, t.target;\""),
            ("Add the derived performance measure and persist the result.",
             "sqlite3 -header -column integrate.db \"CREATE TABLE regional AS SELECT c.region, COUNT(o.order_id) AS orders, COALESCE(SUM(o.amount),0) AS revenue, t.target, ROUND(COALESCE(SUM(o.amount),0)*100.0/t.target,1) AS pct_of_target FROM customers c LEFT JOIN orders o ON c.customer_id=o.customer_id JOIN targets t ON t.region=c.region GROUP BY c.region,t.target; SELECT * FROM regional;\""),
            ("Reconcile: explain in one line why the inner join returned 4 rows but there are 5 orders.", ""),
        ],
        test=("The inner join returns 4 rows, not 5 — order 104 is dropped because customer 5 has no master record. "
              "The regional table shows East at 0% of target (John Lee ordered nothing) and Central above 70%."),
        troubleshoot=[
            ("'.import' left the header as a data row", "Older SQLite lacks --skip 1. Delete it after import: DELETE FROM customers WHERE customer_id='customer_id';"),
            ("SUM returns NULL for East", "That is correct SQL — no rows to sum. COALESCE(...,0) is what turns it into a reportable zero."),
            ("Amounts sort wrongly", "CSV import types everything as TEXT. Use CAST(amount AS REAL) or create the table with explicit types first."),
        ],
    ),
]
