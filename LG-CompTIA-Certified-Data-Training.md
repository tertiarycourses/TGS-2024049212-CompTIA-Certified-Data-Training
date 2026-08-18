# Learner Guide - CompTIA Certified Data+ Training

## Course Overview

This learner guide supports practical CompTIA Data+ training for learners preparing for entry-level data analytics work and DA0-001-style scenarios. The course emphasizes hands-on data handling, analysis, visualization, and governance rather than only memorizing definitions.

The labs follow the five major Data+ skill areas:

1. Data concepts and environments.
2. Data mining.
3. Data analysis.
4. Visualization.
5. Data governance, quality, and controls.

## Before You Start

### Recommended Lab Tools

Use one or more of the following:

- Microsoft Excel.
- LibreOffice Calc.
- Google Sheets.
- SQLite DB Browser or SQLite CLI.
- Power BI Desktop.
- Tableau Public.
- OpenRefine.
- Text editor for CSV, JSON, and SQL.

### Sample Dataset

Use a trainer-provided CSV dataset or a simple business dataset with fields such as:

- `order_id`
- `order_date`
- `customer_segment`
- `region`
- `product_category`
- `quantity`
- `revenue`
- `cost`
- `discount`
- `satisfaction_score`
- `case_status`

If no dataset is provided, create a small table with at least 50 rows and enough variation to support filtering, aggregation, charts, and quality checks.

### Data Ethics Checklist

Before each lab:

1. Do not use real personal data unless authorized.
2. Remove or mask direct identifiers.
3. Keep raw data separate from cleaned data.
4. Document assumptions and changes.
5. Do not overstate conclusions beyond the data.

### Lab Journal

For every lab, record:

- Dataset used.
- Fields analyzed.
- Cleaning steps.
- Formulas or SQL queries.
- Charts created.
- Findings.
- Quality limitations.
- Governance notes.

## Learning Outcomes

By the end of the course, you should be able to:

1. Classify common data types, structures, and sources.
2. Describe relational, flat file, semi-structured, and unstructured data.
3. Import, profile, clean, and validate data.
4. Use simple SQL for extraction, filtering, joining, and grouping.
5. Calculate descriptive statistics and identify outliers.
6. Analyze trends, segments, correlations, and business questions.
7. Define KPIs and build answer-focused findings.
8. Select appropriate charts for different analytical needs.
9. Build a simple dashboard with filters and clear visual hierarchy.
10. Explain data quality, lineage, access, privacy, retention, and controls.
11. Complete an end-to-end data analysis case.

## Course Flow

### Day 1

| Time | Activity |
| --- | --- |
| 09:00 | Course briefing, exam domains, dataset setup |
| 09:30 | Lab 01 - Data Concepts, Environments, and Dataset Inventory |
| 11:00 | Lab 02 - Data Acquisition, Profiling, and Cleaning |
| 13:30 | Lab 03 - Data Mining with SQL, Filtering, and Joins |
| 15:30 | Lab 04 - Statistics, Analysis, Trends, and Correlations |
| 17:00 | Day 1 review and cleaned data backup |

### Day 2

| Time | Activity |
| --- | --- |
| 09:00 | Day 1 recap |
| 09:30 | Lab 05 - Analysis Scenarios, KPIs, and Business Questions |
| 11:30 | Lab 06 - Visualization, Chart Selection, and Dashboard Design |
| 14:00 | Lab 07 - Data Governance, Quality, Controls, and Privacy |
| 15:30 | Lab 08 - Capstone Analysis and Performance-Based Exam Review |
| 17:00 | Final readiness checklist |

## Lab 01 Guide - Data Concepts, Environments, and Dataset Inventory

### Objectives

- Classify data types and structures.
- Identify data sources and storage environments.
- Create a dataset inventory.
- Document metadata.

### Steps

1. Open the sample dataset.
2. Identify each field name and business meaning.
3. Classify fields as numeric, text, date/time, Boolean, categorical, or identifier.
4. Identify whether the data is structured, semi-structured, or unstructured.
5. Identify source type: transactional, operational, survey, log, external, or reference.
6. Create a data dictionary.
7. Record sample values, allowed values, and units.
8. Identify primary key candidates and duplicate risk.
9. Draw a simple data flow from source to report.
10. Identify where the data is stored: file, database, data warehouse, data lake, or application.

### Deliverables

- Data dictionary.
- Dataset inventory.
- Data flow sketch.
- Metadata notes.

### Checkpoint

You can explain what each field means and why metadata matters before analysis.

## Lab 02 Guide - Data Acquisition, Profiling, and Cleaning

### Objectives

- Import data safely.
- Profile data quality.
- Clean missing, duplicate, and inconsistent values.
- Preserve raw data.

### Steps

1. Save a read-only copy of the raw dataset.
2. Import the dataset into your spreadsheet or database tool.
3. Count total rows and columns.
4. Check column data types.
5. Identify missing values.
6. Identify duplicates.
7. Identify inconsistent categories, such as spelling or capitalization differences.
8. Identify invalid dates, negative values, or impossible values.
9. Create a cleaning log.
10. Clean categories and format dates.
11. Remove or flag duplicates based on trainer guidance.
12. Decide how to handle missing values: remove, impute, leave blank, or mark unknown.
13. Save the cleaned dataset separately.

### Deliverables

- Raw dataset backup.
- Data profile summary.
- Cleaning log.
- Cleaned dataset.

### Checkpoint

You can explain every cleaning decision and its effect on analysis.

## Lab 03 Guide - Data Mining with SQL, Filtering, and Joins

### Objectives

- Extract data using simple SQL.
- Filter and group records.
- Join related tables.
- Prepare analysis extracts.

