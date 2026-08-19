"""
Domain 5 — Data Governance, Quality and Controls (14% of the CompTIA Data+ DA0-001 exam).
Maps to LU5 / LO5 (A4).

Labs use the Killercoda Ubuntu playground plus the browser-based Cybersecurity Threat
Simulator for the data-classification and leakage-risk reasoning.
"""

KILLERCODA = "https://killercoda.com/playgrounds/scenario/ubuntu"

DOMAIN5 = [
    dict(
        num=13,
        topic=5,
        title="Lab 13 — Classify, Mask and De-Identify a Dataset (PDPA/GDPR)",
        objective="Compare privacy and protection strategies: access control, encryption and masking (Domain 5); LO5 / A4.",
        desc=("You receive a customer extract containing NRIC numbers, emails and salaries. You classify every column by "
              "sensitivity, then apply the three protection techniques the exam distinguishes — masking, de-identification "
              "and pseudonymisation via a surrogate index field — and prove the analytical value survives the treatment."),
        build="A classification matrix for every column plus three protected versions of the dataset (masked, de-identified, pseudonymised) with the analysis still working.",
        services="Killercoda Ubuntu, Python 3, pandas, hashlib",
        env=KILLERCODA,
        steps=[
            ("Create the working folder and download this lab's dataset. The files also ship in the course repo under labs/lab-13-classify-mask-and-de-identify-a-dataset-pdpa-gdpr/data/ — download them from GitHub or copy them from the folder you cloned.",
             "mkdir -p ~/dataplus/lab13 && cd ~/dataplus/lab13 && BASE=https://raw.githubusercontent.com/tertiarycourses/TGS-2024049212-CompTIA-Certified-Data-Training/main/labs/lab-13-classify-mask-and-de-identify-a-dataset-pdpa-gdpr/data && for f in customers.csv; do curl -fsSO $BASE/$f || echo FAILED $f; done && ls -l"),
            ("CLASSIFY first. For each column write down its classification (public / internal / sensitive / confidential) "
             "and its data type tag (PII, PIFI, none). NRIC is confidential PII; salary is sensitive PIFI; dept is internal.", ""),
            ("Apply MASKING — the value stays partly visible so it can still be recognised by an authorised human.",
             "python3 -c \"import pandas as pd;d=pd.read_csv('customers.csv');d['nric']=d.nric.str[0]+'****'+d.nric.str[-1];d['email']=d.email.str.replace(r'(.).*(@.*)',r'\\1****\\2',regex=True);print(d[['cust_id','name','nric','email']])\""),
            ("Apply DE-IDENTIFICATION — the identifying columns are removed outright.",
             "python3 -c \"import pandas as pd;d=pd.read_csv('customers.csv');deid=d.drop(columns=['name','nric','email']);print(deid)\""),
            ("Apply PSEUDONYMISATION — replace the identifier with a non-reversible surrogate INDEX FIELD.",
             "python3 -c \"import pandas as pd,hashlib;d=pd.read_csv('customers.csv');d['subject_key']=d.nric.map(lambda v: hashlib.sha256(v.encode()).hexdigest()[:12]);print(d[['cust_id','subject_key','dept','salary']])\""),
            ("Prove the ANALYSIS STILL WORKS on the protected data — this is the whole point of the technique.",
             "python3 -c \"import pandas as pd,hashlib;d=pd.read_csv('customers.csv');d['subject_key']=d.nric.map(lambda v: hashlib.sha256(v.encode()).hexdigest()[:12]);print(d.groupby('dept').salary.mean().round(2))\""),
            ("Test the re-identification risk: group by postal code and find the SMALLEST group. Any group of 1 is "
             "uniquely identifying. Discuss why small groups defeat de-identification (the k-anonymity problem).",
             "python3 -c \"import pandas as pd;d=pd.read_csv('customers.csv');print(d.groupby('postal').size())\""),
            ("Save the release-ready pseudonymised extract and note who may access it under which role.",
             "python3 -c \"import pandas as pd,hashlib;d=pd.read_csv('customers.csv');d['subject_key']=d.nric.map(lambda v: hashlib.sha256(v.encode()).hexdigest()[:12]);d[['subject_key','postal','dept','salary']].to_csv('customers_release.csv',index=False)\" && cat customers_release.csv"),
        ],
        test=("Across 40 records masking shows the NRIC as S****G form. De-identification drops name, nric and email. "
              "Pseudonymisation gives a stable 12-character key, and the departmental salary averages "
              "(Operations 4006.25, Sales 4518.75, Technology 5431.25, Finance 4612.50, Marketing 4268.75) are "
              "identical to those computed on the raw data."),
        troubleshoot=[
            ("The CSV contains '404: Not Found'", "curl wrote the error page into the file. Confirm the BASE URL, re-run with -fsSO so curl fails loudly, or copy the files from the repo folder you cloned."),
            ("The email regex did not mask", "Confirm regex=True is passed to str.replace and the backreferences use \\1 and \\2."),
            ("The hash changes between runs", "SHA-256 is deterministic — if it changes, your input has stray whitespace. Strip it first."),
            ("Some postal groups are small", "That is the k-anonymity problem: a group of 1 identifies a person even with the name removed. Note which postal codes fail a k=5 threshold."),
        ],
    ),
    dict(
        num=14,
        topic=5,
        title="Lab 14 — Assess Data-Leakage Risk and Set Access Controls",
        objective="Summarize compliance requirements; compare privacy and protection strategies (Domain 5); LO5 / A4.",
        desc=("Governance is a set of decisions, not a document. You use the Cybersecurity Threat Simulator's "
              "data-leakage risk estimator to score a realistic set of handling practices, then translate the score "
              "into a concrete role-based access matrix and a retention schedule for the Lab 13 dataset."),
        build="A completed risk assessment with a before/after score, a role-based access control matrix, and a retention & destruction schedule.",
        services="Cybersecurity Threat Simulator (https://alfredang.github.io/cybersecuritysimulator/), the Lab 13 dataset",
        env="https://alfredang.github.io/cybersecuritysimulator/",
        steps=[
            ("Open the Cybersecurity Threat Simulator and go to the Data Leakage Risk Estimator.", ""),
            ("Set the toggles to describe a BAD baseline: no encryption, shared logins, no access review, data kept "
             "forever. Record the risk score and its level (Critical / High / Medium).", ""),
            ("Now switch on the controls one at a time — encryption at rest, role-based access, periodic review, "
             "defined retention. Record how much each single control moves the score.", ""),
            ("Note which single control reduced the risk most. That is where governance effort pays off first.", ""),
            ("Open the Password Strength Analyzer and test a weak versus a strong credential — this is the access "
             "control layer protecting everything you built in Lab 13.", ""),
            ("Build the ACCESS MATRIX for the Lab 13 dataset. For each of the four roles (Data Owner, Data Steward, "
             "Data Custodian, Analyst) decide access to: raw NRIC, masked extract, pseudonymised release, salary.", ""),
            ("Write the RETENTION SCHEDULE: how long is each artefact kept, what triggers destruction, and which "
             "method is used (removal vs destruction vs sanitisation)?", ""),
            ("Map each decision to its compliance driver — Singapore PDPA for the personal data, and the organisation's "
             "own audit requirement for the retention log.", ""),
        ],
        test=("Your risk score drops from Critical to Medium or lower once encryption, RBAC, review and retention are "
              "enabled. Your access matrix gives the Analyst the pseudonymised release ONLY, never the raw NRIC."),
        troubleshoot=[
            ("The score does not change", "Some toggles only affect certain threat categories. Change one at a time and re-read the score after each."),
            ("Unsure which role gets what", "Apply least privilege: the Analyst needs the analytical columns, never the identifiers. Only the Data Owner authorises raw access."),
            ("Retention period unclear", "Where no statutory period applies, set it from business need and document the rationale — an undocumented period is itself an audit finding."),
        ],
    ),
    dict(
        num=15,
        topic=5,
        title="Lab 15 — Automated Quality Assurance: Profile, Rule, Monitor",
        objective="Implement quality assurance: profiling, monitoring and testing for data quality; explain data management practices (Domain 5); LO5 / A4.",
        desc=("The capstone governance lab. You write an automated data-quality suite that tests a daily feed against "
              "explicit rules across the exam's quality dimensions — completeness, accuracy, consistency, uniqueness "
              "and validity — then run it against a clean file and a broken one so it proves it can actually fail."),
        build="A reusable dq_check.py suite that scores five quality dimensions, exits non-zero on failure, and produces a dated quality report.",
        services="Killercoda Ubuntu, Python 3, pandas",
        env=KILLERCODA,
        steps=[
            ("Create the working folder and download this lab's dataset. The files also ship in the course repo under labs/lab-15-automated-quality-assurance-profile-rule-monitor/data/ — download them from GitHub or copy them from the folder you cloned.",
             "mkdir -p ~/dataplus/lab15 && cd ~/dataplus/lab15 && BASE=https://raw.githubusercontent.com/tertiarycourses/TGS-2024049212-CompTIA-Certified-Data-Training/main/labs/lab-15-automated-quality-assurance-profile-rule-monitor/data && for f in feed_good.csv feed_bad.csv; do curl -fsSO $BASE/$f || echo FAILED $f; done && ls -l"),
                        ("Write the quality suite — one function per quality dimension.",
             "cat > dq_check.py <<'EOF'\nimport sys, pandas as pd\nVALID_STATUS = {'SHIPPED','PENDING','CANCELLED'}\n\ndef run(path):\n    d = pd.read_csv(path)\n    results = []\n    # COMPLETENESS - no required field may be null\n    nulls = d[['order_id','customer_id','order_date','amount']].isnull().sum().sum()\n    results.append(('completeness', nulls == 0, f'{nulls} null(s) in required fields'))\n    # UNIQUENESS - the primary key must be unique\n    dupes = d.order_id.duplicated().sum()\n    results.append(('uniqueness', dupes == 0, f'{dupes} duplicate order_id'))\n    # VALIDITY - amount must be positive\n    neg = (d.amount < 0).sum()\n    results.append(('validity', neg == 0, f'{neg} negative amount(s)'))\n    # CONSISTENCY - status must be from the agreed domain\n    bad = (~d.status.isin(VALID_STATUS)).sum()\n    results.append(('consistency', bad == 0, f'{bad} invalid status value(s)'))\n    # ACCURACY (proxy) - dates must parse\n    parsed = pd.to_datetime(d.order_date, errors='coerce').isnull().sum()\n    results.append(('accuracy', parsed == 0, f'{parsed} unparseable date(s)'))\n\n    passed = sum(1 for _, ok, _ in results if ok)\n    print(f'\\nDATA QUALITY REPORT - {path}')\n    print('-' * 52)\n    for dim, ok, msg in results:\n        print(f'  {\"PASS\" if ok else \"FAIL\"}  {dim:<14} {msg}')\n    print('-' * 52)\n    print(f'  SCORE: {passed}/5 dimensions passed\\n')\n    return 0 if passed == 5 else 1\n\nif __name__ == '__main__':\n    sys.exit(run(sys.argv[1]))\nEOF\necho written"),
            ("Run the suite against the GOOD feed — it must pass all five and exit 0.",
             "python3 dq_check.py feed_good.csv; echo \"exit code: $?\""),
            ("Run it against the BROKEN feed — it must fail four dimensions and exit 1.",
             "python3 dq_check.py feed_bad.csv; echo \"exit code: $?\""),
            ("This exit code is what makes it MONITORING rather than a report — a scheduler can now block a bad load.",
             "python3 dq_check.py feed_bad.csv > /dev/null 2>&1 && echo 'LOAD APPROVED' || echo 'LOAD BLOCKED - do not ingest'"),
            ("Save a dated quality report so you build a quality history, not just a snapshot.",
             "python3 dq_check.py feed_good.csv > dq_report_$(date +%Y%m%d).txt; ls -1 dq_report_*.txt"),
            ("Add the lineage note: record the source, the owner, the rule version and the run date. "
             "This is the documentation half of the exam's data-management objective.",
             "printf 'source: orders feed (daily)\\nowner: Sales Ops\\nsteward: Data Quality team\\nrules version: 1.0\\nrun: %s\\n' \"$(date +%F)\" > lineage.txt && cat lineage.txt"),
        ],
        test=("feed_good.csv (40 rows) scores 5/5 and exits 0. feed_bad.csv (40 rows) fails ALL FIVE dimensions — "
              "2 nulls, 2 duplicate order_ids, 2 negative amounts, 2 invalid status values and 1 unparseable date — "
              "so it scores 0/5, exits 1, and the 'LOAD BLOCKED' branch fires."),
        troubleshoot=[
            ("The CSV contains '404: Not Found'", "curl wrote the error page into the file. Confirm the BASE URL, re-run with -fsSO so curl fails loudly, or copy the files from the repo folder you cloned."),
            ("The heredoc breaks on the f-strings", "Ensure you used <<'EOF' with the quotes — that stops the shell expanding anything inside."),
            ("Exit code is always 0", "You ran it inside another command. Test with python3 dq_check.py feed_bad.csv; echo $? on its own line."),
            ("accuracy fails on the good feed", "Your dates are not ISO format. pandas parses YYYY-MM-DD reliably — normalise the feed first."),
        ],
    ),
]
