-- =====================================================================
-- SQL Portfolio — Northwind trading company
-- Each query answers a specific business question a data/ops analyst
-- would actually be asked. Run against db/northwind.db (SQLite).
-- =====================================================================


-- 1. Revenue by year — baseline aggregation with a computed line-total
SELECT
    strftime('%Y', o.OrderDate)                          AS order_year,
    ROUND(SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)), 2) AS revenue,
    COUNT(DISTINCT o.OrderID)                            AS orders
FROM Orders o
JOIN "Order Details" od ON od.OrderID = o.OrderID
GROUP BY order_year
ORDER BY order_year;


-- 2. Top 10 customers by lifetime revenue
SELECT
    c.CompanyName,
    c.Country,
    ROUND(SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)), 2) AS lifetime_revenue,
    COUNT(DISTINCT o.OrderID) AS orders
FROM Customers c
JOIN Orders o        ON o.CustomerID = c.CustomerID
JOIN "Order Details" od ON od.OrderID = o.OrderID
GROUP BY c.CustomerID
ORDER BY lifetime_revenue DESC
LIMIT 10;


-- 3. Monthly revenue with month-over-month % growth (window function: LAG)
WITH monthly AS (
    SELECT
        strftime('%Y-%m', o.OrderDate) AS month,
        SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) AS revenue
    FROM Orders o
    JOIN "Order Details" od ON od.OrderID = o.OrderID
    GROUP BY month
)
SELECT
    month,
    ROUND(revenue, 2) AS revenue,
    ROUND(revenue - LAG(revenue) OVER (ORDER BY month), 2) AS change_vs_prior_month,
    ROUND(100.0 * (revenue - LAG(revenue) OVER (ORDER BY month))
          / NULLIF(LAG(revenue) OVER (ORDER BY month), 0), 1) AS pct_change
FROM monthly
ORDER BY month;


-- 4. Running (cumulative) revenue total by month — window function: SUM() OVER
WITH monthly AS (
    SELECT
        strftime('%Y-%m', o.OrderDate) AS month,
        SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) AS revenue
    FROM Orders o
    JOIN "Order Details" od ON od.OrderID = o.OrderID
    GROUP BY month
)
SELECT
    month,
    ROUND(revenue, 2) AS revenue,
    ROUND(SUM(revenue) OVER (ORDER BY month), 2) AS running_total
FROM monthly
ORDER BY month;


-- 5. Top 3 products by revenue WITHIN each category — window function: RANK() PARTITION BY
WITH product_rev AS (
    SELECT
        cat.CategoryName,
        p.ProductName,
        SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) AS revenue,
        RANK() OVER (PARTITION BY cat.CategoryName
                     ORDER BY SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) DESC) AS rank_in_category
    FROM "Order Details" od
    JOIN Products p   ON p.ProductID = od.ProductID
    JOIN Categories cat ON cat.CategoryID = p.CategoryID
    GROUP BY cat.CategoryName, p.ProductName
)
SELECT CategoryName, ProductName, ROUND(revenue, 2) AS revenue, rank_in_category
FROM product_rev
WHERE rank_in_category <= 3
ORDER BY CategoryName, rank_in_category;


-- 6. Employee sales performance ranking — window function: RANK()
SELECT
    e.EmployeeID,
    e.FirstName || ' ' || e.LastName AS employee,
    e.Title,
    ROUND(SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)), 2) AS revenue,
    RANK() OVER (ORDER BY SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) DESC) AS rank
FROM Employees e
JOIN Orders o          ON o.EmployeeID = e.EmployeeID
JOIN "Order Details" od ON od.OrderID = o.OrderID
GROUP BY e.EmployeeID
ORDER BY rank;


