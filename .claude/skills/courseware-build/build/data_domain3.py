"""
Domain 3 — Data Analysis (24% of the CompTIA Data+ DA0-001 exam — the heaviest domain).
Maps to LU3 / LO3 (K2, A3).

Labs run on the Killercoda Ubuntu playground with Python 3, pandas and statistics.
"""

KILLERCODA = "https://killercoda.com/playgrounds/scenario/ubuntu"

DOMAIN3 = [
    dict(
        num=8,
        figure="lab08-outlier-mean-median.png",
        topic=3,
        title="Lab 8 — Descriptive Statistics and the Outlier That Moves the Mean",
        objective="Select statistical methods: apply basic statistical techniques to data (Domain 3); LO3 / K2 / A3.",
        desc=("You compute every descriptive statistic the exam names — mean, median, mode, range, variance, standard "
              "deviation and z-score — on a real salary dataset, then remove one outlier and watch which statistics "
              "move and which do not. This is the exam's central-tendency-versus-robustness point, proven with numbers."),
        build="A descriptive-statistics report showing mean, median, mode, range, variance, SD and z-scores, computed with and without the outlier.",
        services="Killercoda Ubuntu, Python 3, pandas, statistics",
        env=KILLERCODA,
        steps=[
            ("Download this lab's dataset. The same files ship in the course repo under this lab's data/ folder.",
             "mkdir -p ~/dataplus/lab8 && cd ~/dataplus/lab8;\nR=https://raw.githubusercontent.com/tertiarycourses;\nB=$R/TGS-2024049212-CompTIA-Certified-Data-Training/main/labs;\nD=lab-08-descriptive-statistics-and-the-outlier-that-moves-th;\nfor f in salaries.csv; do curl -fsSO $B/$D/data/$f || echo FAILED $f; done; ls -l"),
            ("Compute CENTRAL TENDENCY — mean, median and mode together.",
             "python3 -c \"import pandas as pd;d=pd.read_csv('salaries.csv');s=d.salary;print('mean',round(s.mean(),2));print('median',s.median());print('mode',s.mode().tolist())\""),
            ("Compute DISPERSION — min, max, range, variance and standard deviation.",
             "python3 -c \"import pandas as pd;d=pd.read_csv('salaries.csv');s=d.salary;print('min',s.min(),'max',s.max(),'range',s.max()-s.min());print('variance',round(s.var(),2),'sd',round(s.std(),2))\""),
            ("Compute the Z-SCORE for every row and flag anything beyond the standard |z| > 3 threshold.",
             "python3 -c \"import pandas as pd;d=pd.read_csv('salaries.csv');s=d.salary;d['z']=((s-s.mean())/s.std()).round(2);print(d);print('FLAGGED:');print(d[abs(d.z)>3])\""),
            ("Now remove the outlier and recompute the SAME statistics.",
             "python3 -c \"import pandas as pd;d=pd.read_csv('salaries.csv');c=d[d.salary<20000].salary;print('mean',round(c.mean(),2));print('median',c.median());print('sd',round(c.std(),2))\""),
            ("Compare the two runs side by side and record which statistic moved most.",
             "python3 -c \"import pandas as pd;d=pd.read_csv('salaries.csv');a=d.salary;b=d[d.salary<20000].salary;print(f'mean   {a.mean():>9.2f} -> {b.mean():>8.2f}');print(f'median {a.median():>9.2f} -> {b.median():>8.2f}');print(f'sd     {a.std():>9.2f} -> {b.std():>8.2f}')\""),
            ("Compute the departmental summary — this is the aggregation a manager actually asks for.",
             "python3 -c \"import pandas as pd;d=pd.read_csv('salaries.csv');print(d.groupby('dept').salary.agg(['count','mean','median','std']).round(2))\""),
            ("Write your recommendation: which single number should be reported to the board, and why.", ""),
        ],
        test=("Across 61 employees the mean is ~4978 but the median is only 4550. Removing the single Executive salary "
              "drops the mean to ~4628 while the median barely moves (4550 → 4525). E999 is flagged at z ≈ 7.5, far beyond "
              "the |z| > 3 threshold. Your report recommends the MEDIAN as the typical salary."),
        troubleshoot=[
            ("The CSV contains '404: Not Found'", "curl wrote the error page into the file. Confirm the BASE URL, re-run with -fsSO so curl fails loudly, or copy the files from the repo folder you cloned."),
            ("mode returns several values", "A dataset with no repeated value returns every value. pandas .mode() correctly returns a list — report it as 'no single mode'."),
            ("Variance looks enormous", "Variance is in squared units. Report the standard deviation (its square root) instead, which is in dollars."),
            ("Only one row is flagged", "That is correct — the dataset carries exactly one planted outlier (E999) at z ≈ 7.5. Nothing else appears at |z| > 3, which is what a clean distribution looks like."),
        ],
    ),
    dict(
        num=9,
        figure="lab09-abtest.png",
        topic=3,
        title="Lab 9 — Hypothesis Testing: t-test, p-value and the Two Error Types",
        objective="Select statistical methods: inferential techniques, hypothesis testing (Domain 3); LO3 / K2 / A3.",
        desc=("A marketing team claims the new checkout page lifts order value. You state the null and alternative "
              "hypotheses, run a two-sample t-test, read the p-value against the 0.05 threshold, and state your "
              "conclusion in business language — including which error type you would be risking if you are wrong."),
        build="A completed hypothesis test: stated H0/H1, computed t-statistic and p-value, an accept/reject decision, and the business recommendation.",
        services="Killercoda Ubuntu, Python 3, pandas, scipy",
        env=KILLERCODA,
        steps=[
            ("Download this lab's dataset. The same files ship in the course repo under this lab's data/ folder.",
             "mkdir -p ~/dataplus/lab9 && cd ~/dataplus/lab9;\nR=https://raw.githubusercontent.com/tertiarycourses;\nB=$R/TGS-2024049212-CompTIA-Certified-Data-Training/main/labs;\nD=lab-09-hypothesis-testing-t-test-p-value-and-the-two-error;\nfor f in abtest.csv; do curl -fsSO $B/$D/data/$f || echo FAILED $f; done; ls -l"),
                        ("STATE THE HYPOTHESES before you look at any result — this is the discipline the exam tests.  "
             "H0: there is no difference in mean order value.  H1: the new page has a higher mean order value.", ""),
            ("Look at the group means first — a difference here is necessary but NOT sufficient.",
             "python3 -c \"import pandas as pd;d=pd.read_csv('abtest.csv');print(d.groupby('group').order_value.agg(['count','mean','std']).round(2))\""),
            ("Run the two-sample t-test and read the p-value.",
             "python3 -c \"import pandas as pd;from scipy import stats;d=pd.read_csv('abtest.csv');a=d[d.group=='A'].order_value;b=d[d.group=='B'].order_value;t,p=stats.ttest_ind(a,b);print('t =',round(t,4));print('p =',round(p,6))\""),
            ("Apply the 0.05 decision rule explicitly.",
             "python3 -c \"import pandas as pd;from scipy import stats;d=pd.read_csv('abtest.csv');a=d[d.group=='A'].order_value;b=d[d.group=='B'].order_value;t,p=stats.ttest_ind(a,b);print('REJECT H0 - the difference is statistically significant' if p<0.05 else 'FAIL TO REJECT H0')\""),
            ("Compute the 95% confidence interval for the difference so you can report a range, not just a verdict.",
             "python3 -c \"import pandas as pd,numpy as np;from scipy import stats;d=pd.read_csv('abtest.csv');a=d[d.group=='A'].order_value;b=d[d.group=='B'].order_value;diff=b.mean()-a.mean();se=np.sqrt(a.var()/len(a)+b.var()/len(b));print('diff',round(diff,2),'95% CI',(round(diff-1.96*se,2),round(diff+1.96*se,2)))\""),
            ("Now the error-type question. Write down: if you reject H0 and you are WRONG, which error is that "
             "(Type I) and what does it cost the business? If you fail to reject and you are wrong (Type II), what does that cost?", ""),
            ("Write the one-paragraph recommendation a manager could act on — no statistics jargon.", ""),
        ],
        test=("With 60 observations per group the t-test returns t ≈ -11.3 and p ≈ 1.9e-20, far below 0.05, so you "
              "REJECT H0. Group B averages about 49.65 against 41.14 for group A — a lift of roughly 8.5, with a 95% "
              "confidence interval that excludes zero."),
        troubleshoot=[
            ("The CSV contains '404: Not Found'", "curl wrote the error page into the file. Confirm the BASE URL, re-run with -fsSO so curl fails loudly, or copy the files from the repo folder you cloned."),
            ("ModuleNotFoundError: scipy", "Run pip3 install scipy, adding --break-system-packages if Killercoda's pip refuses."),
            ("p-value is nan", "One group has fewer than two values or zero variance. Check your CSV loaded all 16 rows with d.shape."),
            ("The result feels too clean", "It is a teaching dataset with clean separation. Ask the trainer for the noisy variant to see a borderline p-value."),
        ],
    ),
    dict(
        num=10,
        figure="lab10-correlation-trap.png",
        topic=3,
        title="Lab 10 — Correlation, Regression and the Causation Trap",
        objective="Select statistical methods: correlation and regression; troubleshoot analysis issues (Domain 3); LO3 / LO5 / A3 / A4.",
        desc=("You measure the relationship between marketing spend and revenue with Pearson's r and R-squared, fit a "
              "regression line, use it to predict — and then meet a third dataset where two variables correlate almost "
              "perfectly with no causal link at all. Recognising that trap is an exam objective and a professional duty."),
        build="A correlation matrix, a fitted regression equation with R-squared, a prediction, and a written spurious-correlation analysis.",
        services="Killercoda Ubuntu, Python 3, pandas, scipy",
        env=KILLERCODA,
        steps=[
            ("Download this lab's dataset. The same files ship in the course repo under this lab's data/ folder.",
             "mkdir -p ~/dataplus/lab10 && cd ~/dataplus/lab10;\nR=https://raw.githubusercontent.com/tertiarycourses;\nB=$R/TGS-2024049212-CompTIA-Certified-Data-Training/main/labs;\nD=lab-10-correlation-regression-and-the-causation-trap;\nfor f in marketing.csv; do curl -fsSO $B/$D/data/$f || echo FAILED $f; done; ls -l"),
            ("Compute the full CORRELATION MATRIX — every pair at once.",
             "python3 -c \"import pandas as pd;d=pd.read_csv('marketing.csv');print(d[['spend','revenue','staff']].corr().round(4))\""),
            ("Get Pearson's r and its p-value for spend versus revenue specifically.",
             "python3 -c \"import pandas as pd;from scipy import stats;d=pd.read_csv('marketing.csv');r,p=stats.pearsonr(d.spend,d.revenue);print('r =',round(r,4));print('r-squared =',round(r**2,4));print('p =',round(p,8))\""),
            ("Fit the REGRESSION LINE and read off the slope and intercept.",
             "python3 -c \"import pandas as pd;from scipy import stats;d=pd.read_csv('marketing.csv');lr=stats.linregress(d.spend,d.revenue);print(f'revenue = {lr.slope:.3f} * spend + {lr.intercept:.3f}');print('R-squared =',round(lr.rvalue**2,4))\""),
            ("Use the model to PREDICT revenue at a spend level you have never observed.",
             "python3 -c \"import pandas as pd;from scipy import stats;d=pd.read_csv('marketing.csv');lr=stats.linregress(d.spend,d.revenue);print('predicted revenue at spend=40:',round(lr.slope*40+lr.intercept,2))\""),
            ("State the limit of that prediction: spend=40 is outside the observed range (10–33). Write down why "
             "extrapolating beyond your data is the analysis error the exam warns about.", ""),
            ("THE TRAP — now look at staff versus revenue. The correlation is nearly as strong.",
             "python3 -c \"import pandas as pd;from scipy import stats;d=pd.read_csv('marketing.csv');r,p=stats.pearsonr(d.staff,d.revenue);print('staff vs revenue r =',round(r,4))\""),
            ("Explain in writing: does hiring staff CAUSE revenue? Identify the confounding variable that drives both, "
             "and state the one sentence every analyst must be able to defend — correlation is not causation.", ""),
        ],
        test=("Across 36 months spend and revenue correlate at r ≈ 0.991 with R-squared ≈ 0.982, giving "
              "revenue ≈ 6.55 × spend + 54.1. Staff headcount ALSO correlates with revenue at r ≈ 0.970 — but growth "
              "over time drives both, so that second relationship is not causal."),
        troubleshoot=[
            ("The CSV contains '404: Not Found'", "curl wrote the error page into the file. Confirm the BASE URL, re-run with -fsSO so curl fails loudly, or copy the files from the repo folder you cloned."),
            ("r is exactly 1.0", "Perfect correlation means the data is synthetic and noise-free. Note that real business data never looks like this."),
            ("linregress has no attribute rvalue", "You are on a very old scipy. Use r,p = stats.pearsonr(...) and square r yourself."),
            ("The prediction looks unreasonable", "That is the extrapolation lesson — a linear model fitted on 10–33 has no evidence about 40. Say so in the report."),
        ],
    ),
]
