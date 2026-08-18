"""
SINGLE SOURCE OF TRUTH — WSQ CompTIA Certified Data+ Training (TGS-2024049212).

Every artifact (PPT, LP, LG, LG.md, labs index, assessment) is generated from this
module plus data_domain1.py … data_domain5.py, so they stay 100% aligned.

Guiding principle: the course material is 100% aligned to the CompTIA Data+ (DA0-001)
exam domains AND to the SSG-approved Course Proposal (TSC ATP-PIN-3001-1.1 Data
Analytics, LU1..LU5 / LO1..LO5) so learners can pass both the WSQ assessment and the
CompTIA Data+ certification exam.
"""

# ------------------------------------------------------------------ metadata
TITLE        = "WSQ - CompTIA Certified Data+ Training"
SHORT_TITLE  = "WSQ - CompTIA Certified Data+ Training"   # used in output filenames
COURSE_CODE  = "TGS-2024049212"
CERT_EXAM    = "CompTIA Data+ (DA0-001)"
VERSION      = "v5.0"
VERSION_DATE = "19 August 2026"
ORG          = "Tertiary Infotech Academy Pte Ltd"
UEN          = "UEN: 201200696W"
TRAINER      = "Dr. Alfred Ang"
DAYS         = 5

# Course delivery per the approved Course Proposal (CP_TIPL_compTIAdata+_v2)
TSC_TITLE    = "Data Analytics"
TSC_CODE     = "ATP-PIN-3001-1.1"
CLASSROOM_HOURS  = 19
PRACTICAL_HOURS  = 19
ASSESSMENT_HOURS = 2
TOTAL_HOURS      = 40

COURSE_URL   = "https://www.tertiarycourses.com.sg/wsq-comptia-certified-data-training.html"
REPO_URL     = "https://github.com/tertiarycourses/TGS-2024049212-CompTIA-Certified-Data-Training"
LMS_URL      = "https://lms-tms.tertiaryinfotech.com/"
PRACTICE_EXAM_URL = "https://exams.tertiaryinfotech.com/practice-exams/comptia/comptia-data-plus"

# ------------------------------------------------------------------ outcomes (LO1..LO5 from the CP)
LEARNING_OUTCOMES = [
    "LO1: Integrate multiple datasets to extract and process data efficiently. (K4, A1)",
    "LO2: Conduct data mining to uncover and analyze trends using analysis techniques. (K1, A2)",
    "LO3: Perform statistical data analysis to derive actionable insights. (K2, A3)",
    "LO4: Present analytical outputs visually to communicate data effectively for decision-making. (K3, A5)",
    "LO5: Recognize and interpret sequential patterns to establish linkages between variables. (A4)",
]

# TSC Knowledge & Ability statements (ATP-PIN-3001-1.1 Data Analytics)
TSC_KNOWLEDGE = [
    "K1  Tools and techniques for data collection, mining, cleaning and analysis",
    "K2  Statistical principles underpinning data analysis techniques",
    "K3  Principles of communicating data effectively",
    "K4  Procedures to extract and process data sets",
]
TSC_ABILITIES = [
    "A1  Integrate information from multiple datasets",
    "A2  Conduct data mining exercises to uncover trends in the data",
    "A3  Perform data analysis to derive meaningful and actionable insights",
    "A4  Recognise sequential patterns and sub-graph patterns to draw linkages between variables",
    "A5  Present analytics outputs in a visually appealing format to support decision-making",
]

