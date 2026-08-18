#!/usr/bin/env python3
"""Generate the WSQ CompTIA Certified Data+ Training slide deck (all-white house style).

Content is driven entirely by course_data.py + data_domain1..5.py so the deck stays
100% aligned with the Lesson Plan, Learner Guide, labs and assessment.

Engine (visual components) lives in _engine.py, extracted verbatim from the
wsq-slides v2 reference implementation: cover, section, content, two_col, cards3,
tile_grid, flow_h, process_map, decision_map, compare_table, worked_example,
chart_slide, steps_slide, trainer_slide, big_statement, activity_overview,
step_slide, test_slide, brk.
"""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from _engine import *          # noqa: F401,F403 — visual component library + prs
from _engine import (prs, C, ACTIVITIES, cover, section, content, two_col, cards3,
                     tile_grid, flow_h, process_map, decision_map, compare_table,
                     worked_example, chart_slide, steps_slide, trainer_slide,
                     big_statement, activity_overview, test_slide, brk,
                     _transition, REPO,
                     BLUE, TEAL, VIOLET, AMBER, GREY, INK)

TOPIC_OF = {t["num"]: t for t in C.TOPICS}

# --- slide map: records where each domain and lab starts/ends, for the Lesson Plan
SLIDE_MAP = {"domains": {}, "labs": {}}
def _n():
    return len(prs.slides._sldIdLst)


def acts_for(topic_num):
    return [a for a in ACTIVITIES if a["topic"] == topic_num]


