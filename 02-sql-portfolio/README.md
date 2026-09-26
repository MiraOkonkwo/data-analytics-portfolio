# SQL Portfolio: Northwind Trading Co.

18 SQL queries run against a relational order-management database. Each one answers a specific business question. They run in SQLite, against `db/northwind.db`. This uses the classic Northwind schema: Customers, Orders, Order Details, Products, Categories, Employees, Shippers.

Every query and its real output is in [`queries/queries.sql`](queries/queries.sql) and [`results/sample_output.txt`](results/sample_output.txt). Some highlights below.

## What this shows

| Technique | Queries |
|---|---|
| Joins and aggregation | 1, 2, 8, 14 |
| CTEs (`WITH`) | 3, 4, 5, 7, 9, 10, 12, 16, 17, 18 |
| Window functions: `RANK`, `NTILE`, `LAG`, running `SUM`/`AVG` | 3, 4, 5, 6, 7, 12, 16, 17, 18 |
| Subqueries (correlated and `HAVING`) | 10, 15 |
| Date arithmetic (`julianday`, `strftime`) | 8, 9, 10, 18 |

## Schema

The 18 queries use 7 tables. Here are the columns that matter:

| Table | Key columns |
|---|---|
| **Customers** | `CustomerID` (PK), `CompanyName`, `Country` |
| **Orders** | `OrderID` (PK), `CustomerID` (FK), `EmployeeID` (FK), `ShipVia` (FK), `OrderDate` |
| **Order Details** | `OrderID` (FK), `ProductID` (FK), `UnitPrice`, `Quantity`, `Discount` |
| **Products** | `ProductID` (PK), `ProductName`, `CategoryID` (FK), `UnitPrice` |
| **Categories** | `CategoryID` (PK), `CategoryName` |
| **Employees** | `EmployeeID` (PK), `FirstName`, `LastName`, `Title` |
| **Shippers** | `ShipperID` (PK), `CompanyName` |

A "PK" is the primary key, the column that uniquely identifies a row in that table. An "FK" is a foreign key, a column that points back to another table's primary key.

How they connect:

- **Orders** is the hub. Each order links to one customer (`CustomerID`), one employee who made the sale (`EmployeeID`), and one shipper (`ShipVia`).
- **Order Details** is a line-item table. One order can have many rows here, one per product on that order. This is where quantity, price, and discount actually live.
- **Products** links to **Categories**. Each product belongs to one category.

## Findings

**Q1, revenue by year:** revenue roughly doubled from 2012 ($18.8M) to 2013 ($38.6M). It then held flat through 2017, at around $40M a year. Growth stalled after that first jump.

**Q6, employee sales ranking:** the top and bottom performer sit $2.2M apart in revenue. Margaret Peacock leads at $51.5M. Laura Callahan trails at $49.3M. `RANK() OVER (ORDER BY revenue DESC)` turns the raw totals into a leaderboard in one line.

**Q9, late-shipment rate by carrier:** all three carriers cluster tightly, between 22.9% and 23.3% late. [Project 1](../01-fulfillment-risk-analysis/) found the same pattern. The real driver sits upstream of which carrier gets picked.

**Q10, churn risk:** this query flags customers with no order in the trailing 60 days. It uses `MAX(OrderDate)` per customer against a rolling cutoff. A retention team would use this same logic to build a win-back list.

**Q12, category share of revenue:** `SUM(revenue) OVER ()` computes the grand total inline. Every row can then show its percent of total. No second query needed. No self-join needed. Beverages leads at 20.6% of all revenue.

**Q17, year-over-year growth by category:** `LAG() OVER (PARTITION BY CategoryName ORDER BY order_year)` works out year-over-year growth per category in a single pass. Beverages grew 102.8% in 2013. Growth then flattened to low single digits every year after.

## Running this yourself

```
sqlite3 db/northwind.db < queries/queries.sql   # or open in DB Browser for SQLite
python3 queries/run_all.py                      # regenerates results/sample_output.txt
```

## About the data

[Northwind](https://github.com/jpwhite3/northwind-SQLite3) is a SQLite port of Microsoft's classic sample database. This version is expanded to 16,282 orders, 609K order line items, 93 customers, and 9 employees. It spans 2012 to 2023. `db/northwind.db` is included in this repo, at about 24MB.
