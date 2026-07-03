# Tools Reference

## Free Tools

| Tool | Use |
| --- | --- |
| Microsoft Excel | Data cleaning, formulas, pivots, charts. |
| LibreOffice Calc | Spreadsheet alternative for formulas and charts. |
| Google Sheets | Shared data cleaning and basic dashboards. |
| SQLite DB Browser | SQL queries, joins, and extracts. |
| Power BI Desktop | Dashboards and data modeling where available. |
| Tableau Public | Dashboards and visual storytelling where available. |
| OpenRefine | Data profiling and cleaning where available. |
| diagrams.net | Data flow and lineage diagrams. |

## Spreadsheet Formula Examples

```text
=COUNT(A:A)
=COUNTA(A:A)
=COUNTBLANK(A:A)
=AVERAGE(B:B)
=MEDIAN(B:B)
=STDEV.S(B:B)
=SUMIF(A:A,"East",B:B)
=COUNTIF(C:C,"Open")
=IF(ISBLANK(A2),"Missing","OK")
```

## SQL Snippets

```sql
SELECT * FROM orders LIMIT 10;
SELECT region, COUNT(*) AS row_count
FROM orders
GROUP BY region;

SELECT product_category, SUM(revenue) AS total_revenue
FROM orders
WHERE order_date >= '2026-01-01'
GROUP BY product_category
ORDER BY total_revenue DESC;
```

## Data Quality Dimensions

- Completeness.
- Validity.
- Consistency.
- Uniqueness.
- Accuracy.
- Timeliness.
