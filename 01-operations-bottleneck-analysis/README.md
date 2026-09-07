# Fulfillment Risk Analysis: Why First Class Shipping Fails 95% of the Time

**Live dashboard:** https://claude.ai/code/artifact/89898b82-57df-4b3b-8227-0c03519cc8ae

An operational bottleneck audit of 180,519 order line items from the DataCo Smart
Supply Chain dataset (Jan 2015 - Jan 2018), built to answer one question: *where
in the fulfillment process do late deliveries actually come from?*

## Why this project

Coming from an operations background — tracking scheduling, workflow, and
performance data to support management decisions — the recurring problem was
never a lack of data, it was information gaps that hid where a process was
actually breaking down. This project applies that same lens to a public supply
chain dataset: don't just report the late-delivery rate, trace it to its root
cause and quantify what it costs.

## Key findings

1. **The SLA is the bottleneck, not the warehouse.** Overall late-delivery rate
   is 54.8%, but it is wildly uneven by shipping mode: **First Class late 95.3%**
   of the time, Second Class 76.6%, Same Day 45.7%, Standard Class 38.1%. The
   tier sold as fastest is the least dependable.
2. **It's chronic, not seasonal.** The monthly late rate stays in a tight
   51.9%-56.8% band across all 37 months — no holiday spike, no gradual
   improvement. This is a structural process issue, not an event.
3. **Every region shows the same pattern.** All 23 regions band almost
   identically by shipping mode (First Class 92-100% late in every single
   region), which rules out regional carriers or local ops teams as the cause.
4. **Department is a red herring too.** Product category late rates sit in a
   4.5-point band (54.4%-58.9%) versus a 57-point spread across shipping modes.
5. **Business cost:** $20.1M in sales rides on a late order, and 18,553 orders
   were both late *and* unprofitable, for $2.15M in lost margin.

## Recommendations

1. Re-baseline the First Class / Second Class SLA to what the network can
   actually hit, using real percentile delivery data instead of the current
   promise.
2. Fix this centrally, not through regional or department-level ops — the
   pattern is uniform everywhere those levers would touch.
3. For Standard Class, manage variance, not the average — it ships ~on time on
   average but still misses 38% of the time, so track P90 delay, not just the mean.
4. Flag the late + unprofitable order overlap ($2.15M) before shipment, not
   after a complaint or chargeback.

## Data & methods

- **Source:** [DataCo Smart Supply Chain for Big Data Analysis](https://data.mendeley.com/datasets/8gx2fvg2k6/3)
  (Mendeley Data / Kaggle), 180,519 rows, 53 columns, 2015-2018. The raw CSV
  (~92MB) and the cleaned BI-tool export (~39MB) are not committed to this repo
  (see `.gitignore`) — download `DataCoSupplyChainDataset.csv` from the source
  above and drop it into `data/` to re-run `notebooks/01_analysis.py`.
- **Cleaning:** dropped all PII columns (names, emails, passwords, street
  addresses, customer/order zip codes) before analysis — this repo contains no
  personal data.
- **Analysis:** Python (pandas), see [`notebooks/01_analysis.py`](notebooks/01_analysis.py).
  Computes late-delivery rate by shipping mode, region, department, and month;
  a region x shipping-mode pivot; and sales/profit exposure for late orders.
- **Outputs:** summary tables and charts in [`outputs/`](outputs/); a cleaned,
  BI-tool-ready CSV (`outputs/cleaned_orders_for_bi_tool.csv`) for anyone who
  wants to rebuild this in Power BI or Tableau instead.
- **Dashboard:** a single-page interactive write-up built as the primary
  deliverable (`dashboard.html`), published above.

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
