-- Retail Sales ETL Pipeline
-- Business Analysis Queries
-- Database: SQLite

-- Question: What is the total revenue?

SELECT
    SUM(sales) AS total_revenue
FROM sales;

-- Question: What is the total profit?

SELECT
    SUM(profit) AS total_profit
FROM sales;

-- Question: Which regions generate the most revenue?

SELECT
    region,
    SUM(sales) AS total_revenue
FROM sales
GROUP BY region
ORDER BY total_revenue DESC;

-- Question: Which categories generate the most revenue?

SELECT
    category,
    SUM(sales) AS total_revenue
FROM sales
GROUP BY category
ORDER BY total_revenue DESC;

-- Question: Which categories generate the most revenue and profit?

SELECT
    category,
    SUM(sales) AS total_revenue,
    SUM(profit) AS total_profit
FROM sales
GROUP BY category
ORDER BY total_revenue DESC;

-- Question: What is the profit margin by category?

SELECT
    category,
    SUM(sales) AS total_revenue,
    SUM(profit) AS total_profit,
    ROUND(SUM(profit) * 100.0 / SUM(sales), 2) AS profit_margin
FROM sales
GROUP BY category
ORDER BY profit_margin DESC;

-- Question: How many orders does each region have?

SELECT
    region,
    COUNT(*) AS order_count
FROM sales
GROUP BY region
ORDER BY order_count DESC;

-- Question: How much revenue and how many orders does each region have?

SELECT
    region,
    COUNT(*) AS order_count,
    SUM(sales) AS total_revenue
FROM sales
GROUP BY region
ORDER BY total_revenue DESC;

-- Question: Which regions have the highest average revenue per order?

SELECT
    region,
    COUNT(*) AS order_count,
    SUM(sales) AS total_revenue,
    ROUND(SUM(sales) / COUNT(*), 2) AS average_order_value
FROM sales
GROUP BY region
ORDER BY average_order_value DESC;

-- Question: Which products generate the most revenue?

SELECT
    product_name,
    SUM(sales) AS total_revenue
FROM sales
GROUP BY product_name
ORDER BY total_revenue DESC
LIMIT 10;

-- Question: Which products sell the most units?

SELECT
    product_name,
    SUM(quantity) AS total_units_sold
FROM sales
GROUP BY product_name
ORDER BY total_units_sold DESC
LIMIT 10;

-- Question: What is the average selling price of each product?

SELECT
    product_name,
    SUM(quantity) AS total_units_sold,
    SUM(sales) AS total_revenue,
    ROUND(SUM(sales) / SUM(quantity), 2) AS average_selling_price
FROM sales
GROUP BY product_name
ORDER BY average_selling_price DESC
LIMIT 10;

-- Question: Which customers generate the most revenue?

SELECT
    customer_id,
    customer_name,
    SUM(sales) AS total_revenue
FROM sales
GROUP BY customer_id, customer_name
ORDER BY total_revenue DESC
LIMIT 10;

-- Question: Which customers have the highest order value?

SELECT
    customer_id,
    customer_name,
    COUNT(*) AS order_count,
    SUM(sales) AS total_revenue,
    ROUND(SUM(sales) / COUNT(*), 2) AS average_order_value
FROM sales
GROUP BY customer_id, customer_name
ORDER BY average_order_value DESC
LIMIT 10;

-- Question: How does revenue change over time?

SELECT
    strftime('%Y-%m', order_date) AS sales_month,
    COUNT(*) AS order_count,
    SUM(sales) AS total_revenue,
    SUM(profit) AS total_profit
FROM sales
GROUP BY sales_month
ORDER BY sales_month;