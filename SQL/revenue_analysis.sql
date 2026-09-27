-- 1. Overall Revenue
SELECT
    ROUND(SUM(Amount), 2) AS total_revenue
FROM transactions;

-- 2. Total Transactions
SELECT
    COUNT(*) AS total_transactions
FROM transactions;

-- 3. Revenue by Income Source
SELECT
    Income_Source,
    SUM(Amount) AS revenue,
    ROUND(
        SUM(Amount) * 100.0 /
        (SELECT SUM(Amount) FROM transactions),
        2
    ) AS revenue_percentage
FROM transactions
GROUP BY Income_Source
ORDER BY revenue DESC;

-- 4. Monthly Revenue
SELECT
    strftime('%Y-%m', Transaction_Date) AS month,
    ROUND(SUM(Amount), 2) AS revenue
FROM transactions
GROUP BY month
ORDER BY month;

-- 5. Month-over-Month Revenue Growth

WITH monthly_revenue AS (
    SELECT
        strftime('%Y-%m', Transaction_Date) AS month,
        SUM(Amount) AS revenue
    FROM transactions
    GROUP BY month
),

revenue_with_previous AS (
    SELECT
        month,
        revenue,
        LAG(revenue) OVER (
            ORDER BY month
        ) AS previous_month_revenue
    FROM monthly_revenue
)

SELECT
    month,
    ROUND(revenue, 2) AS revenue,
    ROUND(previous_month_revenue, 2) AS previous_month_revenue,
    ROUND(
        (revenue - previous_month_revenue)
        * 100.0 / previous_month_revenue,
        2
    ) AS mom_growth_percent
FROM revenue_with_previous
ORDER BY month;

-- 6. Yearly Revenue and Transaction Performance

SELECT
    strftime('%Y', Transaction_Date) AS year,
    COUNT(*) AS transaction_count,
    ROUND(SUM(Amount), 2) AS total_revenue,
    ROUND(AVG(Amount), 2) AS average_transaction_value
FROM transactions
GROUP BY year
ORDER BY year;

-- 7. Revenue by Category

SELECT
    Category,
    ROUND(SUM(Amount), 2) AS revenue
FROM transactions
GROUP BY Category
ORDER BY revenue DESC;

-- 8. Revenue by Payment Status

SELECT
    Payment_Status,
    COUNT(*) AS transaction_count,
    ROUND(SUM(Amount), 2) AS revenue
FROM transactions
GROUP BY Payment_Status
ORDER BY revenue DESC;

-- 9. Payment Status Revenue Percentage

SELECT
    Payment_Status,
    ROUND(SUM(Amount), 2) AS revenue,
    ROUND(
        SUM(Amount) * 100.0 /
        (SELECT SUM(Amount) FROM transactions),
        2
    ) AS revenue_percentage
FROM transactions
GROUP BY Payment_Status
ORDER BY revenue DESC;

-- 10. Top Client Products by Revenue

SELECT
    Client_Product,
    COUNT(*) AS transaction_count,
    ROUND(SUM(Amount), 2) AS revenue
FROM transactions
GROUP BY Client_Product
ORDER BY revenue DESC
LIMIT 10;

-- 11. Revenue by Payment Method

SELECT
    Payment_Method,
    COUNT(*) AS transaction_count,
    ROUND(SUM(Amount), 2) AS revenue
FROM transactions
GROUP BY Payment_Method
ORDER BY revenue DESC;