# ------------------------------------------------------------------ topics = CompTIA Data+ exam domains
# num, code, title, subtitle, weighting (exam), LU/LO mapping, concept bullets
TOPICS = [
    dict(num=1, code="01",
         title="Data Concepts and Environments",
         subtitle="Database types · data structures · file extensions · data types · data sources · infrastructure · tools · AI concepts",
         weighting="20%",
         lu="LU1", lo="LO1", ka="K4, A1",
         concepts=[
            "A data schema describes both how data is organised and how tables relate to one another — it is designed before a single row is written.",
            "Relational databases store data in linked tables and are queried with SQL; non-relational (NoSQL) stores trade fixed schemas for scale and flexibility.",
            "Normalisation (1NF–5NF) removes redundancy; denormalisation deliberately re-introduces it to make analytical queries fast.",
            "OLTP systems are built for many small real-time transactions; OLAP systems are built for long, complex analytical queries.",
            "Data warehouses, data marts, data lakes and lakehouses each hold data at a different level of structure, cost and query flexibility.",
            "Data is structured, semi-structured or unstructured, and is carried in file formats such as CSV, TSV, JSON, XML, XLSX and Parquet.",
            "Modern data platforms run on-premise, in the cloud or in containers, and AI/ML, NLP and RPA are now standard parts of the data toolchain.",
         ]),
    dict(num=2, code="02",
         title="Data Acquisition and Preparation",
         subtitle="Data integration · queries · exploration · missing values · duplication · outliers · cleansing · parsing · formatting",
         weighting="22%",
         lu="LU2", lo="LO2", ka="K1, A2",
         concepts=[
            "ETL transforms data before it lands in the warehouse; ELT loads it raw into a lake and transforms it later, on demand.",
            "Data can be acquired from databases, APIs, web scraping, machine and log data, public repositories, surveys and sampling.",
            "Data profiling is the disciplined first pass: identify the source, the field names and types, the keys, and what the data actually contains.",
            "The four recurring data-quality defects are missing values (NULL), duplicated or redundant records, invalid values, and outliers.",
            "Cleansing techniques include filtering or imputing NULLs, deduplication, trimming invisible characters, and correcting data types.",
            "Data manipulation covers recoding, derived variables, imputation, aggregation, transposing, appending, merging and parsing.",
            "SQL joins (inner, left, right, full), filters, subqueries, indexes and execution plans are how analysts combine and optimise datasets.",
         ]),
    dict(num=3, code="03",
         title="Data Analysis",
         subtitle="Descriptive statistics · inferential methods · analysis types · communicating results · troubleshooting",
         weighting="24%",
         lu="LU3", lo="LO3", ka="K2, A3",
         concepts=[
            "Descriptive statistics summarise a dataset: central tendency (mean, median, mode) and dispersion (range, variance, standard deviation).",
            "The mean is pulled by outliers; the median resists them — which one you report changes the story the data tells.",
            "Z-scores express how many standard deviations a value sits from the mean, and are the standard outlier test.",
            "The empirical rule says ~99.7% of normally distributed data falls within three standard deviations of the mean.",
            "Inferential statistics generalise beyond the sample: t-tests, p-values, chi-square, correlation and regression.",
            "A p-value below 0.05 indicates the observed difference is unlikely to be due to chance; correlation still never proves causation.",
            "Analysis types — exploratory, performance, trend, gap and link analysis — each answer a different business question.",
         ]),
    dict(num=4, code="04",
         title="Visualization and Reporting",
         subtitle="Chart selection · maps · tables · design elements · dashboards · report types · validation",
         weighting="20%",
         lu="LU4", lo="LO4", ka="K3, A5",
         concepts=[
            "Chart choice follows the question: composition, comparison, distribution, relationship or trend over time.",
            "Line charts carry time series, bar/column charts compare categories, histograms show distribution, scatter plots show relationship.",
            "Pie charts suit a few broad parts of a whole; treemaps suit hierarchical subcategories; heat maps encode magnitude in colour.",
            "Geographic data is shown as dot, filled (choropleth) or layered maps; ArcGIS, Power BI and Tableau all render them.",
            "A dashboard tracks a small set of decisions — filters, drillthrough and tooltips keep it simple rather than exhaustive.",
            "Reports are static, dynamic, real-time, operational, compliance, ad hoc or self-service — the type follows the audience and cadence.",
            "Reporting accuracy is validated by cross-validation, peer review, record-count checks, recalculation and data audits.",
         ]),
    dict(num=5, code="05",
         title="Data Governance, Quality and Controls",
         subtitle="Documentation · versioning · lineage · compliance · retention · privacy · encryption · masking · quality assurance",
         weighting="14%",
         lu="LU5", lo="LO5", ka="A4",
         concepts=[
            "Data governance keeps data high-quality and controlled across its full lifecycle: creation, storage, use, archive and destruction.",
            "Data roles separate accountability: data owner, data steward, data custodian and privacy officer.",
            "Data is classified by sensitivity (public, internal, sensitive, confidential/restricted) and tagged by type (PII, PHI, PIFI, IP).",
            "Regulations impose retention, audit and sovereignty duties — Singapore's PDPA, the EU GDPR, HIPAA and SOX are the common examples.",
            "Protection strategies layer access control (role-based, group-based), encryption at rest/in transit/in use, masking and de-identification.",
            "Data lineage, a data dictionary and version control make a pipeline auditable and reproducible.",
            "Quality assurance runs continuously: profiling, automated validation on entry, monitoring, and testing against agreed quality dimensions.",
         ]),
]

# ------------------------------------------------------------------ day themes (8 training hours/day)
DAY_THEMES = {
    1: "Data Concepts, Schemas and Environments",
    2: "Data Acquisition, Exploration and Preparation",
    3: "Data Analysis — Descriptive and Inferential Statistics",
    4: "Visualization, Dashboards and Reporting",
    5: "Data Governance, Quality, Controls and Final Assessment",
}

# Which domains are taught on which day (drives the Lesson Plan)
DAY_TOPICS = {1: [1], 2: [2], 3: [3], 4: [4], 5: [5]}

# ------------------------------------------------------------------ assessment
ASSESSMENT = dict(
    written="Written Assessment (WA) — Short-Answer Questions (SAQ), 1 hour, individual, summative, open book.",
    practical="Practical Performance (PP) — hands-on scenario-based data tasks, 1 hour, individual, summative, open book.",
    note="A minimum of 75% attendance is required to be eligible for assessment and funding, and the learner must be assessed 'Competent' in both instruments.",
)

# ------------------------------------------------------------------ lab environment
LAB_TOOLS = [
    ("Killercoda Ubuntu Playground", "https://killercoda.com/playgrounds/scenario/ubuntu",
     "A free, browser-based Ubuntu terminal with Python 3, pandas and SQLite — no local install needed."),
    ("RegexLab", "https://alfredang.github.io/regexgenerator/",
     "Real-time regular-expression tester used to build and validate the parsing patterns that clean messy text fields."),
    ("PCAP Analyzer", "https://alfredang.github.io/pcapanalyzer/",
     "Browser-based packet-capture analyser — the course's worked example of machine/log data as a data source."),
    ("IP Calculator", "https://alfredang.github.io/ipcalculator/",
     "Subnet calculator used to derive structured numeric fields from raw network address data."),
    ("Cybersecurity Threat Simulator", "https://alfredang.github.io/cybersecuritysimulator/",
     "Risk-scoring and data-leakage simulator used in the governance domain to reason about classification and protection."),
]

RECOMMENDED_COURSES = [
    "WSQ - CompTIA Certified Security+ Training",
    "WSQ - CompTIA Certified Network+ Training",
    "WSQ - CompTIA Certified Linux+ Training",
    "WSQ - CompTIA Certified Server+ Training",
    "WSQ - CompTIA Certified A+ Training (Core 1 and Core 2)",
]