-- 7. Customer value quartiles — window function: NTILE(4)
WITH customer_rev AS (
    SELECT
        c.CustomerID,
        c.CompanyName,
        SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) AS revenue
    FROM Customers c
    JOIN Orders o           ON o.CustomerID = c.CustomerID
    JOIN "Order Details" od ON od.OrderID = o.OrderID
    GROUP BY c.CustomerID
)
SELECT
    CompanyName,
    ROUND(revenue, 2) AS revenue,
    NTILE(4) OVER (ORDER BY revenue DESC) AS value_quartile   -- 1 = top spenders
FROM customer_rev
ORDER BY revenue DESC;


-- 8. Average fulfillment time (order -> ship) by shipping carrier
SELECT
    s.CompanyName AS shipper,
    COUNT(*) AS orders,
    ROUND(AVG(julianday(o.ShippedDate) - julianday(o.OrderDate)), 2) AS avg_days_to_ship
FROM Orders o
JOIN Shippers s ON s.ShipperID = o.ShipVia
WHERE o.ShippedDate IS NOT NULL
GROUP BY s.CompanyName
ORDER BY avg_days_to_ship DESC;


-- 9. Late-shipment rate by carrier (shipped after the date promised to the customer)
WITH flagged AS (
    SELECT
        o.OrderID,
        o.ShipVia,
        CASE WHEN o.ShippedDate > o.RequiredDate THEN 1 ELSE 0 END AS is_late
    FROM Orders o
    WHERE o.ShippedDate IS NOT NULL AND o.RequiredDate IS NOT NULL
)
SELECT
    s.CompanyName AS shipper,
    COUNT(*) AS orders,
    ROUND(100.0 * SUM(is_late) / COUNT(*), 1) AS late_pct
FROM flagged f
JOIN Shippers s ON s.ShipperID = f.ShipVia
GROUP BY s.CompanyName
ORDER BY late_pct DESC;


-- 10. Customers with no order in the most recent 60 days of data (churn risk)
WITH last_order AS (
    SELECT CustomerID, MAX(OrderDate) AS last_order_date
    FROM Orders
    GROUP BY CustomerID
),
cutoff AS (
    SELECT date(MAX(OrderDate), '-60 days') AS cutoff_date FROM Orders
)
SELECT
    c.CompanyName,
    lo.last_order_date,
    CAST(julianday((SELECT MAX(OrderDate) FROM Orders)) - julianday(lo.last_order_date) AS INT) AS days_since_last_order
FROM last_order lo
JOIN Customers c ON c.CustomerID = lo.CustomerID
CROSS JOIN cutoff
WHERE lo.last_order_date < cutoff.cutoff_date
ORDER BY days_since_last_order DESC
LIMIT 15;


-- 11. Repeat vs one-time customers
WITH order_counts AS (
    SELECT CustomerID, COUNT(*) AS n_orders
    FROM Orders
    GROUP BY CustomerID
)
SELECT
    CASE WHEN n_orders = 1 THEN 'One-time' ELSE 'Repeat' END AS customer_type,
    COUNT(*) AS customers,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM order_counts), 1) AS pct_of_customers
FROM order_counts
GROUP BY customer_type;


-- 12. Category share of total revenue — window function: SUM() OVER () (grand total)
WITH cat_rev AS (
    SELECT
        cat.CategoryName,
        SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) AS revenue
    FROM "Order Details" od
    JOIN Products p    ON p.ProductID = od.ProductID
    JOIN Categories cat ON cat.CategoryID = p.CategoryID
    GROUP BY cat.CategoryName
)
SELECT
    CategoryName,
    ROUND(revenue, 2) AS revenue,
    ROUND(100.0 * revenue / SUM(revenue) OVER (), 1) AS pct_of_total_revenue
FROM cat_rev
ORDER BY revenue DESC;


-- 13. Revenue given up to discounting, by category
SELECT
    cat.CategoryName,
    ROUND(SUM(od.UnitPrice * od.Quantity * od.Discount), 2) AS revenue_lost_to_discount,
    ROUND(AVG(od.Discount) * 100, 1) AS avg_discount_pct