### Steps

1. Load the cleaned dataset into SQLite or use a trainer-provided database.
2. Run a basic `SELECT` query.
3. Filter records with `WHERE`.
4. Sort records with `ORDER BY`.
5. Group records with `GROUP BY`.
6. Calculate counts, sums, averages, minimums, and maximums.
7. Create a second reference table such as region targets or product categories if needed.
8. Join the main table to the reference table.
9. Export a query result for analysis.
10. Save all SQL queries in a text file.

### Deliverables

- SQL query file.
- Filtered extract.
- Aggregated summary table.
- Join result.

### Checkpoint

You can write a SQL query that answers a specific business question.

## Lab 04 Guide - Statistics, Analysis, Trends, and Correlations

### Objectives

- Calculate descriptive statistics.
- Identify outliers.
- Analyze trends.
- Review correlation carefully.

### Steps

1. Open the cleaned dataset.
2. Calculate count, sum, mean, median, minimum, maximum, range, and standard deviation for key measures.
3. Create a histogram for one numeric measure.
4. Identify possible outliers.
5. Create a time-based summary by day, week, or month.
6. Plot a trend line chart.
7. Compare performance by segment, region, or category.
8. Calculate correlation between two numeric fields where appropriate.
9. Write a warning note that correlation does not prove causation.
10. Write three analytical observations supported by numbers.

### Deliverables

- Descriptive statistics table.
- Histogram.
- Trend summary.
- Segment comparison.
- Correlation note.

### Checkpoint

You can describe what changed, where it changed, and what still needs more evidence.

## Lab 05 Guide - Analysis Scenarios, KPIs, and Business Questions

### Objectives

- Translate business questions into metrics.
- Define KPIs.
- Calculate and compare performance.
- Write answer-first findings.

### Steps

1. Choose three business questions from your dataset.
2. Define the metric needed for each question.
3. Write numerator, denominator, filters, and time period.
4. Calculate KPI values.
5. Compare KPI values across segments.
6. Identify the best and worst performing groups.
7. Check whether sample size is large enough to support the comparison.
8. Create a short findings table with metric, result, interpretation, and caveat.
9. Write one recommendation based on evidence.
10. Identify one follow-up question.

### Deliverables

- Business question list.
- KPI definition table.
- KPI calculations.
- Findings and recommendation table.

### Checkpoint

You can connect metrics to business questions instead of reporting numbers without context.

## Lab 06 Guide - Visualization, Chart Selection, and Dashboard Design

### Objectives

- Select charts based on analytical purpose.
- Build clear visualizations.
- Create a simple dashboard.
- Apply readability and accessibility checks.

### Steps

1. Select four findings from Lab 05.
2. Choose a chart for each finding: bar, line, scatter, histogram, table, or KPI card.
3. Build each chart with clear title, axis labels, and units.
4. Avoid 3D effects and unnecessary decoration.
5. Use consistent colors.
6. Add filters such as region, segment, or date if your tool supports them.
7. Arrange charts into a dashboard.
8. Add a short insight statement for each chart.
9. Check that labels are readable.
10. Export or screenshot the dashboard.

### Deliverables

- Chart selection table.
- Four charts.
- Simple dashboard.
- Dashboard insight notes.

### Checkpoint

You can explain why each visual was chosen and what action it supports.

## Lab 07 Guide - Data Governance, Quality, Controls, and Privacy

### Objectives

- Review data governance concepts.
- Define quality checks.
- Document lineage and access.
- Identify privacy and control risks.

### Steps

1. Identify the owner and steward for the dataset.
2. Draw a simple lineage diagram from source to dashboard.
3. Define quality rules for completeness, validity, consistency, uniqueness, and timeliness.
4. Identify sensitive or personal fields.
5. Decide which fields should be masked, removed, or restricted.
6. Define access roles such as viewer, editor, analyst, and administrator.
7. Define retention and deletion expectations.
8. Identify audit or approval points.
9. Create a governance checklist for the dataset.
10. Add governance caveats to your dashboard notes.

### Deliverables

- Lineage diagram.
- Data quality rule table.
- Access control matrix.
- Governance checklist.

### Checkpoint

You can explain how trustworthy data depends on quality, ownership, security, and controls.

## Lab 08 Guide - Capstone Analysis and Performance-Based Exam Review

### Objectives

- Complete an end-to-end analysis case.
- Produce a clean dataset, findings, visuals, and governance notes.
- Practise performance-based exam thinking.
- Build a final study plan.

### Steps

1. Start with a raw or trainer-provided dataset.
2. Create a data dictionary.
3. Profile and clean the dataset.
4. Write at least three SQL queries or spreadsheet summaries.
5. Calculate at least three KPIs.
6. Create at least three charts.
7. Build a one-page dashboard or report.
8. Add two data quality caveats.
9. Add one governance recommendation.
10. Present your findings in five minutes.
11. Map weak areas to Data+ domains.
12. Write a 14-day study plan.

### Deliverables

- Cleaned dataset.
- Query or formula file.
- KPI table.
- Dashboard or report.
- Governance notes.
- Personal study plan.

### Checkpoint

You can complete a practical data task from raw data to a supported recommendation.

## Final Readiness Checklist

Before finishing the course, confirm that you can:

- Classify data types and structures.
- Create a data dictionary.
- Profile and clean data.
- Use basic SQL or spreadsheet formulas.
- Calculate descriptive statistics.
- Analyze trends and segments.
- Define KPIs.
- Choose appropriate charts.
- Build a simple dashboard.
- Explain data governance and quality controls.
- Document assumptions and caveats.
- Present findings clearly.