def lab_unit(a):
    """Expand ONE lab into a full teaching unit:
    briefing → process map → steps (4 per slide) → verify + troubleshoot."""
    _start = _n() + 1
    t = TOPIC_OF[a["topic"]]
    kicker = f"DOMAIN {t['code']}  ·  LAB {a['num']}"
    activity_overview(
        f"LAB {a['num']}", a["title"], a["desc"], a["build"], a["services"],
        kicker, objective=a["objective"], test=a["test"])

    # process map — synthesise the run from the real steps
    st = a["steps"]
    n = len(st)
    picks = [0, max(1, n // 4), max(2, n // 2), max(3, (3 * n) // 4), n - 1]
    picks = sorted(set(p for p in picks if 0 <= p < n))[:5]
    stages = []
    for i, p in enumerate(picks):
        text = st[p][0]
        label = text.split(".")[0].split(" — ")[0].strip()
        stages.append((label[:44], f"step {p+1} of {n}"))
    process_map(f"How Lab {a['num']} Runs", stages, kicker=kicker, color=TEAL,
                synthesis=("YOU'LL PRODUCE", a["build"]))

    # procedure slides — the real commands. Long commands need a taller code block,
    # so pack fewer steps per slide when this lab's commands are long.
    # A heredoc script is collapsed to a one-line pointer by the engine, so it does not
    # need extra room — measure the effective (rendered) command length instead.
    def _eff(c):
        if "<<'EOF'" in c or '<<"EOF"' in c or c.count("\n") >= 4:
            return len(c.split("\n")[0]) + 44      # + the pointer comment
        return len(" ".join(c.split()))
    longest = max((_eff(c) for _, c in st if c), default=0)
    per = 4 if longest <= 150 else 3
    total = math.ceil(len(st) / per)
    for i in range(total):
        chunk = st[i * per:(i + 1) * per]
        part = f"Procedure {i+1} of {total}" if total > 1 else "Procedure"
        steps_slide(a["title"], chunk, kicker, accent=TEAL,
                    part=part, start=i * per + 1)

    test_slide(f"Lab {a['num']} — Verify Your Work", a["test"], kicker,
               troubleshoot=a.get("troubleshoot"))
    if a.get("figure"):
        img_full(f"Lab {a['num']} — Expected Output", a["figure"],
                 f"This is what your own run should produce. {a['test']}", kicker)
    SLIDE_MAP["labs"][a["num"]] = [_start, _n()]


def img_full(title, figname, caption, kicker):
    """Full-width figure slide — aspect-fit, never stretched, with a caption band."""
    from _engine import slide, head, rect, txt, footer, Inches, Emu, LIGHT
    import os as _os
    from PIL import Image
    path = _os.path.join(REPO, "courseware", "assets", figname)
    s2 = head(slide(), title, kicker, kcolor=TEAL)
    if _os.path.exists(path):
        iw, ih = Image.open(path).size
        maxw, maxh = Inches(11.63), Inches(3.75)
        scale = min(maxw / iw, maxh / ih)
        w, h = int(iw * scale), int(ih * scale)
        x = int(Inches(0.85) + (maxw - w) / 2)
        s2.shapes.add_picture(path, x, Inches(1.95), width=w, height=h)
    by = Inches(5.95)
    rect(s2, Inches(0.85), by, Inches(11.63), Inches(1.0), LIGHT)
    rect(s2, Inches(0.85), by, Inches(0.11), Inches(1.0), TEAL)
    txt(s2, Inches(1.15), int(by + Inches(0.1)), Inches(11.1), Inches(0.3),
        [[("WHAT YOU SHOULD SEE", 11, TEAL, True)]])
    # trim on a SENTENCE boundary — a caption cut mid-clause reads as a defect
    cap = " ".join(str(caption).split())
    if len(cap) > 240:
        cut = cap[:240]
        dot = max(cut.rfind(". "), cut.rfind("! "))
        cap = (cut[:dot + 1] if dot > 90 else cut.rsplit(" ", 1)[0] + " …")
    txt(s2, Inches(1.15), int(by + Inches(0.42)), Inches(11.1), Inches(0.52),
        [[(cap, 11.5, INK, False)]])
    footer(s2)
    return s2

# ============================================================ BUILD
cover()

# ---------------------------------------------------------------- ADMIN
section("COURSE ADMINISTRATION", "Welcome & Housekeeping", "")

tile_grid("Digital Attendance (Mandatory)", [
 ("Three times a day", "Take the AM, PM and Assessment digital attendance — mandatory for every WSQ-funded course."),
 ("Trainer shows the QR", "The trainer or administrator displays the digital attendance QR code generated from TPG."),
 ("Scan with Singpass", "Scan the QR code from your Singpass App and submit your attendance."),
 ("75% minimum", "A minimum of 75% attendance is required to be eligible for assessment and funding.")],
 kicker="TRAQOM · SSG DIGITAL ATTENDANCE", cols=2, size=15)

trainer_slide("YOUR TRAINER · GENERAL", "Your Trainer",
 "General Trainer template —\nto be completed by the trainer",
 [("Name", ""), ("Title / Designation", ""), ("Qualifications", ""),
  ("Areas of expertise", ""), ("Training & industry experience", ""), ("Contact", "")],
 initials="?", accent=GREY)

trainer_slide("YOUR TRAINER", C.TRAINER,
 "Principal Trainer\nTertiary Infotech Academy Pte Ltd",
 [("Role", "Principal Trainer, Tertiary Infotech Academy Pte Ltd"),
  ("Expertise", "Data analytics, data engineering, statistics, business intelligence and applied machine learning."),
  ("Delivers", "WSQ courses on data analytics, CompTIA certifications, Python, AI and cloud technologies."),
  ("Founder", "Founder and lead instructor at Tertiary Infotech / Tertiary Courses.")],
 initials="AA", accent=BLUE)

content("Let's Know Each Other", [
 "Your name, organisation and current role.",
 "How you work with data today — spreadsheets, SQL, BI tools, or none of these yet.",
 "The one data question in your job you wish you could answer confidently.",
 "Whether you intend to sit the CompTIA Data+ (DA0-001) certification exam."],
 kicker="ICE-BREAKER")

tile_grid("Ground Rules", [
 "Set your mobile phone to silent mode.",
 "Participate actively in class — no question is too small.",
 "Mutual respect: agree to disagree.",
 "One conversation at a time.",
 "Be punctual and return from breaks on time.",
 "Step out quietly for calls or breaks.",
 "75% attendance is required for funding.",
 "Complete both assessments to be certified Competent."],
 kicker="HOUSEKEEPING", cols=2, size=15)

tile_grid("Download Your Course Material", [
 ("1 · Go to the LMS portal", "Open https://lms-tms.tertiaryinfotech.com in your browser."),
 ("2 · Log in", "Sign in with the account e-mail you used to register for this course."),
 ("3 · Open this course", f"Select '{C.TITLE}' ({C.COURSE_CODE})."),
 ("4 · Download", "Download the Trainer Slides, Learner Guide and Lesson Plan (PDF)."),
 ("5 · Get the labs", "Clone or download the lab repository from GitHub — link on the next slide."),
 ("6 · Keep them open", "You may use these materials during the open-book assessment.")],
 kicker="LMS / TMS  ·  lms-tms.tertiaryinfotech.com", cols=2, size=14)

tile_grid("Skills Framework Alignment", [
 ("TSC Title", C.TSC_TITLE),
 ("TSC Code", C.TSC_CODE),
 ("K1 · K2", "Tools and techniques for data collection, mining, cleaning and analysis; statistical principles."),
 ("K3 · K4", "Principles of communicating data effectively; procedures to extract and process data sets."),
 ("A1 · A2 · A3", "Integrate multiple datasets; conduct data mining to uncover trends; derive actionable insights."),
 ("A4 · A5", "Recognise sequential and sub-graph patterns; present analytics outputs visually.")],
 kicker="SKILLS FRAMEWORK  ·  TSC", cols=2, size=14, accent=VIOLET)

tile_grid("Learning Outcomes", [
 ("LO1 · Integrate datasets", "Integrate multiple datasets to extract and process data efficiently. (K4, A1)"),
 ("LO2 · Mine for trends", "Conduct data mining to uncover and analyze trends using analysis techniques. (K1, A2)"),
 ("LO3 · Analyse statistically", "Perform statistical data analysis to derive actionable insights. (K2, A3)"),
 ("LO4 · Communicate visually", "Present analytical outputs visually to communicate data effectively for decision-making. (K3, A5)"),
 ("LO5 · Link the variables", "Recognize and interpret sequential patterns to establish linkages between variables. (A4)")],
 kicker="WHAT YOU'LL ACHIEVE", cols=1, size=14)

tile_grid("Course Outline — Five Exam Domains", [
 (f"Domain 1 — {C.TOPICS[0]['title']}  ({C.TOPICS[0]['weighting']})", C.TOPICS[0]["subtitle"]),
 (f"Domain 2 — {C.TOPICS[1]['title']}  ({C.TOPICS[1]['weighting']})", C.TOPICS[1]["subtitle"]),
 (f"Domain 3 — {C.TOPICS[2]['title']}  ({C.TOPICS[2]['weighting']})", C.TOPICS[2]["subtitle"]),
 (f"Domain 4 — {C.TOPICS[3]['title']}  ({C.TOPICS[3]['weighting']})", C.TOPICS[3]["subtitle"]),
 (f"Domain 5 — {C.TOPICS[4]['title']}  ({C.TOPICS[4]['weighting']})", C.TOPICS[4]["subtitle"])],
 kicker=f"FIVE DOMAINS  ·  {len(ACTIVITIES)} HANDS-ON LABS", cols=1, size=13)

chart_slide("How the CompTIA Data+ Exam Is Weighted",
 [f"D{t['num']} {t['title'].split(' and ')[0][:22]}" for t in C.TOPICS],
 [("% of exam", [int(t["weighting"].rstrip("%")) for t in C.TOPICS])],
 kicker="EXAM BLUEPRINT  ·  DA0-001", accent=BLUE, kind="column",
 insight="Data Analysis (24%) and Data Acquisition & Preparation (22%) together make up 46% of the exam — "
         "which is why Days 2 and 3 carry the heaviest lab load.")

two_col(f"Lesson Plan — Days 1 to 3", [
 (f"Day 1 — {C.DAY_THEMES[1]}", 0),
 ("Digital Attendance (AM) · Introductions", 1),
 ("Learning Outcomes · Course Outline", 1),
 ("Domain 1: Data Concepts (Labs 1–3)", 1),
 ("Lunch · Digital Attendance (PM)", 1),
 (f"Day 2 — {C.DAY_THEMES[2]}", 0),
 ("Domain 2: Acquisition & Preparation", 1),
 ("Labs 4–7 · profiling, parsing, joins", 1)],
 [(f"Day 3 — {C.DAY_THEMES[3]}", 0),
 ("Domain 3: Data Analysis", 1),
 ("Descriptive statistics (Lab 8)", 1),
 ("Hypothesis testing (Lab 9)", 1),
 ("Correlation and regression (Lab 10)", 1),
 ("Every day", 0),
 ("9:00 am – 6:00 pm · 8 training hours", 1),
 ("1-hour lunch; tea breaks within", 1)],
 kicker="SCHEDULE  ·  1 OF 2", lhead="Days 1 and 2", rhead="Day 3")

two_col(f"Lesson Plan — Days 4 and 5", [
 (f"Day 4 — {C.DAY_THEMES[4]}", 0),
 ("Domain 4: Visualization and Reporting", 1),
 ("Chart selection (Lab 11)", 1),
 ("KPI dashboard and validation (Lab 12)", 1),
 ("Report types and design principles", 1),
 ("Lunch · Digital Attendance (PM)", 1)],
 [(f"Day 5 — {C.DAY_THEMES[5]}", 0),
 ("Domain 5: Governance, Quality, Controls", 1),
 ("Labs 13–15 · protect, assess risk, automate QA", 1),
 ("Revision across all five domains", 1),
 ("Course Feedback and TRAQOM Survey", 1),
 ("Digital Attendance (Assessment)", 1),
 ("Final Assessment 4:00–6:00 PM", 1),
 ("WA (1 hr) then PP (1 hr) · open book", 1)],
 kicker="SCHEDULE  ·  2 OF 2", lhead="Day 4", rhead="Day 5")

tile_grid("Your Lab Environment", [
 (t[0], f"{t[2]}  ·  {t[1]}") for t in C.LAB_TOOLS],
 kicker="TOOLS YOU'LL USE  ·  ALL BROWSER-BASED", cols=1, size=13, accent=TEAL)

# Access the hands-on labs — with REAL clickable hyperlinks
def labs_access_slide():
    from _engine import slide, head, rect, txt, footer, Inches, Pt, PP_ALIGN, MSO_ANCHOR, LIGHT, WHITE
    s = head(slide(), "Access the Hands-On Labs", "GITHUB  ·  ALL 15 LABS", kcolor=BLUE)
    # repo URL as a real hyperlink
    rect(s, Inches(0.85), Inches(1.9), Inches(11.63), Inches(0.78), LIGHT)
    rect(s, Inches(0.85), Inches(1.9), Inches(0.11), Inches(0.78), BLUE)
    tb = s.shapes.add_textbox(Inches(1.2), Inches(2.02), Inches(11.0), Inches(0.55))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]
    r0 = p.add_run(); r0.text = "Repository:  "
    r0.font.size = Pt(13); r0.font.name = "Arial"; r0.font.color.rgb = GREY
    r = p.add_run(); r.text = C.REPO_URL
    r.font.size = Pt(14); r.font.bold = True; r.font.name = "Arial"; r.font.color.rgb = BLUE
    r.hyperlink.address = C.REPO_URL
    cards = [(BLUE, "OPTION A · CLONE",
              ["Open the Killercoda Ubuntu playground.",
               f"git clone {C.REPO_URL}.git",
               "cd into the labs folder and start Lab 1."]),
             (TEAL, "OPTION B · DOWNLOAD ZIP",
              ["Open the repository page on GitHub.",
               "Click the green Code button → Download ZIP.",
               "Unzip it and open the labs folder."])]
    xs = [Inches(0.85), Inches(6.95)]
    for (col, hdr, items), x in zip(cards, xs):
        rect(s, x, Inches(3.0), Inches(5.53), Inches(2.6), LIGHT)
        rect(s, x, Inches(3.0), Inches(5.53), Inches(0.12), col)
        txt(s, x + Inches(0.3), Inches(3.22), Inches(5.0), Inches(0.4), [[(hdr, 15, col, True)]])
        for i, it in enumerate(items):
            txt(s, x + Inches(0.3), Inches(3.72) + Inches(0.55) * i, Inches(5.0), Inches(0.5),
                [[("•  " + it, 12, INK, False)]])
    rect(s, Inches(0.85), Inches(5.9), Inches(11.63), Inches(0.95), LIGHT)
    rect(s, Inches(0.85), Inches(5.9), Inches(0.11), Inches(0.95), TEAL)
    txt(s, Inches(1.2), Inches(6.02), Inches(11.0), Inches(0.32), [[("NO INSTALL NEEDED", 11, TEAL, True)]])
    txt(s, Inches(1.2), Inches(6.34), Inches(11.0), Inches(0.42),
        [[("Every lab runs free in the browser on the Killercoda Ubuntu playground — "
           "https://killercoda.com/playgrounds/scenario/ubuntu", 12, INK, False)]])
    footer(s)
labs_access_slide()

tile_grid("Briefing for Assessment", [
 ("Do · Clear your desk", "Place phones and other materials under the table or on the floor."),
 ("Don't · No recording", "No photos or recording of assessment scripts."),
 ("Don't · No discussion", "Work individually — no discussion during the assessment."),
 ("Do · Black or blue pen", "Use a black or blue pen for hard-copy assessments."),
 ("Don't · No correction fluid", "No liquid paper or correction tape may be used."),
 ("Do · Stop on time", "Assessment scripts are collected when the time is up.")],
 kicker="BEFORE YOU START", cols=2, size=14, accent=AMBER)

tile_grid("Assessment", [
 ("Written Assessment (WA)", "Short-Answer Questions (SAQ) · 1 hour · individual · summative · open book."),
 ("Practical Performance (PP)", "Scenario-based hands-on data tasks · 1 hour · individual · summative · open book."),
 ("Open book means", "Course slides, the Learner Guide and other approved materials only."),
 ("Eligibility", "A minimum of 75% attendance is required to be eligible for assessment and funding."),
 ("Result", "You are assessed Competent (C) or Not Yet Competent (NYC) on each instrument."),
 ("Appeals", "An appeal process is available if you wish to contest an assessment outcome.")],
 kicker="FINAL ASSESSMENT", cols=2, size=14)

process_map("Assessment Flow", [
 ("TRAQOM attendance", "Scan the QR on the LMS"),
 ("Assessment attendance", "Scan the SSG QR"),
 ("Sit WA then PP", "Open book · 1 hour each"),
 ("Submit on the LMS", "Upload your answers"),
 ("Sign the record", "Assessment Summary Record")],
 kicker="ON ASSESSMENT DAY", color=BLUE,
 synthesis=("REMEMBER", "All five steps are mandatory for WSQ funding — missing the TRAQOM digital attendance "
                        "or the course feedback survey can invalidate your claim."))

tile_grid("Criteria for Funding", [
 ("Attendance", "A minimum attendance rate of 75%, based on the SSG Digital Attendance record."),
 ("Assessment", "Complete both assessment components and be assessed as 'Competent'."),
 ("Digital attendance", "Scan the SSG QR code for AM, PM and Assessment on every training day."),
 ("Course feedback", "Complete the mandatory course feedback / TRAQOM survey on the LMS.")],
 kicker="WSQ FUNDING", cols=2, size=15, accent=AMBER)

# ================================================================ DOMAIN 1
t1 = C.TOPICS[0]
_d1_start = _n() + 1
section(f"DOMAIN {t1['code']}  ·  {t1['weighting']} OF THE EXAM", t1["title"], "01", t1["subtitle"])

tile_grid("Domain 1 — Key Concepts",
 list(zip(["Schemas are designed first","Relational vs non-relational","Normalise, then denormalise",
           "OLTP vs OLAP","Warehouse, mart, lake, lakehouse","Structure and file formats",
           "Cloud, containers and AI"], t1["concepts"])),
 kicker="WHAT THIS DOMAIN COVERS", cols=1, size=12)

big_statement("A schema is a plan, not an afterthought.",
 "A data schema describes both the organisation of the data and the relationships between tables. "
 "Database engineers design the schema BEFORE they create the system — because changing it later means migrating every row.",
 "DATA SCHEMAS", color=BLUE)

compare_table("Relational vs Non-Relational Databases",
 ["Characteristic", "Relational (SQL)", "Non-Relational (NoSQL)"],
 [["Structure", "Tables of rows and columns", "Documents, key-value, column or graph"],
  ["Schema", "Fixed, defined before loading", "Flexible, schema-on-read"],
  ["Query language", "SQL — standard across vendors", "Vendor APIs, GraphQL, MongoDB query"],
  ["Field limits", "Typed, length-constrained fields", "Store as much as you want per key"],
  ["Scaling", "Vertical — a bigger server", "Horizontal — add more nodes"],
  ["Best for", "Transactions, integrity, joins", "Huge volume, varied or unstructured data"],
  ["Examples", "MySQL, MariaDB, PostgreSQL, Aurora", "MongoDB, Redis, Cassandra, Neo4j"]],
 kicker="DATABASE TYPES", accent=BLUE,
 note="Remember for the exam: SQL = relational. NoSQL or GraphQL = non-relational.")

tile_grid("The Four Non-Relational Database Types", [
 ("Document-oriented", "Stores each record as a self-describing XML or JSON document. Example: MongoDB, CouchDB."),
 ("Key-value store", "Stores each value against a unique key — the simplest and fastest model. Example: Redis, DynamoDB."),
 ("Column-oriented", "Stores data down columns instead of across rows, which makes analytical scans very fast. Example: Cassandra, HBase."),
 ("Graph store", "Stores entities as nodes and relationships as edges, so linked queries are cheap. Example: Neo4j, Amazon Neptune.")],
 kicker="NoSQL FAMILIES", cols=2, size=14, accent=TEAL)

process_map("Normalisation — 1NF to 5NF", [
 ("1NF", "No repeating groups"),
 ("2NF", "No partial key deps"),
 ("3NF", "No transitive deps"),
 ("4NF", "No multi-valued deps"),
 ("5NF", "No join dependencies")],
 kicker="DATA NORMALIZATION", color=BLUE,
 synthesis=("THE GOAL", "Normalisation removes redundancy so an update happens in exactly one place. "
                        "Each form builds on the one before it."))

decision_map("Should I Normalise or Denormalise?",
 "Is this database serving transactions or analytics?",
 ("NORMALISE  →  OLTP", "Many small writes, integrity matters most. Remove every redundancy so an update touches one row. This is your operational database."),
 ("DENORMALISE  →  OLAP", "Few huge reads, speed matters most. Deliberately repeat data to avoid expensive joins. This is your warehouse, mart or reporting layer."),
 kicker="DESIGN DECISION", color=VIOLET,
 note="Data warehousing, mining, analysis and visualization all work on deliberately denormalised data.")

tile_grid("Keys and Relationships", [
 ("Primary key", "A unique identifier for a record that cannot contain duplicates or nulls. Every table needs one."),
 ("Foreign key", "A primary key from one table referenced by another — this is what creates the relationship."),
 ("One-to-one", "One record relates to exactly one record in the other table (person ↔ passport)."),
 ("One-to-many", "One record relates to many records in another table (customer → many orders)."),
 ("Many-to-many", "Many records relate to many others, resolved with a junction table (students ↔ courses)."),
 ("Referential integrity", "Guarantees every foreign key value actually exists in the parent table — no orphans.")],
 kicker="DATABASE RELATIONSHIPS", cols=2, size=14)

big_statement("Cascade your changes, or orphan your data.",
 "When a parent record is updated or deleted, ON UPDATE CASCADE and ON DELETE CASCADE push that change through "
 "every dependent record. Without them, deleting a customer leaves their orders pointing at nothing — the classic integrity failure you will build and break in Lab 1.",
 "REFERENTIAL INTEGRITY", color=AMBER)

compare_table("OLTP vs OLAP — Two Different Jobs",
 ["Characteristic", "OLTP", "OLAP"],
 [["Purpose", "Run the business", "Analyse the business"],
  ["Transaction type", "Insert, update, delete, small query", "Long, complex analytical query"],
  ["Volume per query", "One or a few rows", "Millions of rows"],
  ["Users", "Many concurrent operational users", "Fewer analysts and reports"],
  ["Data model", "Normalised (3NF)", "Denormalised (star / snowflake)"],
  ["Example", "Point-of-sale, booking system", "Data warehouse, BI dashboard"]],
 kicker="DATA SYSTEMS", accent=TEAL,
 note="Choosing the wrong system is a classic cause of performance problems — a heavy analytical query on an OLTP database will lock up the business.")

process_map("From Source System to Insight", [
 ("Source systems", "Clickstream, sales"),
 ("Ingest / ETL", "Extract, transform, load"),
 ("Data warehouse", "Single source of truth"),
 ("Data marts", "Departmental subsets"),
 ("Reports & BI", "The decision")],
 kicker="DATA WAREHOUSE ARCHITECTURE", color=BLUE,
 synthesis=("WHY IT MATTERS", "The warehouse combines many source systems into one consistent, efficient place — "
                              "the single source of truth every report can agree on."))

compare_table("Star vs Snowflake Schema",
 ["Aspect", "Star Schema", "Snowflake Schema"],
 [["Shape", "Fact table with one ring of dimensions", "Dimensions branch into further dimensions"],
  ["Dimension depth", "One level — denormalised", "Multiple levels — normalised"],
  ["Joins per query", "Fewer", "More"],
  ["Query speed", "Faster", "Slower"],
  ["Storage", "More redundancy, more space", "Less redundancy, less space"],
  ["Maintenance", "Simpler to query, more to update", "Harder to query, easier to update"]],
 kicker="WAREHOUSE SCHEMAS", accent=VIOLET,
 note="A fact table holds the measures and the keys; a dimension table holds the descriptive attributes.")

tile_grid("Warehouse · Mart · Lake · Lakehouse", [
 ("Data warehouse", "Structured, schema-on-write, single source of truth. Built for reliable, repeatable reporting."),
 ("Data mart", "A subset of the warehouse for one department, so their queries do not slow anyone else down."),
 ("Data lake", "A centralised repository holding structured AND unstructured data cheaply, schema-on-read."),
 ("Data lakehouse", "Queries data in place on the lake using an added schema layer — lake economics, warehouse queries."),
 ("OLAP cube", "A pre-aggregated multi-dimensional structure that answers expected queries almost instantly."),
 ("Choosing", "Structured and well-understood → warehouse. Varied, raw and high-volume → lake or lakehouse.")],
 kicker="STORAGE ARCHITECTURES", cols=2, size=14, accent=TEAL)

tile_grid("Slowly Changing Dimensions", [
 ("The problem", "A dimension table holds descriptive metadata — but names, addresses and categories change over time."),
 ("Type 1", "Overwrite the old value. Simple, but the history is gone forever — you can never query the old name."),
 ("Type 2", "Add a new row with effective dates. Keeps the COMPLETE history, at the cost of more rows."),
 ("Type 3", "Add a 'previous value' column. Keeps current and prior only — a compromise between Type 1 and Type 2.")],
 kicker="CHANGING DIMENSIONAL DATA", cols=2, size=14, accent=AMBER)

compare_table("Quantitative vs Qualitative Data",
 ["", "Quantitative (numeric)", "Qualitative (categorical)"],
 [["Definition", "Measured with numbers", "Grouped by a quality or category"],
  ["Sub-type 1", "Discrete — countable whole values (orders)", "Nominal — named, no order (city, colour)"],
  ["Sub-type 2", "Continuous — any value in a range (weight)", "Ordinal — ordered categories (small/medium/large)"],
  ["Maths allowed", "Full arithmetic — sum, mean, SD", "Counts and modes only"],
  ["Typical chart", "Histogram, line, scatter", "Bar chart, pie chart"]],
 kicker="TYPES AND CHARACTERISTICS OF DATA", accent=BLUE,
 note="Getting this wrong is the root cause of nonsense analysis — you cannot take the mean of a postal code.")

tile_grid("Data Field Types", [
 ("Character / text / string", "Alphanumeric. A number stored as text CANNOT be used in arithmetic until it is converted."),
 ("Numeric — integer", "Whole numbers only. Use for counts, IDs and quantities."),
 ("Numeric — decimal / float", "Fractional values. Beware floating-point rounding in financial calculations."),
 ("Currency", "A special numeric type fixed at two decimal places, representing money."),
 ("Date / datetime", "A calendar date, optionally with a time. Decide the format and the century convention up front."),
 ("Boolean", "Exactly two values — true/false, yes/no, 1/0. The basis of all logical operations.")],
 kicker="DATA TYPES", cols=2, size=14)

big_statement("Data is dynamic, not static.",
 "Just because a value was stored as text does not mean it must stay text. Converting a text field to an integer, "
 "decimal or date is a routine, expected part of preparation — and it is what makes calculation possible.",
 "CONVERTING DATA", color=TEAL)

compare_table("Structured · Semi-Structured · Unstructured",
 ["", "Structured", "Semi-structured", "Unstructured"],
 [["Organisation", "Fixed rows and columns", "Self-describing tags/keys", "None"],
  ["Schema", "Defined before loading", "Carried inside the file", "No schema at all"],
  ["Examples", "SQL tables, CSV", "JSON, XML, HTML, e-mail", "Text, images, audio, video"],
  ["Storage", "Relational database", "Document store, lake", "Blob (Azure) / Bucket (AWS)"],
  ["Query effort", "Low — query directly", "Moderate — parse then query", "High — extract before you can query"]],
 kicker="DATA STRUCTURES", accent=VIOLET,
 note="You measure this difference yourself in Lab 2 — the same record in all three forms.")

tile_grid("File Formats and Extensions", [
 (".CSV", "Comma-separated values — the universal flat file. One record per line."),
 (".TSV / .TAB", "Tab-separated. Safer than CSV when the data itself contains commas."),
 (".TXT", "Plain text with any delimiter you choose — pipe, semicolon, fixed width."),
 (".JSON", "JavaScript Object Notation. Self-describing, nestable, the de facto format for APIs."),
 (".XML", "Extensible Markup Language. Tag-based, built to TRANSFER data rather than display it."),
 (".XLSX / .PARQUET", "Spreadsheet workbook; and Parquet, a compressed columnar format built for analytics.")],
 kicker="FILE EXTENSIONS", cols=2, size=13, accent=TEAL)

tile_grid("Data Languages and Markup", [
 ("SQL", "The structured query language. SELECT chooses fields, FROM chooses tables, WHERE filters rows."),
 ("HTML", "Hypertext Markup Language — tags that tell a browser how to DISPLAY a page. Semi-structured."),
 ("XML", "Similar tags to HTML, but the purpose is to TRANSFER data between systems, not display it."),
 ("JSON", "Arrays and key-value objects — lighter than XML and native to JavaScript and web APIs."),
 ("Python", "General-purpose language dominant in data preparation, analysis and machine learning."),
 ("R", "A language built specifically for statistical computing and graphics.")],
 kicker="DATA LANGUAGES", cols=2, size=14)

tile_grid("Infrastructure — Where Data Lives", [
 ("On-premise", "Servers you own and run in your own facility. Maximum control, maximum capital cost."),
 ("Cloud", "Infrastructure rented on demand from AWS, Azure or Google Cloud. Elastic and operational-cost based."),
 ("Hybrid", "Sensitive data stays on-premise; burst analytical workloads run in the cloud."),
 ("Storage tiers", "Hot storage for active data, cold and archive tiers for cheap long-term retention."),
 ("Containerisation", "Docker packages an application with its dependencies so it runs identically anywhere."),
 ("Orchestration", "Kubernetes schedules and scales those containers across a cluster automatically.")],
 kicker="INFRASTRUCTURE CONCEPTS", cols=2, size=14, accent=BLUE)

tile_grid("AI Concepts in the Data Toolchain", [
 ("Machine learning", "Models learn patterns from historical data to classify or predict, rather than being explicitly programmed."),
 ("Supervised vs unsupervised", "Supervised learns from labelled examples; unsupervised finds structure such as clusters in unlabelled data."),
 ("Natural language processing", "Lets systems parse, classify and generate human language — sentiment analysis, entity extraction, summarisation."),
 ("Large language models", "NLP models trained at scale that generate text; increasingly used to draft queries and explain results."),
 ("Robotic process automation", "Software robots that perform repetitive, rule-based data tasks — extraction, entry, reconciliation."),
 ("Where analysts meet AI", "Most often in data preparation, anomaly detection, forecasting and automated report narratives.")],
 kicker="AI CONCEPTS", cols=2, size=13, accent=VIOLET)

tile_grid("Identifying Data Sources", [
 ("Databases", "Relational and NoSQL operational systems — usually the most reliable and best-documented source."),
 ("APIs", "A defined request/response contract between systems. Pull model polls; push model notifies on change."),
 ("Website data", "Web scraping with Selenium, BeautifulSoup or Scrapy. Fragile, and you must have permission."),
 ("Files", "CSV, Excel, JSON and XML extracts, often the practical reality of inter-company data exchange."),
 ("Logs & machine data", "Server, application and device telemetry — high volume, and the basis of predictive maintenance."),
 ("Repositories", "Public and licensed datasets: data.gov, Kaggle, Pew Research, GeoPostcodes, Singapore's data.gov.sg.")],
 kicker="DATA SOURCES", cols=2, size=13, accent=TEAL)

# --- Domain 1 labs
for a in acts_for(1):
    lab_unit(a)

tile_grid("Recap — Data Concepts and Environments", [
 ("Schemas", "Schemas define both organisation and relationships, and are designed before the system is built."),
 ("Relational vs NoSQL", "Relational databases use SQL and fixed tables; non-relational stores trade schema for scale and flexibility."),
 ("Normalisation", "Normalisation removes redundancy for OLTP; denormalisation restores it for fast OLAP analysis."),
 ("Keys & integrity", "Primary and foreign keys plus referential integrity are what stop your data becoming orphaned."),
 ("Storage architectures", "Warehouses, marts, lakes and lakehouses trade structure, cost and query flexibility against each other."),
 ("Structure & formats", "Data is structured, semi-structured or unstructured, and arrives in CSV, JSON, XML, XLSX or Parquet."),
 ("Infrastructure & AI", "Infrastructure may be on-premise, cloud, hybrid or containerised — and AI/NLP/RPA are now part of the toolchain.")],
 kicker="DOMAIN 01 RECAP", cols=1, size=12)
SLIDE_MAP["domains"][1] = [_d1_start, _n()]

brk("Lunch Break", "1 hour")

# ================================================================ DOMAIN 2
t2 = C.TOPICS[1]
_d2_start = _n() + 1
section(f"DOMAIN {t2['code']}  ·  {t2['weighting']} OF THE EXAM", t2["title"], "02", t2["subtitle"])

tile_grid("Domain 2 — Key Concepts",
 list(zip(["ETL vs ELT","Where data comes from","Profile before you trust",
           "The four defect classes","Cleansing techniques","Manipulation techniques",
           "Joins, filters and indexes"], t2["concepts"])),
 kicker="WHAT THIS DOMAIN COVERS", cols=1, size=12)

process_map("The ETL Pipeline", [
 ("Extract", "Pull from the source"),
 ("Transform", "Clean, convert, conform"),
 ("Load", "Write to the warehouse"),
 ("Validate", "Reconcile the counts"),
 ("Schedule", "Repeat on a cadence")],
 kicker="DATA ACQUISITION", color=BLUE,
 synthesis=("THE RULE", "In ETL the data is transformed BEFORE it lands — so what arrives in the warehouse is already conformed and trustworthy."))

compare_table("ETL vs ELT — When to Use Which",
 ["Aspect", "ETL", "ELT"],
 [["Order", "Extract → Transform → Load", "Extract → Load → Transform"],
  ["Transform runs", "In a staging/processing layer", "Inside the target platform"],
  ["Target", "Data warehouse", "Data lake / lakehouse / cloud warehouse"],
  ["Schema", "Schema-on-write, decided up front", "Schema-on-read, decided at query time"],
  ["Best when", "Requirements are stable and known", "You want to keep raw data for future, unknown uses"],
  ["Trade-off", "Clean on arrival, less flexible", "Flexible, but transformation debt accumulates"]],
 kicker="INTEGRATION METHODS", accent=TEAL,
 note="Use ELT when you are landing into a data lake — hold the raw data and transform it when the question is known.")

tile_grid("Loading Strategies and Frequency", [
 ("Full load", "Every row is loaded every time. Simple and self-correcting, but slow and expensive at scale."),
 ("Delta / incremental load", "Only new or changed records since the last run. Fast, but you must track the watermark reliably."),
 ("Batch processing", "Large volumes processed on a schedule — nightly, hourly. The default for reporting."),
 ("Real-time / streaming", "Records processed as they arrive. Needed when the decision cannot wait for the batch."),
 ("Transaction processing", "Large volumes of individual transactions handled synchronously as they occur."),
 ("Distributed processing", "Very large datasets split across many servers so they can be processed in parallel.")],
 kicker="LOADING DATA", cols=2, size=14)

compare_table("API Pull vs Push",
 ["Aspect", "Pull model", "Push model"],
 [["Who initiates", "Your system requests the data", "The source notifies you when data changes"],
  ["Timing", "On your schedule — polling", "On the source's event — webhook"],
  ["Freshness", "As fresh as your polling interval", "Near real-time"],
  ["Cost", "Wasted calls when nothing changed", "Efficient, but needs a listener endpoint"],
  ["Failure mode", "You miss changes between polls", "A missed notification is lost unless retried"]],
 kicker="APPLICATION PROGRAMMING INTERFACES", accent=BLUE,
 note="Understanding the FREQUENCY of change in the source is what tells you which model you need.")

tile_grid("Acquisition Methods and Their Risks", [
 ("Database query", "Most reliable — typed, documented, joinable. Use it whenever the source offers it."),
 ("API", "A defined contract, usually JSON over HTTPS. Watch rate limits, pagination and authentication."),
 ("Web scraping", "Selenium, BeautifulSoup, Scrapy. FRAGILE — a layout change breaks it — and you must have permission."),
 ("Public repositories", "data.gov.sg, data.gov, Kaggle, Pew Research, GeoPostcodes. Check the licence and the currency of the data."),
 ("Survey data", "Bias is the enemy. Cover the whole range of responses; use a Likert scale for shades of opinion."),
 ("Sampling & observation", "Random, systematic or stratified sampling reduces volume — but a biased sample invalidates everything downstream.")],
 kicker="WHERE THE DATA COMES FROM", cols=2, size=13, accent=TEAL)

big_statement("Profile before you trust. Always.",
 "Data profiling is the disciplined first pass over any new dataset: identify the source, the field names and types, "
 "the keys, the row count and what the values actually contain. Skipping it is how a wrong number reaches the board.",
 "DATA PROFILING", color=VIOLET)

process_map("The Data Profiling Procedure", [
 ("Identify the source", "Where did this come from?"),
 ("Inventory the fields", "Names and data types"),
 ("Find the keys", "Primary, natural, foreign"),
 ("Quantify defects", "Nulls, dupes, outliers"),
 ("Document it", "Record what you found")],
 kicker="DATA EXPLORATION", color=VIOLET,
 synthesis=("THE OUTPUT", "A written profile that says how bad the data is BEFORE you clean it — your baseline for measuring the cleaning."))

tile_grid("The Four Defect Classes You Must Find", [
 ("Missing values (NULL)", "Blank, NULL or N/A. Causes: not applicable, never collected, mismatched fields, incomplete survey."),
 ("Duplicated data", "The same record repeated within one dataset. Inflates every count, sum and average."),
 ("Redundant data", "Identical data stored in multiple places. Not always wrong — but it must be reconciled."),
 ("Invalid data", "Wrong type, hard-coded values, invisible/non-printable ASCII characters, leading and trailing spaces."),
 ("Outliers", "Values far outside the normal distance from the rest. May be an error — or the most important signal."),
 ("Specification failures", "Data that does not meet the type or quality the schema requires — usually a wrong data type.")],
 kicker="DATA EXPLORATION", cols=2, size=13, accent=AMBER)

decision_map("A Value Is Missing. What Do I Do?",
 "Is the value missing at random, or does the missingness itself mean something?",
 ("MISSING AT RANDOM", "Impute it — substitute the mean, median or a modelled estimate — or filter the row out. Document the choice and the count."),
 ("MEANINGFUL MISSING", "Keep it as NULL and treat it as a category. 'No answer' may be your most interesting finding — imputing it destroys that signal."),
 kicker="HANDLING MISSING VALUES", color=AMBER,
 note="Whichever you choose, never silently drop rows — always report how many records the decision affected.")

tile_grid("Data Manipulation Techniques", [
 ("Recoding", "Transforming values from one form to another — e.g. banding ages into groups. Decide: overwrite or new column?"),
 ("Derived variables", "A new data point computed from existing fields. Store it (fast reads) or recompute it (saves space)."),
 ("Imputation", "Substituting a missing value with an estimate — mean, median, last-known or modelled."),
 ("Aggregation & reduction", "Summarising to a coarser grain, or sampling down. Beware introducing bias when you sample."),
 ("Transposing / unpivoting", "Rotating rows into columns or columns into rows so the shape suits the analysis."),
 ("Appending & merging", "Inline append discards the originals; intermediate append keeps them and creates a new combined set.")],
 kicker="DATA TRANSFORMATION", cols=2, size=13, accent=TEAL)

worked_example("Parsing a Messy Field with a Regular Expression",
 "One source column holds a name, an e-mail and a phone number. You validate the pattern in RegexLab, then apply it in pandas.",
 ["# the raw value",
  "'Mei Tan <mei.tan@example.sg> +65 9123 4567'",
  "",
  "# validated in RegexLab first, then applied:",
  "d['name']  = d.contact.str.extract(",
  "    r'^([A-Za-z ]+?)\\s*<')",
  "d['email'] = d.contact.str.extract(",
  "    r'([\\w.%+-]+@[\\w.-]+\\.[A-Za-z]{2,})')",
  "d['phone'] = d.contact.str.extract(",
  "    r'((?:\\+65 ?)?[689]\\d{3} ?\\d{4})')",
  "",
  "# then normalise the phone format",
  "d['phone'] = (d.phone.str",
  "    .replace(r'[^0-9]', '', regex=True)",
  "    .str[-8:])"],
 [("^([A-Za-z ]+?)\\s*<", "Anchored at the start; lazy match up to the first angle bracket gives the name."),
  ("[\\w.%+-]+@[\\w.-]+", "The standard e-mail shape — local part, @, domain, then a 2+ letter TLD."),
  ("[689]\\d{3} ?\\d{4}", "A Singapore mobile or landline: 8 digits starting 6, 8 or 9, optional +65 and spaces."),
  ("Capturing group required", "pandas .str.extract returns the GROUP — without parentheses it returns NaN.")],
 kicker="PARSING STRINGS", accent=TEAL)

tile_grid("Text, Date and Logical Functions", [
 ("Parsing & delimiters", "Split text on spaces, commas, periods, pipes or tabs — the power of a delimiter is limited by the source data."),
 ("Date functions", "NOW() and TODAY() return the current moment; DATEDIFF() gives the interval between two dates."),
 ("Business-day functions", "NETWORKDAYS() counts working days (but not public holidays); WEEKDAY(), WEEKNUM(), MONTH() extract parts."),
 ("Conditional logic", "IF() tests a condition; ISNULL() substitutes a value when the expression is null."),
 ("AND vs OR", "AND requires BOTH conditions true; OR requires EITHER to be true. Getting this backwards silently changes your filter."),
 ("Aggregations", "SUM, COUNT, DISTINCT COUNT, AVERAGE, MIN, MAX — DISTINCT COUNT counts each value only once.")],
 kicker="DATA MANIPULATION FUNCTIONS", cols=2, size=13)

compare_table("SQL Join Types — What Each One Keeps",
 ["Join type", "Keeps", "Typical use"],
 [["INNER JOIN", "Only rows matching in BOTH tables", "Confirmed transactions with a known customer"],
  ["LEFT OUTER JOIN", "All left rows + matches from the right", "All customers, including those with no orders"],
  ["RIGHT OUTER JOIN", "All right rows + matches from the left", "All orders, including orphans with no customer"],
  ["FULL OUTER JOIN", "Every row from both sides", "Reconciling two systems to find what each is missing"],
  ["CROSS JOIN", "Every combination of both tables", "Generating a complete date × product grid"]],
 kicker="QUERYING AND COMBINING DATA", accent=BLUE,
 note="The silent killer: an INNER JOIN drops unmatched rows without warning. Always reconcile your record count before and after.")

tile_grid("Query Optimisation", [
 ("Filtering", "WHERE restricts the result to a subset — and cuts the work the database must do."),
 ("Indexing", "An index speeds up lookups on a column, but costs space, build time and maintenance on every write."),
 ("Parameterisation", "Replace hard-coded values with parameters so one query serves many cases — and resists SQL injection."),
 ("Temporary tables", "Hold an intermediate result in memory. Faster, and much easier to reason about than a giant nested query."),
 ("Subqueries", "A query nested inside another. Readable, but often slower than the equivalent join."),
 ("Execution plan", "The database's own visual explanation of how it will run your query — read it to find the slow step.")],
 kicker="QUERY PERFORMANCE", cols=2, size=14, accent=VIOLET)

# --- Domain 2 labs
for a in acts_for(2):
    lab_unit(a)

tile_grid("Recap — Data Acquisition and Preparation", [
 ("ETL vs ELT", "ETL transforms before loading; ELT loads raw and transforms later — choose by how stable your requirements are."),
 ("Data sources", "Data comes from databases, APIs, scraping, files, logs and public repositories, each with its own reliability risk."),
 ("Profiling first", "Profiling is the disciplined first pass — quantify the defects before you clean, so you can measure the cleaning."),
 ("Defect classes", "The defect classes are missing values, duplicates, redundancy, invalid data and outliers."),
 ("Manipulation", "Manipulation covers recoding, derived variables, imputation, aggregation, transposing, appending and parsing."),
 ("Joins", "Joins combine datasets — and an INNER JOIN silently drops unmatched rows, so always reconcile record counts."),
 ("Query performance", "Indexes, filters, parameters, temp tables and the execution plan are how you make a slow query fast.")],
 kicker="DOMAIN 02 RECAP", cols=1, size=12)
SLIDE_MAP["domains"][2] = [_d2_start, _n()]

brk("Tea Break", "15 minutes", color=TEAL)

# ================================================================ DOMAIN 3
t3 = C.TOPICS[2]
_d3_start = _n() + 1
section(f"DOMAIN {t3['code']}  ·  {t3['weighting']} OF THE EXAM", t3["title"], "03", t3["subtitle"])

tile_grid("Domain 3 — Key Concepts",
 list(zip(["Descriptive statistics","Mean vs median","Z-scores find outliers",
           "The empirical rule","Inferential statistics","p-values and causation",
           "Choosing the analysis type"], t3["concepts"])),
 kicker="THE HEAVIEST DOMAIN ON THE EXAM", cols=1, size=12)

tile_grid("Choosing Your Analysis Type", [
 ("Exploratory analysis", "The first look at a new dataset — what cleaning, profiling and transformation does it need?"),
 ("Performance analysis", "Measures a product, outcome or scenario against a defined objective, using realistic KPIs."),
 ("Trend analysis", "Uses historical data to project a future outcome. Past performance never guarantees future results."),
 ("Gap analysis", "The difference (the delta) between the present state and the desired future state."),
 ("Link analysis", "How one data point connects to others — a network of nodes joined by links."),
 ("Hypothesis-driven", "Start with a testable statement, then gather evidence to support or reject it.")],
 kicker="TYPES OF ANALYSIS", cols=2, size=14, accent=BLUE)

tile_grid("Central Tendency — Three Different 'Averages'", [
 ("Mean", "The sum divided by the count. Uses every value — and is therefore dragged by outliers."),
 ("Median", "The middle value when sorted. Resistant to outliers, which is why salary and house prices use it."),
 ("Mode", "The most frequently occurring value. The only average that works on categorical data."),
 ("Which to report", "Symmetric data → mean. Skewed data or outliers present → median. Categories → mode.")],
 kicker="DESCRIPTIVE STATISTICS", cols=2, size=15, accent=BLUE)

chart_slide("The Outlier Effect — Mean vs Median (Lab 8 data)",
 ["Mean", "Median"],
 [("With outlier", [6560, 4350]), ("Outlier removed", [4400, 4200])],
 kicker="WHY THE CHOICE MATTERS", accent=VIOLET, kind="column",
 insight="One executive salary moves the mean by over 2,100 but the median by only 150. When a distribution is "
         "skewed, reporting the mean overstates what a typical person earns — which is exactly what you prove in Lab 8.")

tile_grid("Dispersion — How Spread Out Is the Data?", [
 ("Minimum / Maximum", "The smallest and largest values in the dataset."),
 ("Range", "Maximum minus minimum. A large range is an early clue that outliers are present."),
 ("Variance (σ²)", "The average of the squared differences from the mean. Its units are squared, so it is hard to interpret directly."),
 ("Standard deviation (σ)", "The square root of the variance — back in the original units, so you can actually read it."),
 ("Z-score", "How many standard deviations a value sits from the mean: z = (x − x̄) / s."),
 ("Outlier rule of thumb", "|z| > 3 is a strong outlier flag; |z| > 2 is worth investigating.")],
 kicker="DISPERSION AND VARIABILITY", cols=2, size=14, accent=TEAL)

tile_grid("Distribution and Frequency", [
 ("Normal distribution", "The symmetric bell curve — the empirical rule says ~99.74% of data lies within 3 standard deviations."),
 ("Parametric data", "Fits a known distribution (usually normal), so mean-and-SD methods are valid."),
 ("Nonparametric data", "Does not fit a normal distribution — use distribution-independent methods and the median."),
 ("Skew", "An asymmetric distribution with a long tail on one side, which pulls the mean away from the median."),
 ("Frequency", "How many times a value appears; frequency percent expresses it relative to the whole dataset."),
 ("Histogram", "The chart that shows a distribution — choose your bin count carefully and include the outliers.")],
 kicker="DISTRIBUTION", cols=2, size=13)

big_statement("Inferential statistics let you speak beyond your sample.",
 "Descriptive statistics summarise the data you have. Inferential statistics — t-tests, chi-square, regression — let you "
 "draw conclusions about a whole population from a sample, and state how confident you are in that conclusion.",
 "INFERENTIAL STATISTICAL METHODS", color=VIOLET)

process_map("Hypothesis Testing, Step by Step", [
 ("State H0 and H1", "Before seeing results"),
 ("Choose the test", "t-test, chi-square, ANOVA"),
 ("Set the threshold", "Usually α = 0.05"),
 ("Compute the p-value", "Run the test"),
 ("Decide and report", "Reject or fail to reject")],
 kicker="HYPOTHESIS TESTING", color=VIOLET,
 synthesis=("THE DISCIPLINE", "State the hypotheses BEFORE you look at the result. Choosing the hypothesis to fit the "
                              "answer you wanted is the most common analytical malpractice."))

compare_table("Null vs Alternative Hypothesis, and the Two Errors",
 ["Concept", "Meaning", "In plain language"],
 [["Null hypothesis (H0)", "No relationship between the variables", "'The new page makes no difference'"],
  ["Alternative (H1)", "A relationship exists", "'The new page lifts order value'"],
  ["p-value", "Probability the difference arose by chance", "Below 0.05 → unlikely to be chance"],
  ["Reject H0", "The evidence supports a real effect", "'We are confident the page works'"],
  ["Type I error", "Rejecting a TRUE null hypothesis", "False alarm — you ship a change that does nothing"],
  ["Type II error", "Failing to reject a FALSE null", "Missed opportunity — you bin a change that worked"]],
 kicker="HYPOTHESIS TESTING", accent=VIOLET,
 note="A p-value below 0.05 means the result is statistically significant — it does NOT tell you the effect is large or commercially important.")

tile_grid("The Inferential Tests You Must Know", [
 ("T-test", "Compares the MEANS of two groups to see whether the difference is significant. Used in every A/B test."),
 ("Chi-square", "Compares observed counts against expected counts for CATEGORICAL data."),
 ("Chi-square: independence", "Tests whether two categorical variables are related to each other."),
 ("Chi-square: goodness of fit", "Tests whether observed counts match an expected baseline distribution."),
 ("Regression analysis", "Estimates the relationship between a dependent variable and one or more independent variables."),
 ("Confidence interval", "The range within which the true population value is likely to fall, at a stated confidence level.")],
 kicker="STATISTICAL METHODS", cols=2, size=13, accent=BLUE)

worked_example("Reading a Regression Output",
 "Lab 10 fits revenue against marketing spend. Here is what each number in the output actually tells you.",
 ["from scipy import stats",
  "",
  "lr = stats.linregress(d.spend, d.revenue)",
  "",
  "# slope      =  6.598",
  "# intercept  = 52.114",
  "# rvalue     =  0.9992",
  "# pvalue     =  1.4e-12",
  "",
  "# the fitted model:",
  "#   revenue = 6.598 * spend + 52.114",
  "",
  "# predict at a new spend level",
  "lr.slope * 40 + lr.intercept",
  "#  -> 316.0"],
 [("Slope = 6.598", "Every extra 1 unit of spend is associated with 6.6 more units of revenue."),
  ("Intercept = 52.1", "The modelled revenue at zero spend — often not meaningful in the real world."),
  ("R² = 0.998", "99.8% of the variation in revenue is explained by spend. Very high — and suspiciously so."),
  ("p = 1.4e-12", "Far below 0.05, so the relationship is statistically significant, not chance.")],
 kicker="REGRESSION ANALYSIS", accent=BLUE)

decision_map("Two Variables Move Together. Now What?",
 "Have I shown correlation, or have I actually shown causation?",
 ("CORRELATION — what you have", "Pearson's r measures the strength and direction of a linear relationship. R² is the proportion of variance explained. This is a pattern, nothing more."),
 ("CAUSATION — what you need", "A controlled experiment, a plausible mechanism, correct time ordering, and the ruling out of confounding variables. Observational data alone can never prove it."),
 kicker="THE ANALYST'S DUTY", color=AMBER,
 note="In Lab 10 staff numbers correlate with revenue at r ≈ 0.99 — but growth over time drives both. Correlation is not causation.")

tile_grid("Troubleshooting Your Analysis", [
 ("The numbers don't reconcile", "Check the record count at every join and filter. An INNER JOIN or a WHERE clause has probably dropped rows."),
 ("The mean looks wrong", "Check for outliers and nulls. pandas skips NaN in a mean — so your denominator may not be what you think."),
 ("Everything correlates", "You may be measuring the same thing twice, or both variables are driven by time. Plot them before you trust r."),
 ("The result is too clean", "Real business data is noisy. A perfect fit usually means leakage, a synthetic dataset, or a duplicated column."),
 ("Dates behave strangely", "Confirm the parse format and the timezone. A DD/MM vs MM/DD mix-up silently corrupts every time series."),
 ("Nobody trusts the number", "Show the lineage: the source, the filters applied, the row counts and the date the data was refreshed.")],
 kicker="TROUBLESHOOTING ANALYSIS ISSUES", cols=2, size=13, accent=AMBER)

tile_grid("Communicating Results to Different Audiences", [
 ("C-level executives", "The big picture only. Lead with the decision and the number that supports it — never the methodology."),
 ("Management", "Performance against target, by unit, with the exceptions highlighted and an action attached."),
 ("Technical experts", "They will ask about your method, your sample and your assumptions. Bring the detail and the caveats."),
 ("External stakeholders", "Know exactly what may and may not be shared. Aggregate and de-identify before it leaves the building."),
 ("General public", "Plain language, no jargon, one message per visual, and a clearly stated source."),
 ("The universal rule", "Lead with the answer, then the evidence. Never make your audience assemble the conclusion themselves.")],
 kicker="COMMUNICATING ANALYSIS RESULTS", cols=2, size=13, accent=TEAL)

# --- Domain 3 labs
for a in acts_for(3):
    lab_unit(a)

tile_grid("Recap — Data Analysis", [
 ("Descriptive stats", "Descriptive statistics summarise: mean, median and mode for centre; range, variance and SD for spread."),
 ("Mean vs median", "The mean is dragged by outliers and the median resists them — which one you report changes the story."),
 ("Z-scores", "Z-scores standardise distance from the mean, and |z| > 3 is the conventional outlier flag."),
 ("Inferential stats", "Inferential statistics generalise from a sample: t-tests, chi-square, correlation and regression."),
 ("Hypothesis testing", "State H0 and H1 before you test; p < 0.05 rejects the null; Type I is a false alarm, Type II a missed effect."),
 ("Correlation", "Correlation measures a pattern; causation requires a mechanism, time ordering and controlled confounders."),
 ("Audience", "Match the delivery to the audience — executives get the decision, technical experts get the method.")],
 kicker="DOMAIN 03 RECAP", cols=1, size=12)
SLIDE_MAP["domains"][3] = [_d3_start, _n()]

brk("Lunch Break", "1 hour")

# ================================================================ DOMAIN 4
t4 = C.TOPICS[3]
_d4_start = _n() + 1
section(f"DOMAIN {t4['code']}  ·  {t4['weighting']} OF THE EXAM", t4["title"], "04", t4["subtitle"])

tile_grid("Domain 4 — Key Concepts",
 list(zip(["The question picks the chart","Time, category, distribution","Composition and hierarchy",
           "Geographic data","Dashboards stay focused","Report types",
           "Validating accuracy"], t4["concepts"])),
 kicker="WHAT THIS DOMAIN COVERS", cols=1, size=12)

big_statement("The question determines the chart. Not your preference.",
 "Composition, comparison, distribution, relationship or trend — every business question falls into one of these five "
 "shapes, and each shape has a chart that fits it. Choose the chart last, after you know the question.",
 "USING THE APPROPRIATE VISUALIZATION", color=BLUE)

compare_table("Which Chart Answers Which Question?",
 ["The question", "The chart", "Why"],
 [["How is it trending over time?", "Line chart", "A continuous line reads as a sequence"],
  ["Which category is biggest?", "Bar / column chart", "Length is the easiest visual comparison"],
  ["What share of the whole?", "Pie chart (few slices)", "Angle shows parts of one whole"],
  ["How is one variable spread?", "Histogram", "Bins reveal the shape of a distribution"],
  ["Do two variables relate?", "Scatter plot", "Position on two axes exposes a pattern"],
  ["Where is it happening?", "Map (dot / filled / layered)", "Geography is its own dimension"],
  ["How does a total build up?", "Waterfall chart", "Shows each contribution to a change"]],
 kicker="CHART SELECTION", accent=BLUE,
 note="Get this wrong and the visual actively misleads — in Lab 11 you build a deliberately wrong chart to see it happen.")

tile_grid("Specialist Chart Types", [
 ("Tree map", "Hierarchical data as nested rectangles sized by value. Label only the large categories."),
 ("Heat map", "Colour encodes magnitude across two dimensions — excellent for spotting concentration."),
 ("Bubble chart", "A scatter plot with a third variable encoded as the size of the point."),
 ("Combination chart", "Two chart types on shared axes — e.g. revenue columns with a margin-percentage line."),
 ("Word cloud", "Word frequency as text size. Eye-catching, but imprecise — never use it for a real measurement."),
 ("Infographic", "A designed narrative combining data and graphics. Built for marketing, not for analysis.")],
 kicker="VISUALIZATION TYPES", cols=2, size=14, accent=TEAL)

tile_grid("Geographic Visualisation", [
 ("Dot map", "Markers placed at specific coordinates — each dot is one event or location."),
 ("Filled (choropleth) map", "Shading fills a bounded region by value. Beware: large regions look more important than they are."),
 ("Layered map", "Two dimensions at once — e.g. shaded regions for revenue, sized dots for store count."),
 ("Tools", "ArcGIS for serious geospatial work; Power BI and Tableau both render maps directly from postal or lat/long data.")],
 kicker="MAPS", cols=2, size=15, accent=VIOLET)

process_map("From Requirement to Delivered Report", [
 ("Define the audience", "Who decides what?"),
 ("Agree the questions", "What must it answer?"),
 ("Document the sources", "Where does data come from?"),
 ("Build and validate", "Draw it, then check it"),
 ("Deliver on cadence", "Who gets it, how often?")],
 kicker="EXPRESSING BUSINESS REQUIREMENTS", color=BLUE,
 synthesis=("THE DISTRIBUTION LIST", "Agree who receives the report BEFORE you build it — the audience determines "
                                     "the level of detail and what may legally be shared."))

tile_grid("Report and Dashboard Components", [
 ("Report header", "First page only — the title, the version number and the reporting period."),
 ("Page header / footer", "Repeat on every page — field headings at the top, page numbers and references at the bottom."),
 ("Report footer", "Last page only — summary information and credit to the authors."),
 ("Watermark", "Signals handling restrictions: DRAFT, CONFIDENTIAL, INTERNAL USE ONLY."),
 ("Refresh date", "When the DATA was last updated — the single most-forgotten and most-important element."),
 ("Print date", "When this copy was produced. Different from the refresh date, and both matter in an audit.")],
 kicker="DOCUMENTATION ELEMENTS", cols=2, size=13)

tile_grid("Report Types", [
 ("Static / point-in-time", "A fixed snapshot that does not update. The record of what was true at that moment."),
 ("Dynamic / real-time", "Refreshes on access or on a schedule — always shows the current state."),
 ("Operational", "The status of projects, products or processes, usually daily and detailed."),
 ("Compliance", "Produced to satisfy a regulator. The format and cadence are usually prescribed for you."),
 ("Ad hoc", "Generated once to answer a specific one-off question."),
 ("Self-service", "The platform lets end users build their own — which shifts governance onto the data model.")],
 kicker="DISTINGUISHING REPORT TYPES", cols=2, size=13, accent=TEAL)

tile_grid("Dashboard Design Principles", [
 ("One purpose", "A dashboard tracks a small set of decisions. If it answers everything, it answers nothing."),
 ("Consistent colour", "Never pick colours at random. One meaning per colour, applied identically on every panel."),
 ("Filters and sorting", "Hardcoded, interactive, visual and date filters; natural order, multi-sort, top/bottom-N and custom sorts."),
 ("Drillthrough & tooltips", "Keep the surface simple, and let the detail live one click away."),
 ("Labels and legends", "Every axis labelled, every unit stated. An unlabelled number is not a finding."),
 ("Test before deploy", "Check the labels, test the filters, confirm permissions and licensing, then document it.")],
 kicker="DESIGNING DASHBOARDS", cols=2, size=13, accent=VIOLET)

process_map("Validating Reporting Accuracy", [
 ("Record count", "Does it cover every row?"),
 ("Recalculate", "Get the total a second way"),
 ("Cross-validate", "Check another source"),
 ("Peer review", "A second analyst checks it"),
 ("Data audit", "Verify the whole chain")],
 kicker="VALIDATE REPORTING ACCURACY", color=TEAL,
 synthesis=("THE TEST OF A GOOD PROCESS", "A validation process that has never caught an error has not been proven. "
                                          "In Lab 12 you plant an error deliberately to prove yours works."))

compare_table("Data Validation vs Data Verification",
 ["", "Validation", "Verification"],
 [["Checks", "The FORMAT and STRUCTURE of the data", "The ACCURACY of the data"],
  ["Question asked", "Is it the right shape and type?", "Is it actually true and correct?"],
  ["Example", "The date field contains a parseable date", "The date matches the source system's record"],
  ["When it runs", "On entry and on import — often automated", "On review — record counts, recalculation, peer review"],
  ["Catches", "Wrong types, invalid values, missing fields", "Wrong joins, wrong formulas, transposed figures"]],
 kicker="QUALITY CHECKS", accent=AMBER,
 note="Both are required. Data can be perfectly valid in format and still be completely wrong in fact.")

# --- Domain 4 labs
for a in acts_for(4):
    lab_unit(a)

tile_grid("Recap — Visualization and Reporting", [
 ("Question first", "The business question determines the chart: composition, comparison, distribution, relationship or trend."),
 ("Chart selection", "Line for time, bar for categories, pie for a few parts of a whole, histogram for distribution, scatter for relationship."),
 ("Maps & magnitude", "Maps come as dot, filled (choropleth) or layered; heat maps and tree maps encode magnitude and hierarchy."),
 ("Audience & sharing", "Agree the audience and the distribution list before you build — they set the detail level and what may be shared."),
 ("Report types", "Reports are static, dynamic, operational, compliance, ad hoc or self-service, and each carries standard elements."),
 ("Dashboard design", "A good dashboard has one purpose, consistent colour, labelled axes and detail hidden behind drillthrough."),
 ("Validation", "Validate by record count, recalculation, cross-validation, peer review and audit — and prove the process catches errors.")],
 kicker="DOMAIN 04 RECAP", cols=1, size=12)
SLIDE_MAP["domains"][4] = [_d4_start, _n()]

brk("Tea Break", "15 minutes", color=TEAL)

# ================================================================ DOMAIN 5
t5 = C.TOPICS[4]
_d5_start = _n() + 1
section(f"DOMAIN {t5['code']}  ·  {t5['weighting']} OF THE EXAM", t5["title"], "05", t5["subtitle"])

tile_grid("Domain 5 — Key Concepts",
 list(zip(["Governance spans the lifecycle","Roles split accountability","Classification and data types",
           "Compliance obligations","Layered protection","Lineage and version control",
           "Continuous quality assurance"], t5["concepts"])),
 kicker="WHAT THIS DOMAIN COVERS", cols=1, size=12)

big_statement("Governance is a set of decisions, not a document.",
 "Data governance is an organisation's capability to ensure high-quality data exists across the complete data lifecycle, "
 "with controls implemented to support its business objectives. Every control is somebody's decision, written down and enforced.",
 "DATA GOVERNANCE", color=VIOLET)

process_map("The Data Lifecycle", [
 ("Creation", "Entry, capture or import"),
 ("Storage", "At rest, permission-controlled"),
 ("Use", "View, process, modify"),
 ("Archive", "Retained but not active"),
 ("Destruction", "Beyond its useful life")],
 kicker="DATA LIFECYCLE", color=VIOLET,
 synthesis=("WHY IT DRIVES POLICY", "Every governance policy you write must say what happens at each of these five "
                                    "stages — otherwise there is a stage where nobody is accountable."))

tile_grid("Data Roles and Accountability", [
 ("Data owner", "A senior executive accountable for the confidentiality, integrity and availability of the data asset."),
 ("Data steward", "Ensures data is properly labelled, identified, collected and stored. The day-to-day quality role."),
 ("Data custodian", "Manages the SYSTEM the data lives on — the technical operator of storage and backup."),
 ("Privacy officer", "Oversees privacy-related data, and owns minimisation, sovereignty, retention and destruction policy."),
 ("Why separate them", "Separation of duties: the person who authorises access should not be the person who grants it."),
 ("In practice", "In Lab 14 you build the access matrix that assigns each of these roles a specific level of access.")],
 kicker="DATA ROLES", cols=2, size=13, accent=BLUE)

compare_table("Data Classification — Commercial and Government",
 ["Level", "Commercial sector", "Government sector"],
 [["Lowest", "Public — the front-facing website", "Unclassified — public information"],
  ["Low-mid", "Sensitive — financial data", "Controlled Unclassified (CUI) — medical records"],
  ["Mid", "Private — personnel records", "Confidential — trade secrets"],
  ["High", "Confidential — intellectual property", "Secret — military plans"],
  ["Highest", "Restricted — regulated or contractual", "Top Secret — weapon blueprints"]],
 kicker="DATA CLASSIFICATION", accent=AMBER,
 note="Classification sets the sensitivity. A separate DATA TYPE tag — PII, PHI, PIFI, IP — says what kind of data it is.")

tile_grid("Compliance and Regulation", [
 ("Regulation vs compliance", "A regulation is a rule backed by law. Compliance is demonstrating that you meet it."),
 ("Singapore PDPA", "Governs collection, use and disclosure of personal data, and mandates breach notification."),
 ("GDPR (EU)", "Rights of access, rectification, erasure and portability — applies to EU residents' data wherever it is held."),
 ("HIPAA / SOX", "US health information privacy; and financial reporting controls with retention obligations."),
 ("Data sovereignty", "The jurisdiction whose law governs the data — usually determined by where it is physically stored."),
 ("Audits", "Periodic independent verification that the controls you documented are actually operating.")],
 kicker="COMPLIANCE REQUIREMENTS", cols=2, size=13, accent=AMBER)

tile_grid("Retention, Preservation and Destruction", [
 ("Data retention", "Keeping data for a defined period to satisfy business policy and applicable law. Consult legal counsel."),
 ("Data preservation", "Holding data for a specific purpose OUTSIDE the retention policy — for example, a litigation hold."),
 ("Data removal", "Deleting data or making it inaccessible. Appropriate only for the least sensitive data."),
 ("Data destruction", "Deleting the data AND destroying the underlying medium so it cannot be reconstructed."),
 ("Data sanitisation", "The verification step that PROVES the data was wiped and is no longer recoverable."),
 ("Document it", "An undocumented retention period is itself an audit finding — record the period and its rationale.")],
 kicker="RETENTION AND DESTRUCTION", cols=2, size=13)

compare_table("Protection Strategies Compared",
 ["Technique", "What it does", "Reversible?", "Analysis still possible?"],
 [["Access control", "Restricts WHO can see the data", "n/a", "Yes, for authorised users"],
  ["Encryption", "Scrambles data into ciphertext", "Yes, with the key", "Only after decryption"],
  ["Masking", "Hides part of the value (S****A)", "No", "Partially — recognition only"],
  ["De-identification", "Removes the identifying fields", "No", "Yes, on remaining fields"],
  ["Pseudonymisation", "Replaces the ID with a surrogate key", "Only with the mapping", "Yes — joins still work"]],
 kicker="PRIVACY AND PROTECTION", accent=TEAL,
 note="You apply masking, de-identification and pseudonymisation to the same dataset in Lab 13 — and prove the analysis survives.")

tile_grid("Encryption and Access Control", [
 ("Data at rest", "Stored as ciphertext on disk; re-encrypted on every write."),
 ("Data in transit", "Encrypted while moving between systems — TLS/HTTPS is the baseline expectation."),
 ("Data in use", "Being processed in memory. The hardest state to protect, and the target of modern attacks."),
 ("Read/write permissions", "The most basic control: who may read, and who may also change."),
 ("Role-based access (RBAC)", "Access assigned by JOB FUNCTION, not by individual. Scales, and survives staff changes."),
 ("User-group permissions", "Access granted by group membership. Simple, but drifts unless it is reviewed regularly.")],
 kicker="DATA SECURITY", cols=2, size=13, accent=BLUE)

tile_grid("Documentation, Versioning and Lineage", [
 ("Data lineage", "The traceable path from origin through every transformation to the final report. Answers 'where did this number come from?'"),
 ("Data dictionary", "Defines every field: its meaning, type, valid values, owner and source. The reference everyone shares."),
 ("Version control", "Tracks changes to queries, models and reports over time, so any figure can be reproduced later."),
 ("Entity relationship models", "Conceptual (what exists), logical (fields and relationships), physical (actual tables and types)."),
 ("Data constraints", "Integrity rules limiting what may enter a column — the schema enforcing quality automatically."),
 ("Record linkage", "Matching records across datasets — with link restrictions preventing protected sets being combined.")],
 kicker="DATA MANAGEMENT PRACTICES", cols=2, size=13, accent=VIOLET)

tile_grid("The Data Quality Dimensions", [
 ("Completeness", "No required data is missing. Measured as the null rate on mandatory fields."),
 ("Accuracy", "The values are actually correct — they match the real-world fact they describe."),
 ("Consistency", "The same thing is recorded the same way everywhere. 'SG', 'Singapore' and 'sg' break this."),
 ("Uniqueness", "No unintended duplicates. The primary key must identify exactly one record."),
 ("Validity", "Values conform to the defined format, type, range and domain."),
 ("Timeliness", "The data is current enough for the decision it supports. A stale figure is a wrong figure.")],
 kicker="IMPLEMENT QUALITY ASSURANCE", cols=2, size=13, accent=TEAL)

process_map("Quality Assurance in Operation", [
 ("Profile", "Measure the current state"),
 ("Define rules", "One rule per dimension"),
 ("Automate", "Validate on entry"),
 ("Monitor", "Run every load, score it"),
 ("Act", "Block load, alert owner")],
 kicker="PROFILE · MONITOR · TEST", color=TEAL,
 synthesis=("WHAT MAKES IT MONITORING", "A report tells you the data was bad. A non-zero exit code STOPS the bad data "
                                        "loading — that is the difference you build in Lab 15."))

tile_grid("Master Data Management", [
 ("Master data", "The golden record — the single authoritative version of a core entity such as a customer or product."),
 ("MDM", "The discipline of creating and maintaining that golden record across every system that holds a copy."),
 ("How golden records are built", "Consolidate duplicate fields, fill gaps from other systems, and standardise the field formats."),
 ("Why it matters", "Without it, Finance, Sales and Support each report a different customer count — all defensible, all different."),
 ("MDM and governance", "They work together: governance sets the rules, MDM enforces them on the core entities."),
 ("Tooling", "Informatica and Reltio are common enterprise MDM platforms.")],
 kicker="MASTER DATA MANAGEMENT", cols=2, size=13, accent=BLUE)

# --- Domain 5 labs
for a in acts_for(5):
    lab_unit(a)

tile_grid("Recap — Data Governance, Quality and Controls", [
 ("Lifecycle", "Governance ensures quality data across the full lifecycle: creation, storage, use, archive and destruction."),
 ("Roles", "Owner, steward, custodian and privacy officer separate accountability — no single person holds every duty."),
 ("Classification", "Classification sets sensitivity; a data-type tag (PII, PHI, PIFI, IP) says what kind of data it is."),
 ("Compliance", "PDPA, GDPR, HIPAA and SOX impose retention, audit and sovereignty duties you must be able to evidence."),
 ("Layered protection", "Access control, encryption, masking, de-identification and pseudonymisation are layered, not alternatives."),
 ("Lineage", "Lineage, a data dictionary and version control are what make a number reproducible and auditable."),
 ("Quality assurance", "Quality assurance runs continuously: profile, define rules, automate validation, monitor and act on failure.")],
 kicker="DOMAIN 05 RECAP", cols=1, size=12)
SLIDE_MAP["domains"][5] = [_d5_start, _n()]

# ================================================================ TOOLS + CLOSE
section("WRAP-UP", "Tools, Revision and Next Steps", "")

tile_grid("Data Analytic Tools — Languages", [
 ("SQL", "The query language for relational databases. Non-negotiable for any data role."),
 ("Python", "General-purpose, with pandas, NumPy, matplotlib and scikit-learn — the dominant analysis stack."),
 ("R", "Purpose-built for statistical computing and graphics; strong among statisticians and researchers."),
 ("Excel / Power Query", "Still the most widely used analysis tool on earth. Pivot tables, formulas and Power Query transforms."),
 ("Notebooks", "Jupyter and Colab combine code, output and narrative in one reproducible document."),
 ("Version control", "Git tracks every change to your queries and scripts, so any result can be reproduced.")],
 kicker="CODING ENVIRONMENTS", cols=2, size=13)

tile_grid("BI, Visualisation and Statistical Platforms", [
 ("Power BI", "Microsoft's interactive BI product — Power Query for prep, DAX for measures, dashboards for delivery."),
 ("Tableau", "Leading visual-analysis tool, strong at exploratory visualisation and mapping."),
 ("Qlik / Domo / MicroStrategy", "Enterprise BI platforms combining data sources, dashboards and distribution."),
 ("AWS QuickSight / Oracle Analytics", "Cloud-native BI delivering dashboards over cloud data warehouses."),
 ("SAS · SPSS · Stata · Minitab", "Established statistical packages used for advanced and regulated analysis."),
 ("SSRS · Crystal Reports", "Paginated, pixel-perfect operational and compliance reporting.")],
 kicker="BI SOFTWARE AND ANALYSIS PLATFORMS", cols=2, size=13, accent=TEAL)

tile_grid("What You Achieved", [
 ("LO1 · Integrate datasets", "Built a normalised schema with enforced referential integrity and integrated three sources with SQL joins (Labs 1, 7)."),
 ("LO2 · Mine for trends", "Profiled a dirty dataset, parsed messy fields with validated regex, and derived new structured fields (Labs 4, 5, 6)."),
 ("LO3 · Analyse statistically", "Computed descriptive statistics, ran a t-test with p-values, and fitted a regression model (Labs 8, 9, 10)."),
 ("LO4 · Communicate visually", "Matched five chart types to five questions and built a validated KPI dashboard (Labs 11, 12)."),
 ("LO5 · Link the variables", "Classified and protected sensitive data, assessed leakage risk, and automated quality monitoring (Labs 13, 14, 15)."),
 ("Certification ready", f"Covered all five {C.CERT_EXAM} exam domains at their examined weightings.")],
 kicker="LEARNING OUTCOMES", cols=2, size=13)

# Practice exam slide — REAL clickable hyperlink
def practice_exam_slide():
    from _engine import slide, head, rect, txt, footer, Inches, Pt, LIGHT
    s = head(slide(), "Practice Exam — Before You Certify", "exams.tertiaryinfotech.com", kcolor=VIOLET)
    txt(s, Inches(0.85), Inches(1.9), Inches(11.63), Inches(0.5),
        [[("Attempt the official practice exam before you sit the real CompTIA Data+ certification.", 16, INK, False)]])
    rect(s, Inches(0.85), Inches(2.55), Inches(11.63), Inches(0.85), LIGHT)
    rect(s, Inches(0.85), Inches(2.55), Inches(0.11), Inches(0.85), VIOLET)
    tb = s.shapes.add_textbox(Inches(1.2), Inches(2.68), Inches(11.0), Inches(0.6))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]
    r0 = p.add_run(); r0.text = "CompTIA Data+ (DA0-001) practice exams:  "
    r0.font.size = Pt(13); r0.font.name = "Arial"; r0.font.color.rgb = GREY
    r = p.add_run(); r.text = C.PRACTICE_EXAM_URL
    r.font.size = Pt(13); r.font.bold = True; r.font.name = "Arial"; r.font.color.rgb = VIOLET
    r.hyperlink.address = C.PRACTICE_EXAM_URL
    tiles = [(BLUE, "6 FULL EXAMS", "The bundle covers all five domains at their examined weightings."),
             (TEAL, "TIMED PRACTICE", "Sit them under exam conditions to build your pacing before the real thing."),
             (VIOLET, "REVIEW EVERY MISS", "Read the explanation for every wrong answer — that is where the learning is."),
             (AMBER, "THEN BOOK", "Book the real DA0-001 exam once you are consistently scoring above your target.")]
    xs = [Inches(0.85), Inches(3.83), Inches(6.81), Inches(9.79)]
    for (col, lbl, body), x in zip(tiles, xs):
        rect(s, x, Inches(3.75), Inches(2.78), Inches(2.35), LIGHT)
        rect(s, x, Inches(3.75), Inches(2.78), Inches(0.1), col)
        txt(s, x + Inches(0.22), Inches(3.95), Inches(2.4), Inches(0.36), [[(lbl, 12, col, True)]])
        txt(s, x + Inches(0.22), Inches(4.38), Inches(2.4), Inches(1.5), [[(body, 11.5, INK, False)]])
    footer(s)
