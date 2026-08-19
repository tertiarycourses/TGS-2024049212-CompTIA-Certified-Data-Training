"""
Domain 4 — Visualization and Reporting (20% of the CompTIA Data+ DA0-001 exam).
Maps to LU4 / LO4 (K3, A5).

Labs run on the Killercoda Ubuntu playground with Python 3, pandas and matplotlib
(rendered to PNG, then viewed/downloaded), producing real chart artefacts.
"""

KILLERCODA = "https://killercoda.com/playgrounds/scenario/ubuntu"

DOMAIN4 = [
    dict(
        num=11,
        figure="lab11-chart-selection.png",
        topic=4,
        title="Lab 11 — Choose the Right Chart: Five Questions, Five Chart Types",
        objective="Create effective visuals: use charts, maps, tables and design elements (Domain 4); LO4 / K3 / A5.",
        desc=("Chart choice is not decoration — it is determined by the question being asked. You take ONE dataset and "
              "answer five different business questions from it, each demanding a different chart type, then build a "
              "deliberately wrong chart so you can articulate exactly why it misleads."),
        build="Five correctly chosen charts (line, bar, pie, histogram, scatter) as PNG files, plus one annotated 'wrong chart' example.",
        services="Killercoda Ubuntu, Python 3, pandas, matplotlib",
        env=KILLERCODA,
        steps=[
            ("Download this lab's dataset. The same files ship in the course repo under this lab's data/ folder.",
             "mkdir -p ~/dataplus/lab11 && cd ~/dataplus/lab11;\nR=https://raw.githubusercontent.com/tertiarycourses;\nB=$R/TGS-2024049212-CompTIA-Certified-Data-Training/main/labs;\nD=lab-11-choose-the-right-chart-five-questions-five-chart-typ;\nfor f in sales.csv; do curl -fsSO $B/$D/data/$f || echo FAILED $f; done; ls -l"),
                        ("Q1 'How is revenue trending?' → LINE CHART, because the x-axis is time.",
             "python3 -c \"import pandas as pd,matplotlib;matplotlib.use('Agg');import matplotlib.pyplot as plt;d=pd.read_csv('sales.csv');p=d.pivot_table(index='month',columns='region',values='revenue').reindex(['Jan','Feb','Mar']);p.plot(marker='o');plt.title('Revenue Trend by Region');plt.ylabel('Revenue (SGD k)');plt.tight_layout();plt.savefig('01_line.png',dpi=120)\""),
            ("Q2 'Which region sells most?' → BAR CHART, because you are comparing categories.",
             "python3 -c \"import pandas as pd,matplotlib;matplotlib.use('Agg');import matplotlib.pyplot as plt;d=pd.read_csv('sales.csv');d.groupby('region').revenue.sum().sort_values().plot(kind='barh',color='#1F6FEB');plt.title('Total Revenue by Region');plt.xlabel('Revenue (SGD k)');plt.tight_layout();plt.savefig('02_bar.png',dpi=120)\""),
            ("Q3 'What share does each region hold?' → PIE CHART, because it is parts of one whole (and only 3 slices).",
             "python3 -c \"import pandas as pd,matplotlib;matplotlib.use('Agg');import matplotlib.pyplot as plt;d=pd.read_csv('sales.csv');d.groupby('region').revenue.sum().plot(kind='pie',autopct='%1.1f%%',colors=['#1F6FEB','#10B981','#7C3AED']);plt.title('Revenue Share by Region');plt.ylabel('');plt.tight_layout();plt.savefig('03_pie.png',dpi=120)\""),
            ("Q4 'How are order sizes distributed?' → HISTOGRAM, because you want the shape of one variable.",
             "python3 -c \"import pandas as pd,matplotlib;matplotlib.use('Agg');import matplotlib.pyplot as plt;d=pd.read_csv('sales.csv');d.orders.plot(kind='hist',bins=5,color='#F59E0B',edgecolor='white');plt.title('Distribution of Order Counts');plt.xlabel('Orders per region-month');plt.tight_layout();plt.savefig('04_hist.png',dpi=120)\""),
            ("Q5 'Do more orders mean higher revenue?' → SCATTER PLOT, because you are testing a relationship.",
             "python3 -c \"import pandas as pd,matplotlib;matplotlib.use('Agg');import matplotlib.pyplot as plt;d=pd.read_csv('sales.csv');plt.scatter(d.orders,d.revenue,c='#7C3AED',s=80);plt.title('Orders vs Revenue');plt.xlabel('Orders');plt.ylabel('Revenue (SGD k)');plt.tight_layout();plt.savefig('05_scatter.png',dpi=120)\""),
            ("Now build the WRONG chart on purpose — a pie chart of a time series, which destroys the time ordering.",
             "python3 -c \"import pandas as pd,matplotlib;matplotlib.use('Agg');import matplotlib.pyplot as plt;d=pd.read_csv('sales.csv');d.groupby('month').revenue.sum().plot(kind='pie',autopct='%1.1f%%');plt.title('WRONG: revenue by month as a pie');plt.ylabel('');plt.tight_layout();plt.savefig('06_wrong.png',dpi=120)\""),
            ("List the generated files and write one line per chart stating the question it answers.",
             "ls -1 *.png"),
            ("Write the critique of 06_wrong.png: what does a pie chart hide that a line chart shows?", ""),
        ],
        test=("Six PNG files exist, built from 24 rows covering 6 months × 4 regions. Each of the five correct charts "
              "answers its stated question, and your critique of the wrong chart explains that a pie destroys the "
              "sequence and makes a trend impossible to read."),
        troubleshoot=[
            ("The CSV contains '404: Not Found'", "curl wrote the error page into the file. Confirm the BASE URL, re-run with -fsSO so curl fails loudly, or copy the files from the repo folder you cloned."),
            ("No display / tkinter error", "You must set matplotlib.use('Agg') BEFORE importing pyplot — headless terminals have no display."),
            ("The PNG is blank", "You saved after calling plt.show() or a new figure. Call plt.savefig() before any clf/show, and use plt.close() between charts."),
            ("Months are out of order", "Alphabetical sorting puts Feb first. The .reindex(['Jan','Feb','Mar']) call is what fixes it."),
        ],
    ),
    dict(
        num=12,
        figure="lab12-dashboard.png",
        topic=4,
        title="Lab 12 — Build a KPI Dashboard and Validate Its Accuracy",
        objective="Deliver reports: dashboards and summaries; validate reporting accuracy (Domain 4); LO4 / K3 / A5.",
        desc=("You assemble a four-panel executive dashboard from the integrated dataset, then run the validation checks "
              "the exam requires — record-count reconciliation, recalculation and cross-validation — and deliberately "
              "plant one error so you can prove your validation process actually catches it."),
        build="A four-panel KPI dashboard PNG plus a signed validation checklist that catches a planted reporting error.",
        services="Killercoda Ubuntu, Python 3, pandas, matplotlib",
        env=KILLERCODA,
        steps=[
            ("Download this lab's dataset. The same files ship in the course repo under this lab's data/ folder.",
             "mkdir -p ~/dataplus/lab12 && cd ~/dataplus/lab12;\nR=https://raw.githubusercontent.com/tertiarycourses;\nB=$R/TGS-2024049212-CompTIA-Certified-Data-Training/main/labs;\nD=lab-12-build-a-kpi-dashboard-and-validate-its-accuracy;\nfor f in kpi.csv; do curl -fsSO $B/$D/data/$f || echo FAILED $f; done; ls -l"),
            ("Compute the headline KPIs first — you must know the true numbers BEFORE you draw anything.",
             "python3 -c \"import pandas as pd;d=pd.read_csv('kpi.csv');print('total revenue',d.revenue.sum());print('total orders',d.orders.sum());print('avg order value',round(d.revenue.sum()*1000/d.orders.sum(),2));print('vs target',round(d.revenue.sum()*100/d.target.sum(),1),'%')\""),
            ("Build the four-panel dashboard in one script.",
             "cat > dashboard.py <<'EOF'\nimport pandas as pd, matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\nd = pd.read_csv('kpi.csv')\nfig, ax = plt.subplots(2, 2, figsize=(12, 7))\nfig.suptitle('Regional Sales Dashboard  ·  Q1', fontsize=15, fontweight='bold')\nd.pivot_table(index='month', columns='region', values='revenue').reindex(['Jan','Feb','Mar']).plot(ax=ax[0][0], marker='o')\nax[0][0].set_title('Revenue Trend'); ax[0][0].set_ylabel('SGD k')\nd.groupby('region').revenue.sum().plot(kind='bar', ax=ax[0][1], color='#1F6FEB')\nax[0][1].set_title('Revenue by Region')\nact = d.groupby('region').revenue.sum(); tgt = d.groupby('region').target.sum()\n(act/tgt*100).plot(kind='bar', ax=ax[1][0], color='#10B981')\nax[1][0].axhline(100, color='red', ls='--'); ax[1][0].set_title('% of Target')\nax[1][1].scatter(d.orders, d.revenue, c='#7C3AED', s=70)\nax[1][1].set_title('Orders vs Revenue'); ax[1][1].set_xlabel('Orders')\nplt.tight_layout(rect=[0,0,1,0.95])\nplt.savefig('dashboard.png', dpi=120)\nprint('dashboard.png written')\nEOF\npython3 dashboard.py"),
            ("VALIDATION 1 — record count. Does the dashboard cover every source row?",
             "python3 -c \"import pandas as pd;d=pd.read_csv('kpi.csv');print('source rows',len(d));print('rows charted',d.groupby(['month','region']).ngroups)\""),
            ("VALIDATION 2 — recalculate the headline total a second, independent way.",
             "python3 -c \"import pandas as pd;d=pd.read_csv('kpi.csv');a=d.revenue.sum();b=sum(d.groupby('region').revenue.sum());print('method A',a,'method B',b,'MATCH' if a==b else 'MISMATCH')\""),
            ("VALIDATION 3 — cross-validate the % of target figure against a hand calculation.",
             "python3 -c \"import pandas as pd;d=pd.read_csv('kpi.csv');print('Central', round(d[d.region=='Central'].revenue.sum()/d[d.region=='Central'].target.sum()*100,1),'% expected 111.9')\""),
            ("Now PLANT AN ERROR — corrupt one revenue value and rebuild the dashboard.",
             "sed -i 's/Mar,North,159.5/Mar,North,1595/' kpi.csv && python3 dashboard.py"),
            ("Re-run validation 2 and 3 and confirm your checks CATCH the planted error.",
             "python3 -c \"import pandas as pd;d=pd.read_csv('kpi.csv');print('total now',round(d.revenue.sum(),1),'(was 3021.3)');print('North % of target',round(d[d.region=='North'].revenue.sum()/d[d.region=='North'].target.sum()*100,1),'%')\""),
            ("Restore the correct value and confirm the dashboard returns to its validated state.",
             "sed -i 's/Mar,North,1595/Mar,North,159.5/' kpi.csv && python3 dashboard.py && python3 -c \"import pandas as pd;print('total',pd.read_csv('kpi.csv').revenue.sum())\""),
            ("Sign off the validation checklist: record count, recalculation, cross-validation, and visual review.", ""),
        ],
        test=("dashboard.png shows four panels built from 24 rows. Total revenue validates at 3021.3 by two independent "
              "methods. After the planted error the total jumps to 4456.8 and North reports 276.9% of target — an "
              "impossible figure your validation catches immediately. Restoring the value returns the total to 3021.3."),
        troubleshoot=[
            ("The CSV contains '404: Not Found'", "curl wrote the error page into the file. Confirm the BASE URL, re-run with -fsSO so curl fails loudly, or copy the files from the repo folder you cloned."),
            ("Panels overlap or the title is cut", "Use plt.tight_layout(rect=[0,0,1,0.95]) so the suptitle gets its own space."),
            ("sed did not change anything", "sed needs a BYTE-EXACT match. Run grep 'Mar,North' kpi.csv and copy the value from the output — 159.5 is not the same string as 159.50 or 161."),
            ("The % of target axis looks wrong", "Confirm you summed target per region (3 months × the monthly target), not just one month's value."),
        ],
    ),
]
