# SQL Portfolio — Northwind Trading Co.

18 SQL queries against a relational order-management database, each written to
answer a specific business question — not a syntax demo. Run in SQLite against
`db/northwind.db` (classic Northwind schema: Customers, Orders, Order Details,
Products, Categories, Employees, Shippers).

Every query and its real output is in [`queries/queries.sql`](queries/queries.sql)
and [`results/sample_output.txt`](results/sample_output.txt). Highlights below.

## What this demonstrates

| Technique | Queries |
|---|---|
| Joins & aggregation | 1, 2, 8, 14 |
| CTEs (`WITH`) | 3, 4, 5, 7, 9, 10, 12, 16, 17, 18 |
| Window functions — `RANK`, `NTILE`, `LAG`, running `SUM`/`AVG` | 3, 4, 5, 6, 7, 12, 16, 17, 18 |
| Subqueries (correlated & `HAVING`) | 10, 15 |
| Date arithmetic (`julianday`, `strftime`) | 8, 9, 10, 18 |

## Selected findings

**Q1 — Revenue by year:** revenue roughly doubled from 2012 ($18.8M) to 2013
($38.6M) then held flat through 2017 (~$40M/yr) — growth stalled, not declined.

**Q6 — Employee sales ranking:** top and bottom performer are $2.2M apart in
revenue attributed to them (`Margaret Peacock` $51.5M vs `Laura Callahan`
$49.3M) — a `RANK() OVER (ORDER BY revenue DESC)` turns raw totals into a
comparable leaderboard in one line.

**Q9 — Late-shipment rate by carrier:** all three carriers cluster tightly
(22.9%–23.3% late), meaning — like the operations analysis in
[Project 1](../01-operations-bottleneck-analysis/) — the carrier isn't the
lever; whatever drives the ~23% miss rate is upstream of carrier choice.

**Q10 — Churn risk:** flags customers with no order in the trailing 60 days
using `MAX(OrderDate)` per customer against a rolling cutoff — the same logic
a retention team would use to build a win-back list.

**Q12 — Category share of revenue:** `SUM(revenue) OVER ()` computes the grand
total inline, so every row can show `% of total` without a second query or a
self-join — Beverages leads at 20.6% of all revenue.

**Q17 — YoY growth by category:** `LAG() OVER (PARTITION BY CategoryName ORDER BY order_year)`
computes year-over-year growth per category in a single pass — Beverages grew
102.8% in 2013 then flattened to low single digits every year after.

## Re-running this

```
sqlite3 db/northwind.db < queries/queries.sql   # or open in DB Browser for SQLite
python3 queries/run_all.py                      # regenerates results/sample_output.txt
```

## Data

[Northwind](https://github.com/jpwhite3/northwind-SQLite3), SQLite port of
Microsoft's classic sample database, expanded to 16,282 orders / 609K order
line items / 93 customers / 9 employees (2012–2023). `db/northwind.db` is
included in this repo (~24MB).