practice_exam_slide()

tile_grid("Continue Your Learning", [
 ("Sit the certification", f"Book the {C.CERT_EXAM} exam while the material is fresh."),
 ("Redo every lab", "Repeat each lab from a blank terminal until the workflow is automatic."),
 ("Apply it at work", "Profile one real dataset from your own job using the Lab 4 procedure this week."),
 ("Build a portfolio", "Publish a cleaned dataset, an analysis and a dashboard you can show an employer."),
 ("Go deeper on SQL", "Joins, window functions and query plans repay every hour you invest."),
 ("Learn a BI platform", "Pick Power BI or Tableau and rebuild your Lab 12 dashboard in it.")],
 kicker="NEXT STEPS", cols=2, size=14, accent=TEAL)

tile_grid("Recommended Courses", [(rc, "") for rc in C.RECOMMENDED_COURSES],
 kicker="CONTINUE WITH TERTIARY INFOTECH", cols=1, size=15)

content("Support", [
 "If you have any enquiries during or after the class, you can contact us below.",
 "Email: enquiry@tertiaryinfotech.com",
 "Tel: +65 6100 0613    ·    WhatsApp: +65 6100 0613",
 "Website: www.tertiarycourses.com.sg",
 "LMS / TMS: https://lms-tms.tertiaryinfotech.com"],
 kicker="WE'RE HERE TO HELP")