FROM "Order Details" od
JOIN Products p    ON p.ProductID = od.ProductID
JOIN Categories cat ON cat.CategoryID = p.CategoryID
WHERE od.Discount > 0
GROUP BY cat.CategoryName
ORDER BY revenue_lost_to_discount DESC;


-- 14. Revenue and order count by country, ranked
SELECT
    c.Country,
    COUNT(DISTINCT o.OrderID) AS orders,
    ROUND(SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)), 2) AS revenue,
    RANK() OVER (ORDER BY SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) DESC) AS revenue_rank
FROM Customers c
JOIN Orders o           ON o.CustomerID = c.CustomerID
JOIN "Order Details" od ON od.OrderID = o.OrderID
GROUP BY c.Country
ORDER BY revenue_rank;


-- 15. Customers whose average order value beats the company-wide average (subquery in HAVING)
SELECT
    c.CompanyName,
    COUNT(DISTINCT o.OrderID) AS orders,
    ROUND(AVG(order_value.value), 2) AS avg_order_value
FROM Customers c
JOIN Orders o ON o.CustomerID = c.CustomerID
JOIN (
    SELECT OrderID, SUM(UnitPrice * Quantity * (1 - Discount)) AS value
    FROM "Order Details"
    GROUP BY OrderID
) order_value ON order_value.OrderID = o.OrderID
GROUP BY c.CustomerID
HAVING AVG(order_value.value) > (
    SELECT AVG(UnitPrice * Quantity * (1 - Discount)) FROM "Order Details"
)
ORDER BY avg_order_value DESC
LIMIT 10;


-- 16. Each employee's revenue vs the company average — window function: AVG() OVER ()
WITH emp_rev AS (
    SELECT
        e.FirstName || ' ' || e.LastName AS employee,
        SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) AS revenue
    FROM Employees e
    JOIN Orders o           ON o.EmployeeID = e.EmployeeID
    JOIN "Order Details" od ON od.OrderID = o.OrderID
    GROUP BY e.EmployeeID
)
SELECT
    employee,
    ROUND(revenue, 2) AS revenue,
    ROUND(AVG(revenue) OVER (), 2) AS company_avg_revenue,
    ROUND(revenue - AVG(revenue) OVER (), 2) AS vs_company_avg
FROM emp_rev
ORDER BY revenue DESC;


-- 17. Year-over-year revenue growth by category — window function: LAG() PARTITION BY
WITH cat_year AS (
    SELECT
        cat.CategoryName,
        strftime('%Y', o.OrderDate) AS order_year,
        SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) AS revenue
    FROM Orders o
    JOIN "Order Details" od ON od.OrderID = o.OrderID
    JOIN Products p    ON p.ProductID = od.ProductID
    JOIN Categories cat ON cat.CategoryID = p.CategoryID
    GROUP BY cat.CategoryName, order_year
)
SELECT
    CategoryName,
    order_year,
    ROUND(revenue, 2) AS revenue,
    ROUND(100.0 * (revenue - LAG(revenue) OVER (PARTITION BY CategoryName ORDER BY order_year))
          / NULLIF(LAG(revenue) OVER (PARTITION BY CategoryName ORDER BY order_year), 0), 1) AS yoy_pct_change
FROM cat_year
ORDER BY CategoryName, order_year;


-- 18. Days between consecutive orders per customer (purchase cadence) — window function: LAG() PARTITION BY
WITH order_dates AS (
    SELECT CustomerID, OrderID, OrderDate
    FROM Orders
)
SELECT
    CustomerID,
    OrderID,
    OrderDate,
    CAST(julianday(OrderDate) - julianday(LAG(OrderDate) OVER (PARTITION BY CustomerID ORDER BY OrderDate)) AS INT) AS days_since_prior_order
FROM order_dates
ORDER BY CustomerID, OrderDate
LIMIT 30;
