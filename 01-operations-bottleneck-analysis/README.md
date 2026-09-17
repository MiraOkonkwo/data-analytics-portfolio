# Fulfillment Risk Analysis: Why First Class Shipping Fails 95% of the Time

**Live dashboard:** https://miraokonkwo.github.io/data-analytics-portfolio/fulfillment-risk-analysis/

I looked at 180,519 order line items from the DataCo Smart Supply Chain dataset (Jan 2015 to Jan 2018) to answer one question: where in the fulfillment process do late deliveries actually come from?

## Why I built this

In my current role as a Data and Operations Coordinator, the recurring problem was never a lack of data. It was information gaps that hid where a process was actually breaking down. I wanted to apply that same lens to a real dataset: don't just report the late-delivery rate, trace it back to its root cause and put a number on what it costs.

## What I found

1. **The SLA is the bottleneck, not the warehouse.** The overall late-delivery rate is 54.8%, but it's wildly uneven by shipping mode. First Class is late 95.3% of the time. Second Class, 76.6%. Same Day, 45.7%. Standard Class, just 38.1%. The tier sold as fastest is the least dependable one.
2. **It's chronic, not seasonal.** The monthly late rate stays in a tight 51.9% to 56.8% band across all 37 months. No holiday spike, no gradual improvement. This is a structural process problem, not a one-off event.
3. **Every region shows the same pattern.** All 23 regions band almost identically by shipping mode (First Class is 92 to 100% late in every single one), which rules out regional carriers or local ops teams as the cause.
4. **Department is a red herring too.** Product category late rates sit in a narrow 4.5-point band (54.4% to 58.9%), compared to a 57-point spread across shipping modes.
5. **The cost is real.** $20.1M in sales rides on a late order, and 18,553 orders were both late and unprofitable, adding up to $2.15M in lost margin.

## What I'd recommend

1. Re-baseline the First Class and Second Class SLA to what the network can actually hit, using real percentile delivery data instead of the current promise.
2. Fix this centrally rather than through regional or department-level ops. The pattern is uniform everywhere those levers would touch, so they won't move the number.
3. For Standard Class, manage variance, not the average. It ships close to on time on average but still misses 38% of the time, so track P90 delay alongside the mean.
4. Flag the overlap between late and unprofitable orders ($2.15M) before shipment, not after a complaint or chargeback.

## Data and methods

- **Source:** [DataCo Smart Supply Chain for Big Data Analysis](https://data.mendeley.com/datasets/8gx2fvg2k6/3) (Mendeley Data / Kaggle). 180,519 rows, 53 columns, 2015 to 2018. The raw CSV (about 92MB) and the cleaned BI-tool export (about 39MB) aren't committed to this repo (see `.gitignore`). Download `DataCoSupplyChainDataset.csv` from the source above and drop it into `data/` if you want to re-run `notebooks/01_analysis.py`.
- **Cleaning:** I dropped all PII columns (names, emails, passwords, street addresses, customer and order zip codes) before analysis. This repo contains no personal data.
- **Analysis:** Python and pandas, in [`notebooks/01_analysis.py`](notebooks/01_analysis.py). It computes late-delivery rate by shipping mode, region, department, and month, builds a region by shipping-mode pivot, and works out sales and profit exposure for late orders.
- **Outputs:** summary tables and charts in [`outputs/`](outputs/), plus a cleaned, BI-tool-ready CSV (`outputs/cleaned_orders_for_bi_tool.csv`) if you'd rather rebuild this in Power BI or Tableau.
- **Dashboard:** a single-page interactive write-up (`dashboard.html`), which is the version published above.

## Repo structure

```
01-operations-bottleneck-analysis/
├── README.md
├── dashboard.html              # the published case-study dashboard
├── data/
│   ├── DataCoSupplyChainDataset.csv
│   └── DescriptionDataCoSupplyChain.csv   # data dictionary
├── notebooks/
│   └── 01_analysis.py
└── outputs/
    ├── 01_late_rate_by_shipping_mode.png
    ├── 02_late_rate_trend.png
    ├── 03_region_shipping_heatmap.png
    ├── 04_late_rate_by_department.png
    ├── summary_by_shipping_mode.csv
    ├── summary_by_region.csv
    ├── summary_by_department.csv
    ├── summary_by_month.csv
    ├── summary_region_shipping_pivot.csv
    └── cleaned_orders_for_bi_tool.csv
```