# ---------------- END-OF-DECK ASSESSMENT BLOCK (mandatory order) ----------------
tile_grid("Assessment", [
 ("Written Assessment (SAQ)", "1 hour · open book · short-answer knowledge questions across all five domains."),
 ("Practical Performance (PP)", "1 hour · open book · scenario-based hands-on data tasks mapped to LO1–LO5."),
 ("Digital attendance", "Take the Assessment digital attendance (TRAQOM) before you start."),
 ("Submit on the LMS", f"Upload your completed answers at {C.LMS_URL}"),
 ("Open book means", "Course slides, the Learner Guide and other approved materials only."),
 ("Result", "You are assessed Competent (C) or Not Yet Competent (NYC) on each instrument.")],
 kicker="FINAL ASSESSMENT", cols=2, size=14)

process_map("Assessment Flow", [
 ("TRAQOM attendance", "Scan the QR on the LMS"),
 ("Assessment attendance", "Scan the SSG QR"),
 ("Sit WA then PP", "Open book · 1 hour each"),
 ("Submit on the LMS", "Upload your answers"),
 ("Sign the record", "Assessment Summary Record")],
 kicker="ON ASSESSMENT DAY", color=BLUE,
 synthesis=("REMEMBER", "All five steps are mandatory for WSQ funding — missing the TRAQOM digital attendance "
                        "or the course feedback survey can invalidate your claim."))

