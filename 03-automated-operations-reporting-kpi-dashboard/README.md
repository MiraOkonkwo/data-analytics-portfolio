# Automated Operations Reporting & KPI Dashboard

**Live dashboard:** https://miraokonkwo.github.io/data-analytics-portfolio/weekly-ops-report/

This one is the most direct match to my actual job. As a Data and Operations Coordinator, I track scheduling, workflow, and performance data. I write it up into a weekly report for management. This project takes a raw call center log and automates that same work. It builds the same KPIs on the same weekly schedule. A script generates it. Nobody has to rebuild it by hand in Excel every Monday.

## What's in the report

- **Volume:** calls received per week
- **Abandonment rate:** the share of calls that hang up before reaching an agent
- **First-contact resolution (FCR):** the share of answered calls resolved without a callback
- **Average handle time:** how long an agent spends on a typical call
- **Customer satisfaction (CSAT):** the average post-call rating
- All of the above broken down by department and by agent, plus week-over-week deltas on the headline KPI tiles

## What I found

1. **Call volume is stable.** It ranges from 356 to 442 calls a week across the quarter. There is no clear upward or downward trend. It's predictable enough to staff against.
2. **Abandonment rate is the real problem.** It never dropped below 16% in any of the 12 full weeks in the quarter. A typical call center benchmark is 5 to 8%. This queue ran at double to quadruple that. It happened every single week, not just on a bad day.
3. **Department and agent performance are both fairly even.** FCR sits in the high 80s to low 90s across all five departments and all eight agents. CSAT hovers around 3.3 to 3.5 out of 5 everywhere. The abandonment problem is not one team or one product line. It's systemic.

## Why this matters as a portfolio piece

A one-off report can miss a problem like this. A single bad week just looks like an anomaly. A running weekly report catches it right away, because week 1 and week 12 tell the same story. That's the real value of automating a report like this. It turns "did this get worse" into a question you can answer by looking, not by re-pulling data.

## Data and methods

- **Source:** a public call center call log (`data/call_center_raw.csv`). It has 5,000 calls across 9 agents and 5 product departments, January to March 2015. See [Data credit](#data-credit) below.
- **Cleaning:** one call was logged under agent "L", a single-letter name with only 1 call in the whole dataset. I treated it as a data-entry error. I left it out of the agent leaderboard. It's not a real ninth agent, just one bad record.
- **Analysis:** Python and pandas, in [`notebooks/01_analysis.py`](notebooks/01_analysis.py). It computes weekly, department-level, and agent-level KPIs from the raw call log. It writes the results to `outputs/`.
- **Partial weeks:** the first and last calendar weeks in the data only cover part of a week. The data starts January 1 and ends March 31. Neither date lands on a Monday. I left both weeks out of the trend charts. This avoids a misleading dip or spike at either edge.
- **Dashboard:** a single-page report (`dashboard.html`). It reads like the actual weekly report I'd hand to a manager: headline KPI tiles with week-over-week deltas, two trend charts, and department and agent breakdown tables.

## The honest limitation

This is a static HTML page. It's built from a CSV snapshot. It is not a live Power BI or Tableau report connected to a real database. The KPI logic in `01_analysis.py` is exactly what I would port into Power BI's data model, or into a scheduled Python pipeline, if this connected to a live system. I built it this way so anyone with a link can view it. There's nothing to install.

## Repo structure

```
03-automated-operations-reporting-kpi-dashboard/
├── README.md
├── dashboard.html              # the published weekly report
├── data/
│   └── call_center_raw.csv
├── notebooks/
│   └── 01_analysis.py
└── outputs/
    ├── weekly_kpis.csv
    ├── department_kpis.csv
    ├── agent_kpis.csv
    └── satisfaction_distribution.csv
```

## Data credit

Call log CSV from [piyusharya8700/CALL-CENTER-DATASET](https://github.com/piyusharya8700/CALL-CENTER-DATASET) on GitHub. It's a cleaned version of a commonly used public call center practice dataset.