tile_grid("Digital Attendance (Mandatory)", [
 ("Three times a day", "Take the AM, PM and Assessment digital attendance — mandatory for every WSQ-funded course."),
 ("Trainer shows the QR", "The trainer or administrator displays the digital attendance QR code generated from TPG."),
 ("Scan with Singpass", "Scan the QR code from your Singpass App and submit your attendance."),
 ("75% minimum", "A minimum of 75% attendance is required to be eligible for assessment and funding.")],
 kicker="TRAQOM · SSG DIGITAL ATTENDANCE", cols=2, size=15)

big_statement("Thank You!",
 "You can now integrate, prepare, analyse, visualise and govern data — and you are ready to sit the "
 "CompTIA Data+ (DA0-001) certification exam.",
 "HAPPY ANALYSING", color=TEAL)

# ---------------- restrained motion pass ----------------
for s in prs.slides:
    joined = " ".join(sh.text_frame.text for sh in s.shapes if sh.has_text_frame)
    is_div = ("COURSE ADMINISTRATION" in joined or "WRAP-UP" in joined
              or any(f"DOMAIN {t['code']}  ·  {t['weighting']}" in joined for t in C.TOPICS))
    _transition(s, "push" if is_div else "fade", speed="med" if is_div else "fast")

import json
with open(os.path.join(HERE, "slide_map.json"), "w") as f:
    json.dump(SLIDE_MAP, f, indent=1)
OUT = os.path.join(REPO, "courseware", f"{C.SHORT_TITLE}-{C.VERSION}.pptx")
prs.save(OUT)
print(f"Saved {OUT}  ({len(prs.slides._sldIdLst)} slides)")
